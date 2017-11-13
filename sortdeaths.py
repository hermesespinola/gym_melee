from pymongo import MongoClient
import pprint

client = MongoClient('mongodb://hermes:hermes@info.gda.itesm.mx:27017/melee')
db = client['melee']
collection = db['games']

one = collection.find()[0]
print(one['date'])


# for i in one['p1']['frame']:


print('=======================================================')

prev = {'percent': 0}
for i in one['p2']['frame']:
    if i['stock'] != 0:
        # pprint.pprint(prev['percent'])
        pprint.pprint(i['percent'])
        print(i['dead'], i['dead_fall'], i['stock'])
    prev = i

# Atributos neutrales
"""
invulnerable
invulnerability
on_ground
charging_smash
hit
shield_release
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
hitted
dead
tumbling
tech_miss
grabbed
grab_break
"""