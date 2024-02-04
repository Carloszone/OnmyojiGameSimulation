# !/usr/bin/python
# -*- coding: utf-8  -*-

import numpy as np
from functions import possibility, serach_hero, costume_sorted, state_check

class Damage:
    def __init__(self, coefficient, category, kind, trigger_item_or_skill, trigger_range,
                 factor=None, additional_damage=0, share=0):
        """

        :param coefficient: 伤害系数
        :param category: 伤害类型：0普通， 1间接， 2真实
        :param kind: 攻击类型： 0单体， 1群体
        :param trigger_item_or_skill: 是否触发御魂或技能， 0不触发， 1触发
        :param trigger_range: 触发范围： 0仅对自己生效， 1仅对目标生效， 2仅对敌方所有生效， 3仅对己方所有生效，4对双方所有生效
        :param factor: 伤害浮动系数
        :param additional_damage: 额外伤害
        :param share: 是否可分担。0不可分担，1可分担
        """
        if factor is None:
            factor = [0.99, 1.01]
        self.coefficient = coefficient
        self.category = category
        self.kind = kind
        self.trigger_item_or_skill = trigger_item_or_skill
        self.trigger_range = trigger_range
        self.factor = factor
        self.additional_damage = additional_damage
        self.share = share


    def random_factor(self):
        upper_bound = max(self.factor)
        lower_bound = min(self.factor)
        return np.random.uniform(lower_bound, upper_bound, size=1)[0]

    def compute_damage_1(self, input_team_pool, input_source_id, input_target_id):
        # 从队伍信息中找到攻击者和被攻击者
        source_hero = serach_hero(input_team_pool, input_source_id)
        target_hero = serach_hero(input_team_pool, input_target_id)

        # 提取需要的状态值
        self_attack_state_plus = state_check(source_hero, 10)  # 攻击绝对值
        self_attack_state_multiply = state_check(source_hero, 0)  # 攻击%
        target_defense_state_plus = state_check(target_hero, 12)  # 防御绝对值
        target_defense_state_multiply = state_check(target_hero, 2)  # 防御%
        self_damage_state_multiply = state_check(source_hero, 8)  # 伤害%
        target_hurt_state_multiply = state_check(target_hero, 9)  # 受伤%
        make_damage_state_multiply = state_check(source_hero, 11)  # 造成伤害增加%
        final_self_attack = (source_hero.attack + self_attack_state_plus) * self_attack_state_multiply
        final_target_defense = max(target_hero.defense + target_defense_state_plus, 0) * target_defense_state_multiply

        # 伤害计算
        if self.category == 0:
            # 可以产生的伤害数值
            damage_value = (final_self_attack * self.coefficient * (300 / (300 + final_target_defense)) *
                            self_damage_state_multiply * target_hurt_state_multiply * self.random_factor())
            # 考虑暴击的伤害数值
            if possibility(source_hero.crit):
                final_attack_value = damage_value * source_hero.crit_damage + self.additional_damage
            else:
                final_attack_value = damage_value + self.additional_damage

            # 攻击时伤害分流

            # 实际能造成的伤害数值
            make_damage = target_hero.shield + target_hero.rot_blood * 3 - final_damage

            # 伤害时伤害分流

            # 最终伤害



        elif self.category == 1:
            damage_value = (state_check(source_hero, 0) *
                            self.coefficient *
                            (300 / (300 + state_check(target_hero, 2))) *
                            state_check(source_hero, 8) *
                            state_check(target_hero, 9) *
                            self.random_factor())

        return final_value




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
        self.shield = 0
        self.rot_blood = 0
        self.states = {}


class Item:
    def __init__(self, host_code, stage_code, related_attributions, value):
        self.host_code = host_code
        self.stage_code = stage_code
        self.related_attributions = related_attributions
        self.value = value

    # 触发判定:检查是否被封印
    def seal_check(self, hero):
        return 'seal' not in hero.debuffs.keys()

    # 触发判定，检查阶段是否副耳环
    def stage_check(self, stage_code):
        return stage_code == self.stage_code

    # 触发效果
    # def add_state(self):


class State:
    def __init__(self, in_source, in_value, in_type, in_category, in_group, in_rule, in_duration, in_count_obj):
        """

        :param in_source: 状态的来源
        :param in_value:  状态的数值，异常状态为0
        :param in_type:  状态的类型，0增益，1减益
        :param in_category: 状态关联的种类，0攻击，1生命，2防御，3速度，4暴击，5暴击伤害，6效果命中，7效果抵抗, 8伤害%，
        9受伤%， 10攻击绝对值， 11生命绝对值， 12防御绝对值， 13速度绝对值， 14暴击绝对值， 15暴击伤害绝对值， 16效果命中绝对值，
        17效果抵抗绝对值, 18造成伤害绝对值， 19受到伤害绝对值, 20 减伤%， 21造成伤害时增伤%， 22受到伤害时减伤%， 23特殊伤害减免%
        :param in_group: 状态的类别, 不同类别叠乘，同类别由in_rule决定
        :param in_rule: 同类别状态的规则，0叠加，如果有多个同类别状态，最终数值为同类别状态数值之和； 1刷新，如果有多个同类别状态，最终数值为最后一个同类别状态的数值
        :param in_duration: 状态的持续时间
        :param in_count_obj: 状态的计数对象
        """
        self.source = in_source
        self.value = in_value
        self.type = in_type
        self.category = in_category
        self.group = in_group
        self.rule = in_rule
        self.duration = in_duration
        self.count_obj = in_count_obj


    # 触发判定
    def trigger(self):
        pass

    # 效果
    def effect(self):
        pass

    # duration更新， duration为0则效果消失
    def remove(self):
        pass