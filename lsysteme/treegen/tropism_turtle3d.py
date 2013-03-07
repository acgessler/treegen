import math
from panda3d.core import *


class tropism_turtle3d:
    """
    3d bracketed tropism turtle with the following commands:

    +,-     Yaw
    &,^     Pitch
    \/      Roll
    |       Flip (yaw by 180deg)

    F       Move forward
    """

    def __init__(self, d, angles, trop, e):
        """
        Parameters:

        angles
            Angles for roll, pitch and yaw operations as a
            (phi, theta, psi) 3-tuple. Angles are given in
            degrees.

        d  
            Move distance for F

        trop
            3-tuple of the (x,y,z) tropism vector,
            this vector will be normalized
            before use.

        e
            Intensity coefficient of the tropism
            effect. 0 disables it altogether,
            higher values mean stronger influence
            of the tropism vector on turtle movements.
        """
        self.d = d
        self.angles = angles
        assert(len(self.angles) == 3)
   
        self.trop = Vec3(*trop) \
            if not isinstance(trop, Vec3) else trop
        self.trop.normalize()
        self.e = e


    def get_3d_lines(self, program, start = (0,0,0), start_forward = (0,1,0), start_right= (1,0,0)):
        """ 
        Get a list of (x1,y1,x2,y2) line segments for a given
        turtle program.

        Parameters:

        program
            Program text to be interpreted

        [start]
            (x,y,z) tuple as starting position 

        [start_forward]
            (x,y,z) tuple as starting forward (z) axis

        [start_right]
            (x,y,z) tuple as starting right (x) axis

        Exceptions:
            str - For unknown input commands
        """

        # obtain a quaternion representation of the initial turtle orientation
        start = Point3(*start) \
            if not isinstance(start, Point3) else start

        start_forward = Vec3(*start_forward) \
            if not isinstance(start, Vec3) else start_forward
     
        start_right = Vec3(*start_right) \
            if not isinstance(start, Vec3) else start_right

        start_up = -start_forward.cross(start_right)

        all_nonzero = start_forward.normalize() and start_up.normalize() and start_right.normalize()
        assert all_nonzero

        orient = Mat3()
        orient.setRow(0, start_right)
        orient.setRow(1, start_up)
        orient.setRow(2, start_forward)

        quat = LOrientationf(orient)
        output = [] # of (Vec3, Vec3)

        # interpret the program, collecting lines in [output]
        total = self._rec_eval(program, 0, start, quat, output)
        assert(total == len(program))

        return output


    def _rec_eval(self, program, cursor, start, quat, output):
        lstart = Point3(start)
        lquat = LOrientationf(quat)
        lquat.normalize() # normalize the quat each time to prevent numerical errors

        n = cursor
        processed = 0
        while n < len(program):
            processed += 1
            c = program[n]
            if c == 'F' or c == 'f':          
                newPoint = self._compute_next(lstart, lquat, c=='f') 
                output.append((lstart,newPoint))
                lstart = newPoint
            elif c == '-':
                lquat *= LRotationf(Vec3(0,1,0),-self.angles[2])
            elif c == '+':
                lquat *= LRotationf(Vec3(0,1,0),self.angles[2])
            elif c == '\\':
                lquat *= LRotationf(Vec3(0,0,1), self.angles[0])
            elif c == '/':
                lquat *= LRotationf(Vec3(0,0,1),-self.angles[0])
            elif c == '&':
                lquat *= LRotationf(Vec3(1,0,0),self.angles[1])
            elif c == '^':
                lquat *= LRotationf(Vec3(1,0,0),-self.angles[1])
            elif c == '|':
                lquat *= LRotationf(Vec3(0,1,0),180)
            elif c == '[':
                cnt = self._rec_eval(program, n + 1, lstart, lquat, output) 
                n += cnt
                processed += cnt
            elif c == ']':
                break
            #else:
                #raise ("unknown turtle command: " + c)
                #continue
                #break
            n += 1

        return processed


    def _compute_next(self, lstart, lquat, small):
        dir = lquat.getUp() + self.trop * self.e
        dir.normalize()
        return lstart + dir * self.d * (0.1 if small else 1.0)
        
   


