import numpy as np

class Character:
    def __init__(self, name, health, mana, attack, defense, speed):
        self.name = name
        self.health = health
        self.mana = mana
        self.attack = attack
        self.defense = defense
        self.speed = speed
        self.current_location = 0

    def details(self):
        print(f"{self.name}'s Attributions:")
        for attr_name in vars(self):
            attr_value = getattr(self, attr_name)
            print(f'{attr_name}: {attr_value}')

    def skill_1(self, target, coefficient=1):
        skill_name = 'skill_1'
        damage = self.attack * coefficient - target.defense
        target.health -= damage
        print(f'{self.name} uses {skill_name} to attack {target.name}, dealing {damage} damage!')
        print(f'{target.name} has {target.health} health left!')

    def skill_2(self, target, coefficient=1):
        # s powerful attack
        pass

    def skill_3(self, target, coefficient=1):
        # ultra skill with special effect
        pass

    def choose_skill(self, target):
        if self.mana <= 1:
            self.skill_1(target)
        elif self.mana == 3:
            self.skill_3(target)
        else:
            self.skill_2(target)


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
        print(f"{self.player_1.name}' action time is {palyer_1_time}")
        print(f"{self.player_2.name}' action time is {palyer_2_time}")

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
            print(f'{action_player.name} is acting! He has {action_player.mana} mana!')
            action_player.choose_skill(target_player)
            print('\n')


if __name__ == '__main__':
    class Batman(Character):
        def skill_1(self, target, coefficient=1.25):
            skill_name = 'bat_punch'
            damage = self.attack * coefficient - target.defense
            target.health -= damage
            print(f'{self.name} uses {skill_name} to attack {target.name}, dealing {damage} damage!')
            print(f'{target.name} has {target.health} health left!')
            self.mana += 1

        def skill_2(self, target, coefficient=3):
            skill_name = 'bat_kick'
            damage = self.attack * coefficient - target.defense
            target.health -= damage
            print(f'{self.name} uses {skill_name} to attack {target.name}, dealing {damage} damage!')
            print(f'{target.name} has {target.health} health left!')
            self.mana -= 2

        def skill_3(self, target, coefficient=2):
            skill_name = 'bat_nature'
            self.defense = self.defense * coefficient
            self.attack = self.attack * coefficient
            self.speed = self.speed * coefficient
            print(f'{self.name} uses {skill_name} to enhance himself!')
            print(f"{self.name}'s defense from {self.defense / coefficient} to {self.defense} !")
            print(f"{self.name}'s attack from {self.attack / coefficient} to {self.attack} !")
            print(f"{self.name}'s speed from {self.speed / coefficient} to {self.speed} !")
            self.mana -= 3


    class Joker(Character):
        def skill_1(self, target, coefficient=0.7):
            skill_name = "joker's trick"
            for i in range(2):
                damage = self.attack * coefficient - target.defense
                target.health -= damage
                print(f'{self.name} uses {skill_name} to attack {target.name}, dealing {damage} damage!')
                print(f'{target.name} has {target.health} health left!')
            self.mana += 1

        def skill_2(self, target, coefficient=1.5):
            skill_name = "joker's laugh"
            damage = self.attack * coefficient - target.defense
            target.health -= damage
            print(f'{self.name} uses {skill_name} to attack {target.name}, dealing {damage} damage!')
            print(f'{target.name} has {target.health} health left!')

            self.mana += 1
            print(f'{self.name} uses {skill_name} to gain an additional mana! Now he has {self.mana} mana!')
            self.mana -= 2

        def skill_3(self, target, coefficient=0.5):
            skill_name = "joker's shadow"
            # self.defense = self.defense * coefficient
            # self.speed = self.speed * coefficient
            self.attack = self.attack / coefficient
            self.health = self.health / coefficient
            print(f'{self.name} uses {skill_name} to enhance himself!')
            # print(f"{self.name}'s defense from {self.defense / coefficient} to {self.defense} !")
            # print(f"{self.name}'s speed from {self.speed / coefficient} to {self.speed} !")
            print(f"{self.name}'s attack from {self.attack * coefficient} to {self.attack} !")
            print(f"{self.name}'s health from {self.health * coefficient} to {self.health} !")
            self.mana -= 3

    hero_1 = Joker('Joker', 1000, 3, 100, 50, 150)
    hero_2 = Batman('batman', 800, 3, 150, 50, 200)

    game = env(hero_1, hero_2)
    game.step()