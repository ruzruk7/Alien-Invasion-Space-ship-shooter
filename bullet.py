import pygame
from pygame.sprite import Sprite 
import random
# the bullet class inherits from class Sprite which is imported from pygame.sprite module
# sprites allows you to group elements inside a game and act on all grouped elements at the same time.
class Bullet(Sprite):
    '''a class that manages bullets fired from ship'''
    def __init__(self, ai_game): # bullet needs a current instance of Alien_Invasion
        '''create a bullet object at the ships current location'''
        super().__init__() # super().__init__() is called to inherit properly from Sprite.
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color
        self.ship = ai_game.ship
        #create a bullet rect at (0, 0) then set correct location
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height) # this created the bullets rect object. since its not based on an image ->
        #-> we have to build a rect from scratch using the pygame.Rect() class
        # This class .Rect() needs to have the (x-0, y-0) of the rect and width/height of rect.     rects = rect of the bullet  
        #x = [self.ship.rect.center = (70, 0), self.ship.rect.midright]
        self.rect.midtop = self.ship.rect.midtop#random.choice(x) # we set the bullets midtop attribute to match the right wing of the ships topright attribute

        #store the bullets position as a float
        self.y = float(self.rect.y) # we use a float so that we can make fine adjustments to the bullets speed. 
    def update(self):
        '''Move the bullet up the screen'''
        # update the exact position of the bullet 
        self.y -= self.settings.bullet_speed # when a bullet is fired up the screen it means a decreasing y-coordinate value.
        # to update this movement we are subratracting this from bullets rect position on the screen
        # Update the rect position
        self.rect.y = self.y # this tells update() method that the bullet rect is now known as self.y
     
    def draw_bullet(self):
        '''draw the bullet to the screen'''
        pygame.draw.rect(self.screen, self.color, self.rect)
        # draw.rect(window, color, rect of bullet) fills the part of the screen defined by the bullet's rect with the color stored in self.color
# def alternating_bullet():
#         x= ['self.ship.rect.midleft', 'self.ship.rect.midright']
#         while True:
#             for value in x:
#                 print(value)


