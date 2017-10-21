#!/usr/bin/python3
import argparse
import gym_melee

parser = argparse.ArgumentParser(description='Example of libmelee in action')
parser.add_argument('--port', '-p',
                    help='The controller port your AI will play on',
                    default=2)
parser.add_argument('--opponent', '-o',
                    help='The controller port the opponent will play on',
                    default=1)
parser.add_argument('--controller', '-i',
                    help='The controller type, options are gcna, ps4, xbox, bot and unplugged',
                    default='gcna')
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
controller = args.controller

# Starts dolphin, inits some stuff.
env = gym_melee.MeleeEnv(stage, controllertype=controller, debug=debug)

# The ai player
# TODO: use a real player
player = gym_melee.RLPlayer(character, env.get_ai_controller(), debug=debug)

# Game loop
env.start('Super Smash Bros. Melee (v1.02).iso')
while True:
    dframe = env.step(player).ai
    if dframe.dead:
        print("dead")
    if dframe.shield_reflect:
        print("shield_reflect")
    if dframe.falling:
        print("falling")
    if dframe.falling_aerial:
        print("falling_aerial")
    if dframe.dead_fall:
        print("dead_fall")
    if dframe.tumbling:
        print("tumbling")
    if dframe.crouching:
        print("crouching")
    if dframe.landing:
        print("landing")
    if dframe.landing_special:
        print("landing_special")
    if dframe.shield:
        print("shield")
    if dframe.shield_stun:
        print("shield_stun")
    if dframe.ground_getup:
        print("ground_getup")
    if dframe.ground_roll_forward_up:
        print("ground_roll_forward_up")
    if dframe.ground_roll_backward_up:
        print("ground_roll_backward_up")
    if dframe.tech_miss_down:
        print("tech_miss_down")
    if dframe.lying_ground_down:
        print("lying_ground_down")
    if dframe.getup_attack:
        print("getup_attack")
    if dframe.grab:
        print("grab")
    if dframe.grab_break:
        print("grab_break")
    if dframe.grabbed:
        print("grabbed")
    if dframe.roll_forward:
        print("roll_forward")
    if dframe.roll_backward:
        print("roll_backward")
    if dframe.spotdodge:
        print("spotdodge")
    if dframe.airdodge:
        print("airdodge")
    if dframe.bounce_wall:
        print("bounce_wall")
    if dframe.bounce_ceiling:
        print("bounce_ceiling")
    if dframe.sliding_off_edge:
        print("sliding_off_edge")
    if dframe.edge_hanging:
        print("edge_hanging")
    if dframe.hit:
        print("hit:", dframe.opponent_percent)
    if dframe.hitted:
        print("hitted:", dframe.percent)
