import numpy as np

class State:
    def __init__(self, source, state_type, effect, effect_mun, max_effect_mun, lasting_round, max_round, direction)
        self.source = source
        self.type = state_type
        self.effect = effect
        self.mun = effect_mun
        self.max_mun = max_effect_mun
        self.lasting_round = lasting_round
        self.max_round = max_round
        self.direction = direction


class Skill:
    def __init__(self, skill_type, effect, effect_range, target, value):
        self.skill_type = skill_type
        self.effect = effect
        self.effect_range = effect_range
        self.target = target
        self.value = value

    def __call__(self, *args, **kwargs):

