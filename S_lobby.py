import S_gameMain

class S_Lobby():

    def __init__(self, networkHandler, window):
        self.GM = None
        self.window = window
        self.NetworkHandler = networkHandler
        self.isActive = True

        self.NrOfConnectedClients = 0

    def update(self, dt):
        if(self.isActive == True):
            self.lobbyUpdate()
        else:
            self.GM.mainUpdate(self.NetworkHandler, dt)

    def lobbyUpdate(self):
        self.executeQueuedCommands()
        self.checkIfSomeoneConnected()

    def executeQueuedCommands(self):
        CList = self.NetworkHandler.recievedCommandsList
        self.NetworkHandler.recievedCommandsList = [] #empties the original list to make room for new commands.

        for i in CList:
            #if its a chat message
            if(i.command == "Cstart"):
                self.NetworkHandler.broadcastToAllClients(i.command)
                self.turnOffLobbyAndStartGame()
            #Cchange changes the team of the player
            if(i.command == "Cchange"):
                for Connections in self.NetworkHandler.connectionsList:
                    if(Connections.address == i.address):
                        Connections.PlainsMasterTeam = not Connections.PlainsMasterTeam
                        self.sendTeamNumbersToClients()
            else:
                return

    def sendTeamNumbersToClients(self):
        PlainsMasters = 0
        Runners = 0

        for Connections in self.NetworkHandler.connectionsList:
            if(Connections.PlainsMasterTeam == True):
                PlainsMasters += 1

        for Connections in self.NetworkHandler.connectionsList:
            if(Connections.PlainsMasterTeam == False):
                Runners += 1

        data = "T" + str(PlainsMasters) + "F" + str(Runners)
        self.NetworkHandler.broadcastToAllClients(data)

    def getIsActive(self):
        return self.isActive

    def checkIfSomeoneConnected(self):
        if(self.NetworkHandler.CheckIfConnectionListHasChanged()):
            self.sendTeamNumbersToClients()

    def turnOffLobbyAndStartGame(self):
        self.isActive = False
        self.NetworkHandler.acceptingconnection = False
        self.GM = S_gameMain.GameMain(self.NetworkHandler, self.window)