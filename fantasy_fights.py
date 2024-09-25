import random
import os 
import time
import sys
import inspect

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

class Orc(Character): #children class
    base_health_points = 100
    base_attack_power = 10
    base_defence = 20
    name = 'Orc'
    perk_info = 'Berserk - when Orc has less than 30% hp, the attack power is doubled'
    perk_flag = False
    priority =0

    def attack(self, *, target : "Character") -> None:
        '''Method that implements a character damage'''
        attack_power = self.attack_power
        if self.health_percentage() < 30:
            attack_power *= 2
            if not self.perk_flag:
                print('Orc entered Berserk mode')
                self.perk_flag = True
        target.got_damage(damage = attack_power)

class Elf(Character): #children class
    base_health_points = 70
    base_attack_power = 20
    base_defence = 15
    name = 'Elf'
    perk_info = "Elves' wisdom - When an Elf has half of his health, he restores 10% once"
    perk_flag = False
    priority = 0

    def got_damage(self, *, damage : int) -> None:
        '''Method that implements a character receiving damage'''
        damage = round(damage * (100 - self.defence()) / 100)
        if self.health_points - damage > 0:
            self.health_points -= damage
            if (not self.perk_flag) & (self.health_percentage() <= 50):
                self.perk_flag = True
                self.health_points += round(0.1 * self.max_health_points())
                print('Elf was healed')
        else: 
            self.health_points = 0

is_here = lambda a, b : a in b

os.chdir(os.path.dirname(os.path.abspath(__file__)))
race_dict = {}

if os.path.isdir('plugins'):
    for files in os.listdir('plugins'):
        if files.endswith('.py'):
            __import__('plugins.'+files[:-3])
            race_dict = {cls.name : cls for _, cls in inspect.getmembers(sys.modules['plugins.'+files[:-3]], inspect.isclass) if cls.__module__ == 'plugins.'+files[:-3]}
            if is_here('Character', race_dict):
                del race_dict['Character']

race_dict['Orc'] = Orc
race_dict['Elf'] = Elf


def fight(*, fighter_1 : Character, fighter_2 : Character) -> None:
    '''Function of fight between 2 characters'''
    choice_coin = [True, False]

    round_counter = 0
    print('\nFighter 1:')
    fighter_1.info()
    print('Fighter 2:')
    fighter_2.info()

    order = ''
    while (order != 'start') & (order != 'exit'):
        print("Your order start/exit: ", end = '')
        order = input()
        if (order != 'start') & (order != 'exit'):
            print("Please, repeat the order. ", end = '')

    while fighter_1.is_alive() & fighter_2.is_alive() & ((order != 'exit')):

        if fighter_1.priority < fighter_2.priority:
            fighter_1, fighter_2 = fighter_2, fighter_1
        elif fighter_1.priority == fighter_2.priority:
            if random.choice(choice_coin):
                fighter_1, fighter_2 = fighter_2, fighter_1

        round_counter += 1
        time.sleep(1)
        print(f'====================\nRound: {round_counter}')
        fighter_1.attack(target = fighter_2)
        print(f'{fighter_1.name} attacks {fighter_2.name}...')
        if  fighter_2.is_alive():
            fighter_2.attack(target = fighter_1)
            print(f'{fighter_2.name} attacks {fighter_1.name}...')
            print(f'In the end of round {round_counter}:')
            print(f'{fighter_1.name} has {fighter_1.health_points} hp')
            print(f'{fighter_2.name} has {fighter_2.health_points} hp')
            print(f'====================')
        else: 
            print(f'====================')
            print(f'{fighter_2.name} died')
            print(f'{fighter_1.name} has {fighter_1.health_points} hp\n')
    if not fighter_1.is_alive():
        print(f'{fighter_1.name} died')
        print(f'{fighter_2.name} has {fighter_2.health_points} hp\n')

@decorator
def hello_king() -> None:  
    '''Greetings'''
    print('Welcome, Your Majestry!')
    time.sleep(1)
    print('Today, on the feast of the Holy Warrior, we are holding an annual')
    time.sleep(1)
    print('martial arts tournament as usual. And, of course, Your Majestry are')
    time.sleep(1)
    print('the Head of the tournament. Your Majestry will get a list of warriors')
    time.sleep(1)
    print('with a description of their skills and abilities, choose 2 warriors')
    time.sleep(1)
    print('and they will fight each other to the END to glorify of their skills')
    time.sleep(1)
    print('and abilities, to glorify themselves as the ...\n')
    time.sleep(1)
    print('GREATEST WARRIOR!\n')
    time.sleep(1)
    print("Let's get started!")
    hello = ''
    while hello != 'start':
        print("Give the order to 'start':", end = '  ')
        hello = input()
        if hello != 'start':
            print('Please, Your Majestry,', end = ' ')

@decorator
def orders() -> None: 
    '''The list of commands'''
    print('Manage the tournament as Your Majestry wishes')
    print("'warriors' to get info about warriors")
    print("'fight' to begin fight")
    print("'restart' to start The Tournament again")
    print("'end' to end The Tournament, don't rush with this order")
    print("'info' to get Your's Majestry order list")

def warriors_info() -> None:
    '''Function returning the description of characters'''
    print("All right, today the greatest warriors of Your's Majestry kingdom arrived at The Holy Warror Tournament:")
    print('====================')
    for i in race_dict.keys():
        print(i)
    print('====================')
    manage = ''
    while manage != 'exit':
        print("Choose warrior you want to know more about or 'exit': ", end = '')
        manage = input()
        if (manage != 'exit') & is_here(manage, race_dict.keys()):
            race_dict[manage].class_info(race_dict[manage])
        elif (manage != 'exit'):
            print("I don't know this warrior. ", end = '')
    print()
def fighter_choice(i) -> Character:
    '''Function of choice 2 characters by user'''
    fighter = ''
    while not is_here(fighter, race_dict.keys()):
        print(f"Choose warrior {i}: ", end = '')
        fighter = input()
        if  not is_here(fighter, race_dict.keys()):
            print("I don't know this warrior. ", end = '')
    level = 0
    while (level < 1) | (level > 10):
        print("Choose his level [1 .. 10]: ", end ='')
        level = input()
        if level.isnumeric():
            level = int(level)
        else:
            level = 0
        if (level < 1) | (level > 10):
            print("I don't know", fighter, "with this level. ", end = '')
    return race_dict[fighter](level = level)

def start_fight() -> None:
    '''Function of fight preparing'''
    print("All right, today the greatest warriors of Your's Majestry kingdom arrived at The Holy Warror Tournament:")
    print('====================')
    for i in race_dict.keys():
        print(i)
    print('====================')
    print("Choose 2 warriors and their levels")
    fighter_1 = fighter_choice(1)
    fighter_2 = fighter_choice(2)
    fight(fighter_1 = fighter_1, fighter_2 = fighter_2)

def restart() -> None:
    '''Restart terminal and game'''
    os.system('cls' if os.name == 'nt' else 'clear')
    hello_king()
    orders()


order_list = {'warriors' : warriors_info, 'fight' : start_fight, 'restart' : restart, 'info' : orders}

restart()
order = ''
while order !='end':
    print("Your Majestry, give the order ('info'): ", end = '')
    order = input()
    if (order != 'end') & is_here(order, order_list.keys()):
        print()
        order_list[order]()
    elif order != 'end':
        print("I don't know how to fullfil this order. ", end = '')

print('\nIt was the greatest Tournament, Thank you, Your Majestry! The whole kingdom will be waiting the next Holy Warrior Tournament')