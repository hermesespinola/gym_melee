#!/usr/bin/python3
import argparse
import gym_melee
import melee.enums
from pymongo import MongoClient
from pprint import pprint
from math import sqrt
from copy import deepcopy as copy

parser = argparse.ArgumentParser(description='Example gym_melee')
parser.add_argument('--port', '-p',
                    help='The controller port your AI will play on',
                    default=2)
parser.add_argument('--opponent', '-o',
                    help='The controller port the opponent will play on',
                    default=1)
parser.add_argument('--controller', '-i',
                    help='The controller type, options are gcna, ps4, xbox, bot and unplugged',
                    default='gcna')
parser.add_argument('--aicontroller', '-a',
                    help='Should the ai port play as a bot or read from a controller same options as in --controller',
                    default='bot')
parser.add_argument('--debug', '-d', action='store_true',
                    help='Debug mode.')
parser.add_argument('--character', '-c', default='fox',
                    help='The ai selected character')
parser.add_argument('--stage', '-s', default='battlefield',
                    help='The selected stage')
parser.add_argument('--p1name', '-q',
                    help='Name for p1',
                    default='Jorge')
parser.add_argument('--p2name', '-w',
                    help='Name for p2',
                    default='Carlos')

args = parser.parse_args()
character = args.character
stage = args.stage
debug = args.debug

# tells controller type (standard, gc, etc.)
# STANDARD = "6"
# GCN_ADAPTER = "12"
# UNPLUGGED = "0"
# XBOX = "2"
# PS4 = "4"
controller_type = args.controller
ai_controller_type = args.aicontroller

# Starts dolphin, inits some stuff.
env = gym_melee.MeleeEnv(stage, controller_type=controller_type,
                    ai_controller_type=ai_controller_type, debug=debug)

# The ai player
player = gym_melee.RLPlayer(character, env.get_ai_controller(), debug=debug)

# Game loop
# TODO: Guardar datos en mongo
client = MongoClient('mongodb://hermes:hermes@info.gda.itesm.mx:27017/melee')
db = client['melee']
collection = db['games']

# env.start('/run/media/andres/TI10701100B/Things/ROMs & ISOs/Super Smash Bros. Melee (v1.02).iso')
env.start('Super Smash Bros. Melee (v1.02).iso')

from datetime import datetime

while env.step(player).gamestate.menu_state != melee.enums.Menu.IN_GAME:
    continue

step = env.step(player)
p1_name = str(step.gamestate.player[args.opponent].character)[10:]
p2_name = str(step.gamestate.player[args.port].character)[10:]

now = datetime.now()

buffer_p1 = {
    'name': args.p1name,
    'flip': False,
    'date': datetime.now(),
    'global_date': now,
    'p1': {
        'character':p1_name,
        'frame':[]
    },
    'p2': {
    'character': p2_name,
    'frame': []
    }
}
buffer_p2 = {
    'name': args.p2name,
    'flip': True,
    'date': datetime.now(),
    'global_date': now,
    'p1': {
        'character':p2_name,
        'frame':[]
    },
    'p2': {
    'character': p1_name,
    'frame': []
    }
}

plays = []

step = env.step(player)
while step.gamestate.menu_state == melee.enums.Menu.IN_GAME:
    buffer_p1['p1']['frame'].append(step.opponent.todict())
    buffer_p1['p2']['frame'].append(step.ai.todict())
    buffer_p2['p2']['frame'].append(step.opponent.todict())
    buffer_p2['p1']['frame'].append(step.ai.todict())
    if step.opponent.stock == -1:
        plays.append(buffer_p1)
        buffer_p1 = {
            'name': args.p1name,
            'flip': False,
            'date': datetime.now(),
            'global_date': now,
            'p1': {
                'character':p1_name,
                'frame':[]
            },
            'p2': {
                'character': p2_name,
                'frame': []
            }
        }
    if step.ai.stock == -1:
        plays.append(buffer_p2)
        buffer_p2 = {
            'name': args.p2name,
            'flip': True,
            'date': datetime.now(),
            'global_date': now,
            'p1': {
                'character':p2_name,
                'frame':[]
            },
            'p2': {
                'character': p1_name,
                'frame': []
            }
        }
    step = env.step(player)
    if step.opponent.attack_state == melee.enums.AttackState.ATTACKING:
        print (step.opponent.attack_state)

winner = plays[-1]['flip']
for p in plays:
    if not p['flip']:
        p['winner'] = winner
    else:
        p['winner'] = not winner
print('Saving...')
[print ('Saved:', collection.insert_one(p).inserted_id) for p in plays]
# mongo_id = collection.insert_one(game)
# collection.update_one({'_id': mongo_id.inserted_id}, {"$set": {
#     'p2.frame': p2_frame
# }}, upsert=False)
print('Saved.')

while True:
    env.step(player)
