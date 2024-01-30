import numpy as np


class Hero:
    def __init__(self, id, attack, health, defense, speed, crit, crit_damage, effect_rate, effect_defense, item):
        self.id = id
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
    def __init__(self, target_code, change_code):
        self.target_code = target_code
        self.change_code = change_code

    def trigger(self, stage_code):
        return stage_code == self.target_code

    def seal_check(self, hero):
        return 'seal' not in hero.debuffs.keys()

    def change_check(self, change_code):
        return change_code == self.change_code



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
    def __init__(self, source, target, category, count_object=None, value=None, duration=None):
        """

        :param source: 效果来源id
        :param target: 效果目标id
        :param category: 效果类型：即时效果（1伤害，2治疗），持续效果（3状态，4印记），状态可以驱散而印记不能
        :param count_object: 效果消退计数对象。只针对持续效果，当count_object的对象行动后，效果持续回合减少
        :param value: 效果数值，可以为None。为None意味无数值或需要其他信息计算
        :param duration: 效果持续回合数，可以为None，为None意味着即时效果
        """
        self.source = source
        self.target = target
        self.category = category
        self.count_object = count_object
        self.value = value
        self.duration = duration

    # 触发判定
    def trigger(self):
        pass

    # 效果
    def effect(self):

    # duration更新， duration为0则效果消失
    def remove(self):
        pass