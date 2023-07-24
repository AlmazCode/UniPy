import UniPy as up

"""
A complete sound player with stop, pause and play sound.

author: almazcode; #discord
"""

class sound:
    def __init__(self):
        
        # Variables that can be edited from the inspector
        self.sound = up.PATH()  # Sound file path
        self.playAtStart = False  # Flag indicating if the sound should play automatically at start
        self.volume = 100  # Sound volume (percentage)
        self.replay = False  # Flag indicating if the sound should replay
        
        self._paused = False  # Flag indicating if the sound is paused
        self._channel = None  # Sound channel
        self._played = False  # Flag indicating if the sound has been played
    
    def SetVolume(self, volume: int):
        """
        Set the sound volume.
        
        Args:
            volume (int): Volume level (0-100).
        """
        self.volume = volume
        self.sound.set_volume(self.volume / 100)
    
    def play(self):
        """
        Play the sound.
        """
        if not self._paused and not self._played:
            self._channel = self.sound.play(0 if not self.replay else -1)
            self._played = True
        elif self._paused:
            self._channel.unpause()
            self._paused = False
    
    def stop(self):
        """
        Stop the sound.
        """
        self._channel.stop()
        self._paused = False
        self._played = False
    
    def pause(self):
        """
        Pause the sound.
        """
        self._channel.pause()
        self._paused = True
        
    def Start(self):
        """
        Start the sound player.
        """
        self.SetVolume(self.volume)
        if self.playAtStart:
            self.play()