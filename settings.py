import pygame
class Settings:
    #this class only has the __init__ method, which initialized attributes controlling the game's appearance and the ships speed.
    '''A Class to store all the settings for Alien_invasion.py'''
    def __init__(self):
        '''initialize the game's settings'''
        #screen settings
        self.screen_width = 1200 #reduced by 200
        self.screen_height = 800 #reduced by 200 
        self.bg_color = pygame.image.load('C:\\Users\\DSAXPS_13_9360\\Documents\\coding languages\\CODE files\\first_game_Alien_invasion\\images\\Starset.bmp') #(255, 255, 255)

        #ship settings 
        self.ship_limit = 3

        #bullet settings
        self.bullet_width = 10
        self.bullet_height = 15
        self.bullet_color = (0, 174, 239)
        self.bullets_allowed = 17

        #Alien settings 
        self.fleet_drop_speed = 10

        self.speedup_scale = 1.1
        self.score_scale = 1.5
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        '''initialize settings that change throughout the game'''
        self.ship_speed = 3.5
        self.bullet_speed = 7.5
        self.alien_speed = 1.0

        #fleet direction of 1 represents right; -1 represents left 
        self.fleet_direction = 1

        #scoring settings:
        self.alien_point = 10
    
    def increase_speed(self):
        '''Increase speed settings'''
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_point = int(self.alien_point *self.score_scale)
