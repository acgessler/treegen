import math

class bracketed_turtle2d:
    """
    Interpreter for the turtle drawing language with the following
    commands:

    [   Push stack
    ]   Pop stack
    -   Rotate to the left 
    +   Rotate to the right 
    F   Move forward
    """

    def __init__(self, d, phi):
        """
        Parameters:

        phi  
            Rotation angle for +,- (radians)
        d  
            Move distance for F
        """
        self.d = d
        self.phi = phi


    def get_2d_lines(self, program, start = (0,0,0)):
        """ 
        Get a list of (x1,y1,x2,y2) line segments for a given
        turtle program.

        Parameters:

        program
            Program text to be interpreted

        [start]
            (x,y,theta) tuple as starting position (theta in radians)

        Exceptions:
            str - For unknown input commands
        """

        output = [] # of (x1,y1,x2,y2)
        total = self._rec_eval(program, 0, start, output)

        assert(total == len(program))

        return output


    def _rec_eval(self, program, cursor, start, output):
        x,y,theta = start

        n = cursor
        processed = 0
        while n < len(program):
            processed += 1
            c = program[n]
            if c == 'F':          
                xs = x + self.d * math.cos(theta)
                ys = y + self.d * math.sin(theta)
                output.append((x,y,xs,ys))
                x = xs
                y = ys
            elif c == '-':
                theta -= self.phi
            elif c == '+':
                theta += self.phi
            elif c == '[':
                d = self._rec_eval(program, n + 1, [x,y,theta], output) 
                n += d
                processed += d
            elif c == ']':
                break
            else:
                raise ("unknown turtle command: " + c)
            n += 1

        return processed


