import levelLoader
import courseRunner
import camera
import collisionHandler
import S_clientMessageTranslator
import goomba


class GameMain:
    def __init__(self, NetworkHandler, window):
        self.courseArray = []
        self.physicsEntitiesArray = []
        self.CollisionHandler = collisionHandler.CollisionHandler()
        self.giveRunnersAControllable(NetworkHandler)
        #self.physicsEntitiesArray.append(goomba.Goomba(310 + 196, 110))

        self.camera = camera.Camera(window)

        self.levelLoader = levelLoader.LevelLoader()
        self.levelLoader.createLevel(self.courseArray, (0,450))



    def mainUpdate(self, NetworkHandler, deltatime):
        dt = deltatime

        #executed the reciefed commands from the clients
        self.executeQueuedCommands(NetworkHandler)

        #loops trough all physics entities. players, enemies, powerups etc and updates them and sees if they collided with anything..
        for i in self.physicsEntitiesArray:
            i.update(dt)
            self.CollisionHandler.findCollidingBlocks(i, self.courseArray)

        #runs the update function for every block in the map. normal blocks have no update but blocks with update might be added to the map alter on.
        for i in self.courseArray:
            i.update()

        self.sendEntityPositionsToClients(NetworkHandler)


    def sendEntityPositionsToClients(self, NetworkHandler):
        loopNr = 0
        for i in self.physicsEntitiesArray:
            msg = "Px"
            msg += str(i.getCenterX())
            msg += "y"
            msg += str(i.getCenterY())
            msg += "i"
            msg += str(loopNr)
            NetworkHandler.broadcastToAllClients(msg)
            loopNr+=1


    def mainRender(self):

        self.camera.worldProjection()

        for i in self.physicsEntitiesArray:
            i.render(self.camera)

        for i in self.courseArray:
            i.render(self.camera)

        self.camera.hudProjection()

    def giveRunnersAControllable(self, NetworkHandler):

        #give every connected client a runner also spawn them at very client.
        for i in NetworkHandler.connectionsList:
            if(i.PlainsMasterTeam == False):
                insertSpot = self.physicsEntitiesArray.__len__()

                ent = courseRunner.CourseRunner(310, 310)
                self.physicsEntitiesArray.append(ent)
                i.ActiveEntity = ent
                NetworkHandler.tellClientsToSpawnEnt(ent)
                self.tellClientToFocusEntity(NetworkHandler, insertSpot, i)


    def tellClientToFocusEntity(self,Networkhandler, indexOfEntity, client):
        msg = "I" + str(indexOfEntity)
        Networkhandler.sendToSingleClient(msg, client)
        print("Sent I message")

    def executeQueuedCommands(self, NetworkHandler):
        CList = NetworkHandler.recievedCommandsList
        NetworkHandler.recievedCommandsList = [] #empties the original list to make room for new commands.

        for i in CList:
            if(i.command[0] == "T"):
                for j in NetworkHandler.connectionsList:
                    if(i.address == j.address):
                        self.doCommandToEntity(j.ActiveEntity, i.command)
            elif(i.command[0] == "E"):
                self.spawnEntity(i.command, NetworkHandler)

    def spawnEntity(self, msg, NetworkHandler):
        xpos, ypos, moduleName, className = S_clientMessageTranslator.S_ClientMessageTranslator.translateSpawnPosAndEnemytype(msg)

        module = __import__(moduleName)
        class_ = getattr(module, className)
        ent = class_(float(xpos),float(ypos))

        self.physicsEntitiesArray.append(ent)
        NetworkHandler.tellClientsToSpawnEnt(ent)

    def doCommandToEntity(self, entity, command):

        #removes the C from the commandstring.
        command = command[1:]

        if(command == "up"):
            entity.jump()

        if(command == "right"):
            entity.moveRight()

        if(command == "left"):
            entity.moveLeft()