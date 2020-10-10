import ast

tit_for_tat_bot_source = """
class TitForTatBot:
    def __init__(self, round=1):
        self.round = round
        self.previous = None
    def move(self, previous=None):
        self.previous = previous
        if self.previous:
            output = self.previous
            return output
        else:
            return 3
"""
exec(compile(ast.parse(tit_for_tat_bot_source), '<string>', mode='exec'), {}, globals())
TitForTatBot.source = tit_for_tat_bot_source


threebot_source = """
class ThreeBot:
    def __init__(self, round=1):
        pass

    def move(self, previous):
        return 3
"""
exec(compile(ast.parse(threebot_source), '<string>', mode='exec'), {}, globals())
ThreeBot.source = threebot_source


escalatorbot_source = """class EscalatorBot:
    def __init__(self, round=1):
        self.round = round
        self.our_previous = None
        self.their_previous = None

    def move(self, previous=None):
        self.their_previous = previous
        if self.their_previous is None or self.our_previous is None:
            self.our_previous = 2
            return 2

        if self.their_previous + self.our_previous > 5:
            play = self.our_previous - 1
        else:
            play = self.our_previous + 1

        # clamp
        if play > 5:
            play = 5
        if play < 0:
            play = 0

        self.our_previous = play
        return play
"""
exec(compile(ast.parse(escalatorbot_source), '<string>', mode='exec'), {}, globals())
EscalatorBot.source = escalatorbot_source


def get_opponent_source(_self):
    # have the test/demo rig set this
    return _self.opponent_source
