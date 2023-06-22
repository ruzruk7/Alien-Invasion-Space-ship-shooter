import pygame
from pygame.sprite import Sprite
#pygames group method automatically draws all the elements of a group on the screen as well
class Alien(Sprite):
    '''a class to represent a single alien inside a fleet'''
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        #load the alien image and retreive the image rect for placment,movement
        self.image = pygame.image.load('images//enemy_wraith.bmp')
        self.rect = self.image.get_rect()

        #start each new alien near the top left of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        #store the alien's exact horizontal position
        # we are are only concerned with the horizontal speed hence we track it precicely
        self.x = float(self.rect.x)

    def check_edge(self):
        '''return True if alien is at edge of the screen'''
        screen_rect = self.screen.get_rect()
        return (self.rect.right >= screen_rect.right) or (self.rect.left <= 0) # this returns true if it is at either the right or left side of screen.->
        #-> otherwise it returns False if the alien rect is not at either edge 


    def update(self):
        '''Move the alien to the right'''
        self.x += self.settings.alien_speed * self.settings.fleet_direction # might be able to use itertools.cycle using a list with equal +/- values
        self.rect.x = self.x
