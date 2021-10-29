from classes.deck import *
from classes.player import *
import random

anya    = Computer('Anya')
beth    = Computer('Beth')
chad    = Computer('Chad')
jason   = Human('Jason')
players = [anya, beth, chad, jason]


def book_check(player):
    if 4 in player.ranks.values():
        book = ''
        for r in player.ranks:
            if player.ranks[r] == 4:
                player.books.append(r)
                book = r
                break
        for c in player.hand.copy():
            if c.string_val == book:
                player.hand.remove(c)
        player.update_ranks()
        return True
    else:
        return False


class Game:
    def __init__(self, players, index = 0):
        self.players    = players
        self.index      = index
        self.deck       = Deck()
        self.turn       = 0
        self.log        = []
        self.book_count = 0
        self.init_deal  = 7
        random.shuffle(self.players)
        if len(self.players) > 3:
            self.init_deal = 5
        self.deal()

    def deal(self):
        for n in range(self.init_deal):
            for p in self.players:
                p.hand.append(self.deck.cards.pop(0))
        for p in players: 
            p.update_ranks()

    def end_turn(self):
        if self.turn == len(self.players) - 1:
            self.turn = 0
        else:
            self.turn += 1

    def ask(self):
        fisher = self.players[self.turn]
        if len(fisher.hand) == 0:
            self.end_turn()
        else:
            log_entry = {'fisher': fisher.name, 'target': '', 'rank': '', 'response': '', 'transfer': [], 'book': ''}
            target = fisher.select_target()
            rank = fisher.select_rank()
            fisher_ranks = set()
            for c in fisher.hand:
                fisher_ranks.add(c.string_val)
            if len(fisher_ranks) == 0:
                pass
            else:
                print(f'{fisher.name} asks {target.name} for {rank}')
                target_ranks = set()
                for c in target.hand:
                    target_ranks.add(c.string_val)
                if rank not in fisher_ranks:
                    print('Pick a proper rank')
                elif rank not in target_ranks:
                    # update log entry
                    log_entry['target']   = target.name
                    log_entry['rank']     = rank
                    log_entry['response'] = 'no_fish'
                    if len(self.deck.cards) > 0:
                        log_entry['response'] = 'go_fish'
                        print('... go fish')
                        fisher.hand.append(self.deck.cards.pop(0))
                        fisher.update_ranks()
                        log_entry['transfer'] = [fisher.hand[-1]]
                    if not book_check(fisher):
                        self.log.append(log_entry)
                        self.end_turn()
                    else:
                        log_entry['book'] = log_entry['rank']
                        print('... lucky though!')
                        self.log.append(log_entry)
                        self.book_count += 1
                else:
                    log_entry['target']   = target.name
                    log_entry['rank']     = rank
                    log_entry['response'] = 'catch'
                    print('... catch made!')
                    match_indexes = []
                    for i in range(len(target.hand)):
                        if target.hand[i].string_val == rank:
                            match_indexes.append(i)
                    print(f'... {len(match_indexes)} cards')
                    for i in range(len(match_indexes)-1, -1, -1):
                        fisher.hand.append(target.hand.pop(match_indexes[i]))
                        target.update_ranks()
                    fisher.update_ranks()
                    if book_check(fisher):
                        self.book_count += 1
                    # update log entry
                    self.log.append(log_entry)
    

print('BEGIN!')
print('players: ')
for p in players:
    print('  ' + p.name)
print('')
game = Game(players)
while game.book_count < 13:
    game.ask()

for p in players:
    print('\n' + p.name + "'s books:")
    print(str(len(p.books)) + ': ' + str(p.books))
