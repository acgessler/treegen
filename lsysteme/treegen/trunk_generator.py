



class trunk_generator:
    """ 
    Generates geometry for a tree trunk, given a list of trunk segments.
    """

    def __init__(self, segments):
        """ 
        Initialize from a list of trunk segments. Use `get_geometry()`
        to actually generate trunk geometry.

        Parameters:

            segments
                List of (Vec3 start, Vec3 end, int branching_level) segments
                branching_level is 0 for the stem, 1 for first-level branches,
                2 for second-level branches and so on.

        """
        self.segments = segments



    def get_geometry

