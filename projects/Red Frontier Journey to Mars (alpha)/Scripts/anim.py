import UniPy as up

# Class to animate text typing

class anim:
    def __init__(self):
        self.speed = 3
        self.bg = up.OBJ()
        self._thisFrame = 0
        self._thisText = ""
        self.__TEXT = ""
        self._end = True
        self._delBS = False
    
    def Restart(self):
        self.__TEXT = self.this.text
        self._thisText = ""
        self.this.text = ""
        self._end = False
        self._delBS = False
        self._thisFrame = 0
    
    def Update(self):
        if not self._end:
            self._thisFrame += 1
            if self._thisFrame == self.speed:
                self._thisText += self.__TEXT[len(self._thisText)]
                if self.__TEXT[len(self._thisText)-1] == "\\" and self.__TEXT[len(self._thisText)] in ["n", "t"]:
                    self._delBS = True
                else:
                    self._delBS = False
                self._thisFrame = 0
                self.this.text = self._thisText if not self._delBS else self._thisText[::-1].replace("\\", "", 1)[::-1]
                self.bg.height = self.this.height + 10
                self.bg.setPos()
                if self._thisText == self.__TEXT:
                    self._end = True