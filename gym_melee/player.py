import melee

class RLPlayer(object):
    """docstring for RLPlayer."""
    def __init__(self, character, controller, debug=False):
        self.character = parse_character(character)
        self.controller = controller
        self.debug = debug

    def take_action(self, gamestate, deltastate):
        melee.techskill.upsmashes(gamestate.ai_state, self.controller)
        if self.debug:
            gamestate.print_state()
            print()
        self.controller.flush()

    def choose_character(self, gamestate):
        melee.menuhelper.choosecharacter(character=self.character,
            gamestate=gamestate, controller=self.controller, swag=True, start=True)
        self.controller.flush()

    def handle_postgame(self, gamestate):
        # Send a Ctrl-C signal to shut down the program. asta la vista
        os.kill(os.getpid(), signal.SIGINT)


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
        if self.debug:
            print('Unrecognized character, using Fox')
        return melee.enums.Character.FOX
