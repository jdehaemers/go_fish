import random
from . import card

class Player:
    all_players = []
    def __init__(self, name):
        self.name  = name
        self.hand  = []
        self.ranks = {}
        self.books = []
        Player.all_players.append(self)

    def show_hand(self):
        for card in self.hand:
            card.card_info()
    
    def update_ranks(self):
        self.ranks = {}
        for c in self.hand:
            if c.string_val not in self.ranks:
                self.ranks[c.string_val] = 1
            else:
                self.ranks[c.string_val] += 1
    
    @classmethod
    def show_books(cls):
        all_books = []
        for p in cls.all_players:
            all_books += p.books
        return all_books
    
    @staticmethod
    def is_adult(age):
        return age >= 18


class Computer(Player):
    def __init__(self, name):
        super().__init__(name)

    def select_target(self):
        x = Player.all_players.copy()
        x.remove(self)
        for p in x:
            if len(p.hand) == 0:
                x.remove(p)
        random.shuffle(x)
        return x[0]
    
    def select_rank(self):
        random.shuffle(self.hand)
        return self.hand[0].string_val


class Human(Player):
    def __init__(self, name):
        super().__init__(name)
    
    def select_target(self):
        print(self.ranks)
        target = input('Indicate which player to target: ')
        for p in Player.all_players:
            if p.name == target:
                return p

    def select_rank(self):
        return input ('Indicate which rank to target: ')

class Smart(Player):
    def __init__(self, name):
        super().__init__(name)
    
    def select_target(self):
        pass

    def select_rank(self):
        pass