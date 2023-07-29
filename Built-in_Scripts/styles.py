import UniPy as up

"""
Simple text styling module.

author: almazcode; #discord
"""

class styles:
    def __init__(self):
        self.bold = False
        self.italic = False
        self.underline = False
    
    def restyle(self):
        self.this.font.set_bold(self.bold)
        self.this.font.set_italic(self.italic)
        self.this.font.set_underline(self.underline)
        self.this.compileText()
    
    def Start(self):
        self.restyle()