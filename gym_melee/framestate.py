from melee.enums import Action
from copy import copy

class FrameDelta(object):
    """Defines the change in player and opponent state between frames."""
    def __init__(self, gamestate):
        self.prev_opponent_state = gamestate.opponent_state
        self.prev_ai_state = gamestate.ai_state
        self.opponent = PlayerDelta(self.prev_opponent_state, gamestate.opponent_state)
        self.ai = PlayerDelta(self.prev_ai_state, gamestate.ai_state)
        self.gamestate = gamestate

    def step(self):
        self.opponent = PlayerDelta(self.prev_opponent_state, self.gamestate.opponent_state)
        self.ai = PlayerDelta(self.prev_ai_state, self.gamestate.ai_state)
        self.opponent.hit = self.ai.hitted
        self.ai.hit = self.opponent.hitted
        self.opponent.opponent_percent = self.ai.percent
        self.ai.opponent_percent = self.opponent.percent
        self.prev_opponent_state = copy(self.gamestate.opponent_state)
        self.prev_ai_state = copy(self.gamestate.ai_state)

class PlayerDelta(object):
    """Defines the change in relevant (for the ai) states of a player."""
    def __init__(self, prev_state, new_state):
        self.facing = new_state.facing
        self.invulnerable = new_state.invulnerable
        self.on_ground = new_state.on_ground
        self.move_x = new_state.x - prev_state.x
        self.move_y = new_state.y - prev_state.y
        self.percent =  new_state.percent - prev_state.percent
        self.hitstun_left = new_state.hitstun_frames_left
        self.hitted = (self.percent > 0)
        self.hit = False
        self.opponent_percent = 0
        act = new_state.action
        self.dead = act in (Action.DEAD_DOWN, Action.DEAD_LEFT, \
                        Action.DEAD_RIGHT, Action.DEAD_FLY_STAR, Action.DEAD_FLY, \
                        Action.DEAD_FLY_SPLATTER, Action.DEAD_FLY_SPLATTER_FLAT)
        if self.dead:
            self.percent = 100 # to give feedback to the ai
        else:
            self.percent = new_state.percent - prev_state.percent
        self.shield_reflect = (act == Action.SHIELD_REFLECT)
        self.knee_bend = (act == Action.KNEE_BEND)
        self.falling = (act == Action.FALLING)
        self.falling_aerial = (act == Action.FALLING_AERIAL)
        self.dead_fall = (act == Action.DEAD_FALL)
        self.tumbling = (act == Action.TUMBLING)
        self.crouching = (act == Action.CROUCHING)
        self.landing = (act == Action.LANDING)
        self.landing_special = (act == Action.LANDING_SPECIAL)
        self.shield = (act == Action.SHIELD)
        self.shield_stun = (act == Action.SHIELD_STUN)
        self.ground_getup = (act == Action.GROUND_GETUP)
        self.ground_roll_forward_up = (act == Action.GROUND_ROLL_FORWARD_UP)
        self.ground_roll_backward_up = (act == Action.GROUND_ROLL_BACKWARD_UP)
        self.tech_miss_down = (act == Action.TECH_MISS_DOWN)
        self.lying_ground_down = (act == Action.LYING_GROUND_DOWN)
        self.getup_attack = (act == Action.GETUP_ATTACK)
        self.grab = (act == Action.GRAB)
        self.grab_break = (act == Action.GRAB_BREAK)
        self.grabbed = (act == Action.GRABBED)
        self.roll_forward = (act == Action.ROLL_FORWARD)
        self.roll_backward = (act == Action.ROLL_BACKWARD)
        self.spotdodge = (act == Action.SPOTDODGE)
        self.airdodge = (act == Action.AIRDODGE)
        self.bounce_wall = (act == Action.BOUNCE_WALL)
        self.bounce_ceiling = (act == Action.BOUNCE_CEILING)
        self.sliding_off_edge = (act == Action.SLIDING_OFF_EDGE)
        self.edge_hanging = (act == Action.EDGE_HANGING)
