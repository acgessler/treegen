from direct.showbase.ShowBase import ShowBase


from direct.showbase import DirectObject
from panda3d.core import *

from direct.gui.OnscreenText import OnscreenText
from direct.showbase.ShowBase import ShowBase

from tropism_turtle3d import tropism_turtle3d
from stochastic_lsystem import stochastic_lsystem

import math

d = 1
angles = (22,22,22)
trop = (0.2,-0.5,0)
e = 0.0
 
class TestApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        title = OnscreenText(text="stochastic_lsystem w/ 3d tropism turtle paint",
                       style=1, fg=(1,1,1,1),
                       pos=(0.6,-0.95), scale = .07)

        base.setBackgroundColor(0.0, 0.0, 0.0) 
        base.disableMouse()
        camera.setPos(0.0, 0.0, 20.0) 
        camera.setHpr(0.0, -90.0, 0.0) 

        vdata = GeomVertexData('name', GeomVertexFormat.getV3(), Geom.UHStatic)

        ls = stochastic_lsystem([
            ('A',   r'[&FLA]/////[&FLA]///////[&FLA]',              1),
            ('F',   r'S/////F',                                     1),
            ('S',   r'F',                                           1),
            ('L',   r'[F^^F][F\\\\F]',                              1)], 
        'A' )

        turtle = tropism_turtle3d(d,angles,trop,e)
        evaluated = ls.evaluate(5)
        #print evaluated
        lines = turtle.get_3d_lines(evaluated,(0,-2,0), start_forward=(0,1,0), start_right=(1,0,0)) 
        #print lines

        vertex = GeomVertexWriter(vdata, 'vertex')
        for v1,v2 in lines:          
            vertex.addData3f(v1)
            vertex.addData3f(v2)

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











