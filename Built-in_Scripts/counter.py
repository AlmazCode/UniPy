import UniPy as up

"""
A simple animation of a smooth transition from one number to another.
author: almazcode; #discord
"""

class counter:
    def __init__(self):
        """
        Initializes the counter object with default values.

        Attributes:
            thisNum (float): Current number in the transition.
            speed (float): Speed of the transition animation.
            _started (bool): Flag indicating if the animation has started.
            factor (float): Factor by which the current number is multiplied during each update.
        """
        self.thisNum = None
        self.speed = 1.0
        self._started = False
        self.factor = 1.001
    
    def run(self, start=0, end=100, *args):
        """
        Starts a smooth transition animation between two numbers.

        Args:
            start (float): Starting number for the transition.
            end (float): Ending number for the transition.
            *args: Additional arguments.

        Sets the animation parameters and starts the animation.
        """
        self.end = end
        self.thisNum = start
        self._started = True
        self.this.text = str(self.thisNum)
    
    def Start(self):
        """
        Alias for the 'run' method with default arguments.
        """
        self.run()
    
    def Update(self):
        """
        Updates the animation frame.

        Updates the current number based on the animation parameters,
        and stops the animation if the target number is reached.
        """
        if self._started:
            self.thisNum = up.Math.lerp(self.thisNum, self.end, self.speed * up.deltaTime) * self.factor
            if self.thisNum >= self.end:
                self.thisNum = self.end
                self._started = False
            self.this.text = str(int(self.thisNum))