import numpy as np
from class_collection import Hero, Item, Skill, EffectPool
import random

# Item
class Fuyi(Item):
    def effect(self, hero, stage_code):
        if self.trigger(stage_code) and self.seal_check(hero) and self.change_check(change_code):



