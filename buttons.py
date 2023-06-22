import pygame.font #this import lets pygame render text to the screen

class Button:
    '''initialize button attributes'''
    def __init__(self, ai_game, msg): #
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        #set the dimesnions and the properties of the button
        self.width, self.height = 200, 50 # sets the buttons dimensions.
        self.button_color = (0, 135, 0) #dark green
        self.text_color = (255, 255, 255) #white
        self.font = pygame.font.SysFont(None, 48) # the None attribute tells py to use default font and make it sized 48

        #build the buttons rect-object and center it.
        self.rect = pygame.Rect(0, 0, self.width, self.height)# creates the rect and 
        self.rect.center = self.screen_rect.center # sets the center of the button's rect to the center of the pygame window

        #the button message needs to be prepped only once 
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        '''turn msg into a rendered image and center text on the button'''
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color) #1 font.render turns text into an image  the boolean is for AA on or off
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        '''Draw a blank button then draw message'''
        self.screen.fill(self.button_color, self.rect) # draws the rectangular portion of the button on the screen 
        self.screen.blit(self.msg_image, self.msg_image_rect) # pass in the image-to-draw, image's-rect
