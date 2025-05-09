from utils.functions import create_shikigami
from utils.basic_classes import Team, Summon, EventManger, ActionManger
import utils.spirits as spirits
from utils.game import Stimulation
import inspect
import logging
import os
import time
import numpy as np
import random


class BattleManager:
    def __init__(self):
        # team attribution

        # role attribution

        # manager attribution
        self.event_manager = EventManger()
        self.action_manager = ActionManger()

        # stat attribution


    def log_setting(self):
        pass

    def reset(self):
        pass

    def game_check(self):
        pass

    def death_check(self):
        pass

    def result_recoder(self):
        pass

    def results_stat(self):
        pass

    def round(self, character, round_type=1, do_first_skill=True):
        if round_type:
            # 回合开始前
            self.event_manager.call('round_start')

            # 行动开始前

            # 行动结算

            # 行动结束后

            # 回合结束后
        else:
            if do_first_skill:
                # 行动开始前

                # 行动结算

                # 行动结束后

            else:
                # 行动开始前

                # 行动结算

                # 行动结束后



    def run(self, loop_count):
        # 日志记录设定

        # 游戏组件创建

        # 开始模拟
        for i in range(loop_count):
            # 初始化模拟
            self.reset()

            # 开始本次战斗模拟
            while self.game_check():
                action_character = self.action_manager.next_action_character()
                self.round(action_character)

            # 记录本次模拟结果
            self.result_record()

        # 输出分析结果
        self.results_stat()