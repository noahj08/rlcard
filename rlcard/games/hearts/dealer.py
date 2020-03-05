import random

from rlcard.utils.utils import init_standard_deck


class HeartsDealer(object):
    
    def __init__(self):
        ''' Initialize a hearts dealer class
        '''
        self.deck = init_standard_deck()
        self.shuffle()

    def shuffle(self):
        ''' Shuffle the deck
        '''
        random.shuffle(self.deck)

    def deal_cards(self, players):
        ''' Deal all cards in deck evenly to all players '''
        i = 0
        while len(self.deck) > 0:
            players[i].hand.append(self.deck.pop())
            i += 1
            if i > len(players)-1:
                i = 0


class HeartsMiniDealer(HeartsDealer):
    def __init__(self):
        super().__init__()
        # restricted_deck = ['A', 'K', 'Q', '2']
        restricted_deck = ['Q', '2']

        if restricted_deck:
            new_deck = []
            for card in self.deck:
                if card.rank in restricted_deck:
                    new_deck.append(card)
            self.deck = new_deck

        self.shuffle()
# Done
