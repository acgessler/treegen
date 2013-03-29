

from panda3d.core import *

class tag(object):
    """Tag used to mark a point in the generated tree geometry.
    
    A tag has a position and an associated coordinate space (given 
    as a normalized quaternion). It can optionally have a textual name.
    """

    def __init__(self, position, orientation, name = None):
        self.__position = position
        self.__orientation = orientation
        self.__name = name

    def get_position(self):
        return self.__position

    def get_orientation(self):
        return self.__orientation

    def get_name(self):
        return self.__name


