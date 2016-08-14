import  C_runnerGameMain
import C_plainsmasterGameMain
import C_networkHandler
import C_textInput
import pyglet
import C_lobbyInputHandler
import C_serverMessageTranslator

from pyglet.window import key

class C_Lobby():

    def __init__(self, keys, window, udpport):
        #this variable determines what team the player is on. everyone starts on lpainsmaster team.
        self.PlainsMasterTeam = True
        self.NrOfRunners = 0
        self.NrOfPlainsMasters = 0

        self.isActive = True
        self.UDPlisteningPort = udpport

        self.networkHandler = C_networkHandler.C_NetworkHandler(self.UDPlisteningPort)
        self.keys = keys
        self.window = window
        self.GM = None

        self.lobbyInputHandler = C_lobbyInputHandler.C_LobbyInputHandler(self.window, self.networkHandler)
        self.lobbyInputHandler.createButton("change_team.png", 20,400, self.changeTeam)

    def changeTeam(self):
        self.PlainsMasterTeam = not self.PlainsMasterTeam
        self.networkHandler.sendMessageToServer("Cchange")
        #print(self.PlainsMasterTeam)

    def render(self):
        if(self.isActive == True):
            self.lobbyInputHandler.on_draw()
            self.renderLobbyUI()
        else:
            self.GM.mainRender()

    def update(self, dt):
        if(self.isActive == True):
            if self.keys[key.W]:
                self.isActive = False

            self.handleNetworkedMessages()
        else:
            self.GM.mainUpdate(dt)

    def on_mouse_press(self, x, y, button, modifiers):

        if(self.isActive == True):
            self.lobbyInputHandler.on_mouse_press(x,y,button,modifiers)
        else:
            self.GM.on_mouse_press(x,y,button,modifiers)

    def on_mouse_motion(self, x, y, dx, dy, window):
        if(self.isActive == True):
            self.lobbyInputHandler.on_mouse_motion(x,y,dx,dy, window)
        else:
            self.GM.on_mouse_motion(x,y,dx,dy, window)



    #this is temporary but it shows what is need at this moment.
    def renderLobbyUI(self):
        label = pyglet.text.Label("Plainsmasters: " + str(self.NrOfPlainsMasters),
                          font_name='Times New Roman',
                          font_size=36,
                          x=400, y=400,
                          anchor_x='center', anchor_y='center')
        label2 = pyglet.text.Label("Runners: " + str(self.NrOfRunners),
                          font_name='Times New Roman',
                          font_size=36,
                          x=400, y=450,
                          anchor_x='center', anchor_y='center')

        if(self.PlainsMasterTeam):
            team = "Plainsmaster"
        else:
            team = "Runner"
        label3 = pyglet.text.Label("Your team: " + team,
                          font_name='Times New Roman',
                          font_size=36,
                          x=400, y=350,
                          anchor_x='center', anchor_y='center')
        label.draw()
        label2.draw()
        label3.draw()

    #checks for messages in the message queue that are updates on the position of all the entities.
    def handleNetworkedMessages(self):
        activeMessageList = list(self.networkHandler.queuedNetworkMessages)
        self.networkHandler.queuedNetworkMessages.clear()

        for i in activeMessageList:
            #If the first letter is P then the message tells a position.
            if(i[0] == 'M'):
                self.lobbyInputHandler.textinputer.textOutputBox.addTextLine(i[1:])
            elif(i[0] == 'C'):
                msg = i[1:]
                if(msg == "start"):
                    self.startGame(activeMessageList)
            elif(i[0] == 'T'):
                self.NrOfPlainsMasters, self.NrOfRunners = C_serverMessageTranslator.C_ServerMessageTranslator.translateNumberInTeams(i)

            #if the clients get a message to spawn enetity or set controller during the lobby it will be put back in queue untill game starts.
            elif(i[0] == 'F'):
                self.networkHandler.queuedNetworkMessages.append(i)
            elif(i[0] == 'I'):
                self.networkHandler.queuedNetworkMessages.append(i)

            else:
                print("unidentified message in C_lobby: " + i)

    def startGame(self, activeMessageList):
        self.isActive = False

        if(self.PlainsMasterTeam):
            self.GM = C_plainsmasterGameMain.PlainsmasterGameMain(self.PlainsMasterTeam, self.keys, self.networkHandler, self.window)
        else:
            self.GM = C_runnerGameMain.RunnerGameMain(self.PlainsMasterTeam, self.keys, self.networkHandler, self.window)