
class tree_skeleton(object):
    """Describes the tree skeleton obtained by running a tropism_turtle3d 
    on a evaluated lsystem grammar.
     
    A tree skeleton is given as as set of lines to form the tree hierarchy,
    a list of attachment tags and a list of polygons. In addition there should be
    spatial adjacency information for all of these (TODO).
    """

    def __init__(self, segments, polygons, tags):
        self.__segments = segments
        self.__polygons = polygons
        self.__tags = tags

    def get_segments(self):
        """([(Vec3 start,Vec3 end, int branching_level)]""" 
        return self.__segments

    def get_polygons(self):
        """[(Vec3 vertex)]"""
        return self.__polygons

    def get_tags(self):
        """[Tag]"""
        return self.__tags


