import pygame

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