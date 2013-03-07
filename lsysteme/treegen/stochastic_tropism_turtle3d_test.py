from direct.showbase.ShowBase import ShowBase

from direct.showbase import DirectObject
from panda3d.core import *

from direct.gui.OnscreenText import OnscreenText
from direct.showbase.ShowBase import ShowBase

from tropism_turtle3d import tropism_turtle3d
from stochastic_lsystem import stochastic_lsystem

import itertools
import math

import util

d = 10
angles = (22.5,22.5,22.5)
trop = (0.2,-0.5,0)
e = 0.0

# global vars for camera rotation 
heading = 0 
pitch = 0 

 
class TestApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        title = OnscreenText(text="bracketed, stochastic lsystem with tropism + 3D turtle paint",
                       style=1, fg=(1,1,1,1),
                       pos=(0.2,-0.95), scale = .07)

        base.setBackgroundColor(0.0, 0.0, 0.0) 
        base.disableMouse()

        vdata = GeomVertexData('name', GeomVertexFormat.getV3(), Geom.UHStatic)

        ls = stochastic_lsystem([
            ('A',   r'[&FL!A]/////[&FL!A]///////[&FL!A]',               1),
            ('F',   r'S/////F',                                         1),
            ('S',   r'F L',                                             1),
            ('L',   r'[^^-f+f+f-|-f+f+f]',                              1)], 
        'A' )

        turtle = tropism_turtle3d(d,angles,trop,e)
        evaluated = ls.evaluate(6)
        #print evaluated
        lines = turtle.get_3d_lines(evaluated,(0,-2,0), start_forward=(0,0,1), start_right=(1,0,0)) 
        #print lines

        # center
        vmin, vmax = util.find_aabb(itertools.chain(*lines))   
        center = (vmin+vmax)*0.5    

        vertex = GeomVertexWriter(vdata, 'vertex')
        for v1,v2 in lines:          
            vertex.addData3f(v1 - center)
            vertex.addData3f(v2 - center)

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

        # orbit camera code taken from
        # http://www.panda3d.org/forums/viewtopic.php?t=9292

        # hide mouse cursor, comment these 3 lines to see the cursor 
        props = WindowProperties() 
        props.setCursorHidden(True) 
        base.win.requestProperties(props) 

        # dummy node for camera, we will rotate the dummy node fro camera rotation 
        parentnode = render.attachNewNode('camparent') 
        parentnode.reparentTo(nodePath) # inherit transforms 
        parentnode.setEffect(CompassEffect.make(render)) # NOT inherit rotation 

        # the camera 
        base.camera.reparentTo(parentnode) 
        base.camera.lookAt(parentnode) 
        base.camera.setY(-30) # camera distance from model 

        # camera zooming 
        base.accept('wheel_up', lambda : base.camera.setY(base.camera.getY()+200 * globalClock.getDt())) 
        base.accept('wheel_down', lambda : base.camera.setY(base.camera.getY()-200 * globalClock.getDt())) 

        # camera rotation task 
        def thirdPersonCameraTask(task): 
           global heading 
           global pitch 
    
           md = base.win.getPointer(0) 
      
           x = md.getX() 
           y = md.getY() 
    
           if base.win.movePointer(0, 300, 300): 
              heading = heading - (x - 300) * 0.5 
              pitch = pitch - (y - 300) * 0.5 
    
           parentnode.setHpr(heading, pitch,0) 
           return task.cont 

        taskMgr.add(thirdPersonCameraTask, 'thirdPersonCameraTask')      

        # set dummy material
        myMaterial = Material()
        myMaterial.setShininess(5.0) 
        myMaterial.setAmbient(VBase4(0,1,0,1)) 
        myMaterial.setDiffuse(VBase4(0.2,1,0.5,1))
        nodePath.setMaterial(myMaterial)
        nodePath.setTwoSided(True)

        nodePath.setDepthTest(False)

if __name__ == '__main__':
    app = TestApp()
    app.run()
