# import package
import numpy as np

class god:
    def __init__(self, attack, health, defend, speed, critical_hit_rate, critical_multiplier, accuracy, dodge, gem):
        self.attack = attack
        self.health = self.max_health = health
        self.defend = defend
        self.speed = speed
        self.critical_hit_rate = critical_hit_rate
        self.critical_multiplier = critical_multiplier
        self.accuracy = accuracy
        self.dodge = dodge
        self.gem = gem


class summmons(god):
    def __init__(self, attack, health, defend, speed, critical_hit_rate, critical_multiplier, accuracy, dodge, gem):
        super().__init__(attack, health, defend, speed, critical_hit_rate, critical_multiplier, accuracy, dodge, gem)

