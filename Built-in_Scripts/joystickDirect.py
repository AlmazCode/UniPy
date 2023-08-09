import math
import UniPy as up

"""
Simple and convenient graphic joystick.

author: almazcode; #discord
"""

class joystickDirect:
    def __init__(self):
        self.handlerBg = ""
        self.player = ""
        
        self._ih1p = False  # Flag indicating if the joystick is pressed
        self.zone = 100  # Area to which the joystick can be moved
        self.speed = 5
        
        self.moveX = True
        self.moveY = True
        self.rotate = False

    def Start(self):
        """
        Initialize the joystick.
        """
        self.handlerBg = up.GetObj(self.handlerBg)
        self.player = up.GetObj(self.player)
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
            
            if self.moveX:
                if normalized_dx > 0.3:
                    self.player.angle = -90
                    self.player.rect.x += self.speed
                    return
                elif normalized_dx < -0.3:
                    self.player.angle = 90
                    self.player.rect.x -= self.speed
                    return
            if self.moveY:
                if normalized_dy > 0.3:
                    self.player.angle = -180
                    self.player.flipX = False
                    self.player.rect.y += self.speed
                elif normalized_dy < -0.3:
                    self.player.angle = 0
                    self.player.rect.y -= self.speed