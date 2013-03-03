from direct.showbase.ShowBase import ShowBase

import direct.directbase.DirectStart
from direct.showbase import DirectObject
from panda3d.core import *

from direct.gui.OnscreenText import OnscreenText

base.setBackgroundColor(0.0, 0.0, 0.0) 
base.disableMouse()
camera.setPos(0.0, 0.0, 20.0) 
camera.setHpr(0.0, -90.0, 0.0) 

title = OnscreenText(text="Panda3D: turtle display test",
                       style=1, fg=(1,1,1,1),
                       pos=(0.6,-0.95), scale = .07)


vdata = GeomVertexData('name', GeomVertexFormat.getV3n3t2(), Geom.UHStatic)

vertex = GeomVertexWriter(vdata, 'vertex')
normal = GeomVertexWriter(vdata, 'normal')
texcoord = GeomVertexWriter(vdata, 'texcoord')

vertex.addData3f(1, 0, 0)
normal.addData3f(0, 0, 1)
texcoord.addData2f(1, 0)
 
vertex.addData3f(1, 1, 0)
normal.addData3f(0, 0, 1)
texcoord.addData2f(1, 1)
 
vertex.addData3f(0, 1, 0)
normal.addData3f(0, 0, 1)
texcoord.addData2f(0, 1)
 
vertex.addData3f(0, 0, 0)
normal.addData3f(0, 0, 1)
texcoord.addData2f(0, 0)

prim = GeomLines(Geom.UHStatic)
prim.addVertex(0)
prim.addVertex(1)
prim.closePrimitive()

prim2 = GeomLines(Geom.UHStatic)
prim2.addVertex(1)
prim2.addVertex(2)
prim2.closePrimitive()

geom = Geom(vdata)
geom.addPrimitive(prim)
geom.addPrimitive(prim2)
 
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


alight = AmbientLight('alight')
alight.setColor(Vec4(0.5, 0.5, 0.5, 1))
alnp = render.attachNewNode(alight)
render.setLight(alnp)

slight = Spotlight('slight')
slight.setColor(Vec4(1, 1, 1, 1))
lens = PerspectiveLens()
slight.setLens(lens)
slnp = render.attachNewNode(slight)
render.setLight(slnp)

slnp.setPos(0, 0,40)

if __name__ == '__main__': 
    run()