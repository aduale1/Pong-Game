import pygame

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
   