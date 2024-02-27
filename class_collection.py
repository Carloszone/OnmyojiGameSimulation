# !/usr/bin/python
# -*- coding: utf-8  -*-
# 模拟过程中需要使用的类

import numpy as np
from functions import possibility, search_hero_info, costume_sorted, state_check


class Effect:
    def __init__(self, in_source, in_target, in_value, in_type, in_damage_type=None):
        """

        :param in_source: 效果来源id
        :param in_target: 效果对象id
        :param in_value: 效果数值
        :param in_type: 效果类型，1 伤害； 2 治疗； 3 恢复生命； 4 失去生命
        :param in_damage_type: 伤害类型： 0 非暴击伤害， 1 暴击伤害， 2 间接伤害， 3 传导伤害， 4 真实伤害；
        """
        self.source = in_source
        self.target = in_target
        self.value = in_value
        self.type = in_type
        self.damage_type = in_damage_type
        self.is_call = 0  # 效果是否已经结算

    def call(self, hero_pool):
        """
        效果结算函数, 返回溢出伤害或治疗
        :param hero_pool: 有效式神池
        :return:
        """
        if self.is_call == 0:
            target = hero_pool.search_hero(self.target)
            if self.type == 1:
                target.health = max(target.health - self.value, 0)
                diff = target.health - self.value
            elif self.type == 2:
                target.health = min(target.health + self.value, target.max_health)
                diff = target.health - self.value
            elif self.type == 3:
                target.health = min(target.health + self.value, target.max_health)
                diff = target.health - self.value
            elif self.type == 4:
                target.health = max(target.health - self.value, 0)
                diff = target.health - self.value
            else:
                raise ValueError(f'No such effect type! {self.type}')
        self.is_call = 1
        return diff


