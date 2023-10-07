import numpy as np


class Env:
    def __init__(self, team1, team2):
        self.team1 = team1
        self.team2 = team2
        self.round = 0

        self.judge = Character()

    def reset(self, team1, team2):
        self.team1 = team1
        self.team2 = team2

    def game_start(self):
        for team in [self.team1, self.team2]:
            for char in team.chars:
                for skill in char.skills:
                    if skill.skill_type == 'game_start':
                        skill.call_skill(skill)


        pass

    def round_start(self):
        pass

    def round_action(self):
        pass

    def round_end(self):
        pass

    def game_end(self):
        pass

    def round_check(self):

    def step(self):
        pass

class Team:
    def __init__(self, chars):
        self.chars = chars
        pass

class Character:
    def __init__(self, name, heath, attack, defense, speed, crit, crit_damage, hit, resist):
        self.name = name
        self.id = name_id_mapping[name]
        self.skill1 = name_skill_mapping[name][0]
        self.skill2 = name_skill_mapping[name][1]
        self.skill3 = name_skill_mapping[name][2]
        self.health = heath
        self.max_health = heath
        self.attack = attack
        self.defense = defense
        self.speed = speed
        self.crit = crit
        self.crit_damage = crit_damage
        self.hit = hit
        self.resist = resist


        self.state = []

    def call_skill(self):






    # def equal(self, state=None):
    #     if state is None:
    #         return 0
    #     if self.effect == state.effect:
    #         if self.lasting_round == state.lasting_round:
    #             return 2
    #         else:
    #             return 1
    #     else:
    #         return 0
