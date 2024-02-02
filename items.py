import numpy as np
from class_collection import Hero, Item, EffectPool, Effect
from functions import damage, heal, add_effect

# Item
class Fuyi(Item):
    def __init__(self, host_code):
        super().__init__(host_code, stage_code=None)

    def trigger(self, hero, value):
        if self.seal_check(hero):
            heal(self.host_code, value)




