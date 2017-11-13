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

from pymongo import MongoClient
from pprint import pprint
from math import sqrt

def reward_attack(p1_frames, p2_frames):
    """ Count rewards for attacking """
    atk_reward = 0
    for i in range( 0, len(p1_frames) ):
        # Good values
        if p1_frames[i]['grab']:
            atk_reward = atk_reward + 2
        if p1_frames[i]['hit']:
            atk_reward = atk_reward + 1
        if p2_frames[i]['dead_fall'] and (not p1_frames[i]["hitstun_left"] or not p1_frames[i]["hitlag_left"]) and p1_frames[i]["distance_vector"][1] > 0:
            atk_reward = atk_reward + 5
        if p2_frames[i]['falling_aerial'] and (not p1_frames[i]["hitstun_left"] or not p1_frames[i]["hitlag_left"]) and p1_frames[i]["distance_vector"][1] > 0:
            atk_reward = atk_reward + 3

        # Negative Values
        if p2_frames[i]['grab_break']:
            atk_reward = atk_reward - 1
        if p2_frames[i]['hit']:
            atk_reward = atk_reward - 1
        if p1_frames[i]['dead_fall'] and (not p2_frames[i]["hitstun_left"] or not p2_frames[i]["hitlag_left"]) and p1_frames[i]["distance_vector"][1] < 0:
            atk_reward = atk_reward - 5
        if p1_frames[i]['falling_aerial'] and (not p2_frames[i]["hitstun_left"] or not p2_frames[i]["hitlag_left"]) and p1_frames[i]["distance_vector"][1] < 0:
            atk_reward = atk_reward - 3

        if atk_reward < 0:
            # Meterlo a una coleccion de frames negativos
            print("Frame malo: " + str(atk_reward))

        if atk_reward > 0:
            # Meterlo a una coleccion de frmaes positivos
            print("Frame bueno: " + str(atk_reward))

        atk_reward = 0


    return atk_reward

def reward_defense(p1_frames, p2_frames):
    """ Count rewards for defense """
    def_reward = 0
    dist = 0
    for i in range( 0, len(p1_frames) ):
        dist = sqrt(p1_frames[i]["distance_vector"][0] ** 2 + p1_frames[i]["distance_vector"][1] ** 2)
        # Good Values
        if p1_frames[i]['shield_stun']:
            def_reward = def_reward + 3
        if p1_frames[i]['airdodge'] and p2_frames[i]["is_atacking"] and dist <= 20:
            def_reward = def_reward + 7
        if p1_frames[i]['spotdodge'] and p2_frames[i]["is_atacking"] and dist <= 20:
            def_reward = def_reward + 7
        if p1_frames[i]['crouching'] and p2_frames[i]['hit']:
            def_reward = def_reward + 2
        
        # Negative Values
        if p1_frames[i]['tech_miss_down']:
            def_reward = def_reward - 1
        if p1_frames[i]['tumbling']:
            def_reward = def_reward - 1


        if def_reward < 0:
            # Meterlo a una coleccion de frames negativos
            print("Frame malo: " + str(def_reward))

        if def_reward > 0:
            # Meterlo a una coleccion de frmaes positivos
            print("Frame bueno: " + str(def_reward))
        def_reward = 0

def reward_combos(frames):
    """ Count rewards for combos """
    pass

def reward_long_actions(frames):
    """ Count rewar for long actions"""
    #charging smash, shieldstunstuck, spotdodge fail, ground roll, roll

def check_deads(frames):
    """ Check whether if was suicide or killed by opponent """
    pass

# Connect to mongoDB.
client = MongoClient('mongodb://hermes:hermes@info.gda.itesm.mx:27017/melee')
db = client['melee']
collection = db['games']

# Get only one 'game'.
one = collection.find()[0]

# Print meta data
print(one['date'])
print(one['p1']['character'] + " vs " + one['p2']['character'])

#print("Offensive frames")
#reward_attack(one['p1']['frame'], one['p2']['frame'])

print("Defensive frames")
reward_defense(one['p1']['frame'], one['p2']['frame'])


