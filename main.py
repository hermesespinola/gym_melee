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
                    help='The controller port the second player will play on',
                    default=2)
parser.add_argument('--opponent', '-o',
                    help='The controller port the first player will play on',
                    default=1)
parser.add_argument('--controller', '-i',
                    help='The controller type of the first player, options are gcna, ps4, xbox and unplugged',
                    default='gcna')
parser.add_argument('--aicontroller', '-a',
                    help='The controller type of the second player. options are gcna, ps4, xbox, bot and unplugged',
                    default='bot')
parser.add_argument('--debug', '-d', action='store_true',
                    help='Debug mode.')
parser.add_argument('--character', '-c', default='fox',
                    help='The bot selected character')
parser.add_argument('--stage', '-s', default='battlefield',
                    help='The bot selected stage')
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

controller_type = args.controller
ai_controller_type = args.aicontroller

# Starts dolphin, inits some stuff.
env = gym_melee.MeleeEnv(stage, controller_type=controller_type,
                    ai_controller_type=ai_controller_type, debug=debug)

# The ai player
player = gym_melee.RLPlayer(character, env.get_ai_controller(), debug=debug)

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

# Game loop
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

winner = plays[-1]['flip']
for p in plays:
    if not p['flip']:
        p['winner'] = winner
    else:
        p['winner'] = not winner
print('Saving...')
[print ('Saved:', collection.insert_one(p).inserted_id) for p in plays]

while True:
    env.step(player)
