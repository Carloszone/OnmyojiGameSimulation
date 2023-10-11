import numpy as np
import random

class Judge:
    def __init__(self, speed, round=0, buff_ratio=0.15, debuff_ratio=0.15):
        self.id = 0
        self.speed = speed
        self.process = 0
        self.time = np.round((1000-self.process) / speed,4)
        self.round = round
        self.buff_factor = buff_ratio * min(10, self.round)
        self.debuff_factor = debuff_ratio * min(10, self.round)

    def action(self):
        self.round += 1

    def locate_info(self, att, n, reverse=False):
        return [(self, self.time)]

    def att_update(self, att, value):
        setattr(self, att, )



class Env:
    def __init__(self, team1, team2, judge):
        self.team1 = team1
        self.team2 = team2
        self.judge = judge
        self.step_count = 0

    def locate_actor(self):
        actors = []
        for obj in [self.judge, self.team1, self.team2]:
            actors += obj.locate_info('time', 1)

        actors = sorted(actors, key=lambda x: x[1])
        return actors[0]

    def update_process(self, actor, value):
        for team in [self.team1.team, self.team2.team]:
            for char in team:
                if char.id != actor.id:
                    char.process += np.round(min(value * char.speed + char.process, 1000), 4)
                else:
                    char.process = 0
                char.time = np.round((1000 - char.process) / char.speed, 4)

    def begainning_effect(self):
        pass

    def step(self):
        actor, time = self.locate_actor()
        self.update_process(actor, time) # 更新所有对象的进度条和时间属性

        if self.step_count == 0:
            self.begainning_effect() # 开局效果

        actor.action() # 执行行动

        death_flag, death_num = self.death_check() # 死亡检查
        if death_flag:
            self.team1.death_effect(death_num)
            self.team2.death_effect(death_num)



