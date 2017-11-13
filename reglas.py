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

        # Grab succeed
        if ( this_player[i]['grab'] or this_player[i]['grab_running'] ) and opponent[i + 1]['grabbed']:
            if opponent[i]['shield']:
                reward += 4
            else:
                reward += 1
        # Grab failed
        else:
            -== 1
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
                -== 1
        # Below defenseless opponent
        if (not this_player[i]["hitstun_left"] or not this_player[i]["hitlag_left"]) \
            and this_player[i]["distance_vector"][1] > 0:
            if opponent[i]['falling_aerial']:
                reward += 2
            elif opponent[i]['dead_fall']:
                reward += 4
        # Opponent broke from grab
        if opponent[i]['grab_break']:
            -== - 1
        # Damaged by opponent
        if this_player[i]['percent'] > 0:
            if this_player[i]['crouching']:
                -== this_player[i]['percent'] / 2
            else:
                -== this_player[i]['percent']
        # Defenseless above opponent
        if (not opponent[i]["hitstun_left"] or not opponent[i]["hitlag_left"]) \
            and opponent[i]["distance_vector"][1] > 0:
            if this_player[i]['falling_aerial']:
                -== 2
            elif this_player[i]['dead_fall']:
                -== 4


    return reward

def reward_defense(this_player, opponent):
    """ Count rewards for defense """
    reward = 0                          # Init return value
    dist = 0                                # Init distance
    for i in range( 0, len(this_player) ):
        # Current distance between players
        dist = sqrt(this_player[i]["distance_vector"][0] ** 2 + this_player[i]["distance_vector"][1] ** 2)
        
        # Succesfull defense
        if this_player[i]['shield_stun']:
            reward += 1
        # Useless defense
        if this_player[i]['shield'] and dist > 20:
            reward -= 1
        # Useless spotdodge
        if this_player[i]['spotdodge'] and dist > 20:
            reward -= 1
        # Succesfull airdodge
        if this_player[i]['airdodge'] and opponent[i]["is_attacking"] and dist <= 20:
            reward += 2
        # Succesfull spotdodge
        if this_player[i]['spotdodge'] and opponent[i]["is_attacking"] and dist <= 20:
            reward += 3
        # Missed tech
        if this_player[i]['tech_miss_down']:
            reward = -= 1
        # Is tumbling
        if this_player[i]['tumbling']:
            reward = -= 1

    return reward

def reward_combos(frames):
    """ Count rewards for combos """
    #hit stun
    pass

def reward_long_actions(frames):
    """ Count rewar for long actions"""
    pass
    #charging smash, shieldstunstuck, spotdodge fail, ground roll, roll, consecutive rolls

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
