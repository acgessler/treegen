
from panda3d.core import *

def vecmin(a,b):
    return Vec3(min(a.getX(),b.getX()),min(a.getY(),b.getY()),min(a.getZ(),b.getZ()))

def vecmax(a,b):
    return Vec3(max(a.getX(),b.getX()),max(a.getY(),b.getY()),max(a.getZ(),b.getZ()))


def find_aabb(iterable):
    vmin = Vec3(1e10,1e10,1e0)
    vmax = Vec3(-1e10,-1e10,-1e0)
    for v in iterable:
        vmin = vecmin(vmin,v)
        vmax = vecmax(vmax,v)
    return vmin, vmax


