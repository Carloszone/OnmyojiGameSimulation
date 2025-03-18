from utils.basic_classes import Character, Summon, State


class Judge(Character):
    def __init__(self, name, speed, available, attackable):
        super().__init__(name='judge', speed=130)

    def trigger(self):
        self.round += 1
