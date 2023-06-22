import pygame.font

# these are being imported because we are making a group of ships, hence Ship and Sprite
from pygame.sprite import Group
from ship import Ship
class Scoreboard:
    def __init__(self, ai_game):
        '''A class to report scoring information'''
        self.ai_game = ai_game # assigned game instance to an attribute, since it is needed to create some ships.
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats


        #Font settings for scoring information
        self.text_color = (255, 255, 255)
        self.text_bg_color = (0, 0, 0)
        self.font = pygame.font.SysFont(None, 48)

        #Prepare the initial score image.
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ship()
    
    def prep_score(self):
        '''Turn the score into a rendered image'''
        # round() rounds to a set number of decimal places given as the second argument, when given a negative it will round to nearest 10th, 100th, 1000th etc
        rounded_score = round(self.stats.score, -1)
        score_str = (f'{rounded_score:,}')# we turn the numerical value of .score into a string
        # the :,  is a 'format specifier' that modifies the way a variables value is presented
        self.score_image = self.font.render(score_str, True, self.text_color, self.text_bg_color)# we pass this string into .render to draw the image

        #Display the score at the top right of the screen.
        self.score_rect = self.score_image.get_rect() #3 gets the rect coord values of self.score_image
        self.score_rect.right = self.screen_rect.right - 20 # we set its right edge to the right side of the screen - 20 pixels
        self.score_rect.top = 20 # we place the top of the rect at y = 20 
    
    def prep_high_score(self):
        '''Turn the high score into a rendered image'''
        high_score = round(self.stats.high_score, -1)# round the high_score to the nearest 10 and ->
        high_score_str = (f'{high_score:,}')#-> seperate it with , 
        self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.text_bg_color)
        
        # Center the high score at the top of the screen.
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx # center the high_score.rect horizontally
        self.high_score_rect.top = self.score_rect.top# top attribute to match the scores top for symmetry 

    def check_high_score(self):
        '''check to see if theres a new high score'''
        # this checkes to see if the score is higher than the newest high score 
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()

    def prep_level(self):
        '''Turn the level into a rendered  image'''
        level_str = str(self.stats.level)
        self.level_image = self.font.render(level_str, True, self.text_color, self.text_bg_color) # creates an image of the value stored in stats.level

        #position the Level below the score.
        self.level_rect = self.level_image.get_rect()
        # set level_rect's right and top attribute to a certain position
        self.level_rect.right = self.score_rect.right 
        self.level_rect.top = self.score_rect.bottom + 10 
    
    # def warning_message(self, msg):
    #     self.warn_mes_rect = self.font.render(msg, True, self.text_color, self.text_bg_color)
    #     self.warn_rect = self.warn_mes_rect.get_rect()
    #     self.warn_rect.center =

    def prep_ship(self):# 
        '''show how many ships are left'''
        # you will need to make the ship smaller
        self.ships = Group() # creates an empty group to hold all the ship instances. ->
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_game) #-> to fill this group, a loop runs once for every ship the player has left
            ship.rect.x = 10 + ship_number * ship.rect.width #ships apprear next to each other with a 10 pixel margin
            ship.rect.y = 630
            self.ships.add(ship) # add each of these ships.
        

    
    def show_score(self):
        '''Draw the score to the screen'''
        self.screen.blit(self.score_image, self.score_rect) # draws self.score_image at location self.score_rect
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen) # Sprites and Groups use draw() to draw sprites on a given surface.