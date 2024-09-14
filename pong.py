# Pong: A game where two player use their paddle to hit a ball into their opponents
#       edge for a point. The first player to reach 11 points wins.
import pygame,random

# User-defined functions

def main():
   # initialize all pygame modules (some need initialization)
   pygame.init()
   # create a pygame display window
   pygame.display.set_mode((500, 400))
   # set the title of the display window
   pygame.display.set_caption('Pong')   
   # get the display surface
   w_surface = pygame.display.get_surface() 
   # create a game object
   game = Game(w_surface)
   # start the main game loop by calling the play method on the game object
   game.play() 
   # quit pygame and clean up the pygame window
   pygame.quit() 
   


# User-defined classes

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
     
   
class Paddle:
   # An object in this class represents a Paddle that moves
   
   def __init__(self,x,y,width,height,color,surface):
      # - self is the Paddle object
      # - x, y are the top left corner coordinates of the rectangle of type int
      # - width is the width of the rectangle of type int
      # - height is the heightof the rectangle of type int
      # - surface is the pygame.Surface object on which the rectangle is drawn

      # == for drawing
      self.rect = pygame.Rect(x,y,width,height)
      self.color = pygame.Color(color)
      self.surface = surface
      
      # == for motion
      self.vertical_velocity = 0  # paddle is not moving at the start
      
      
   def draw(self):
      # -self is the Paddle object to draw
      pygame.draw.rect(self.surface,self.color,self.rect)
      
   def set_vertical_velocity(self,vertical_distance):
      # set the horizontal velocity of the Paddle object
      # -self is the Paddle object
      # -vertical_distance is the int increment by which the paddle moves vertically
      self.vertical_velocity = vertical_distance
      
   def move(self):
      # moves the paddle such that paddle does not move outside the window
      # - self is the Paddle object
      self.rect.move_ip(0,self.vertical_velocity) # move in place
   
      
      if self.rect.bottom >= self.surface.get_height(): # hits bottome edge
         self.rect.bottom = self.surface.get_height() # setting the bottom of the paddle to the height of the window
      
      elif self.rect.top  <= 0: # hits bottome edge
         self.rect.top = 0 # setting the top of the paddle to 0
   
  
   def get_vertical_velocity(self):
      # return the velocity of the paddle
      return self.vertical_velocity  
   
  
   
class Ball:
   
   def __init__(self, surface, color, center, radius, velocity):
      #  - surface: pygame surface object
      #  - color: tuple with three ints
      #  - center: list with two number; [x,y]
      #  - radius: a number
      #  - velocity: a list with two numbers; (x,y) velocity
      
      # == for drawing
      self.surface = surface
      self.color = color
      self.center = center
      self.radius = radius
      
      # == for motion
      self.velocity = velocity

   def draw(self):
      # need the self argument to access ball attributes
      pygame.draw.circle(self.surface, self.color, self.center, self.radius)
      
   def move(self,paddle_right,paddle_left):
      # -moves the ball so it doesn't leave the window and changing its 
      #  velocity once it hits the paddles
      # -self is the Ball object
      # -paddle_right and paddle_left are Paddle objects 
      
      # initializing the center to its center value plus its velocity to update its position in the window
      self.center[0] = self.center[0] + self.velocity[0]
      self.center[1] = self.center[1] + self.velocity[1]      
         
      # checks if the ball hits the top of the window
      if self.center[1] + self.radius > self.surface.get_height():
         self.velocity[1] = -self.velocity[1] 
      # checks if the ball hits the bottom of the window  
      if self.center[1] < self.radius:
         self.velocity[1] = -self.velocity[1]      
      # checks if the ball hits the right edge of the window
      if self.center[0] + self.radius > self.surface.get_width():
         self.velocity[0] = -self.velocity[0]
      # checks if the ball hits the left edge of the window
      if self.center[0] < self.radius:
         self.velocity[0] = -self.velocity[0]
         
     
      # checks if the paddle has collided with the center of the ball and reverses the horizantal
      # velocity if it does
      if paddle_right.rect.collidepoint(self.center[0],self.center[1]) and self.velocity[0] < 0:
            self.velocity[0] = -self.velocity[0]
         
      if paddle_left.rect.collidepoint(self.center[0],self.center[1]) and self.velocity[0] > 0:
         self.velocity[0] = -self.velocity[0]      
 
   
   def touching_left(self):
      # returns True if the ball has touched the left edge of the window
      return self.center[0] < self.radius
   
   def touching_right(self):
      # returns True if the ball has touched the right edge of the window
      return self.center[0] + self.radius > self.surface.get_width()
   
 

main()

