from melee import techskill
from pprint import pprint

class Player(object):
    """docstring for Player."""
    def __init__(self, gamestate, controller, log=False):
        super(Player, self).__init__()
        self.gamestate = gamestate
        self.controller = controller
        self.log = log

    def play(self):
        # TODO: recognize a good or bad move and filter them, create a csv that
        #       contains the good lines of framedata and actiondata and a tag
        #       of the stage and the opponent
        techskill.upsmashes(ai_state=self.gamestate.ai_state, controller=self.controller)
        if self.log:
            self.gamestate.print_state()
            print("")
