# The bulk of functional code is in here

import numpy as np

from rlcard.core import Card

class HeartsRound(object):

    def __init__(self, dealer, num_players, first_player_id):
        ''' Initialize the round class

        Args:
            dealer (object): the object of HeartsDealer
            num_players (int): the number of players in game
        '''
        self.dealer = dealer
        self.current_player = first_player_id
        self.num_players = num_players
        self.target_suit = 'C'
        self.played_cards = [] # Cards played so far in trick
        self.is_over = False
        self.hearts_broken = False
        self.values = {'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'T':10,'J':11,'Q':12,'K':13,'A':14}

    def proceed_round(self, players, action):
        ''' Call other Classes's functions to keep one round running

        Args:
            player (object): object of HeartsPlayer
            action (str): string of legal action
        '''
        suit = action[0]
        rank = action[1]

        player = players[self.current_player]
        # remove correspongding card from player hand
        remove_index = None
        for index, card in enumerate(player.hand):
            if rank == card.rank and suit == card.suit:
                remove_index = index
                break
        card = player.hand.pop(remove_index)
        self.played_cards.append(card)

        if len(self.played_cards) == 1:  # Set target suit
            self.target_suit = suit

        if len(self.played_cards) == 4:
            last_player_in_round = self.current_player
            # Figure out who to give the cards to
            max_value = 2
            max_player = 0
            for idx, card in enumerate(self.played_cards):
                # NOTE: since played cards array isn't in the same order as players
                # we need to rotate indexes to locate correct player ID.
                player_id = (last_player_in_round + 1 + idx) % self.num_players
                if self.values[card.rank] > max_value and card.suit == self.target_suit:
                    max_value = self.values[card.rank]
                    max_player = player_id

            players[max_player].collected.extend(self.played_cards)

            if not player.hand: # Check if over
                self.is_over = True

        if suit == 'H':
            self.hearts_broken = True
        
        if len(self.played_cards) == 4:
            self.current_player = max_player
            self.played_cards = []
        else:
            self.current_player = (self.current_player + 1) % self.num_players

    def get_legal_actions(self, players, player_id):
        legal_actions = []
        if players[player_id].has_2_of_clubs():
            return ["C2"]
        hand = players[player_id].hand
        if len(self.played_cards) == 0: # Going first
            if self.hearts_broken:
                for card in hand:
                    legal_actions.append(card.get_index())
            else:
                for card in hand:
                    if not card.suit == 'H':
                       legal_actions.append(card.get_index())
                if len(legal_actions) == 0: # We only have hearts in our hand
                    for card in hand:
                       legal_actions.append(card.get_index())
            return legal_actions

        # Put all cards of suit self.target_suit into legal_actions
        for card in hand:
            if card.suit == self.target_suit:
                legal_actions.append(card.get_index())
        
        if len(legal_actions) == 0: # No cards in hand of target suit
            for card in hand:
                legal_actions.append(card.get_index())

        return legal_actions
            
    def get_state(self, players, player_id):
        ''' Get player's state

        Args:
            players (list): The list of HeartsPlayer
            player_id (int): The id of the player
        '''
        state = {}
        player = players[player_id]
        state['hand'] = [c.get_index() for c in player.hand]
        state['target'] = self.target_suit
        state['played_cards'] = [c.get_index() for c in self.played_cards]
        state['legal_actions'] = self.get_legal_actions(players, player_id)
        #state['collected'] = [c.get_index() for c in player.collected] # For game debugging only (will increase state space)
        return state
