import numpy as np


class Hero:
    def __init__(self, attack, health, defense, speed, crit, crit_damage, effect_rate, effect_defense, item):
        self.attack = attack
        self.health = health
        self.max_health = health
        self.defense = defense
        self.speed = speed
        self.crit = crit
        self.crit_damage = crit_damage
        self.effect_rate = effect_rate
        self.effect_defense = effect_defense
        self.item = item
        self.buffs = {}
        self.debuffs = {}


class Item:
    def __init__(self, target_code):
        self.target_code = target_code

    def trigger(self, stage_code):
        if stage_code == self.target_code:
            return True
        else:
            return False

    def seal_check(self, hero):
        if 'seal' not in hero.debuffs.keys():
            return False
        else:
            return True

    # def effect(self, hero, stage_code):
    #     if self.trigger(stage_code) and self.seal_check(self, hero):



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