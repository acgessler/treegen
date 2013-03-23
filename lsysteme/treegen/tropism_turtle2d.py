import math

from bracketed_turtle2d import bracketed_turtle2d

class tropism_turtle2d(bracketed_turtle2d):
    """
    Adds a tropism vector and -strength to bracketed_turtle2d to simulate
    the tropism (i.e. light-seeking) effect for plants.
    """

    def __init__(self, d, phi, trop, e):
        """
        Parameters:

        phi  
            Rotation angle for +,- (radians)
        d  
            Move distance for F

        trop
            2-tuple of the (x,y) tropism vector,
            this vector will be normalized
            before use.

        e
            Intensity coefficient of the tropism
            effect. 0 disables it altogether,
            higher values mean stronger influence
            of the tropism vector on turtle movements.
        """
        bracketed_turtle2d.__init__(self,d,phi)
   
        slen = math.sqrt(trop[0]**2+trop[1]**2)
        self.trop = (trop[0]/slen,trop[1]/slen)

        self.e = e


    def _compute_next(self, x, y, theta):
        xd = math.cos(theta) + self.trop[0] * self.e
        yd = math.sin(theta) + self.trop[1] * self.e
        mag = math.sqrt(xd**2+yd**2)

        xs = x + self.d * xd / mag
        ys = y + self.d * yd / mag
        return xs,ys


