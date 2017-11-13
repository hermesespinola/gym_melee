from melee.enums import Action
from copy import copy

DEAD_ACTIONS = (Action.DEAD_DOWN, Action.DEAD_LEFT, Action.DEAD_RIGHT,
                Action.DEAD_FLY_STAR, Action.DEAD_FLY, Action.DEAD_FLY_SPLATTER,
                Action.DEAD_FLY_SPLATTER_FLAT)

def separate_projectiles(gamestate, op_name, ai_name):
    op_proj = []
    ai_proj = []
    for projectile in gamestate.projectiles:
        if str(projectile.subtype)[18:18+len(op_name)] == op_name:
            op_proj.append(projectile.todict())
        elif str(projectile.subtype)[18:18+len(ai_name)] == ai_name:
            ai_proj.append(projectile.todict())
    return op_proj, ai_proj

class DeltaState(object):
    """Defines the change in player and opponent state between frames."""
    def __init__(self, gamestate):
        self.prev_opponent_state = gamestate.opponent_state
        self.prev_ai_state = gamestate.ai_state
        self.opponent = PlayerDelta(self.prev_opponent_state, gamestate.opponent_state)
        self.ai = PlayerDelta(self.prev_ai_state, gamestate.ai_state)
        self.op_name = str(gamestate.player[gamestate.opponent_port].character)[10:]
        self.ai_name = str(gamestate.player[gamestate.ai_port].character)[10:]
        self.opponent.projectiles, self.ai.projectiles = \
                separate_projectiles(gamestate, self.op_name, self.ai_name)
        self.opponent.vector = [self.opponent.x - self.ai.x, self.opponent.y - self.ai.y]
        self.opponent.vector = [self.ai.x - self.opponent.x, self.ai.y - self.opponent.y]
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
        self.op_name = str(self.gamestate.player[self.gamestate.opponent_port].character)[10:]
        self.ai_name = str(self.gamestate.player[self.gamestate.ai_port].character)[10:]
        self.opponent.projectiles, self.ai.projectiles = \
                separate_projectiles(self.gamestate, self.op_name, self.ai_name)
        self.opponent.vector = [self.opponent.x - self.ai.x, self.opponent.y - self.ai.y]
        self.opponent.vector = [self.ai.x - self.opponent.x, self.ai.y - self.opponent.y]

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
        self.invulnerability_left = new_state.invulnerability_left
        self.on_ground = new_state.on_ground
        self.x = new_state.x
        self.y = new_state.y
        self.charging_smash = new_state.charging_smash
        self.jumps_left = new_state.jumps_left
        self.move_x = new_state.x - prev_state.x
        self.move_y = new_state.y - prev_state.y
        self.percent =  new_state.percent - prev_state.percent
        self.total_percent = new_state.percent
        self.hitstun_left = new_state.hitstun_frames_left
        self.hitted = (self.percent > 0)
        self.hit = False
        self.opponent_percent = 0
        act = new_state.action
        prev_act = prev_state.action
        self.stock = new_state.stock - prev_state.stock
        self.dead = prev_act not in DEAD_ACTIONS and act in DEAD_ACTIONS
        self.percent = new_state.percent - prev_state.percent
        self.hitlag_left = new_state.hitlag_frames_left
        self.shield_reflect = (act == Action.SHIELD_REFLECT)
        self.shield_release = (act == Action.SHIELD_RELEASE)
        self.knee_bend = (act == Action.KNEE_BEND)
        self.falling = (act == Action.FALLING)
        self.falling_aerial = (act == Action.FALLING_AERIAL)
        self.dead_fall = (act == Action.DEAD_FALL)
        self.tumbling = (act == Action.TUMBLING)
        self.crouching = (act == Action.CROUCHING)
        self.crouch_end = (act == Action.CROUCH_END)
        self.landing = (act == Action.LANDING)
        self.landing_special = (act == Action.LANDING_SPECIAL)
        # self.NEUTRAL_ATTACK_1 = (act == Action.NEUTRAL_ATTACK_1)
        # self.NEUTRAL_ATTACK_2 = (act == Action.NEUTRAL_ATTACK_2)
        # self.NEUTRAL_ATTACK_3 = (act == Action.NEUTRAL_ATTACK_3)
        # self.LOOPING_ATTACK_START = (act == Action.LOOPING_ATTACK_START)
        # self.LOOPING_ATTACK_MIDDLE = (act == Action.LOOPING_ATTACK_MIDDLE)
        # self.LOOPING_ATTACK_END = (act == Action.LOOPING_ATTACK_END)
        # self.DASH_ATTACK = (act == Action.DASH_ATTACK)
        self.ftilt = (act == Action.FTILT_HIGH or act == Action.FTILT_HIGH_MID or
                        act == Action.FTILT_MID or act == Action.FTILT_LOW_MID or
                        act == Action.FTILT_LOW)
        # self.FTILT_HIGH_MID = (act == Action.FTILT_HIGH_MID)
        # self.FTILT_MID = (act == Action.FTILT_MID)
        # self.FTILT_LOW_MID = (act == Action.FTILT_LOW_MID)
        # self.FTILT_LOW = (act == Action.FTILT_LOW)
        # self.UPTILT = (act == Action.UPTILT)
        # self.DOWNTILT = (act == Action.DOWNTILT)
        # self.fsmash = (act == Action.FSMASH_HIGH or act == Action.FSMASH_MID_HIGH or \
        #             act == Action.FSMASH_MID or act == Action.FSMASH_MID_LOW or \
        #             act == Action.FSMASH_LOW)
        # self.FSMASH_HIGH = (act == Action.FSMASH_HIGH)
        # self.FSMASH_MID_HIGH = (act == Action.FSMASH_MID_HIGH)
        # self.FSMASH_MID = (act == Action.FSMASH_MID)
        # self.FSMASH_MID_LOW = (act == Action.FSMASH_MID_LOW)
        # self.FSMASH_LOW = (act == Action.FSMASH_LOW)
        # self.UPSMASH = (act == Action.UPSMASH)
        # self.DOWNSMASH = (act == Action.DOWNSMASH)
        # self.NAIR = (act == Action.NAIR)
        # self.FAIR = (act == Action.FAIR)
        # self.BAIR = (act == Action.BAIR)
        # self.UAIR = (act == Action.UAIR)
        # self.DAIR = (act == Action.DAIR)
        # self.NAIR_LANDING = (act == Action.NAIR_LANDING)
        # self.FAIR_LANDING = (act == Action.FAIR_LANDING)
        # self.BAIR_LANDING = (act == Action.BAIR_LANDING)
        # self.UAIR_LANDING = (act == Action.UAIR_LANDING)
        # self.DAIR_LANDING = (act == Action.DAIR_LANDING)
        self.shield = (act == Action.SHIELD_START or act == Action.SHIELD)
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
        # self.bounce_wall = (act == Action.BOUNCE_WALL)
        # self.bounce_ceiling = (act == Action.BOUNCE_CEILING)
        self.sliding_off_edge = (act == Action.SLIDING_OFF_EDGE)
        self.edge_hanging = (act == Action.EDGE_HANGING)
        self.edge_catching = (act == Action.EDGE_CATCHING)
        self.off_stage = new_state.off_stage
        self.iasa = new_state.iasa
        # self.hitbox_1_size = new_state.hitbox_1_size
        # self.hitbox_2_size = new_state.hitbox_2_size
        # self.hitbox_3_size = new_state.hitbox_3_size
        # self.hitbox_4_size = new_state.hitbox_4_size
        # self.hitbox_1_status = new_state.hitbox_1_status
        # self.hitbox_2_status = new_state.hitbox_2_status
        # self.hitbox_3_status = new_state.hitbox_3_status
        # self.hitbox_4_status = new_state.hitbox_4_status
        # self.hitbox_1_x = new_state.hitbox_1_x
        # self.hitbox_1_y = new_state.hitbox_1_y
        # self.hitbox_2_x = new_state.hitbox_2_x
        # self.hitbox_2_y = new_state.hitbox_2_y
        # self.hitbox_3_x = new_state.hitbox_3_x
        # self.hitbox_3_y = new_state.hitbox_3_y
        # self.hitbox_4_x = new_state.hitbox_4_x
        # self.hitbox_4_y = new_state.hitbox_4_y
        self.is_attacking = (new_state.hitbox_1_status or new_state.hitbox_2_status or
                new_state.hitbox_3_status or new_state.hitbox_4_status)
        self.self_kill = self.stock == -1 and not self.dead
        self.vector = [0, 0]
        # DEAD_ACTIONS = (Action.DEAD_DOWN, Action.DEAD_LEFT, Action.DEAD_RIGHT,
        #                 Action.DEAD_FLY_STAR, Action.DEAD_FLY, Action.DEAD_FLY_SPLATTER,
        #                 Action.DEAD_FLY_SPLATTER_FLAT)
        self.projectiles = []

    def todict(self):
        return {
            # "facing": self.facing,
            "invulnerable": self.invulnerable,
            # "invulnerability_left": self.invulnerability_left,
            "on_ground": self.on_ground,
            "x": self.x,
            "y": self.y,
            "charging_smash": self.charging_smash,
            "jumps_left": self.jumps_left,
            "on_ground": self.on_ground,
            "move_x": self.move_x,
            "move_y": self.move_y,
            "percent": self.percent,
            "total_percent": self.total_percent,
            "hitstun_left": self.hitstun_left,
            "hit": self.hit,
            # "opponent_percent": self.opponent_percent,
            # "NEUTRAL_ATTACK_1": self.NEUTRAL_ATTACK_1,
            # "NEUTRAL_ATTACK_2": self.NEUTRAL_ATTACK_2,
            # "NEUTRAL_ATTACK_3": self.NEUTRAL_ATTACK_3,
            # "LOOPING_ATTACK_START": self.LOOPING_ATTACK_START,
            # "LOOPING_ATTACK_MIDDLE": self.LOOPING_ATTACK_MIDDLE,
            # "LOOPING_ATTACK_END": self.LOOPING_ATTACK_END,
            # "DASH_ATTACK": self.DASH_ATTACK,
            # "ftilt": self.ftilt,
            # "FTILT_HIGH": self.FTILT_HIGH,
            # "FTILT_HIGH_MID": self.FTILT_HIGH_MID,
            # "FTILT_MID": self.FTILT_MID,
            # "FTILT_LOW_MID": self.FTILT_LOW_MID,
            # "FTILT_LOW": self.FTILT_LOW,
            # "UPTILT": self.UPTILT,
            # "DOWNTILT": self.DOWNTILT,
            # "fsmash": self.fsmash,
            # "FSMASH_MID_HIGH": self.FSMASH_MID_HIGH,
            # "FSMASH_MID": self.FSMASH_MID,
            # "FSMASH_MID_LOW": self.FSMASH_MID_LOW,
            # "FSMASH_LOW": self.FSMASH_LOW,
            # "UPSMASH": self.UPSMASH,
            # "DOWNSMASH": self.DOWNSMASH,
            # "NAIR": self.NAIR,
            # "FAIR": self.FAIR,
            # "BAIR": self.BAIR,
            # "UAIR": self.UAIR,
            # "DAIR": self.DAIR,
            # "NAIR_LANDING": self.NAIR_LANDING,
            # "FAIR_LANDING": self.FAIR_LANDING,
            # "BAIR_LANDING": self.BAIR_LANDING,
            # "UAIR_LANDING": self.UAIR_LANDING,
            # "DAIR_LANDING": self.DAIR_LANDING,
            "dead": self.dead,
            "percent": self.percent,
            # "shield_reflect": self.shield_reflect,
            # "shield_release": self.shield_release,
            # "knee_bend": self.knee_bend,
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
            # "lying_ground_down": self.lying_ground_down,
            "getup_attack": self.getup_attack,
            "grab": self.grab,
            "grab_break": self.grab_break,
            "grabbed": self.grabbed,
            "roll_forward": self.roll_forward,
            "roll_backward": self.roll_backward,
            "spotdodge": self.spotdodge,
            "airdodge": self.airdodge,
            # "bounce_wall": self.bounce_wall,
            # "bounce_ceiling": self.bounce_ceiling,
            "sliding_off_edge": self.sliding_off_edge,
            "edge_hanging": self.edge_hanging,
            "off_stage": self.off_stage,
            # "stock": self.stock,
            "iasa": self.iasa,
            "hitlag_left": self.hitlag_left,
            # "moonwalkwarning": self.moonwalkwarning,
            # "hitbox_1_size": self.hitbox_1_size,
            # "hitbox_2_size": self.hitbox_2_size,
            # "hitbox_3_size": self.hitbox_3_size,
            # "hitbox_4_size": self.hitbox_4_size,
            # "hitbox_1_status": self.hitbox_1_status,
            # "hitbox_2_status": self.hitbox_2_status,
            # "hitbox_3_status": self.hitbox_3_status,
            # "hitbox_4_status": self.hitbox_4_status,
            # "hitbox_1_x": self.hitbox_1_x,
            # "hitbox_1_y": self.hitbox_1_y,
            # "hitbox_2_x": self.hitbox_2_x,
            # "hitbox_2_y": self.hitbox_2_y,
            # "hitbox_3_x": self.hitbox_3_x,
            # "hitbox_3_y": self.hitbox_3_y,
            # "hitbox_4_x": self.hitbox_4_x,
            # "hitbox_4_y": self.hitbox_4_y,
            "edge_catching": self.edge_catching,
            "distance_vector": self.vector,
            "is_attacking": self.is_attacking
            # "projectiles": self.projectiles
        }
