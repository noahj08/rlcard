import json
import os
import numpy as np

import rlcard
from rlcard.envs.env import Env
from rlcard.games.hearts.game import HeartsGame as Game

class HeartsEnv(Env):
    ''' Hearts Environment
    '''

    def __init__(self, allow_step_back=False):
        ''' Initialize the Hearts environment
        '''
        super().__init__(Game(allow_step_back), allow_step_back)
        valid_suit = ['S', 'H', 'D', 'C']
        valid_rank = ['A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K']
        self.actions = [x + y for x in valid_suit for y in valid_rank]

        self.state_shape = [104]

        with open(os.path.join(rlcard.__path__[0], 'games/hearts/card2index.json'), 'r') as file:
            self.card2index = json.load(file)

    def get_legal_actions(self):
        ''' Get all leagal actions

        Returns:
            encoded_action_list (list): return encoded legal action list (from str to int)
        '''
        return self.game.get_legal_actions()

    def extract_state(self, state):
        ''' Extract the state representation from state dictionary for agent

        Note: Currently the use the hand cards and the public cards. TODO: encode the states

        Args:
            state (dict): Original state from the game

        Returns:
            observation (list): combine the player's score and dealer's observable score for observation
        '''
        # TODO for project group: Improve this
        processed_state = {}

        for key,value in state.items():
            if key == 'legal_actions':
                legal_actions = [self.actions.index(a) for a in state['legal_actions']]
                processed_state['legal_actions'] = legal_actions
            else:
                processed_state[key] = value # Current hand (list of IDs), played cards (list of IDs), target suit (String)

        obs = np.zeros(104)
        # add card in players own hand to the observed state
        idx = [self.card2index[card] for card in state['hand']]
        obs[idx] = 1

        # add played cards to the observed state.
        # TODO: create separate representation for history of played cards and
        #  cards played in the current round thus far
        idx = [self.card2index[card] + 52 for card in state['played_cards']]
        obs[idx] = 1
        processed_state['obs'] = obs
        return processed_state

    def get_payoffs(self):
        ''' Get the payoff of a game

        Returns:
           payoffs (list): list of payoffs
        '''
        return self.game.get_payoffs()

    def decode_action(self, action_id):
        ''' Decode the action for applying to the game

        Args:
            action id (int): action id

        Returns:
            action (str): action for the game
        '''
        legal_actions = self.game.get_legal_actions()
        if self.actions[action_id] not in legal_actions:
            raise "Selected action is illegal!"
        return self.actions[action_id]
