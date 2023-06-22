import settings
class GameStats:
    '''Track statistics for Alien Invasion'''
    def __init__(self, ai_game):
        '''initialize statistics'''
        self.settings = ai_game.settings
        self.reset_stats()
        self.level = 1
        self.high_score = 0 


    def reset_stats(self):
        '''initialize statistics that can change during the game'''
        self.ships_left = self.settings.ship_limit
        self.score = 0 # this is in reset_stats so that each time a new game begans its reset 
