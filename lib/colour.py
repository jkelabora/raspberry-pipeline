class Colour:

  def __init__(self, r=0.0, g=0.0, b=0.0, bright=1.0):
    if(r > 255.0 or r < 0.0 or g > 255.0 or g < 0.0 or b > 255.0 or b < 0.0):
      raise ValueError('RGB values must be between 0 and 255')
    if(bright > 1.0 or bright < 0.0):
      raise ValueError('Brightness must be between 0.0 and 1.0')
    self.R = r * bright
    self.G = g * bright
    self.B = b * bright

  def __str__( self ):
    return "%d,%d,%d" % (self.R, self.G, self.B)
