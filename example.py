#!/usr/bin/python3
import melee
import argparse
import signal
import shutil
import sys, os, time

cwd = os.path.realpath(os.path.curdir)
framesaves = os.path.join(cwd, "saves")

def parse_character(character):
    _character = "".join(character.split('_')).lower()
    if _character == 'fox' or _character == 'hack':
        return melee.enums.Character.FOX
    elif _character == 'cptfalcon' or _character == 'falcon' or _character == 'captainfalcon':
        return melee.enums.Character.CPTFALCON
    elif _character == 'doc' or _character == 'doctor' or _character == 'doctormario':
        return melee.enums.Character.DOC
    elif _character == 'mario':
        return melee.enums.Character.MARIO
    elif _character == 'luigi':
        return melee.enums.Character.LUIGI
    elif _character == 'bowser':
        return melee.enums.Character.BOWSER
    elif _character == 'peach':
        return melee.enums.Character.PEACH
    elif _character == 'yoshi':
        return melee.enums.Character.YOSHI
    elif _character == 'dk' or _character == 'donkeykong':
        return melee.enums.Character.DK
    elif _character == 'ganondorf':
        return melee.enums.Character.GANONDORF
    elif _character == 'falco':
        return melee.enums.Character.FALCO
    elif _character == 'ness':
        return melee.enums.Character.NESS
    elif _character == 'iceclimbers':
        return melee.enums.Character.ICECLIMBERS
    elif _character == 'kirby':
        return melee.enums.Character.KIRBY
    elif _character == 'zelda':
        return melee.enums.Character.ZELDA
    elif _character == 'link':
        return melee.enums.Character.LINK
    elif _character == 'ylink' or _character == 'younglink':
        return melee.enums.Character.YLINK
    elif _character == 'pichu':
        return melee.enums.Character.PICHU
    elif _character == 'pikachu':
        return melee.enums.Character.PIKACHU
    elif _character == 'jigglypuff':
        return melee.enums.Character.JIGGLYPUFF
    elif _character == 'mewtwo':
        return melee.enums.Character.MEWTWO
    elif _character == 'gameandwatch':
        return melee.enums.Character.GAMEANDWATCH
    elif _character == 'marth':
        return melee.enums.Character.MARTH
    elif _character == 'roy':
        return melee.enums.Character.ROY
    elif _character == 'sheik':
        return melee.enums.Character.SHEIK
    else:
        print('Unrecognized character, using Fox')
        return melee.enums.Character.FOX

def parse_stage(stage):
    _stage = "".join(stage.split('_')).lower()
    if _stage == 'battlefield':
        return melee.enums.Stage.BATTLEFIELD
    elif _stage == 'finaldestination' or _stage == 'final' or _stage == 'destination':
        return melee.enums.Stage.FINAL_DESTINATION
    elif _stage == 'pokemonstadium' or _stage == 'pokemon' or _stage == 'stadium':
        return melee.enums.Stage.POKEMON_STADIUM
    elif _stage == 'dreamland':
        return melee.enums.Stage.DREAMLAND
    elif _stage == 'fountain' or _stage == 'fountainofdreams':
        return melee.enums.Stage.FOUNTAIN_OF_DREAMS
    elif _stage == 'yoshisstory' or _stage == 'yoshis' or _stage == 'story':
        return melee.enums.Stage.YOSHIS_STORY
    else:
        print('Unrecognized stage, using Battlefield')
        return melee.enums.Stage.BATTLEFIELD

def check_port(value):
    ivalue = int(value)
    if ivalue < 1 or ivalue > 4:
         raise argparse.ArgumentTypeError("%s is an invalid controller port. \
         Must be 1, 2, 3, or 4." % value)
    return ivalue

parser = argparse.ArgumentParser(description='Example of libmelee in action')
parser.add_argument('--port', '-p', type=check_port,
                    help='The controller port your AI will play on',
                    default=2)
parser.add_argument('--opponent', '-o', type=check_port,
                    help='The controller port the opponent will play on',
                    default=1)
