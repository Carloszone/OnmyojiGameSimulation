import numpy as np

class Character:
    def __init__(self, name, health, attack, defense, speed):
        self.name = name
        self.health = health
        self.attack = attack
        self.defense = defense
        self.speed = speed
        self.current_location = 0

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

    def action_bar(self, length=1000):
        palyer_1_time = (length - self.player_1.current_location) / self.player_1.speed
        palyer_2_time = (length - self.player_2.current_location) / self.player_2.speed

        if palyer_1_time < palyer_2_time:
            self.player_1.current_location = 0
            self.player_2.current_location += self.player_2.speed * palyer_1_time
            return self.player_1, self.player_2
        else:
            self.player_2.current_location = 0
            self.player_1.current_location += self.player_1.speed * palyer_2_time
            return self.player_2, self.player_1


    def step(self):
        round_count = 0
        while self.death_check():
            round_count += 1
            print(f'***Round {round_count} starts!***')
            action_player, target_player = self.action_bar()
            print(f'{action_player.name} is acting!')
            action_player.make_damage(target_player)
            print('\n')


if __name__ == '__main__':
    hero_1 = Character('Joker', 1000, 100, 50, 150)
    hero_2 = Character('batman', 800, 150, 50, 200)

    game = env(hero_1, hero_2)
    game.step()