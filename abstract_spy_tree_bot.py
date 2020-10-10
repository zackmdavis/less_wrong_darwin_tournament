import ast
import logging
from string import ascii_lowercase

from extra import get_opponent_source


class AbstractSpyTreeBot:
    def __init__(self, round=1):
        self.round = round
        self.our_previous = None
        self.their_previous = None

    def fallback_play(self):
        # mostly uninspired copycat behavior, but—
        if self.their_previous is not None and self.our_previous is not None:
            # let's at least try to break out of overdemand deadlocks
            if self.our_previous + self.their_previous > 5:
                play = 5 - self.their_previous
            else:
                play = self.their_previous
        else:
            play = 3

        self.our_previous = play
        return play

    def move(self, previous=None):
        self.their_previous = previous
        try:
            # try to spy on and simulate what they'll do and grab all the
            # surplus
            spy_agent_name = ''.join(
                ascii_lowercase[(ascii_lowercase.find(c)+13) % 26]
                if c in ascii_lowercase else '_'
                for c in "trg_bccbarag_fbhepr"
            )
            raw_enemy = globals().get(spy_agent_name)(self)
            # but if they're spying on us (look for the function name, or
            # `globals` if someone else thought of the same obfuscation as us),
            # we don't want to participate in an infinite loop that'll get us
            # disqualified—fall back to fallback behavior
            if spy_agent_name in raw_enemy or "globals" in raw_enemy:
                return self.fallback_play()

            enemy_tree = ast.parse(raw_enemy)
            enemy_classes = [
                s for s in enemy_tree.body if isinstance(s, ast.ClassDef)
            ]
            assert len(enemy_classes) == 1
            enemy_true_name = enemy_classes[0].name
            enemy_tree.body.append(
                ast.parse(
                    "prediction_box[0] = {}(round={}).move(previous={})".format(
                        enemy_true_name, self.round, self.our_previous
                    )
                ).body[0]
            )
            prediction_box = [2]
            exec(  # simulate!
                compile(enemy_tree, '<string>', mode='exec'),
                {}, {'prediction_box': prediction_box}
            )
            prediction, = prediction_box
            logging.debug("prediction: %s", prediction)
            assert prediction in [0, 1, 2, 3, 4, 5]
            self.our_previous = 5 - prediction
            return 5 - prediction
        except Exception as e:
            logging.error(e.args)
            # if anything goes wrong that we didn't anticipate, fall back to
            # fallback behavior
            return self.fallback_play()
