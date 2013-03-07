import math
from panda3d.core import *


class tropism_turtle3d:
    """
    3d bracketed tropism turtle with the following instruction set:

    +,-     Yaw
    &,^     Pitch
    \/      Roll
    |       Flip (yaw by 180deg)

    F       Move forward in line mode
    f       Move forward in polygon mode

    []      Branch (stack push/pop)
    {}      Start/End polygon mode

    There are two operating modes:
       line (default)
         The turtle generates 2D line segments
       polygon
         The turtle connects multiple adjacent 2D line segments
         to form a single polygon. Triangulation is left to the 
         caller.
    """

    def __init__(self, d_line, d_polygon, angles, trop, e):
        """
        Parameters:

        angles
            Angles for roll, pitch and yaw operations as a
            (phi, theta, psi) 3-tuple. Angles are given in
            degrees.

        d_line
            Move distance for F

        d_polygon
            Move distance for f

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
        self.d_line = d_line
        assert self.d_line > 0

        self.d_polygon = d_polygon
        assert self.d_polygon > 0

        self.angles = angles
        assert len(self.angles) == 3
   
        self.trop = Vec3(*trop) \
            if not isinstance(trop, Vec3) else trop
        self.trop.normalize()
        self.e = e


    def get_turtle_path(self, program, start = (0,0,0), start_forward = (0,1,0), start_right= (1,0,0)):
        """ 
        Gets the output lines and output polygons that the turtle generates 
        for a given turtle3d program text.

        Parameters:

        program
            Program text to be interpreted. See class doc for the instruction set.

        [start]
            (x,y,z) tuple as starting position 

        [start_forward]
            (x,y,z) tuple as starting forward (z) axis

        [start_right]
            (x,y,z) tuple as starting right (x) axis

        Exceptions:
            str - For unknown input commands

        Returns:
            ([(Vec3 start,Vec3 end)] output_lines, [(Vec3 vertex)] output_polygons)
        """

        # build a coordinate space based on the two given vectors
        start = Point3(*start) \
            if not isinstance(start, Point3) else start

        start_forward = Vec3(*start_forward) \
            if not isinstance(start, Vec3) else start_forward
     
        start_right = Vec3(*start_right) \
            if not isinstance(start, Vec3) else start_right
        start_up = -start_forward.cross(start_right)

        # obtain a orthonormal system
        all_nonzero = start_forward.normalize() and \
            start_up.normalize() and \
            start_right.normalize()

        assert all_nonzero

        # obtain a quaternion representation of the ONS
        orient = Mat3()
        orient.setRow(0, start_right)
        orient.setRow(1, start_up)
        orient.setRow(2, start_forward)
        quat = LOrientationf(orient)

        output_lines = [] # of (Vec3, Vec3)
        output_polygons = [] # of Vec3

        # interpret the program, collecting lines and polygons in separate lists
        total = self._rec_eval(program, 0, start, quat, output_lines, output_polygons)
        assert(total == len(program))

        return output_lines, output_polygons


    def _rec_eval(self, program, cursor, start, quat, output_lines, output_polygons):
        lstart = Point3(start)
        lquat = LOrientationf(quat)
        lquat.normalize() # normalize the quat each time to prevent numerical errors

        is_poly = False
        current_poly = []
    
        n = cursor
        processed = 0
        while n < len(program):
            processed += 1
            c = program[n]
            if c == 'F':  
                if is_poly:
                    raise "F not allowed while the turtle is in poly mode"        
                newPoint = self._compute_next(lstart, lquat, True) 
                output_lines.append((lstart,newPoint))
                lstart = newPoint
            elif c == 'f':          
                if not is_poly:
                    raise "f not allowed while the turtle is in line mode"    
                lstart = self._compute_next(lstart, lquat, False) 
                current_poly.append(lstart)
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
                if is_poly:
                    raise "[ not allowed while the turtle is in poly mode"
                cnt = self._rec_eval(program, n + 1, lstart, lquat, output_lines, output_polygons) 
                n += cnt
                processed += cnt
            elif c == ']':
                if is_poly:
                    raise "] not allowed while the turtle is in poly mode"
                break
            elif c == '{':
                if is_poly:
                    raise "nesting of { not allowed"
                is_poly = True
                current_poly = []
            elif c == '}':
                if not is_poly:
                    raise "unmatched } not allowed"
                is_poly = False

                # drop duplicate end points
                if current_poly and current_poly[-1].almostEqual(current_poly[0]):
                    current_poly = current_poly[:-1]

                # ignore anything less than a triangle
                if len(current_poly) >= 3:
                    output_polygons.append(tuple(current_poly))
                else:
                    print "ignoring degenerate polygon (line, point or empty)"

            # ignore anything else - i.e. unconsumed grammar symbols
            #else:
                #raise ("unknown turtle command: " + c)
                #continue
                #break
            n += 1

        return processed


    def _compute_next(self, lstart, lquat, line):
        dir = lquat.getUp() + self.trop * self.e
        dir.normalize()
        return lstart + dir * (self.d_line if line else self.d_polygon)
        
   


