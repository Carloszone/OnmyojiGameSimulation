# !/usr/bin/python
# -*- coding: utf-8  -*-
# 模拟过程中需要使用的类

import numpy as np
from functions import possibility, search_hero_info, costume_sorted, state_check


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
        self.share = share


    def random_factor(self):
        upper_bound = max(self.factor)
        lower_bound = min(self.factor)
        return np.random.uniform(lower_bound, upper_bound, size=1)[0]

    def compute_damage_1(self, input_hero_pool, input_source_id, input_target_id):
        # 从队伍信息中找到攻击者和被攻击者
        source_hero = search_hero_info(input_hero_pool, 'hero_id', input_source_id)
        target_hero = search_hero_info(input_hero_pool, 'hero_id', input_target_id)

        # 提取需要的状态值
        self_attack_state_plus = state_check(source_hero, 10)  # 攻击绝对值
        self_attack_state_multiply = state_check(source_hero, 0)  # 攻击%
        target_defense_state_plus = state_check(target_hero, 12)  # 防御绝对值
        target_defense_state_multiply = state_check(target_hero, 2)  # 防御%
        self_damage_state_multiply = state_check(source_hero, 8)  # 伤害%
        target_hurt_state_multiply = state_check(target_hero, 9)  # 受伤%
        self_damage_state_plus = state_check(source_hero, 18)  # 造成伤害绝对值
        target_damage_state_plus = state_check(target_hero, 19)  # 受到伤害绝对值
        self_make_damage_state_multiply = state_check(source_hero, 21)  # 造成伤害%
        target_make_damage_state_multiply = state_check(target_hero, 22)  # 受到伤害%
        final_self_attack = (source_hero.attack + self_attack_state_plus) * self_attack_state_multiply
        final_target_defense = max(target_hero.defense + target_defense_state_plus, 0) * target_defense_state_multiply

        # 伤害计算
        if self.category == 0:
            # 计算伤害A
            damage_value = (final_self_attack * self.coefficient * (300 / (300 + final_target_defense)) *
                            self_damage_state_multiply * target_hurt_state_multiply * self.random_factor() +
                            self_damage_state_plus + target_damage_state_plus)
            # 考虑暴击的伤害数值
            if possibility(source_hero.crit):
                damage_a_value = damage_value * source_hero.crit_damage
            else:
                damage_a_value = damage_value

            # 计算护盾,得到伤害B
            damage_b_value = max(damage_a_value - target_hero.shield - target_hero.rot_blood * 3, 0)


            if damage_b_value > 0:
                # 计算造成伤害时效果
                ddamage_b_value = damage_b_value * self_make_damage_state_multiply * target_make_damage_state_multiply

                # 锁定分担目标
                if search_hero_info(target_hero, 'state_id', '孤立'):  # 如果有孤立状态
                    pass
                else:
                    if search_hero_info(source_hero, 'state_id', '椒图'):  #椒图状态
                        share_num = len('椒图_count')
                    if search_hero_info(source_hero.emeny_team - target_hero, 'state_id', '剃魂'): # 如果有剃魂状态
                        damage_b_value = damage_b_value * 0.5

                # 计算伤害C
                damage_c_value = damage_b_value * (1 - self.share)

                # 计算伤害D

                # 伤害D修正

                # 扣除生命



        elif self.category == 1:
            damage_value = (state_check(source_hero, 0) *
                            self.coefficient *
                            (300 / (300 + state_check(target_hero, 2))) *
                            state_check(source_hero, 8) *
                            state_check(target_hero, 9) *
                            self.random_factor())

        return final_value


class Character:
    def __init__(self, id, team, enemy_team, attack, health, defense, speed, crit, crit_damage, effect_rate, effect_defense, item, bar_length, position):
        # 属性相关
        self.id = id
        self.team = team
        self.enemy_team = enemy_team
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

        # 状态相关
        self.shield = 0
        self.rot_blood = 0
        self.states = []

        # 行动条相关
        self.remaining_length = bar_length
        self.remaining_time = bar_length / speed
        self.reach_method = None

        # 其他
        self.position = position

    def get_current_attribution(self, in_attribution_name):
        # 获取原始属性值
        original_value = getattr(self, in_attribution_name, None)
        related_state_ids = state2attribution[in_attribution_name]  # 获取相关状态的id
        multiply_value = 0
        plus_value = 0
        for state in self.states:
            if state.id in related_state_ids:
                if state.category < 10:
                    multiply_value += state.value
                else:
                    plus_value += state.value
        return (original_value + plus_value) * (1 + multiply_value)


    # 行动条状态更新
    def update_action_bar(self, in_time, in_length):
        current_speed = self.get_current_attribution('speed')
        # 拉条场景处理
        if in_time is None:  # 如果时间为空，说明是拉条场景
            self.remaining_length = max(self.remaining_length - in_length, 0)
            if self.remaining_length == 0:
                self.reach_method = 1
                self.remaining_time = 0
            else:
                self.remaining_time = self.remaining_length / current_speed
        # 跑条场景处理
        else:
            self.remaining_time = max(self.remaining_time - in_time, 0)
            if self.remaining_time == 0:
                self.reach_method = 0
                self.remaining_length = 0
            else:
                self.remaining_length = self.remaining_time * current_speed


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
    def __init__(self, in_id, in_source, in_value, in_type, in_category, in_group, in_rule, in_duration, in_count_obj):
        """
        :param in_id: 状态的id
        :param in_source: 状态的来源
        :param in_value:  状态的数值，异常状态为0
        :param in_category: 状态关联的种类，0攻击%，1生命%，2防御%，3速度%，4暴击%，5暴击伤害%，6效果命中%，7效果抵抗, 8伤害%，
        9受伤%， 10攻击绝对值， 11生命绝对值， 12防御绝对值， 13速度绝对值， 14暴击绝对值， 15暴击伤害绝对值， 16效果命中绝对值，
        17效果抵抗绝对值, 18造成伤害绝对值， 19受到伤害绝对值, 20 减伤%， 21造成伤害时增伤%， 22受到伤害时减伤%， 23特殊伤害减免%
        :param in_group: 状态的类别, 不同类别叠乘，同类别由in_rule决定
        :param in_rule: 同类别状态的规则，0叠加，如果有多个同类别状态，最终数值为同类别状态数值之和； 1刷新，如果有多个同类别状态，最终数值为最后一个同类别状态的数值
        :param in_duration: 状态的持续时间
        :param in_count_obj: 状态的计数对象
        """
        self.id = in_id
        self.source = in_source
        self.value = in_value
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