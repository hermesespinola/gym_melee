import melee
from melee.enums import Button
import random

A = Button.BUTTON_A.value
A_UP = A + "_UP"
A_DOWN = A + "_DOWN"
A_LEFT = A + "_LEFT"
A_RIGHT = A + "_RIGHT"
SMASH = Button.BUTTON_B.value
SMASH_LEFT = SMASH + "_LEFT"
SMASH_RIGHT = SMASH + "_RIGHT"
SMASH_UP = SMASH + "_UP"
SMASH_DOWN = SMASH + "_DOWN"
GRAB = Button.BUTTON_Z.value
SHIELD = Button.BUTTON_R.value
DODGE_LEFT = SHIELD + "_LEFT"
DODGE_RIGHT = SHIELD + "_RIGHT"
DODGE_DOWN = SHIELD + "_DOWN"
DODGE_UP = SHIELD + "_UP"
MAIN_UP = Button.BUTTON_MAIN.value + "_UP"
MAIN_HALF_UP = Button.BUTTON_MAIN.value + "_HALF_UP"
MAIN_DOWN = Button.BUTTON_MAIN.value + "_DOWN"
MAIN_LEFT = Button.BUTTON_MAIN.value + "_LEFT"
MAIN_RIGHT = Button.BUTTON_MAIN.value + "_RIGHT"

actions = [A, A_UP, A_DOWN, A_LEFT, A_RIGHT, SMASH, SMASH_LEFT, SMASH_RIGHT, \
        SMASH_UP, SMASH_DOWN, GRAB, SHIELD, DODGE_LEFT, DODGE_RIGHT, DODGE_UP, \
        DODGE_DOWN, MAIN_UP, MAIN_HALF_UP, MAIN_DOWN, MAIN_LEFT, MAIN_RIGHT]

def random_action(deltastate):
    action = random.choice(actions)
    return action

class RLPlayer(object):
    """docstring for RLPlayer."""
    action_space_size = len(actions)

    def __init__(self, character, controller, action_chooser=random_action, debug=False):
        self.character = parse_character(character)
        self.controller = controller
        self.debug = debug
        self.action_chooser = action_chooser
        self.controller_action = {
            A: lambda: self.controller.simple_press(0.5, 0.5, Button.BUTTON_A),
            A_UP: lambda: self.controller.simple_press(0.5, 1, Button.BUTTON_A),
            A_DOWN: lambda: self.controller.simple_press(0.5, 0, Button.BUTTON_A),
            A_LEFT: lambda: self.controller.simple_press(0, .5, Button.BUTTON_A),
            A_RIGHT: lambda: self.controller.simple_press(1, .5, Button.BUTTON_A),
            SMASH: lambda: self.controller.simple_press(0.5, 0.5, Button.BUTTON_B),
            SMASH_LEFT: lambda: self.controller.simple_press(0, 0.5, Button.BUTTON_B),
            SMASH_RIGHT: lambda: self.controller.simple_press(1, 0.5, Button.BUTTON_B),
            SMASH_UP: lambda: self.controller.simple_press(0.5, 1, Button.BUTTON_B),
            SMASH_DOWN: lambda: self.controller.simple_press(0.5, 0, Button.BUTTON_B),
            GRAB: lambda: self.controller.simple_press(0.5, 0.5, Button.BUTTON_Z),
            SHIELD: lambda: self.controller.simple_press(0.5, 0.5, Button.BUTTON_R),
            DODGE_UP: lambda: self.controller.simple_press(0.5, 1, Button.BUTTON_R),
            DODGE_DOWN: lambda: self.controller.simple_press(0.5, 0, Button.BUTTON_R),
            DODGE_LEFT: lambda: self.controller.simple_press(0, 0.5, Button.BUTTON_R),
            DODGE_RIGHT: lambda: self.controller.simple_press(1, 0.5, Button.BUTTON_R),
            MAIN_UP: lambda: self.controller.simple_press(0.5, 1, None),
            MAIN_HALF_UP: lambda: self.controller.simple_press(0.5, 0.75, None),
            MAIN_DOWN: lambda: self.controller.simple_press(0.5, 0, None),
            MAIN_LEFT: lambda: self.controller.simple_press(0, 0.5, None),
            MAIN_RIGHT: lambda: self.controller.simple_press(1, 0.5, None)
        }

    def choose_character(self, gamestate):
        melee.menuhelper.choosecharacter(character=self.character,
            gamestate=gamestate, controller=self.controller, swag=True, start=True)
        self.controller.flush()

    def handle_postgame(self, gamestate):
        pass

    def take_action(self, deltastate):
        action = self.action_chooser(deltastate)
        self.controller_action.get(action, lambda: None)()
        self.controller.flush()


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
    elif _character == 'ganondorf' or _character == 'ganon':
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