class Character:
    def __init__(self, role_id, attack, health, defense, speed, crit, crit_damage, effect_rate,
                 effect_defense, item, position):
        # 属性相关
        self.id = role_id
        self.attack = attack
        self.health = health
        self.max_health = health
        self.defense = defense
        self.speed = speed
        self.crit = crit
        self.crit_resistance = 0
        self.crit_damage = crit_damage
        self.effect_hit = effect_rate
        self.effect_resistance = effect_defense
        self.item = item

        # 状态相关
        self.shield = 0
        self.rot_blood = 0
        self.states = []

        # 行动条相关
        self.total_action_point = 1000
        self.current_action_point = speed
        self.remaining_time = (self.total_action_point - self.current_action_point) / speed
        self.reach_method = None

        # 其他
        self.position = position  # 式神站位次序

    def get_current_attribution(self, in_attribution_name: str, input_hero=None, attack_type=None):
        if input_hero is None:
            input_hero = self

        # 获取原始属性值
        original_value = getattr(input_hero, in_attribution_name, None)
        if in_attribution_name == 'defense' and attack_type == 2:
            related_state_ids = state2attribution[in_attribution_name]  # 获取相关状态的id
        else:
            related_state_ids = state2attribution[in_attribution_name]  # 获取相关状态的id
        multiply_value = 0
        plus_value = 0
        for state in input_hero.states:
            if state.id in related_state_ids:
                if state.category < 10:
                    multiply_value += state.value
                else:
                    plus_value += state.value
        return (original_value + plus_value) * (1 + multiply_value)

    # 行动条状态更新
    def update_action_point(self, in_time=None, in_length=None):
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

    def search2call_hero_info(self, input_targets, input_obj_type, input_obj_ids):
        """
        通用函数，根据给出的信息和范围查找对应目标
        :param input_targets: 技能或效果的目标式神
        :param input_obj_type: 查找的信息类型
        :param input_obj_ids: 查找的对象id
        :return:
        """
        # 调整参数的数据类型
        if type(input_targets) is not list:
            input_targets = [input_targets]
        if type(input_obj_ids) is int:
            input_obj_ids = [input_obj_ids]

        # 查找对应的式神信息
        if input_obj_type == 'hero_id':
            for hero in input_targets:
                if hero.id in input_obj_ids:
                    return hero, hero.id  # 如果找到对应式神，返回该式神
            return 0, None
        elif input_obj_type == 'item_id':
            for hero in input_targets:
                if hero.item.id in input_obj_ids:
                    item_value = hero.item.call(self, hero)
                    return item_value, hero.item.id  # 如果找到对应御魂，触发御魂效果，返回数值
            return 0, None
        elif input_obj_type == 'state_id':
            for hero in input_targets:
                states = [state.id for state in hero.states]
                intersection_sates = list(set(states) & set(input_obj_ids))
                if intersection_sates:
                    return 1, intersection_sates  # 如果找到对应状态， 返回1 否则返回0
            return 0, None

    def compute_damage_a(self, in_hero_attack, in_target_defense, in_coefficient, in_hero_damage_state_multiply,
                         in_target_damage_state_multiply, in_independent_damage_multiply):
        damage_a = (in_hero_attack * in_coefficient * (300 / (300 + in_target_defense)) * in_hero_damage_state_multiply
                    * in_target_damage_state_multiply * in_independent_damage_multiply)
        return damage_a

    def crit_check(self, target):  # 暴击判定函数
        self_crit = self.get_current_attribution('crit')
        target_crit_resistance = target.get_current_attribution('crit_resistance')
        if np.random.rand() < self_crit - target_crit_resistance:
            return True
        else:
            return False

    def damage_share(self, in_target, in_target_team, in_damage, in_hero_pool):
        if in_damage.value > 0:
            # 锁定分担目标
            if search_hero_info(in_target, 'state_id', '孤立'):  # 如果有孤立状态，不进行伤害分担
                return 0, 0
            else:
                if self.search2call_hero_info(in_target, 'state_id', '小白守护'): # 小白守护状态
                    shared_damage = Effect(self, in_target, in_damage.value, 1, 0)
                    in_damage.value = 0
                    shared_damage.call(in_hero_pool) # 小白守护状态结算
                    return 0, shared_damage
                elif self.search2call_hero_info(in_target, 'state_id', '椒图'):  # 椒图状态
                    for target in in_target_team.characters:
                        share_num = 0
                        share_character_ids = []
                        if search_hero_info(target, 'state_id', '椒图') and target.id != in_target.id:
                            share_num += 1
                            share_character_ids.append(target.id)
                    if share_num > 0:
                        in_damage.value = in_damage.value / share_num
                        shared_damage = Effect(self, share_character_ids, in_damage.value, 1, 3)
                        return in_damage, shared_damage
                else:  # 没有椒图状态时才检测剃魂状态
                    for target in in_target_team.characters:
                        if target.id != in_target.id:
                            item_check = search_hero_info(target, 'itemid', '剃魂')  # 如果有剃魂状态
                            if item_check:
                                shared_value = in_damage.value * 0.8 * 0.5
                                in_damage.value = shared_value
                                shared_damage = Effect(self, target.id, shared_value, 1, 0)
                            return in_damage, shared_damage
        return 0, 0

    def receive_damage_trigger(self):


    def make_damage(self, targets, coefficient, category, kind, trigger_item, trigger_range, skill_type, factor=None):
        """

        :param targets: 目标
        :param coefficient: 伤害系数
        :param category: 伤害类型：0普通， 1间接， 2真实
        :param kind: 攻击类型： 0单体， 1群体
        :param trigger_item: 是否触发御魂， 0不触发， 1触发
        :param trigger_range: 触发范围： 0仅对自己生效， 1仅对目标生效， 2仅对敌方所有生效， 3仅对己方所有生效，4对双方所有生效
        :param skill_type: 技能类型： 0普通攻击， 1主动， 2被动
        :param factor: 伤害浮动系数
        """
        # 提取需要的状态值
        for target in targets:  # 需要补充的状态值，
            self_damage_state_multiply = state_check(self, 8)  # 造成伤害增减%
            target_hurt_state_multiply = state_check(target, 9)  # 受到伤害增减%
            self_damage_state_plus = state_check(self, 18)  # 造成伤害增减绝对值
            self_independent_damage_multiply = state_check(self, 21)  # 独立增伤伤害%  # 独立增伤，如吸血姬，次林被动，鸣屋
            self_damage_multiply = state_check(self, 22)  # 伤害放大%， 如食灵buff
            target_A_damage_reduction_state_multiply = state_check(target, 23)  # A类减伤%，独立乘算减伤
            target_B_damage_reduction_state_multiply = state_check(target, 24)  # B类减伤%，如触发免死，免死后计算的独立乘算减伤
            final_self_attack = self.get_current_attribution(in_attribution_name='attack')
            final_target_defense = self.get_current_attribution(in_attribution_name='defense', input_hero=target)

            # 伤害计算
            if category == 0:  # 直接伤害
                # 计算伤害A
                damage_value = self.compute_damage_a(final_self_attack, final_target_defense, coefficient,
                                                 self_damage_state_multiply, target_hurt_state_multiply,
                                                 self_independent_damage_multiply)
                damage = Effect(self, target, damage_value, 1, 0)

                # 考虑暴击
                if self.crit_check(target):
                    damage.value = damage.value * self.get_current_attribution(in_attribution_name='crit_damage')
                    damage.damage_type = 1

                # 考虑伤害波动
                damage.value = damage.value * np.random.uniform(0.99, 1.01, size=1)[0]


                # 计算护盾,得到伤害B
                damage_b_multiply, _ = self.search2call_hero_info(target, 'item_ids', '')
                if damage_b_multiply == 0:  # 如果没找到加成御魂，伤害乘数为1
                    damage_b_multiply = 1
                damage.value = max(damage.value - target.shield - target.rot_blood * 3, 0) * self_damage_multiply * damage_b_multiply

                # 计算分担伤害
                damage, shared_damage = self.damage_share(target, target_team, damage, hero_pool)

                # 计算白藏主结界减伤
                check_result, _ = self.search2call_hero_info(target, 'state_ids', '')  # 如果有白藏主结界状态
                if check_result:
                    if damage:
                        damage.value = damage.value * 0.6
                    if shared_damage:
                        shared_damage.value = shared_damage.value * 0.6

                # 计算受到伤害时效果（如：地藏，镜姬）

                item_effect_value, item_id = self.search2call_hero_info(target, 'item_ids', '地藏镜姬')  # 补充触发信息

                # 分担伤害结算
                for id in shared_object_ids:
                    character.health = max(character.health - damage_b_value, 0)
                    if character.health == 0:
                        character.death()

                # 计算A类减伤（buff栏的受到伤害减伤，独立乘算）
                damage_c_value = damage_b_value * target_A_damage_reduction_state_multiply

                # 熏记录伤害

                # 免死效果结算
                if death_check():
                    escape_death()

                # 计算B类减伤
                # damage_d_value = damage_c_value * target_B_damage_reduction_state_multiply

                # 扣除生命
                target.health = max(target.health - damage_d_value, 0)

                # 结算日和坊能量收集，海忍守护反击，鬼童丸锁链，SP雪女冰冻
                if search_hero_info(self, 'state_id', 'XXX')  # 如果有结算需求
                    damage_b_value = damage_b_value * 0.5

                # 死亡判定，死亡单位御魂，被动失效
                if death_check():
                    # 结算死亡效果（伤魂鸟、御怨般若面具、跳跳哥哥反击等
                    if search_hero_info(self, 'state_id', 'XXX')  # 如果有结算需求
                        damage_b_value = damage_b_value * 0.5

                # 结算狰的反击
                if search_hero_info(self, 'state_id', 'XXX')  # 如果有结算需求
                    damage_b_value = damage_b_value * 0.5

                # 结算犬神万年竹反击，木魅，日女，返魂香是否触发，御灵是否触发
                if search_hero_info(self, 'state_id', 'XXX')  # 如果有结算需求
                    damage_b_value = damage_b_value * 0.5




    def make_heal(self):
        pass

    def make_effect(self):
        pass




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
                    if search_hero_info(source_hero, 'state_id', '椒图'):  # 椒图状态
                        share_num = len('椒图_count')
                    if search_hero_info(source_hero.emeny_team - target_hero, 'state_id', '剃魂'):  # 如果有剃魂状态
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