parser.add_argument('--live', '-l',
                    help='The opponent is playing live with a GCN Adapter',
                    default=True)
parser.add_argument('--debug', '-d', action='store_true',
                    help='Debug mode. Creates a CSV of all game state')
parser.add_argument('--framerecord', '-r', default=False, action='store_true',
                    help='Records frame data from the match, stores into framedata.csv')
parser.add_argument('--character', '-c', default='fox',
                    help='The ai selected character')
parser.add_argument('--stage', '-s', default='battlefield',
                    help='The selected stage')
parser.add_argument('--ai', '-a', action='store_true',
                    help='Run ai')


args = parser.parse_args()

character = parse_character(args.character)
stage = parse_stage(args.stage)

log = None
if args.debug:
    log = melee.logger.Logger()

framedata = melee.framedata.FrameData(args.framerecord)

#Options here are:
#   "Standard" input is what dolphin calls the type of input that we use
#       for named pipe (bot) input
#   GCN_ADAPTER will use your WiiU adapter for live human-controlled play
#   UNPLUGGED is pretty obvious what it means
opponent_type = melee.enums.ControllerType.UNPLUGGED
if args.live:
    opponent_type = melee.enums.ControllerType.GCN_ADAPTER

# Create our Dolphin object. This will be the primary object that we will interface with
dolphin = melee.dolphin.Dolphin(ai_port=args.port, opponent_port=args.opponent,
    opponent_type=opponent_type, logger=log)
#Create our GameState object for the dolphin instance
gamestate = melee.gamestate.GameState(dolphin)
#Create our Controller object that we can press buttons on
controller = melee.controller.Controller(port=args.port, dolphin=dolphin)

def signal_handler(signal, frame):
    dolphin.terminate()
    if args.debug:
        log.writelog()
        print("") #because the ^C will be on the terminal
        print("Log file created: " + log.filename)
    print("Shutting down cleanly...")
    if args.framerecord:
        framedata.saverecording()
        # organize our data
        now = time.strftime('%Y\-%m\-%d_%H\-%M\-%S')
        directory = os.path.join(framesaves, args.character, now)
        if not os.path.exists(directory):
            os.makedirs(directory)
        shutil.move("framedata.csv", os.path.join(directory))
        shutil.move("actiondata.csv", os.path.join(directory))
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

#Run dolphin and render the output
dolphin.run(render=True)

# Plug our controller in
#   Due to how named pipes work, this has to come AFTER running dolphin
#   NOTE: If you're loading a movie file, don't connect the controller,
#   dolphin will hang waiting for input and never receive it
controller.connect()

#Main loop
while True:
    #"step" to the next frame
    gamestate.step()
    if(gamestate.processingtime * 1000 > 12):
        print("WARNING: Last frame took " + str(gamestate.processingtime*1000) + "ms to process.")

    #What menu are we in?
    if gamestate.menu_state == melee.enums.Menu.IN_GAME:
        if args.framerecord:
            framedata.recordframe(gamestate)

        # This is where your AI does all of its stuff!
        if args.framerecord and args.ai:
            melee.techskill.upsmashes(ai_state=gamestate.ai_state, controller=controller)
        else:
            melee.techskill.multishine(ai_state=gamestate.ai_state, controller=controller)
    #If we're at the character select screen, choose our character
    elif gamestate.menu_state == melee.enums.Menu.CHARACTER_SELECT:
        melee.menuhelper.choosecharacter(character=character,
            gamestate=gamestate, controller=controller, swag=True, start=False)
    #If we're at the postgame scores screen, spam START
    elif gamestate.menu_state == melee.enums.Menu.POSTGAME_SCORES:
        melee.menuhelper.skippostgame(controller=controller)
    #If we're at the stage select screen, choose a stage
    elif gamestate.menu_state == melee.enums.Menu.STAGE_SELECT:
        melee.menuhelper.choosestage(stage=stage,
            gamestate=gamestate, controller=controller)
    #Flush any button presses queued up
    controller.flush()
    if log:
        log.logframe(gamestate)
        log.writeframe()
