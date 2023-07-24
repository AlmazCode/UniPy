import UniPy as up

"""
Simple typing animation.

author: almazcode; #discord
"""

class anim:
    def __init__(self):
        
        self.speed = 3  # Speed of typing animation (number of frames per character)
        self._thisFrame = 0  # Current frame count
        self._thisText = ""  # Current text being typed
        self.__TEXT = ""  # Complete text to be typed
        self._end = True  # Flag indicating if typing animation has ended
        self._delBS = False  # Flag indicating if the backslash character should be deleted
    
    def Restart(self):
        """
        Restart the typing animation.
        """
        self.__TEXT = self.this.text  # Store the original text
        self._thisText = ""  # Reset the current typed text
        self.this.text = ""  # Clear the text field
        self._end = False  # Reset the end flag
        self._delBS = False  # Reset the backslash deletion flag
        self._thisFrame = 0  # Reset the frame count
    
    def Update(self):
        """
        Update the typing animation.
        """
        if not self._end:
            self._thisFrame += 1
            if self._thisFrame == self.speed:
                self._thisText += self.__TEXT[len(self._thisText)]
                if self.__TEXT[len(self._thisText)-1] == "\\" and self.__TEXT[len(self._thisText)] == "n":
                    self._delBS = True
                else:
                    self._delBS = False
                self._thisFrame = 0
                self.this.text = self._thisText if not self._delBS else self._thisText[::-1].replace("\\", "", 1)[::-1]
                if self._thisText == self.__TEXT:
                    self._end = True