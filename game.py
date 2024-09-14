
import pygame
from paddle import Paddle
from ball import Ball

class Game:
   # An object in this class represents a complete game.

   def __init__(self, surface):
      # Initialize a Game.
      # - self is the Game to initialize
      # - surface is the display window surface object

      # === objects that are part of every game that we will discuss
      self.surface = surface
      self.bg_color = pygame.Color('black')
      
      # === control the flow of the game
      self.FPS = 60
      self.game_Clock = pygame.time.Clock()
      self.close_clicked = False
     
      self.continue_game = True # use to see if any player has won
      
      # === game specific objects
      self.paddle_increment = 10
      self.paddle_left = Paddle(100,150,10,50,'blue',self.surface)
      self.paddle_right = Paddle(400,150,10,50,'white',self.surface)
      self.ball = Ball(self.surface,'magenta', [50,50], 5, [7,7])
      self.right_score = 0
      self.left_score = 0      
                    
   def play(self):
      # Play the game until the player presses the close box.
      # - self is the Game that should be continued or not.

      while not self.close_clicked:  # until player clicks close box
         # play frame
         self.handle_events() # handle user inputs
         self.draw()           # draws objects in the game
         if self.continue_game:
            self.update()       # move the objects of the game
            self.decide_continue()  # check if any player has won
         self.game_Clock.tick(self.FPS) # run at most with FPS Frames Per Second 

   def handle_events(self):
      # Handle each user event by changing the game state appropriately.
      # - self is the Game whose events will be handled

      events = pygame.event.get() # returns a list of events
      for event in events:
         if event.type == pygame.QUIT:      # player closes the window
            self.close_clicked = True
         elif event.type == pygame.KEYDOWN: # player presses a key
            self.handle_key_down(event)
         elif event.type == pygame.KEYUP: # player releases a key
            self.handle_key_up(event)
            
   def handle_key_down(self,event):
      # reponds to KEYDOWN event
      # - self is the Game object
      if event.key == pygame.K_q: # move left paddle up
         self.paddle_left.set_vertical_velocity(-self.paddle_increment)
      elif event.key == pygame.K_a : # move left paddle down
         self.paddle_left.set_vertical_velocity(self.paddle_increment)
      elif event.key == pygame.K_p: # move right paddle up
         self.paddle_right.set_vertical_velocity(-self.paddle_increment)
      elif event.key == pygame.K_l: # move right paddle down
         self.paddle_right.set_vertical_velocity(self.paddle_increment)      
   
      
   
   def handle_key_up(self,event):
      # responds to KEYUP event
      # - self is the Game object
      if event.key == pygame.K_q and self.paddle_left.get_vertical_velocity() < 0: # left paddle: stop if up
         self.paddle_left.set_vertical_velocity(0)
      elif event.key == pygame.K_a and self.paddle_left.get_vertical_velocity() > 0: # left paddle: stop if down
         self.paddle_left.set_vertical_velocity(0)
      elif event.key == pygame.K_p and self.paddle_right.get_vertical_velocity() < 0: # right paddle: stop if up 
         self.paddle_right.set_vertical_velocity(0)
      elif event.key == pygame.K_l and self.paddle_right.get_vertical_velocity() > 0: # right paddle: stop if down
         self.paddle_right.set_vertical_velocity(0)    
         
   def draw_score(self):
      # calls the left and write draw score methods
      self.draw_left_score()
      self.draw_right_score()
      
   def draw_left_score(self):
      # draws the left score
      # step 1: create font object
      font = pygame.font.SysFont('',70)
      # render the font to create a text image
      text_image = font.render(str(self.left_score),True,pygame.Color('white'),self.bg_color)
      # compute the location
      location = (0,0)
      # blit the text_image
      self.surface.blit(text_image,location)
      
   def draw_right_score(self):
      # draws the right score
      # step 1: create font object
      font = pygame.font.SysFont('',70)
      # render the font to create a text image
      text_image = font.render(str(self.right_score),True,pygame.Color('white'),self.bg_color)
      # compute the location
      location = (self.surface.get_width() - text_image.get_width(),0)
      # blit the text_image
      self.surface.blit(text_image,location)   

   def draw(self):
      # Draw all game objects.
      # - self is the Game to draw
      
      self.surface.fill(self.bg_color) # clear the display surface first
      self.paddle_left.draw() # draws the left paddle
      self.paddle_right.draw() # draws the right paddle
      self.ball.draw() # draws the ball
      self.draw_score() # calls the draw score method which draws both scores
      
     
      pygame.display.update() # make the updated surface appear on the display
      
   
   def update(self):
      # Update the game objects for the next frame.
      # - self is the Game to update
      self.paddle_left.move() # moves the left paddle
      self.paddle_right.move() # moves the right paddle
      self.ball.move(self.paddle_left,self.paddle_right) # moves the ball with the right and left paddle passed in to access their properties
      
      if self.ball.touching_left():
         # increase the right score when the ball touches the left edge
         self.right_score = self.right_score + 1
         
      elif self.ball.touching_right():
          # increase the left score when the ball touches the right edge
         self.left_score = self.left_score + 1
         
         
   def decide_continue(self): 
      # checkes game over conditions
      # Check and remember if the game should continue
      # - self is the Game to check
      # game over conditions
      if self.right_score == 11 or self.left_score == 11:
         self.continue_game = False
      else:
         self.continue_game = True