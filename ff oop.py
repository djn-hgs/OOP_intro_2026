import random


class Dice:
    def __init__(self, rolls, sides=6):
        self.rolls = rolls
        self.sides = sides
        self.last_roll = None

    def roll(self):
        self.last_roll = []

        for _ in range(self.rolls):
            self.last_roll.append(
                random.randint(1, self.sides)
            )

    def sum(self):
        return sum(self.last_roll)

    def __repr__(self):
        return str(self.last_roll)

class Game:
    def __init__(self):
        self.characters = []
        self.rounds = []
        self.current_fight = None

    @property
    def on(self):
        left_standing = 0
        for c in self.characters:
            if c.is_alive:
                left_standing += 1

        if left_standing > 1:
            return True
        else:
            return False

    def add_character(self, character):
        self.characters.append(character)

    def setup_fight(self, a, b):
        self.current_fight = a, b

    def fight(self):
        a, b = self.current_fight

        a.roll()
        b.roll()

        if a.score > b.score:
            self.rounds.append(a)
            b.wound()
        elif b.score > a.score:
            self.rounds.append(b)
            a.wound()
        else:
            self.rounds.append(None)
            a.wound(1)
            b.wound(1)

    def __repr__(self):
        return f'Game on: {self.on}, Players: {self.characters}'



class Character:
    def __init__(self, name, stamina, skill):
        self.score = 0
        self.name = name
        self.stamina = stamina
        self.skill = skill
        self.dice = Dice(2)

    @property
    def is_alive(self):
        return self.stamina > 0

    def roll(self):
        self.dice.roll()
        self.score = self.skill + self.dice.sum()

    def wound(self, amount=2):
        self.stamina -= amount

    def __repr__(self):
        return f'Character: {self.name}, Skill: {self.skill}, Stamina: {self.stamina}'

if __name__ == '__main__':
    game = Game()
    hero = Character('Hero', 12, 10)
    ogre = Character('Ogre', 8, 9)

    game.add_character(hero)
    game.add_character(ogre)

    while game.on:
        game.setup_fight(hero, ogre)
        game.fight()
        print(game)








