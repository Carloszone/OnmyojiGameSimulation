import numpy as np
import random


class shishen:
    def __init__(self, name, hp, atk, defense, speed, crit, crit_damage, hit, resist):
        self.name = name
        self.hp = self.max_hp = hp
        self.atk = atk
        self.defense = defense
        self.speed = speed
        self.crit = crit
        self.crit_damage = crit_damage
        self.hit = hit
        self.resist = resist
        self.state = {}

    def get_info(self, obj):
        pass

class skill:
    def __init__(self, character, target, skill_type, skill_effect, skill_effect_type):
        self.character = character
        self.target = target
        self.skill_type = skill_type
        self.skill_effect = skill_effect
        self.skill_effect_type = skill_effect_type

    def get_info(self, obj):
        pass

    def skill_effect(self):
        pass

