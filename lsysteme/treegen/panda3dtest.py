
# - install panda3d
# - make sure, the panda3d root folder + \bin are in the
#   python search path

from direct.showbase.ShowBase import ShowBase
 
class MyApp(ShowBase):
 
    def __init__(self):
        ShowBase.__init__(self)
 
app = MyApp()
app.run()