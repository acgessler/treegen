
import math
from panda3d.core import *

class trunk_generator:
    """ 
    Generates geometry for a tree trunk, given a list of trunk segments.
    """

    def __init__(self, segments, thickness = 0.2, thickness_decay = 0.9):
        """ 
        Initialize from a list of trunk segments. Use `get_geometry()`
        to actually generate trunk geometry.

        Parameters:

            segments
                List of (Vec3 start, Vec3 end, int branching_level) segments
                branching_level is 0 for the stem, 1 for first-level branches,
                2 for second-level branches and so on.

            thickness
                Initial stem thickness

            thickness_decay
                Exponential thickness decay factor

        """
        self.segments = segments
        self.thickness = thickness
        self.thickness_decay = thickness_decay


    def get_geometry(self, quad_count = 16):
        quads = []
        for v1, v2, nesting_level in self.segments:
            circumf = self.thickness * math.pow(self.thickness_decay, nesting_level)

            # find a 2D coordinate system orthogonal to v1->v2
            up = v2-v1

            right = Vec3(1,0,0)
            if abs(right.dot(up)) < 1e-6:
                right = Vec3(0,1,0)
    
            up.normalize()

            forward = up.cross(right)
            right = forward.cross(up)

            forward.normalize()
            forward *= circumf

            angle = math.pi * 2.0 / quad_count
            rotater = LOrientationf()
            rotater.setFromAxisAngleRad(angle, up)
            for i in xrange(quad_count):
                t1 = v1 + forward
                t2 = v2 + forward
                forward = rotater.xform(forward) 
                t3 = v1 + forward * self.thickness_decay
                t4 = v2 + forward * self.thickness_decay
                quads.append((t1,t3,t4,t2))
        return quads