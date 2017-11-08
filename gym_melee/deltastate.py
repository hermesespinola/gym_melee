from melee.enums import Action
from copy import copy

DEAD_ACTIONS = (Action.DEAD_DOWN, Action.DEAD_LEFT, Action.DEAD_RIGHT,
                Action.DEAD_FLY_STAR, Action.DEAD_FLY, Action.DEAD_FLY_SPLATTER,
                Action.DEAD_FLY_SPLATTER_FLAT)

class DeltaState(object):
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

    def todict(self):
        return {
            "ai": self.ai.todict(),
            "opponent": self.opponent.todict()
        }

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
        prev_act = prev_state.action
        self.dead = prev_act not in DEAD_ACTIONS and act in DEAD_ACTIONS
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
        self.off_stage = new_state.off_stage
        def todict(self):
            return {
                "facing": self.facing,
                "invulnerable": self.invulnerable,
                "on_ground": self.on_ground,
                "move_x": self.move_x,
                "move_y": self.move_y,
                "percent": self.percent,
                "hitstun_left": self.hitstun_left,
                "hitted": self.hitted,
                "hit": self.hit,
                "opponent_percent": self.opponent_percent,
                "dead": self.dead,
                "percent": self.percent,
                "shield_reflect": self.shield_reflect,
                "knee_bend": self.knee_bend,
                "falling": self.falling,
                "falling_aerial": self.falling_aerial,
                "dead_fall": self.dead_fall,
                "tumbling": self.tumbling,
                "crouching": self.crouching,
                "landing": self.landing,
                "landing_special": self.landing_special,
                "shield": self.shield,
                "shield_stun": self.shield_stun,
                "ground_getup": self.ground_getup,
                "ground_roll_forward_up": self.ground_roll_forward_up,
                "ground_roll_backward_up": self.ground_roll_backward_up,
                "tech_miss_down": self.tech_miss_down,
                "lying_ground_down": self.lying_ground_down,
                "getup_attack": self.getup_attack,
                "grab": self.grab,
                "grab_break": self.grab_break,
                "grabbed": self.grabbed,
                "roll_forward": self.roll_forward,
                "roll_backward": self.roll_backward,
                "spotdodge": self.spotdodge,
                "airdodge": self.airdodge,
                "bounce_wall": self.bounce_wall,
                "bounce_ceiling": self.bounce_ceiling,
                "sliding_off_edge": self.sliding_off_edge,
                "edge_hanging": self.edge_hanging,
                "off_stage": self.off_stage
            }
