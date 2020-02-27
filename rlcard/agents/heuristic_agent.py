import numpy as np


class HeuristicAgent(object):
    ''' A heuristic agentfor the HEARTS GAME ONLY. Heuristic agents use a fixed strategy
    '''

    def __init__(self, action_num):
        ''' Initilize the random agent

        Args:
            action_num (int): the size of the ouput action space
        '''
        self.action_num = action_num
        self.card2id = {"SA": 0, "S2": 1, "S3": 2, "S4": 3, "S5": 4, "S6": 5, "S7": 6, "S8": 7, "S9": 8, "ST": 9, "SJ": 10, "SQ": 11, "SK": 12, "HA": 13, "H2": 14, "H3": 15, "H4": 16, "H5": 17, "H6": 18, "H7": 19, "H8": 20, "H9": 21, "HT": 22, "HJ": 23, "HQ": 24, "HK": 25, "DA": 26, "D2": 27, "D3": 28, "D4": 29, "D5": 30, "D6": 31, "D7": 32, "D8": 33, "D9": 34, "DT": 35, "DJ": 36, "DQ": 37, "DK": 38, "CA": 39, "C2": 40, "C3": 41, "C4": 42, "C5": 43, "C6": 44, "C7": 45, "C8": 46, "C9": 47, "CT": 48, "CJ": 49, "CQ": 50, "CK": 51}
        self.id2card = dict([(val, key) for key,val in self.card2id.items()])
        self.values = {'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'T':10,'J':11,'Q':12,'K':13,'A':14}

    def step(self,state):
        ''' Predict the action given the curent state in gerenerating training data.

        Args:
            state (numpy.array): an numpy array that represents the current state

        Returns:
            action (int): the action predicted (randomly chosen) by the random agent
        '''
        legal_actions = [self.id2card[ID] for ID in state['legal_actions']]
        is_last = (len(state['played_cards']) == 3)
        is_first = (len(state['played_cards']) == 0)
        has_target = (legal_actions[0][0] == state['target'])
        has_QS = ('SQ' in legal_actions)
        smallest_card_idx = np.argmin([self.values[card[1]] for card in legal_actions])
        largest_card_idx = np.argmax([self.values[card[1]] for card in legal_actions])
        largest_heart_idx = np.argmax([self.values[card[1]] if card[0] == 'H' else 0 for card in legal_actions])
        if is_first:
            return self.card2id[legal_actions[smallest_card_idx]]
        else:
            if not has_target:
                if has_QS:
                    return self.card2id['SQ']
                if not largest_heart_idx == 0 or legal_actions[0][0] == 'H':
                    return self.card2id[legal_actions[largest_heart_idx]]
                else:
                    return self.card2id[legal_actions[largest_card_idx]]
            elif is_last:
                return self.card2id[legal_actions[largest_card_idx]]
            else:
                return self.card2id[legal_actions[smallest_card_idx]]
        return np.random.choice(state['legal_actions'])

    def eval_step(self, state):
        ''' Predict the action given the curent state for evaluation.
            Since the random agents are not trained. This function is equivalent to step function

        Args:
            state (numpy.array): an numpy array that represents the current state

        Returns:
            action (int): the action predicted (randomly chosen) by the random agent
        '''
        return self.step(state)
