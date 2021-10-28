from classes.deck import Deck
from classes.player import *
import random


# SET UP THE GAME
bicycle = Deck()
adam    = Computer('Adam')
beth    = Computer('Beth')
chad    = Computer('Chad')
jason   = Human('Jason')
players = [adam, beth, chad, jason]

random.shuffle(players)
turn = 0
initial_card_count = 7
if len(players) > 3:
    initial_card_count = 5


# GAMEPLAY FUNCTIONS
def deal(deck, players):
    for n in range(initial_card_count):
        for p in players:
            p.hand.append(deck.cards.pop(0))
    for p in players: 
        p.update_ranks()

def end_turn():
    global turn
    if turn == len(players) - 1:
        turn = 0
    else:
        turn += 1

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


def ask(fisher):
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
            if len(bicycle.cards) > 0:
                print('... go fish')
                fisher.hand.append(bicycle.cards.pop(0))
                fisher.update_ranks()
            if not book_check(fisher):
                end_turn()
            else:
                print('... lucky though!')
        else:
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
            book_check(fisher)


# GAME PLAY!
bicycle.shuffle()
deal(bicycle, players)

while len(Player.show_books()) < 13:
    if len(players[turn].hand) == 0:
        end_turn()
    else:
        ask(players[turn])

for p in players:
    print('\n' + p.name + "'s books:")
    print(str(len(p.books)) + ': ' + str(p.books))
