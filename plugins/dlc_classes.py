import random

def decorator(func): #decorator for beauty output
    def wrapper(*args):
        print('============================================')
        func(*args)
        print('============================================\n')
    return wrapper

class Character: #general class of our game characters
    name = 'Character'

    def __init__(self, *, level : int) -> None:
        self.level = level
        self.health_points = self.base_health_points * level
        self.attack_power = self.base_attack_power * level
        self.name = self.name
        self.priority = self.priority
    
    @decorator
    def info(self) -> None:
        '''Information about chatacter'''
        print(f'Race: {self.name}, level: {self.level}')
        print(f'HP: {self.health_points}')
        print(f'Attack power: {self.attack_power}')
        print(f'Defence: {self.defence()}')
        print(f'Perk: {self.perk_info}')

    @decorator
    def class_info(self):
        '''Information about game class'''
        print(f'Race: {self.name}')
        print(f'Base HP: {self.base_health_points}')
        print(f'Base attack power: {self.base_attack_power}')
        print(f'Base defence: {self.base_defence}')
        print(f'Perk: {self.perk_info}')

    def got_damage(self, *, damage : int) -> None:
        '''Method that implements a character receiving damage'''
        damage = round(damage * (100 - self.defence()) / 100)
        if self.health_points - damage > 0:
            self.health_points -= damage
        else: 
            self.health_points = 0

    def defence(self) -> int:
        '''Method returning the character's defence'''
        defence = self.base_defence * self.level
        if defence > 60:
            defence = 60
        return defence
    
    def attack(self, *, target : "Character") -> None:
        '''Method that implements a character damage'''
        target.got_damage(damage = self.attack_power)

    def is_alive(self) -> bool:
        '''Method returning is character stil alive'''
        return self.health_points > 0
    
    def max_health_points(self) -> int:
        '''Method returning the character's maximum health points'''
        return self.base_health_points * self.level

    def health_percentage(self) -> int:
        '''Method returning the character's health points in percents'''
        percent = round(100 * self.health_points / self.max_health_points())
        return percent

class Goblin(Character): #children class
    base_health_points = 60
    base_attack_power = 10
    base_defence = 15
    name = 'Goblin'
    perk_info = 'Meannes - Goblins always attack first'
    priority = 1

class Dwarf(Character): #children class
    base_health_points = 70
    base_attack_power = 10
    base_defence = 10
    name = 'Dwarf'
    perk_info = "Miner - Dwarfs have a 10% chance of taking the enemy's health for themselves"
    priority = 0

    def attack(self, *, target : "Character") -> None:
        '''Method that implements a character damage'''
        chance = [False if i != 9 else True for i in range(10)]
        attack_power = self.attack_power
        target.got_damage(damage = attack_power)
        if random.choice(chance):
            self.health_points += round(self.attack_power * (100 - target.defence()) / 100)
            print(f"Dwarf mined {target.name} hp")

class Human(Character): #children class
    base_health_points = 50
    base_attack_power = 15
    base_defence = 10
    name = 'Human'
    perk_info = "Human will - when Humans have less than 20% hp, their defence increases 3 times and have a higher upper bound"
    priority = 0
    perk_flag = False

    def defence(self) -> int:
        '''Method returning the character's defence'''
        defence = self.base_defence * self.level
        if self.health_percentage() < 20:
            defence *= 3
            if not self.perk_flag:
                self.perk_flag = True
                print('Human will! Defence increased')
        if defence > 70:
            defence = 70
        return defence