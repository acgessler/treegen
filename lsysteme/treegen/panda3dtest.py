
# - install panda3d
# - make sure, the panda3d root folder + \bin are in the
#   python search path

from direct.showbase.ShowBase import ShowBase
 
class TreegenApp(ShowBase):
 
    def __init__(self):
        ShowBase.__init__(self)
 
        # Load the environment model.
        self.environ = self.loader.loadModel("models/environment")
        # Reparent the model to render.
        self.environ.reparentTo(self.render)
        # Apply scale and position transforms on the model.
        self.environ.setScale(0.25, 0.25, 0.25)
        self.environ.setPos(-8, 42, 0)
 
 
      
if __name__ == '__main__':
    app = TreegenApp()
    app.run()