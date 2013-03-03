from direct.showbase.ShowBase import ShowBase


from direct.showbase import DirectObject
from panda3d.core import *

from direct.gui.OnscreenText import OnscreenText
from direct.showbase.ShowBase import ShowBase

from bracketed_turtle2d import bracketed_turtle2d
from bracketed_lsystem import bracketed_lsystem

import math

d = 0.15
phi = math.radians(25)
 
class TestApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        title = OnscreenText(text="bracketed_lsystem w/ 2d turtle paint",
                       style=1, fg=(1,1,1,1),
                       pos=(0.6,-0.95), scale = .07)

        base.setBackgroundColor(0.0, 0.0, 0.0) 
        base.disableMouse()
        camera.setPos(0.0, 0.0, 20.0) 
        camera.setHpr(0.0, -90.0, 0.0) 

        vdata = GeomVertexData('name', GeomVertexFormat.getV3(), Geom.UHStatic)


        ls = bracketed_lsystem( { 'F': 'FF-[-F+F+F]+[+F-F-F]'},'F')
        turtle = bracketed_turtle2d(d,phi)
        lines = turtle.get_2d_lines(ls.evaluate(4),(-1,-4,math.radians(90)))

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











