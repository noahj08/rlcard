
class HeartsPlayer(object):

    def __init__(self, player_id):
        ''' Initialize a Hearts player class

        Args:
            player_id (int): id for the player
        '''
        self.player_id = player_id
        self.hand = []
        self.collected = []
        self.score = 0

    def get_player_id(self):
        ''' Return player's id
        '''
        return self.player_id

    # NOTE: games rules dictate that player with
    # 2 of clubs rather than spades starts?
    def has_2_of_spades(self):
        ''' Returns whether or not the player
            is holding the 2 of spades for the
            first turn (-1 if not)
        '''
        for idx in range(len(self.hand)):
            card = self.hand[idx]
            if card.suit == 'S' and card.rank == '2':
                return True
        return False

    def has_2_of_clubs(self):
        ''' Returns whether or not the player
            is holding the 2 of spades for the
            first turn (-1 if not)
        '''
        for idx in range(len(self.hand)):
            card = self.hand[idx]
            if card.suit == 'C' and card.rank == '2':
                return True
        return False
