import numpy as np
import random


class Env:
    def __init__(self):
        pass
        self.stage_code = 0
        self.round_count = 0

    def reset(self):
        pass

    def step(self):
        while True:
            # game start
            if self.stage_code == 0 and self.round_count == 0:
                speciall_call()  # 结算特殊开场事件
                hero_call()  # 结算式神开局效果
                Item_call()  # 结算御魂开局效果
                hero_update()  # 英雄状态更新
                self.stage_code = 1  # 阶段更新

            # round start
            if self.stage_code == 1:
                hero = pick_next_act_hero()  # 决定下一个行动的式神
                hero_call()  # 结算式神回合开始前效果
                Item_call()  # 结算御魂回合开始前效果
                hero_update()  # 英雄状态更新
                death_check()  # 死亡检查
                death_call()  # 结算死亡效果
                hero_update()  # 英雄状态更新
                self.stage_code += 0.01  # 阶段更新

            # action start
            if self.stage_code == 1.01:
                hero_call()  # 结算式神行动开始前效果
                Item_call()  # 结算御魂行动开始前效果
                hero_update()  # 英雄状态更新
                death_check()  # 死亡检查
                death_call()  # 结算死亡效果
                hero_update()  # 英雄状态更新
                self.stage_code += 0.01  # 阶段更新


            # action process
            if self.stage_code == 1.02:
                hero.skill_pick()  # 选择，使用使用
                skill_call()  # 结算技能和触发效果
                hero_update()  # 英雄状态更新
                death_check()  # 死亡检查
                death_call()  # 结算死亡效果
                hero_update()  # 英雄状态更新
                self.stage_code += 0.01  # 阶段更新

            # action end
            if self.stage_code == 1.03:
                effect_call()  # 结算效果
                hero_update()  # 英雄状态更新
                death_check()  # 死亡检查
                death_call()  # 结算死亡效果
                hero_update()  # 英雄状态更新
                self.stage_code = 2

            # round end
            if self.stage_code == 2:
                hero_call()  # 结算式神回合结束后效果
                Item_call()  # 结算御魂回合结束后效果
                hero_update()  # 英雄状态更新
                death_check()  # 死亡检查
                death_call()  # 结算死亡效果
                hero_update()  # 英雄状态更新
                game_over_check()  # 游戏结束检查
                self.stage_code = 1

            if game_over_flag:
                break





