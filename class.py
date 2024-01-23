import numpy as np


class ShiShen:
    def __init__(self):
        pass

    def skill_choose(self):
        pass

    def skill_01(self):
        pass

    def skill_02(self):
        pass

    def skill_03(self):
        pass


class Yuhun:
    def __init__(self, target_code):
        self.target_code = target_code

    def trigger(self, stage_code):
        if stage_code == self.target_code:
            return True
        else:
            return False

    def seal_check(self, debuff_pool=None):
        if debuff_pool is None:
            return False
        else:
            pass
        pass


class Skill:
    def __init__(self):
        pass

    def damage(self):
        pass

    def heal(self):
        pass

    def add_effect(self):
        pass


class EffectPool:
    def __init__(self):
        pass

    def add(self):
        pass

    def remove(self):
        pass


class Effect:
    def __init__(self):
        pass

    def trigger(self):
        pass

    def remove(self):
        pass