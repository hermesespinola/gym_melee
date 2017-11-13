from pymongo import MongoClient
from math import sqrt

def Frame_rewards(id):
    """Calculate total rewards for specific game Id.

    :param id: A string, the game id from MongoDB
    :rtype: A dictionary with reward data
    """
    # Connect to mongoDB.
    client = MongoClient('mongodb://hermes:hermes@info.gda.itesm.mx:27017/melee')
    db = client['melee']
    collection = db['games']

    # Get the specific game
    one = collection.find_one( {"_id": id} )

    # Init dictionary of data
    game_info = {}

    # Init player frames
    player_frames = one['p1']['frame']
    opponent_frames = one['p2']['frame']

    # Add meta data
    game_info['date'] = one['date']
    game_info['matchup'] = one['p1']['character'] + " vs " + one['p2']['character']

    # Add total of Offensive Rewards
    game_info['offensive_reward'] = reward_attack( player_frames, opponent_frames  )

    # Add total of Defense Rewards
    game_info['defensive_reward'] = reward_defense( player_frames, opponent_frames  )

    return game_info

def reward_attack(this_player, opponent):
    """Count offense reward."""
    dist = 0                                    # Init distance
    reward = 0                                  # Init return value
    for i in range( 0, len(this_player) ):
        """ Iterate over each frame data """
        # Current distance between players
        dist = sqrt(this_player[i]["distance_vector"][0] ** 2 + this_player[i]["distance_vector"][1] ** 2)

        # Charging smash
        if this_player[i]['charging_smash']:
            while this_player[i]['charging_smash'] and i < len(this_player):
                i += 1
            # Frame ended
            if i < len(this_player):
                break
            # Smash did damage
            elif opponent[i]['percent'] > 0:
                reward += 10
            # Smash hit shield
            elif opponent[i]['shield_stun'] > 0:
                reward += 1
            # Smash missed or useless
            else:
                reward -= 5
        else:
            # Grab succeed
            if ( this_player[i]['grab'] or this_player[i]['grab_running'] ) and opponent[i + 1]['grabbed']:
                if opponent[i]['shield']:
                    reward += 4
                else:
                    reward += 1
            # Grab failed
            if ( this_player[i]['grab'] or this_player[i]['grab_running'] ) and not opponent[i + 1]['grabbed']:
                reward -= 1
            """ Add GRAB_PUMMEL to DB
            # Damage p2 with grab
            if this_player[i]['grab_pummel']:
                reward += 1
            """
            # Attack
            if this_player[i]['is_attacking']:     
                # Success                               
                if opponent[i]['percent'] > 0:                                 
                    reward += opponent[i]['percent']
                # Attacking ghosts
                if dist > 20:
                    reward -= 1
                # Trade off
                if opponent[i]['percent'] > 0 and this_player[i]['percent'] > 0:
                    reward += (this_player[i]['percent'] - opponent[i]['percent'])
            # Below defenseless opponent
            if (not this_player[i]["hitstun_left"] or not this_player[i]["hitlag_left"]) \
                and this_player[i]["distance_vector"][1] > 0:
                if opponent[i]['falling_aerial']:
                    reward += 2
                elif opponent[i]['dead_fall']:
                    reward += 4
            # Opponent broke from grab
            if opponent[i]['grab_break']:
                reward -= 1
            # Damaged by opponent
            if this_player[i]['percent'] > 0:
                if this_player[i]['crouching']:
                reward -= this_player[i]['percent'] / 2
                else:
                reward -= this_player[i]['percent']
                
    return reward

