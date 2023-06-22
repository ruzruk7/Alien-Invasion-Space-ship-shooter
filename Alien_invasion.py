#no-starch 1 page 294 CHAPT 12 13 14
############## FIRST GAME####################### code named Alien invasion
#py -m pip install setuptools -U   The setuptools Python package version must be at least 34.4.0.
#py -m pip install --user pygame
#py -m pip install pygame --pre    this is installing a pre-release-version for pygame
#py -m pip install wheel   this installs pre-compiled binaries for most OS
#py -m pip(package manager) install (package name) --upgrade   to upgrade a package

import random
import sys # provides functionality to be able to quit using the tools sys provodes
from time import sleep # this allows us to pause the game when the ship is hit
import pygame #all the functionality needed to make a game is provided by pygame
from settings import Settings
from game_stats import GameStats #
from scoreboard import Scoreboard
from buttons import Button
from ship import Ship # MADE FIFTH
from bullet import Bullet #MADE EIGHTH
from alien import Alien # MADE NINETH

class AlienInvasion:
    '''Overall class to manage game assests and behavior'''
    def __init__(self): # MADE FIRST
        '''initialize the game and create game resources'''
        pygame.init() 
        # this initializes the background settings that pygame needs to run properly
        self.clock = pygame.time.Clock()
        # anytime the event loop processes faster than we defined, pygame will calculate the correct amount pause time 
        # to get a consistent fps.
        # this is to be defined in the __init__ method
        # NOTICE .Clock is a class inside of method .time inside module pygame ***

        self.settings = Settings()
        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN) # this tells pygame to figure out a screen size that will fill the entire screen
        # pygame.display is the main display surface, the new window
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height # we do this because we do not know how big the screen size will be so we use .get_rect().width/.height attribute of .get_rect() to update settings object
        # this module of pygame .display.set_mode(zzzz,xxxx) creates a display window
        # the display window will be zzzz pixels high and xxxx pixels wide
        # we assign this to self.screen so that it will be available to all methods in this class
        # the object(pygame.display.set_mode(zz,xx)) is called a 'surface' which is where a game element can be displayed 
        # each element in a game like a ship or an alien is its own surface
        # the surface returned by display.set_mode() represents the entire game window, which will be redrawn on every pass of the loop ->
        #-> so that it can be updated with user input
        
        pygame.display.set_caption('Alien Invasion') 
        # this sets the caption of the pygame.display surface

        #####self.bg_color = (230, 230, 230) done using module settings.py
        ####set background color
        self.ship = Ship(self) # Ship(self) is the argument to the instance of AlienInvasion. This paramter gives class Ship access to the game's resources like screen object
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        self.bullets = pygame.sprite.Group()# pygame.sprite.Group() produces a Group class which acts like a list[], this list[] will store all active bullets
        # this group will draw and update the position of each bullet on each pass of the while loop in run_game()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()
        self.game_active = False # a flag for ending the game based on defined parameters.
        #make the play button
        self.play_button = Button(self, 'Play') #creates a button with a text render of Play

    def run_game(self): # MADE SECOND
        '''Start the main loop for the game'''
        # this is the main loop of the game, a 'while loop'
        # the main loop here checks for player input, updates position of ship and any bullets fired,->
        #-> we then use the updated positions of everything to draw a new screen and tick clock at end of each pass through loop
        while True:
            # to call method from within a class we use dot.notation with variable self.method()
            self._check_events() 
            if self.game_active: # what parts of the game should run if game is active. the included methods are the only ones necessary while the game is running. the rest are needed even if the game is not being played i.e:waiting for player to start the game
                self.ship.update()
                self._update_bullets()
                self._update_alien() # after bullet so that we can see if bullet.rect hit alien.rect
            self._update_screen() #make sure this is after all of the updates we want to be drawn. or the update will not be drawn each tick
            self.clock.tick(60)
            #we make the .Clock() tick at end of this 'while' loop
            # .tick() method takes one argument: fps (aka set fps to 30)

    def _update_bullets(self):       
        self.bullets.update() # this calls bullet.update() on each sprite in the group bullets (line 46)
        # get rid of old bullets that have dissappeared.
        for bullet in self.bullets.copy(): # py excepts lists/groups in pygame will remain the same for the duration of an active for loop.->
            #-> this makes it that we cannot remove items from such lists/group that are within a for loop. the .copy() lets us modify the original list without messing up this loop
            if bullet.rect.bottom <= 0: # we check to see has moved past y-0 coordinate AKA off the screen
                self.bullets.remove(bullet) # we remove it from bullets.Group()  bullet refers to a variable but originial groups is the Group() class
                #print(len(self.bullets)) # verify  number of bullets is being deleted after it gets of the screena 

    def _update_alien(self):
        '''update the position of all aliens in fleet'''
        self._check_fleet_edges()
        self.aliens.update()
        #check for any bullets that have hit aliens. if yes remove both bullet and alien
        #-> which are based on the order of sprites given to pygame.groupcollide()
        # look for alien to ship collisions
        self._check_bullet_alien_collision()
        if pygame.sprite.spritecollideany(self.ship, self.aliens): #.spritecollideany takes in (sprite=ship, group=self.aliens)
            self._ship_hit()
        for alien in self.aliens.copy(): 
            if alien.rect.bottom >= self.settings.screen_height:
                self._ship_hit()
                break

    def _check_bullet_alien_collision(self):
        '''Respond to bullet-Alien collisions'''
        #remove any bullets and aliens that have collided
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True) # this tells py to check whether (sp1, sp2, kill1, kill2) sp1 has touched sp2 and if it does which one dies based on kill1 kill2->
        if collisions:
            for aliens in collisions.values():
                self.stats.score +=  self.settings.alien_point * len(aliens) # we are multiplying alien_point with the amount of aliens in side dict collisions{}
            self.sb.prep_score()
            self.sb.check_high_score()

        # if len(self.aliens) < 6: ##########################*********************this  function is placed in redraw alien() so that a new level is denoted each time that method is called. alien reinforemcent based level
        #     #destroy  existing bullets  and create new fleet
        #     self.bullets.empty()
        #     self._redraw_alien
        #     #self.settings.increase_speed()

        #     # increase level 
        #     self.stats.level += 1 
        #     self.sb.prep_level()

    def _ship_hit(self):
        '''Respond to the ship being hit by an alien.'''
        if self.settings.ship_limit > 0 :
            #decrement ships_left by 1 and update scoreboard
            self.stats.ships_left -= 1
            self.sb.prep_ship() # we call this AFTER decrasing ships so that correct number of remaining ships are rendered
            # get rid of any remaining bullets and aliens
            self.bullets.empty()# .empty removes all sprites inside the group
            self.aliens.empty() 
            # create a new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()
            # pause the screen 
            sleep(1.0)
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)

    def _check_fleet_edges(self):
        '''respond appropriately if any aliens have reached an edge'''
        for alien in self.aliens.sprites():#1 we loop through all elements in the list of pygame.sprite.Group()
            if alien.check_edge():# we check if .check_edges has returned True
                self._change_fleet_direction()# if returned true all aliens in the fleet will do this method
                break
    def _change_fleet_direction(self):
        '''drop the entire fleet and change the fleets direction'''
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed #3 we drop each alien by adding fleet_drop_speed amount to the y value of alien.rect.y
        self.settings.fleet_direction *= -1 # this isent inside the for loop due to us only needing to change the direction once. not at the pass of each loop.

    def _create_fleet(self):
        '''Create the fleet of Aliens'''
        ##Make an alien ->
        #-> and keep adding an aliens until there is no room left
        alien = Alien(self)##
        alien_width, alien_height = alien.rect.size #using a rect.size we can get the width and height, respectively. rect.size is a () which contains x, y
        
        current_x, current_y = alien_width, 0 # we set the initial x- and y- values for the placement of the first alien in fleet, so alien1's x, y from left and top of screen    # current_x is euqal to the first Alien(self)
        while current_y < (self.settings.screen_height - 3 * alien_height):# we define how many rows can be placed, inside a column
            while current_x < (self.settings.screen_width - 1 * alien_width): 
                self._create_alien(current_x, current_y)# updated to take in current x and y position of
                current_x += 2 * alien_width #we increment the value of current_x towards the right of the screen
            #finish row; reset the x value and increment y value
            #this is in the outer loop because the outer loop is responsible for each row vertically. inner loop is responsible for each column horizontally
            #% x = [10, 20, 30, 40, 50, 60 ,70 ,80 ,90]
            current_x = alien_width #%random.choice(x)
            current_y += 2 * alien_height #%random.choice(x)

    def _create_alien(self, x_position=100, y_position=104): # needs one parameter, the x-value of where the alien should be placed.
        # the refactoring of this allows for easier addition of rows and make an entire fleet
        '''Create an alien and place it in the row'''
        new_alien = Alien(self) # making a new  alien
        new_alien.x = x_position # set the precise location of new alien at location of x_position
        new_alien.rect.y = y_position
        new_alien.rect.x = x_position # the new_aliens rect.x value is also set at the location of current_x
        self.aliens.add(new_alien)## we add the new_aliens to the same Sprite group

    def _redraw_alien(self):
        x = [100, 110, 120, 150, 200, 210, 220, 250, 600, 650, 500, 550,] #makes the aliens show up at different start locations
        y = [0, 50, 150, 250, 350, 25, 100, 130, 330]
        while len(self.aliens.sprites()) <= 3: # another way to check == if not self.aliens    to empty a group we can self.group_name.empty()
            self._create_alien(random.choice(x),random.choice(y))
            self._create_alien(random.choice(x),random.choice(y))
            self._create_alien(random.choice(x),random.choice(y))
            self._create_alien(random.choice(x),random.choice(y))
            self._create_alien(random.choice(x),random.choice(y))
            self._create_alien(random.choice(x),random.choice(y))
            self._create_alien(random.choice(x),random.choice(y))
            self.settings.increase_speed()###################################
            self.stats.level += 1 
            self.sb.prep_level()

    def _update_screen(self): 
        '''update images on the screen, and flip to the new screen'''
        #this method redraws the screen on each pass of the main loop
        # order items in order of which image you want to be drawn on top of the previouse image
        self.screen.blit(self.settings.bg_color, (0, 0)) # was originally self.screen.fill (R, G, B)
        #redraw the screen during each pass of 'event' loop
        # .fill() only takes one argument: a color. works on 'pygame.Surface.'s
        #NOTICE .Surface is a class inside pygame
        # .blit draws one image on another 

        for bullet in self.bullets.sprites(): # bullets.sprites returns a list of all sprites in the list of pygame.sprite.Group()
            bullet.draw_bullet() # to draw all fired bullets to screen, we loop through all sprites in Group(line46)
        
        self.ship.blitme() # after background is filled, we draw the ship on the screen using method .blitme() of module class Ship
        self.aliens.draw(self.screen) # this is responsible for drawing the aliens method on the screen.
        self.sb.show_score() #Draw the score information
        if not self.game_active:
            self.play_button.draw_button() # to make the play button visible above all other elements we draw the element after all other ones have been drawn
        self._redraw_alien()
        pygame.display.flip()
        # pygame.display.flip makes the most recently drawn screen visible, this constantly replaces the older screen and updates in-game elements (like pygame.event.get())
        #this creates an illusion of smooth movement
    def _check_events(self): # MADE FOURTH
        '''respont to key presses and mouse events'''        
            # a 'event' of pygame.event is an action that the user does like a key-press or mouse movement
            # for our program to respond to events, we write an 'event' loop to listen for events and perform appropriate tasks
            # watch for keyboard and mouse movements AKA event loop
            # pygame.event.get() function returns a list of all events taken place since the last function call
            # any keyboard/mouse event will make this
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                sys.exit()
                # the above 2 lines quit the game window
            elif event.type == pygame.KEYDOWN: #  whenever pygame detects a KEYDOWN event ->
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN: #1 py detects a buttondown event anytime mouse is clicked->
                mouse_pos = pygame.mouse.get_pos() #-> we only want it to effect when the play button is clicked, hence we are gettings the position of the mouse using .get_pos(tuple)
                self._check_play_button(mouse_pos)
        # each keypress is registered as a 'KEYDOWN' event 
        # right arrow key should increase ships.rect() positively in the x- plane

    def _check_play_button(self, mous_pos):
        '''start a new game when the player clicks Play'''
        button_clicked = self.play_button.rect.collidepoint(mous_pos) # this = __> checks whether the point of the mouse click overlaps with Button.rect
        if button_clicked and not self.game_active:
            #reset game stats
            self.stats.reset_stats()
            self.sb.prep_score()
            self.sb.prep_level()#to show which level the game starts at
            self.sb.prep_ship() #to show how many ships the player starts with
            self.settings.initialize_dynamic_settings()
            self.game_active = True

            #get rid of any aliens and bullets
            self.aliens.empty()
            self.bullets.empty()

            #create a new fleet and center ship
            self._create_fleet()
            self.ship.center_ship()

            #hide the cursor 
            pygame.mouse.set_visible(False) #tells py to hide cursor.

    def _check_keydown_events(self, event): #MADE SIXTH
        '''check for any key presses'''
        if event.key == pygame.K_d: #-> we will check if the key is the D key ->
            self.ship.moving_right = True #-> if it was the D key it will move the ship to the right
        if event.key == pygame.K_a:
            self.ship.moving_left = True  
        if event.key == pygame.K_w:
            self.ship.moving_up = True
        if event.key == pygame.K_s:
            self.ship.moving_down = True
        if event.key == pygame.K_ESCAPE:
            sys.exit()
        if event.key == pygame.K_SPACE:
            self._fire_bullet() 
        if event.key == pygame.K_m:
            self.game_active = False
            pygame.mouse.set_visible(True)

    def _check_keyup_events(self, event): #MADE SEVENTH
        '''check for any key release'''
        if event.key == pygame.K_d:
            self.ship.moving_right = False        
        if event.key == pygame.K_a:
            self.ship.moving_left = False 
        if event.key == pygame.K_w:   
            self.ship.moving_up = False     
        if event.key == pygame.K_s:
            self.ship.moving_down = False
    
    def _fire_bullet(self):
        '''create a new bullet and add it to the bullet group ('pygame.sprite.Group()')'''
        if len(self.bullets) < self.settings.bullets_allowed: # the corresponding bullets_allowed is mentioned in settings. this limits the amount of shots we can fire
            new_bullet = Bullet(self) # this is a new instance of class bullet
            self.bullets.add(new_bullet) #  .add is similar to .append but .add is used specifically for pygame

if __name__ == '__main__':
    # this 'if' block only runs the game if the file is called directly Alien_invasion.py
    #make a game instance and run the game
    ai = AlienInvasion()
    ai.run_game()