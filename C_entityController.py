from pyglet.window import key

class EntityController():

    def __init__(self, keys, controlledUnit=None):
        self.controlledUnit = controlledUnit
        self.jumpKeyPressed = False
        self.rightKeyOnce = False
        self.leftKeyOnce = False
        self.keys = keys

    def setControlledUnit(self, controlledUnit):
        self.controlledUnit = controlledUnit

    def sendCommandToServer(self, command, networkHandler):
        networkHandler.sendMessageToServer("T" + command)

    def checkButtonInputs(self, networkHandler):
        if(self.controlledUnit == None):
            return

        #checks if jump button was pressed once.
        if self.keys[key.W]:
            self.sendCommandToServer("up", networkHandler)
            #checks if the entity is on the ground
            if(self.jumpKeyPressed == False):
                #print("pressed w")
                self.jumpKeyPressed = True
                self.controlledUnit.jump()


        #checks if player let go of button
        if self.keys[key.W] == False:
            if(self.jumpKeyPressed):
                pass
                #print("let go of w")

            self.jumpKeyPressed = False


        if self.keys[key.A]:
            self.sendCommandToServer("left", networkHandler)
            self.controlledUnit.moveLeft()
            if(self.leftKeyOnce == False):
                self.leftKeyOnce = True
                #print("pressed a")

        if self.keys[key.A] == False and self.leftKeyOnce == True:
            self.leftKeyOnce = False
            #print("let go of a")


        if self.keys[key.D]:
            self.sendCommandToServer("right", networkHandler)
            self.controlledUnit.moveRight()
            if(self.rightKeyOnce == False):
                self.rightKeyOnce = True
                #print("pressed d")

        if self.keys[key.D] == False and self.rightKeyOnce == True:
            self.rightKeyOnce = False
            #print("let go of d")