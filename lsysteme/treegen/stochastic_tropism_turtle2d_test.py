from direct.showbase.ShowBase import ShowBase


from direct.showbase import DirectObject
from panda3d.core import *

from direct.gui.OnscreenText import OnscreenText
from direct.showbase.ShowBase import ShowBase

from tropism_turtle2d import tropism_turtle2d
from stochastic_lsystem import stochastic_lsystem

import math

d = 0.09
phi = math.radians(15)
trop = (0.2,-0.5)
e = 0.3
 
class TestApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        title = OnscreenText(text="stochastic_lsystem w/ 2d tropism turtle paint",
                       style=1, fg=(1,1,1,1),
                       pos=(0.6,-0.95), scale = .07)

        base.setBackgroundColor(0.0, 0.0, 0.0) 
        base.disableMouse()
        camera.setPos(0.0, 0.0, 20.0) 
        camera.setHpr(0.0, -90.0, 0.0) 

        vdata = GeomVertexData('name', GeomVertexFormat.getV3(), Geom.UHStatic)

        ls = stochastic_lsystem([('F','F[+F]F[-F]F',0.333),
            ('F','F[+F]F',0.333),
            ('F','F[-F]F',0.333)], 'F' )

        turtle = tropism_turtle2d(d,phi,trop,e)
        lines = turtle.get_2d_lines(ls.evaluate(5),(-3,-4,math.radians(90))) +\
            turtle.get_2d_lines(ls.evaluate(5),(-1,-4,math.radians(90))) +\
            turtle.get_2d_lines(ls.evaluate(5),(1,-4,math.radians(90))) +\
            turtle.get_2d_lines(ls.evaluate(5),(3,-4,math.radians(90)))

        vertex = GeomVertexWriter(vdata, 'vertex')
        for x1,y1,x2,y2 in lines:          
            vertex.addData3f(x1, y1, 0)
            vertex.addData3f(x2, y2, 0)

        geom = Geom(vdata)
        for i in xrange(len(lines)):
            prim = GeomLines(Geom.UHStatic)
            prim.addVertex(i*2)
            prim.addVertex(i*2+1)
            prim.closePrimitive()
            geom.addPrimitive(prim)
 
        node = GeomNode('test_tri')
        node.addGeom(geom)
     
        nodePath = render.attachNewNode(node)
        nodePath.setPos(0,0,0)
       
        myMaterial = Material()
        myMaterial.setShininess(5.0) 
        myMaterial.setAmbient(VBase4(0,1,0,1)) 
        myMaterial.setDiffuse(VBase4(1,1,1,1))
        nodePath.setMaterial(myMaterial)
        nodePath.setTwoSided(True)

        nodePath.setDepthTest(False)

if __name__ == '__main__':

    

    app = TestApp()
    app.run()











