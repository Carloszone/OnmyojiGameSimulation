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

    def round(self):
        # 真回合 推动鬼火条
        # 新回合 不推动鬼火条
        # 伪回合 不推动鬼火条 下一个行动单位到达行动条底端
        # 回合效果检查与结算
            # 选择技能
            # 选择目标
            # 结算技能
        # 检查是否回复鬼火
       pass

    def get_single_attribution_from_pool(self, in_attribution_name, standard='min'):
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
        min_time, min_character = self.get_single_attribution_from_pool(self, 'remaining_time', standard='min')  # 返回最小时间和角色

        # 1.2 更新所有角色的行动条时间
        for character in self.character_pool:
            character.update_action_bar(in_time=min_time)

        # 1.3 执行其他游戏开始时效果

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




