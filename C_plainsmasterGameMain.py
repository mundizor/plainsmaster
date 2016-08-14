import C_gameMain
import button
import goomba

from pyglet.window import key

class PlainsmasterGameMain(C_gameMain.GameMain):
    def __init__(self, plainmasterTeam, keys, networkHandler, window):
        C_gameMain.GameMain.__init__(self, plainmasterTeam, keys, networkHandler, window)

        self.buttonList = []
        self.buttonList.append(button.Button("goomba.png", 10,10, self.setSelectedPlacingEnemy, goomba.Goomba))

        self.selectedPlacingType = None

        self.scrollSpeed = 5

    def mainUpdate(self, deltatTime):
        C_gameMain.GameMain.mainUpdate(self, deltatTime)

        self.scrollScreen()

    def mainRender(self):
        C_gameMain.GameMain.mainRender(self)

        for i in self.buttonList:
            i.render()

    def on_mouse_press(self, x,y,button,modifiers):
        for i in self.buttonList:
            i.on_mouse_press(x,y,button,modifiers)

        if(self.selectedPlacingType != None):
            self.placeSelectedEnemy(x, y, self.selectedPlacingType);

    def on_mouse_motion(self, x, y, dx, dy, window):
        pass

    def scrollScreen(self):
        if self.keys[key.W]:
            self.camera.addCamPos(0, -self.scrollSpeed)
        if self.keys[key.A]:
            self.camera.addCamPos(self.scrollSpeed, 0)
        if self.keys[key.S]:
            self.camera.addCamPos(0, self.scrollSpeed)
        if self.keys[key.D]:
            self.camera.addCamPos(-self.scrollSpeed, 0)


    def placeSelectedEnemy(self, x, y, enemyType):


        width = self.camera.win.screen.width
        height = self.camera.win.screen.height
        widthRatio = width / height
        zoom = self.camera.zoom

        x = (-zoom) + x/width
        y = (zoom) - y/height

        x -= self.camera.camX
        y -= self.camera.camY

        msg = "Ex"
        msg += str(x)
        msg += "y"
        msg += str(y)
        msg += "T"

        #removes the additional characters python adds when you convert class type to string
        msg += str(enemyType)[8:]
        msg = msg[:-2]

        self.networkHandler.sendMessageToServer(msg)

    def setSelectedPlacingEnemy(self, type):
        self.selectedPlacingType = type