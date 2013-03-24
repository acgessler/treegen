
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


    def get_geometry(self, quad_count = 16, gen_normals = True):
        """
        Generates quadrangular geometry (i.e. a list of quads) for the trunk.

        Parameters:
            
            quad_count
                Initial number of quads per full circle

            gen_normals
                Generate normal vectors?

        Returns:
            List of (o1,o2,o3,o4) where oN is a tuple containing
            vertex position, normals, UV coordinates (if requested)
            in this order.
            
        """
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
            forward *= circumf * 0.5

            angle = math.pi * 2.0 / quad_count
            rotater = LOrientationf()
            rotater.setFromAxisAngleRad(angle, up)

            temp_quads = []
            for i in xrange(quad_count):

                # vertex positions
                t1 = v1 + forward
                t2 = v2 + forward
                forward = rotater.xform(forward) 
                t3 = v1 + forward * self.thickness_decay
                t4 = v2 + forward * self.thickness_decay

                if gen_normals:
                    # approximate quad normal vector
                    n = (forward + forward * self.thickness_decay) * 0.5
                    temp_quads.append(([t1,n],[t3,n],[t4,n],[t2,n]))
                else:
                    temp_quads.append(([t1],[t2],[t3],[t4]))

            if gen_normals:
                # now generate smooth per-vertex normals by averaging out
                # adjacent quads
                for i in xrange(len(temp_quads)):
                    n1 = temp_quads[i][0][1] + temp_quads[(i-1) % len(temp_quads)][0][1]
                    n1.normalize()

                    n2 = temp_quads[i][0][1] + temp_quads[(i+1) % len(temp_quads)][0][1]
                    n2.normalize()

                    o1,o2,o3,o4 = temp_quads[i]
                    quads.append(((o1[0],n1),(o2[0],n1),(o3[0],n2),(o4[0],n2)))
            else:
                quads.extend(temp_quads)

        return quads