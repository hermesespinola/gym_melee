#!/usr/bin/python3
import argparse
import gym_melee
import melee.enums
from pymongo import MongoClient
from pprint import pprint
from math import sqrt

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
now = datetime.now()
# Date of game
col_time = '%s-%s-%s-%s-%s' % (now.year, now.month, now.day, now.hour, now.minute)

while env.step(player).gamestate.menu_state != melee.enums.Menu.IN_GAME:
    continue

step = env.step(player)
p1_name = str(step.gamestate.player[args.opponent].character)[10:]
p2_name = str(step.gamestate.player[args.port].character)[10:]
game = {
    'date':now,
    'p1': {
        'character':p1_name,
        'frame':[]
    },
    'p2': {
    'character': p2_name,
    'frame': []
    }
}
p2_frame = []

step = env.step(player)
while step.gamestate.menu_state == melee.enums.Menu.IN_GAME:
    game['p1']['frame'].append(step.opponent.todict())
    p2_frame.append(step.ai.todict())
    step = env.step(player)
    # if step.opponent.dead_fall:
    #     print ("Deadfall!!!!")
    # if step.opponent.falling:
    #     print ("Falling!!!!")
    # if step.opponent.falling_aerial:
    #     print ("falling aerial!!!!!")
    # if step.opponent.shield_stun:
    #     print("shield stun!!!")
    # if step.opponent.shield_reflect:
    #     print("shield reflect!!!")
    # if step.opponent.shield:
    #     print("shield!!!")
    # print ("Vector:", step.opponent.x - step.ai.x, step.opponent.y - step.ai.y)
    # print ("Distance:", sqrt((step.opponent.x - step.ai.x) ** 2 + (step.opponent.y - step.ai.y) ** 2))

mongo_id = collection.insert_one(game)
collection.update_one({'_id': mongo_id.inserted_id}, {"$set": {
    'p2.frame': p2_frame
}}, upsert=False)
print('Saved.')

while True:
    env.step(player)
