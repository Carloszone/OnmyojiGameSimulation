# !/usr/bin/python
# -*- coding: utf-8  -*-
# 环境类

import numpy as np
import random


class Env:
    def __init__(self, in_team_a, in_team_b):
        # 常规属性
        self.team_a = in_team_a
        self.team_b = in_team_b

        # 回合属性
        self.round_count = 0

        # 角色集合
        self.judge = judge   # 裁判，特殊角色
        self.character_pool = [] + [] + [judge]  # 角色池， 两队+裁判

    def reset(self):
        pass

    def get_single_attribution_from_pool(self, in_attribution_name, standard='min'):
        sored_attributions = sorted([getattr(character, in_attribution_name) for character in self.character_pool])
        if standard == 'min':
            return sored_attributions[0]
        elif standard == 'max':
            return sored_attributions[-1]
        else:
            raise ValueError('No such standard!')

    def damage_process(self):
        # 计算伤害A

        # 计算护盾

        # 计算伤害B

        # 计算造成伤害时效果

        # 锁定分担目标

        # 计算分担伤害

        # 得到伤害B1

        # 计算伤害B2

        # 伤害B2修正

        # 扣除生命
        pass

    # 行动条计算

    # 能量条计算

    # 回合模拟
    def round(self, in_action_hero, in_round_code):
        """

        :param in_action_hero: 行动的式神
        :param in_round_code: 回合代码， 0普通回合， 1新回合，2伪回合
        :return:
        """
        pass


    def step(self):
        # 1. 游戏开始时
        ## 1.1 统计各个角色的剩余行动条时间，找出最小时间和角色


        ## 1.2 更新所有角色的行动条时间

        ## 1.3 执行其他游戏开始时效果

        # 2. 游戏回合开始
        round_code = 0
        while True:
            # if round_code == 0:  # 普通回合/真回合
            # 2.1 更新回合数
            self.round_count += 1
            print(f'第{self.round_count}回合开始')

            # 2.2 统计各个角色的剩余行动条时间，找出最小时间和角色

            # 2.3 更新所有角色的行动条时间

            # 2.4 决定行动角色和行动次序

            # 2.5 决定当前执行行动的角色

            # 2.6 执行行动

            # 2.6.1 结算行动前效果

            # 2.6.2 选择行动目标




