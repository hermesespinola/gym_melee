import signal
import shutil
import melee
import time
import sys
import os
from copy import deepcopy as copy

from gym_melee.framestate import FrameDelta

class MeleeEnv(object):
    """
    Defines a Smash Bros. Melee environment for training an artificial inteligence
    Rewards are proportional to taken (negative) and provoked (Positive) damage.
    Aditionally, a correct use of shield and dodge yields small positive rewards.
    """
    def __init__(self, stage, opponent_port=1, ai_port=2, controllertype='gcna', debug=False):
        check_port(opponent_port)
        check_port(ai_port)
        self.framesaves = os.path.join(os.path.realpath(os.path.curdir), "saves")
        self.debug = debug
        self.log = None
        if debug:
            self.log = melee.logger.Logger()
        self.ai_port = ai_port
        self.ai_character = 'generic'
        self.stage = parse_stage(stage)
        self.opponent_type = parse_controller(controllertype)
        self.framedata = melee.framedata.FrameData(True)

        # Create our Dolphin object. This will be the primary object that we will interface with
        self.dolphin = melee.dolphin.Dolphin(ai_port=ai_port, opponent_port=opponent_port,
            opponent_type=self.opponent_type, logger=self.log)
        # Create our GameState object for the dolphin instance
        self.gamestate = melee.gamestate.GameState(self.dolphin)
        self.deltastate = FrameDelta(self.gamestate)

        def signal_handler(signal, frame):
            self.dolphin.terminate()
            if self.debug:
                self.log.writelog()
                print("") # Because the ^C will be on the terminal
                print("Log file created: " + self.log.filename)
            print("\nShutting down cleanly...")

            self.framedata.saverecording()
            # Delete the empty frame data if there was no game
            with open("framedata.csv", 'r') as f:
                if sum(1 for _ in f) > 2:
                    # organize our data
                    now = time.strftime('%Y_%m_%d_%H_%M_%S')
                    directory = os.path.join(self.framesaves, self.ai_character, now)
                    if not os.path.exists(directory):
                        os.makedirs(directory)
                    shutil.move("framedata.csv", os.path.join(directory))
                    shutil.move("actiondata.csv", os.path.join(directory))
                else:
                    os.remove("framedata.csv")
                    os.remove("actiondata.csv")
            sys.exit(0)

        signal.signal(signal.SIGINT, signal_handler)

    # IDEA: add auto_train feature
    def start(self, iso_path):
        if self.opponent_type == melee.enums.ControllerType.UNPLUGGED:
            self.dolphin.run(render=True)
        else:
            self.dolphin.run(render=True, iso_path=iso_path)
        if self.controller:
            self.controller.connect()

    def step(self, watcher):
        # step to the next frame
        self.gamestate.step()
        if self.gamestate.processingtime * 1000 > 12 and self.debug:
            print("WARNING: Last frame took " + \
                    str(self.gamestate.processingtime*1000) + "ms to process.")

        # What menu are we in? !!!
        if self.gamestate.menu_state == melee.enums.Menu.IN_GAME:
            # Filter states
            self.framedata.recordframe(self.gamestate)

            self.deltastate.step()

            # TODO: add reward
            watcher.take_action(self.deltastate)

        elif self.gamestate.menu_state == melee.enums.Menu.CHARACTER_SELECT:
            watcher.choose_character(self.gamestate)
        elif self.gamestate.menu_state == melee.enums.Menu.POSTGAME_SCORES:
            # Send a Ctrl-C signal to shut down the program. asta la vista
            os.kill(os.getpid(), signal.SIGINT)

        # If we're at the stage select screen, choose a stage
        elif self.gamestate.menu_state == melee.enums.Menu.STAGE_SELECT:
            melee.menuhelper.choosestage(stage=self.stage,
                gamestate=self.gamestate, controller=watcher.controller)
            watcher.controller.flush()
        if self.log:
            self.log.logframe(self.gamestate)
            self.log.writeframe()

        if self.debug:
            self.gamestate.print_state()
        return self.deltastate

    def set_ai_character(self, character):
        self.ai_character = character

    def get_ai_controller(self):
        self.controller = melee.controller.Controller(port=self.ai_port, dolphin=self.dolphin)
        return self.controller

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

def parse_controller(controller):
    if controller == 'gcna':
        return melee.enums.ControllerType.GCN_ADAPTER
    elif controller == 'ps4':
        return melee.enums.ControllerType.PS4
    elif controller == 'xbox':
        return melee.enums.ControllerType.XBOX
    elif controller == 'bot':
        return melee.enums.ControllerType.STANDARD
    else:
        return melee.enums.ControllerType.UNPLUGGED
