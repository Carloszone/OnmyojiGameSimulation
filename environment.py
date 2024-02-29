# !/usr/bin/python
# -*- coding: utf-8  -*-
# 环境类

import numpy as np
import random
from class_collection import Character


class Env:
    def __init__(self, in_team_1, in_team_2):
        # 常规属性
        self.team_1 = in_team_1
        self.team_2 = in_team_2

        # 回合属性
        self.round_count = 0

        # 角色集合
        self.judge = judge   # 裁判，特殊角色
        self.character_pool = [] + [] + [judge]  # 角色池， 两队+裁判

    # 重置环境
    def reset(self):
        pass

    # 基础回合
    def basic_round(self, in_hero, in_skill=None, in_exclude_condition=None):
        # 回合行动
        hero_team, target_team = self.team_seach(in_hero)  # 查找角色所在队伍和敌对队伍
        skill_id = in_hero.skill_pick(hero_team.energy_bar) # 基于团队能量选择技能
        target = in_hero.target_pick(target_team)  # 选择目标
        in_hero.skill_execute(skill_id, target)

        # 能量检查
        hero_team.energy_bar.check() # 检查能量条,是否回复能量

    # 真回合：通过跑条，拉条获得的回合。特点是在回合开始时推动鬼火条
    def true_round(self, in_hero):
        hero_team, target_team = self.team_seach(in_hero)  # 查找角色所在队伍和敌对队伍
        hero_team.push_energy_bar()  # 推动能量条

        self.basic_round(in_hero)

    # 新回合：通过技能或者御魂触发的回合。特点是不会再回合开始是推动鬼火条
    def new_round(self, in_hero):
        hero_team, target_team = self.team_seach(in_hero)
        self.basic_round(in_hero)

    # 伪回合：通过技能或者御魂触发的回合。特点是不会再回合开始是推动鬼火条，且下一个行动单位到达行动条底端
    def fake_round(self, in_hero):
        # 式神check： 是否有其他单位到达底端。 如果有，直接进行后续结算，如果没有，让下一行动单位到达低端后，锁定进度条并并进行连接
        hero_team, target_team = self.team_seach(in_hero)  # 查找角色所在队伍和敌对队伍
        all_team = Team(hero_team + target_team)
        time = all.next_action()
        all_team.action_bar.update(time)

        self.basic_round(in_hero)

        # 真回合 推动鬼火条
        # 新回合 不推动鬼火条
        # 伪回合 不推动鬼火条 下一个行动单位到达行动条底端
        # 回合效果检查与结算
            # 选择技能
            # 选择目标
            # 结算技能
        # 检查是否回复鬼火
       pass

    # 功能函数
    # 根据需要搜集所有符合的角色
    def collect_characters(self, in_character: Character, in_method: str):
        available_method_values = ['all', 'home', 'enemy']
        if in_method not in available_method_values:
            raise ValueError('No such method! the method should be all, home or enemy')

        if in_method == 'all':
            return self.team_1.add_character(self.team_2.available_characters() + [self.judge])
        elif in_method == 'home':
            if self.team_1.search(in_character.id):
                return self.team_1
            else:
                return self.team_2
        else:
            if self.team_1.search(in_character.id):
                return self.team_2
            else:
                return self.team_1

    # 查找特定属性并排序
    def get_single_attribution_from_pool(self, in_attribution_1, in_attribution_2, in_operator, in_range: str, in_stand: str):

        sored_attributions = sorted([(getattr(character, in_attribution_name), character) for character in self.character_pool])
        if standard == 'min':
            return sored_attributions[0]
        elif standard == 'max':
            return sored_attributions[-1]
        else:
            raise ValueError('No such standard!')

    def step(self):
        # 1. 游戏开始时
        # 1.1 统计各个角色的剩余行动条时间，找出最小时间和角色
        min_time, min_character = self.get_single_attribution_from_pool(self.get_all_availble_character(), 'remaining_time', standard='min')  # 返回最小时间和角色

        # 1.2 更新所有角色的行动条时间
        for character in self.character_pool:
            character.update_action_bar(in_time=min_time)

        # 1.3 执行其他游戏开始时效果

        # 2. 游戏回合开始
        while True:
            true_round(self, min_character)

            # 2.2 统计各个角色的剩余行动条时间，找出最小时间和角色

            # 2.3 更新所有角色的行动条时间

            # 2.4 决定行动角色和行动次序

            # 2.5 决定当前执行行动的角色

            # 2.6 执行行动

            # 2.6.1 结算行动前效果

            # 2.6.2 选择行动目标




