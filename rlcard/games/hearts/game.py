from rlcard.games.hearts.dealer import HeartsDealer as Dealer
from rlcard.games.hearts.player import HeartsPlayer as Player
from rlcard.games.hearts.round import HeartsRound as Round
from rlcard.games.hearts.utils import get_first_player

class HeartsGame(object):

    def __init__(self, allow_step_back=False, shooting_the_moon_enabled=False):
        self.allow_step_back = allow_step_back
        self.shooting_the_moon_enabled = shooting_the_moon_enabled
        self.num_players = 4
        self.payoffs = [0 for _ in range(self.num_players)]
        self.history = []
 
    def init_game(self):
        ''' Initialize players and state

        Returns:
            (tuple): Tuple containing:

                (dict): The first state in one game
                (int): Current player's id
        '''
        # Initalize payoffs
        self.payoffs = [0 for _ in range(self.num_players)]

        # Initialize a dealer that can deal cards
        self.dealer = Dealer()

        # Initialize four players to play the game
        self.players = [Player(i) for i in range(self.num_players)]

        # Deal all cards to each player to prepare for the game
        self.dealer.deal_cards(self.players)
        
        first_player = get_first_player(self.players)

        self.round = Round(self.dealer, self.num_players, first_player)

        # Save the hisory for stepping back to the last state.
        self.history = []

        player_id = self.round.current_player
        state = self.get_state(player_id)
        return state, player_id

    def step(self, action):
        ''' Get the next state

        Args:
            action (str): A specific action

        Returns:
            (tuple): Tuple containing:

                (dict): next player's state
                (int): next plater's id
        '''

        if self.allow_step_back:
            # First snapshot the current state
            his_dealer = deepcopy(self.dealer)
            his_round = deepcopy(self.round)
            his_players = deepcopy(self.players)
            self.history.append((his_dealer, his_players, his_round))

        self.round.proceed_round(self.players, action)

        player_id = self.round.current_player
        state = self.get_state(player_id)
        return state, player_id

    def step_back(self):
        ''' Return to the previous state of the game

        Returns:
            (bool): True if the game steps back successfully
        '''
        if not self.history:
            return False
        self.dealer, self.players, self.round = self.history.pop()
        return True

    def get_state(self, player_id):
        ''' Return player's state

        Args:
            player_id (int): player id

        Returns:
            (dict): The state of the player
        '''
        state = self.round.get_state(self.players, player_id)
        return state

    def get_payoffs(self):
        ''' Return the payoffs of the game 
            (negative scores of each player)
       
        Returns:
            (list): Each entry corresponds to the payoff of one player
        '''
        for idx in range(len(self.players)):
            player = self.players[idx]
            for card in player.collected:
                if card.suit == 'H':
                    self.payoffs[idx] -= 1
                elif (card.suit == 'S' and card.rank == 'Q'):
                    self.payoffs[idx] -= 13
            if self.shooting_the_moon_enabled:
                if self.payoffs[idx] == -26: # Shooting the moon
                    self.payoffs[idx] = 0
                    for idx2 in range(len(self.players)):
                        if not idx2 == idx:
                            self.payoffs[idx2] = -26
                    return self.payoffs
        return self.payoffs

    def get_legal_actions(self):
        ''' Return the legal actions for current player

        Returns:
            (list): A list of legal actions
        '''

        return self.round.get_legal_actions(self.players, self.round.current_player)

    def get_player_num(self):
        ''' Return the number of players in Limit Texas Hold'em

        Returns:
            (int): The number of players in the game
        '''
        return self.num_players

    @staticmethod
    def get_action_num():
        ''' Return the number of applicable actions

        Returns:
            (int): The number of actions. There are 52 (size of deck) actions
        '''
        return 52

    def get_player_id(self):
        ''' Return the current player's id

        Returns:
            (int): current player's id
        '''
        return self.round.current_player

    def is_over(self):
        ''' Check if the game is over

        Returns:
            (boolean): True if the game is over
        '''
        return self.round.is_over
# Done

## For test
import numpy as np
if __name__ == '__main__':
     #import time
     #random.seed(0)
     #start = time.time()
    game = HeartsGame()
    for _ in range(1):
        state, button = game.init_game()
        print(button, state)
        i = 0
        while not game.is_over():
            i += 1
            legal_actions = game.get_legal_actions()
            print('legal_actions', legal_actions)
            action = np.random.choice(legal_actions)
            print('action', action)
            print()
            state, button = game.step(action)
            print(button, state)
        print(game.get_payoffs())
    print('step', i)
