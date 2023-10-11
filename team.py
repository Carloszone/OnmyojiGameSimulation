import numpy as np

class mana_bar:
    def __init__(self, mana=4, max_mana=8, round=0, process=0, max_process=6):
        self.mana = mana
        self.max_mana = max_mana
        self.round = round
        self.process = process
        self.max_process = max_process

    def update_process(self, value=1):
        self.process += value

        if self.process >= self.max_process:
            self.process = self.process % self.max_process
            self.round += 1
            if self.round == 1:
                self.mana = min(self.mana + 3, self.max_mana)
            elif self.round == 2:
                self.mana = min(self.mana + 4, self.max_mana)
            else:
                self.mana = min(self.mana + 5, self.max_mana)


class Team:
    def __init__(self, char1, char2, char3, char4, char5, mana, mana_bar):
        self.char1 = char1
        self.char2 = char2
        self.char3 = char3
        self.char4 = char4
        self.char5 = char5
        self.team = [char1, char2, char3, char4, char5]

        self.magic_bar = 0

    def locate_info(self, att, n, reverse=False):
        atts = {}
        for char in self.team:
            atts[char] = char.get_att(att)

        atts = sorted(atts.items(), key=lambda x: x[1], reverse=reverse)[:n]
        return atts

    def locate_char(self, att, n, reverse=False):
        atts = self.locate_info(att, n, reverse)
        char_ids = [info[0] for info in atts]
        return char_ids




