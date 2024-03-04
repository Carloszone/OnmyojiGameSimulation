import numpy as np

class Character:
    def __init__(self, name, health, attack, defense):
        self.name = name
        self.health = health
        self.attack = attack
        self.defense = defense

    def details(self):
        print(f"{self.name}'s Attributions:")
        for attr_name in vars(self):
            attr_value = getattr(self, attr_name)
            print(f'{attr_name}: {attr_value}')

    def make_damage(self, target):
        damage = self.attack - target.defense
        target.health -= damage
        print(f'{self.name} attacks {target.name}, dealing {damage} damage!')
        print(f'{target.name} has {target.health} health left!')

class env:
    def __init__(self, player_1, player_2):
        self.player_1 = player_1
        self.player_2 = player_2

    def death_check(self):
        if self.player_1.health <= 0:
            print(f'{self.player_1.name} is dead!')
            print(f'{self.player_2.name} wins!')
            return 0
        if self.player_2.health <= 0:
            print(f'{self.player_2.name} is dead!')
            print(f'{self.player_1.name} wins!')
            return 0
        return 1

    def step(self):
        round_count = 0
        while self.death_check():
            round_count += 1
            print(f'***Round {round_count} starts!***')
            play_list = [self.player_1, self.player_2]

            if round_count % 2:
                action_player = self.player_1
                target_player = self.player_2
            else:
                action_player = self.player_2
                target_player = self.player_1
            action_player.make_damage(target_player)
            print('\n')


if __name__ == '__main__':
    hero_1 = Character('Joker', 100, 10, 5)
    hero_2 = Character('batman', 80, 15, 5)

    game = env(hero_1, hero_2)
    game.step()