def reward_defense(this_player, opponent):
    """ Count rewards for defense """
    reward = 0                              # Init return value
    dist = 0                                # Init distance
    for i in range( 0, len(this_player) ):
        # Current distance between players
        dist = sqrt(this_player[i]['distance_vector'][0] ** 2 + this_player[i]['distance_vector'][1] ** 2)
        # Next didtance
        dist_next = sqrt(this_player[i + 1]['distance_vector'][0] ** 2 + this_player[i + 1]['distance_vector'][1] ** 2)

        # Spotdodging
        if this_player[i]['spotdodge']:
            while this_player[i]['spotdodge'] and i < len(this_player):
                # Succesfull spotdodge
                if opponent[i]['is_attacking'] and dist <= 20:
                    reward += 3
                # Useless spotdodge
                if dist > 20:
                    reward -= 1
                i += i
            # Frame ended
            if i < len(this_player):
                break
            # Spotdodge ended and you was hit by opponent
            elif this_player[i]['percent'] > 0:
                reward -= 3
        # Ground rolling
        elif this_player[i]['ground_roll_forward_up'] or this_player[i]['ground_roll_backward_up']:
            while this_player[i]['ground_roll_forward_up'] or this_player[i]['ground_roll_backward_up'] and i < len(this_player):
                i += 1
            # Frame ended
            if i < len(this_player):
                break
            # Ground rolling ended and you was hit by opponent
            elif this_player[i]['percent'] > 0:
                reward -= 3
        # Rolling
        elif this_player[i]['roll_forward'] or this_player[i]['roll_backward']:
            while this_player[i]['roll_forward'] or this_player[i]['roll_backward'] and i < len(this_player):
                # Good roll
                if dist <= 20 and opponent[i]['is_attacking']:
                    if dist_next > dist and (this_player[i]['roll_forward'] or this_player[i]['roll_backward']):
                        reward += 2
                i += 1
            # Frame ended
            if i < len(this_player):
                break
            # Rolling ended and you was hit by opponent
            elif this_player[i]['percent'] > 0:
                reward -= 3
        else:
            # Succesfull defense
            if this_player[i]['shield_stun']:
                reward += 1
            # Useless defense
            if this_player[i]['shield'] and dist > 20:
                reward -= 1
            # Succesfull airdodge
            if this_player[i]['airdodge'] and opponent[i]['is_attacking'] and dist <= 20:
                reward += 2
            # Missed tech
            if this_player[i]['tech_miss_down']:
                reward -= 2
            # Is tumbling
            if this_player[i]['tumbling']:
                reward -= 1
            # Defenseless above opponent
            if (not opponent[i]["hitstun_left"] or not opponent[i]["hitlag_left"]) \
                and opponent[i]["distance_vector"][1] > 0:
                if this_player[i]['falling_aerial']:
                    reward -= 2
                elif this_player[i]['dead_fall']:
                    reward -= 4

    return reward

def reward_combos(this_player, opponent):
    """ Count rewards for combos """
    #hit stun
    # TODO Checar si hitstun comienza con hit o depues de hitlag
    # TODO Threshold para non-true combos
    # TODO get reward
    combos = []
    current = None
    for i in range(len(this_player)):
        if current is None:
            current = {
                'percent': 0,
                'hits': 0,
                'ends_offstage': False
                'kills': False
            }

        pf = this_player[i]
        of = opponent[i]

        if of['percent'] > 0:
            current['percent'] += of['percent']
            current['hits'] += 1

        if of['stock'] == -1:
            current['kills'] = True

        if of['hitstun_left'] == 0:
            current['ends_offstage'] = of['off_stage']
            if current['hits'] > 1:
                combos.append(current)
            current = None
    pass

#shieldstunstuck

def check_deads(frames):
    """ Check whether if was suicide or killed by opponent """
    pass





"""Used For testing: can be deleted any time
# Connect to mongoDB.
client = MongoClient('mongodb://hermes:hermes@info.gda.itesm.mx:27017/melee')
db = client['melee']
collection = db['games']

# Get only one 'game'.
one = collection.find()[6]

# Print meta data
print(one['date'])
print(one['p1']['character'] + " vs " + one['p2']['character'])

#print("Offensive frames")
#reward_attack(one['p1']['frame'], one['p2']['frame'])

print("Defensive frames")
reward_defense(one['p1']['frame'], one['p2']['frame'])

"""

# Atributos neutrales
"""
invulnerable
invulnerability
on_ground
charging_smash
hit
shield
falling
falling_aerial
dead_fall
crouching
ground_getup
ground_roll_forward_up
grounf_roll_backward_up
roll_forward dist:20
roll_backward
spotdodge
airdodge
offstage
iasa
"""
# Atributos Buenos
"""
shield_reflect
grab
"""
#Atributos Malos
"""
hit_lag
hit_stun
dead
tumbling
tech_miss
grabbed
grab_break
"""
