from . import card
import random

class Deck:


    def __init__( self ):
        suits = [ "spades" , "hearts" , "clubs" , "diamonds" ]
        self.cards = []

        for s in suits:
            for i in range(2,15):
                str_val = ""
                if i == 14:
                    str_val = "A"
                elif i == 11:
                    str_val = "J"
                elif i == 12:
                    str_val = "Q"
                elif i == 13:
                    str_val = "K"
                else:
                    str_val = str(i)
                self.cards.append( card.Card( s , i , str_val ) )

    def shuffle(self):
        random.shuffle(self.cards)
    
    def show_cards(self):
        for card in self.cards:
            card.card_info()

