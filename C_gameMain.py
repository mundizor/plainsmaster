#all the gamelogic, rules etc

import levelLoader
import courseRunner
import camera
import goomba
import C_networkHandler
import C_serverMessageTranslator
import C_entityController
import collisionHandler
import DEBUGCLASS
import camera

class GameMain:
    def __init__(self, plainmasterTeam, keys, networkHandler, window):
        self.keys = keys

        self.PlainsMasterTeam = plainmasterTeam

        #connects to the server
        self.CollisionHandler = collisionHandler.CollisionHandler()
        self.networkHandler = networkHandler

        self.courseArray = []
        self.physicsEntitiesArray = []

        self.camera = camera.Camera(window)
        self.controller = C_entityController.EntityController(keys)

        self.levelLoader = levelLoader.LevelLoader()
        self.levelLoader.createLevel(self.courseArray, (0,450))


    def mainUpdate(self, deltatTime):
        dt = deltatTime

        self.controller.checkButtonInputs(self.networkHandler)

        #loops trough all physics entities. players, enemies, powerups etc and updates them and sees if they collided with anything etc...
        for i in self.physicsEntitiesArray:
            i.update(dt)
            self.CollisionHandler.findCollidingBlocks(i, self.courseArray)

        for i in self.courseArray:
            i.update()

        self.handleNetworkedMessages()

    #checks for messages in the message queue that are updates on the position of all the entities.
    def handleNetworkedMessages(self):
        #creates a new list with no references to the existing one.
        activeMessageList = list(self.networkHandler.queuedNetworkMessages)
        self.networkHandler.queuedNetworkMessages.clear()
        for i in activeMessageList:
            #If the first letter is P then the message tells a position.
            if(i[0] == 'P'):
                #index, x, y = self.serverMessageTranslator.translatePositionMessage(i)
                index, x, y = C_serverMessageTranslator.C_ServerMessageTranslator.translatePositionMessage(i)
                self.moveIndexedUnitToPos(index,x,y)
            elif(i[0] == 'F'):
                self.spawnEntityAtPos(i[1:])
            elif(i[0] == 'I'):
                self.handleControllableAssignmentMessage(i[1:])
            else:
                print("NON-RECOGNIZALBE MSG IN C_GAMEMAIN: " + i)


    def spawnEntityAtPos(self, msg):

        moduleName, className, x, y = C_serverMessageTranslator.C_ServerMessageTranslator.translateEntitySpawningMessage(msg)

        module = __import__(moduleName)
        class_ = getattr(module, className)
        instance = class_(x,y)

        self.physicsEntitiesArray.append(instance)

    def handleControllableAssignmentMessage(self, msg):
        index = int(msg)

        unit = self.physicsEntitiesArray[index]
        self.controller.setControlledUnit(unit)
        self.camera.SetNewTarget(unit)

    def moveIndexedUnitToPos(self, index, x, y):
        if(index >= self.physicsEntitiesArray.__len__()):
            print("Server sent a pos to an entity not spawned on client. - C_gameMain")
            return
        self.physicsEntitiesArray[index].setCenterPosition(x,y)

    def mainRender(self):
        self.camera.render()
        self.camera.worldProjection()

        for i in self.physicsEntitiesArray:
            i.render(self.camera)

        for i in self.courseArray:
            i.render(self.camera)

        self.camera.hudProjection()