import logging
import sys

from abstract_spy_tree_bot import AbstractSpyTreeBot
from extra import TitForTatBot, ThreeBot, EscalatorBot

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


def demo(bot_a, bot_b):
    for one, other in [(bot_a, bot_b), (bot_b, bot_a)]:
        if getattr(one, 'source', None):
            other.opponent_source = one.source

    previous_a = None
    previous_b = None
    for _ in range(10):
        move_a = bot_a.move(previous=previous_b)
        move_b = bot_b.move(previous=previous_a)

        previous_a = move_a
        previous_b = move_b

        print("{} vs. {}".format(move_a, move_b))


if __name__ == "__main__":
    demo(AbstractSpyTreeBot(), EscalatorBot())
