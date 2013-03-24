
# p3d
from direct.showbase.ShowBase import ShowBase
from direct.showbase import DirectObject
from panda3d.core import *

from direct.gui.OnscreenText import OnscreenText
from direct.showbase.ShowBase import ShowBase
from direct.filter.CommonFilters import CommonFilters

# pystd
import itertools
import math

# own stuff
import util

from tropism_turtle3d import tropism_turtle3d
from stochastic_lsystem import stochastic_lsystem
from trunk_generator import trunk_generator


# lsystem + turtle parameters
d_line = 10
d_poly = 1
angles = (22.5,30.5,22.5)
trop = (0.2,0.0,0.4)
e = 0.3
iterations = 6

# d0 grammar to generate the tree
ls = stochastic_lsystem([
    ('A',   r'[&FL!A]/////[&FFL!A]///[&FL!A]',                  0.5),
    ('A',   r'[&FL!A]/////[&FL!A]//////[&FFL!A]',               0.5),
    ('F',   r'S/////F',                                         0.5),
    ('F',   r'S//F',                                            0.5),
    ('S',   r'F L',                                             0.5),
    ('S',   r'L',                                               0.5),
    ('L',   r'[^^{-f+f+f-|-f+f+f}]',                            1)], 
'A' )

# global vars for camera rotation 
heading = 0 
pitch = 0 
 
class TestApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        title = OnscreenText(text="bracketed, stochastic lsystem with tropism + 3D turtle paint",
                       style=1, fg=(1,1,1,1),
                       pos=(0.2,-0.95), scale = .07)

        base.setBackgroundColor(0x74 / 255.0, 0x9a / 255.0, 0xcb / 255.0) 
        base.disableMouse()

        turtle = tropism_turtle3d(d_line, d_poly,angles,trop,e)
        evaluated = ls.evaluate(iterations)
        #print evaluated
        lines, polygons = turtle.get_turtle_path(evaluated,(0,-2,0), start_forward=(0,0,1), start_right=(1,0,0)) 
        #print lines

        # center
        vmin, vmax = util.find_aabb(itertools.chain(*((a,b) for a,b,c in lines)))   
        center = (vmin+vmax)*0.5    

        trunk_gen = trunk_generator(lines, thickness=5, thickness_decay=0.5)
        stem_quads = trunk_gen.get_geometry()
        

        # generate geometry objects to draw the stem quads
        vdata = GeomVertexData('stem_quads', GeomVertexFormat.getV3n3(), Geom.UHStatic)     
        vertex = GeomVertexWriter(vdata, 'vertex')
        normal = GeomVertexWriter(vdata, 'normal')
        for t1,t2,t3,t4 in stem_quads:          
            vertex.addData3f(t1[0] - center)
            normal.addData3f(t1[1]) # nor
            vertex.addData3f(t2[0] - center)
            normal.addData3f(t2[1]) # nor
            vertex.addData3f(t3[0] - center)
            normal.addData3f(t3[1]) # nor
            vertex.addData3f(t4[0] - center)
            normal.addData3f(t4[1]) # nor   

        geom = Geom(vdata)
        prim = GeomTriangles(Geom.UHStatic)
        for i in xrange(len(stem_quads)):
            i4 = i*4
            prim.addVertex(i4)
            prim.addVertex(i4+1)
            prim.addVertex(i4+2)
            prim.closePrimitive()
            prim.addVertex(i4+2)
            prim.addVertex(i4+3)
            prim.addVertex(i4)
            prim.closePrimitive()
        geom.addPrimitive(prim)
        

        # generate geometry objects to draw the leaves
        # save full triangulation, for the current leaf topology a trifan is enough
        n = 0
        prim = GeomTriangles(Geom.UHStatic)
        vdata = GeomVertexData('polys', GeomVertexFormat.getV3(), Geom.UHStatic)     
        vertex = GeomVertexWriter(vdata, 'vertex')

        for poly in polygons:
            assert len(poly) >= 3
            for v in poly:
                vertex.addData3f(v - center)

        for poly in polygons:          
            for i in xrange(1, len(poly) - 1):
                prim.addVertex(n)
                prim.addVertex(n + i)
                prim.addVertex(n + i + 1)
                prim.closePrimitive()
            n += len(poly)
        
        geom_poly = Geom(vdata)
        geom_poly.addPrimitive(prim)
            
        # and attach both geometry objects to fresh scenegraph nodes
        node = GeomNode('tree_stem')
        node.addGeom(geom)
           
        node_path = render.attachNewNode(node)
        node_path.setPos(0,0,0)

        node = GeomNode('tree_leaves')
        node.addGeom(geom_poly)
        node_path_leaves = node_path.attachNewNode(node)

        # orbit camera code taken from
        # http://www.panda3d.org/forums/viewtopic.php?t=9292

        # hide mouse cursor, comment these 3 lines to see the cursor 
        props = WindowProperties() 
        props.setCursorHidden(True) 
        base.win.requestProperties(props) 

        # dummy node for camera, we will rotate the dummy node fro camera rotation 
        parentnode = render.attachNewNode('camparent') 
        parentnode.reparentTo(node_path) # inherit transforms 
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

        # set stem material
        myMaterial = Material()
        myMaterial.setShininess(5.0) 
        myMaterial.setAmbient(VBase4(0.1,0.1,0.1,1)) 
        myMaterial.setDiffuse(VBase4(0.4,0.4,0.0,1))
        node_path.setMaterial(myMaterial)
        node_path.setTwoSided(True)

        # set leaves material
        myMaterial = Material()
        myMaterial.setShininess(2.0) 
        myMaterial.setAmbient(VBase4(0.1,0.2,0.1,1)) 
        myMaterial.setDiffuse(VBase4(0.1,0.6,0.0,1))
        myMaterial.setEmission(VBase4(0.1,0.8,0.0,1))
        node_path_leaves.setMaterial(myMaterial)
        node_path_leaves.setTwoSided(True)

        dlight = DirectionalLight('my dlight')
        dlnp = render.attachNewNode(dlight)
        dlnp.setHpr(0, -60, 0)
        render.setLight(dlnp)

        
        #node_path.setShaderAuto()

        render.setShaderAuto()

        filters = CommonFilters(base.win, base.cam)
        filters.setBloom(size = "large", mintrigger = 0.5, intensity=0.4)
  
        #filters.setVolumetricLighting(caster=dlight)

        render.setAttrib(LightRampAttrib.makeHdr1())
        #render.setAntialias(AntialiasAttrib.MMultisample)
        #render.setShaderAuto(BitMask32.allOn() & ~BitMask32.bit(Shader.BitAutoShaderGlow))


if __name__ == '__main__':
    app = TestApp()
    app.run()
