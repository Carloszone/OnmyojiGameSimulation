import random
import numpy as np
import logging
from utils.basic_classes import Summon, State, Team
from utils.states import JudgeState
from utils.characters import Judge


class Stimulation:
    def __init__(self, team1: Team, team2: Team):
        # team related
        self.team1 = team1
        self.team2 = team2

        # simulation related
        self.judge = Judge()
        self.seed = 0
        self.length = 1000
        self.action_row = []

        # winner related
        self.winner = None
        self.red_win_count = 0
        self.blue_win_count = 0

    def apply_seed(self, seed):
        self.seed = seed
        random.seed(seed)
        np.random.seed(seed)

    def reset(self):
        self.action_row = []
        self.winner = None

    def get_global_effect(self):
        judge_round = self.judge.round
        healing_reduction_coefficient = 0.1
        if judge_round < 10:
            vulnerability_coefficient = 0.15
        else:
            vulnerability_coefficient = 0.3

        # create global effect
        global_vulnerability_effect = JudgeState(name='force of judgement',  # 裁决之力
                                                 state_type=0,
                                                 removable=False,
                                                 dispellable=False,
                                                 attribute='damage_multiplier',
                                                 value=vulnerability_coefficient,
                                                 source=self.judge,
                                                 count=judge_round)
        global_healing_reduction_effect = JudgeState(name='force of judgement',  # 裁决之力
                                                     state_type=0,
                                                     removable=False,
                                                     dispellable=False,
                                                     attribute='damage_multiplier',
                                                     value=healing_reduction_coefficient,
                                                     source=self.judge,
                                                     count=judge_round)

        return [global_vulnerability_effect, global_healing_reduction_effect]

    def next_action_char(self):
        team1_candidates = [char for char in self.team1.members if not char.is_empty]
        team2_candidates = [char for char in self.team2.members if not char.is_empty]
        action_candidates = team1_candidates + team2_candidates + [self.judge]
        while True:
            if len(self.action_row) > 0:
                return self.action_row.pop(0)
            else:
                # calculate time needed for each character to act and store them
                player_info = []  # (time_needed, speed)
                for char in action_candidates:
                    if char.current_speed > 0:
                        time_need = np.round(self.length / char.current_speed, 6)
                        char.time_to_act = time_need
                        player_info.append(time_need)
                    else:
                        char.time_to_act = np.inf
                        player_info.append(np.inf)

                # get the minimum time needed
                min_time = np.min(player_info)

                # filter the second candidates
                second_candidates = [char for char in action_candidates if char.time_to_act == min_time]

                # resorted them by their speed
                self.action_row = sorted(second_candidates, key=lambda x: x.current_speed, reverse=True)

    def fatal_check(self):
        for char in self.team1.members:
            if char.is_main_char <= 0 and not char.suffer_fatal_damage:
                char.suffer_fatal_damage = True
                char.trigger(trigger_id=-1)

        for char in self.team2.members:
            if char.is_main_char <= 0 and not char.suffer_fatal_damage:
                char.suffer_fatal_damage = True
                char.trigger(trigger_id=-1)

    def death_check(self):
        for char in self.team1.members:
            if char.current_health <= 0:
                char.is_empty = True
                logging.info(f'【{self.team1.name}】队伍中的角色【{char.name}】阵亡')
                char.trigger(trigger_id=-2)

        for char in self.team2.members:
            if char.current_health <= 0:
                logging.info(f'【{self.team1.name}】队伍中的角色【{char.name}】阵亡')
                char.is_empty = True
                char.trigger(trigger_id=-2)

    def end_check(self):
        team1_count = 0
        team2_count = 0
        for char in self.team1.members:
            if char.is_main_char and not char.is_empty:
                team1_count = 1
        for char in self.team2.members:
            if char.is_main_char and not char.is_empty:
                team2_count = 1

        if team1_count:
            self.winner = self.team2
            return True
        elif team2_count:
            self.winner = self.team1
            return True
        else:
            return False

    def before_game(self):
        # set stage_id
        stage_id = 0

        # trigger
        self.team1.trigger(stage_id)
        self.team2.trigger(stage_id)

        # update attributes
        global_effect = self.get_global_effect()
        self.team1.update_attributes(global_effect)
        self.team2.update_attributes(global_effect)

        # death check and end check
        self.death_check()
        self.end_check()

    def start_game(self):
        # set stage_id
        stage_id = 1

        # update attributes
        global_effect = self.get_global_effect()
        self.team1.update_attributes(global_effect)
        self.team2.update_attributes(global_effect)

        # death check and end check
        self.death_check()
        self.end_check()

    def before_round(self):
        # set stage_id
        stage_id = 2

        # update attributes
        global_effect = self.get_global_effect()
        self.team1.update_attributes(global_effect)
        self.team2.update_attributes(global_effect)

        # determine the order of action
        next_char = self.next_action_char()

        # settle state triggered in the before round stage
        next_char.settle_state()

        # death check and end check
        self.death_check()
        self.end_check()

        return next_char

    def start_round(self, char):
        # set stage_id
        stage_id = 3

        # update attributes
        global_effect = self.get_global_effect()
        self.team1.update_attributes(global_effect)
        self.team2.update_attributes(global_effect)

        # settle state triggered in the start_round stage
        char.settle_state()

        # death check and end check
        self.death_check()
        self.end_check()

    def before_action(self, char):
        # set stage_id
        stage_id = 4

        # update attributes
        global_effect = self.get_global_effect()
        self.team1.update_attributes(global_effect)
        self.team2.update_attributes(global_effect)

        # settle state triggered in the before_action stage
        char.settle_state()

        # death check and end check
        self.death_check()
        self.end_check()

    def start_action(self, char):
        # set stage_id
        stage_id = 5

        # update attributes
        global_effect = self.get_global_effect()
        self.team1.update_attributes(global_effect)
        self.team2.update_attributes(global_effect)

        # settle state triggered in the start_action stage
        char.settle_state()

        # action

        # death check and end check
        self.death_check()
        self.end_check()

    def after_action(self, char):
        # set stage_id
        stage_id = 6

        # update attributes
        global_effect = self.get_global_effect()
        self.team1.update_attributes(global_effect)
        self.team2.update_attributes(global_effect)

        # settle state triggered in the start_action stage
        char.settle_state()

        # death check and end check
        self.death_check()
        self.end_check()

    def after_round(self):
        # set stage_id
        stage_id = 7

        # update attributes
        global_effect = self.get_global_effect()
        self.team1.update_attributes(global_effect)
        self.team2.update_attributes(global_effect)
