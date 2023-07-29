import math
import UniPy as up

"""
Simple and convenient graphic joystick.

author: almazcode; #discord
"""

class joystick:
    def __init__(self):
        self.handlerBg = up.OBJ()  # Background object for the joystick handler
        self.player = up.OBJ()  # Object to be controlled by the joystick
        
        self._ih1p = False  # Flag indicating if the joystick is pressed
        self.zone = 100  # Area to which the joystick can be moved
        self.speed = 5  # Speed of the controlled object
        self.moveX = True
        self.moveY = True
        self.flipX = True
        self.flipY = False
        self.rotate = False

    def Start(self):
        """
        Initialize the joystick.
        """
        self.this.rect.center = self.handlerBg.rect.center
        self.this.onPressed = self.h1p
        self.this.onUnPressed = self.h1p
    
    def h1p(self):
        """
        Toggle the state of `ih1p` flag.
        """
        self._ih1p = not self._ih1p
        
        if not self._ih1p:
            self.this.rect.center = self.handlerBg.rect.center
    
    def Update(self):
        """
        Update the joystick and control the object.
        """
        if self._ih1p:
            self.this.rect.center = up.fingersPos[self.this.finger_id]
            if self.this.rect.centerx - self.zone > self.handlerBg.rect.centerx:
                self.this.rect.centerx = self.handlerBg.rect.centerx + self.zone
            elif self.this.rect.centerx + self.zone < self.handlerBg.rect.centerx:
                self.this.rect.centerx = self.handlerBg.rect.centerx - self.zone
        
            if self.this.rect.centery - self.zone > self.handlerBg.rect.centery:
                self.this.rect.centery = self.handlerBg.rect.centery + self.zone
            elif self.this.rect.centery + self.zone < self.handlerBg.rect.centery:
                self.this.rect.centery = self.handlerBg.rect.centery - self.zone
        
            # Set the direction of movement of the object
            dx = self.this.rect.centerx - self.handlerBg.rect.centerx
            dy = self.this.rect.centery - self.handlerBg.rect.centery

            # Normalize the values of dx and dy in the range [-1, 1]
            max_distance = self.zone
            normalized_dx = dx / max_distance
            normalized_dy = dy / max_distance
        
            # Calculate the angle based on joystick position
            if self.rotate: self.player.angle = -math.atan2(normalized_dy, normalized_dx) * 180 / math.pi
            
            if self.flipX:
                if normalized_dx < 0:
                    self.player.flipX = True
                else:
                    self.player.flipX = False
            
            if self.flipY:
                if normalized_dy > 0:
                    self.player.flipY = True
                else:
                    self.player.flipY = False
            
            # Set the speed of the object based on normalized values
            self.player_speed_x = normalized_dx * self.speed
            self.player_speed_y = normalized_dy * self.speed

            if self.moveX: self.player.rect.x += self.player_speed_x
            if self.moveY: self.player.rect.y += self.player_speed_y