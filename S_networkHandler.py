import S_clientUDPConnector
import socket
import threading

class S_NetworkHandler():

    def __init__(self):
        self.connectionsList = []
        self.recievedCommandsList = []
        self.acceptingConnection = True
        self.ConnectionListChanged = False

        self.RECUDPPORT = 12347

        #creates the TCP connector. this class allows clients to connect to the server and saves their adresses
        #self.ClientConnector = S_clientUDPConnector.S_ClientUDPConnector(self.RECUDPPORT)

        try :
            self.UDPsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            print("UDP socket created!")
        except socket.error as msg:
            print('Failed to create socket. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])

        try:
            self.UDPsocket.bind(("", self.RECUDPPORT))
            print("UDP socket bound!")
        except socket.error as msg:
            print('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])

        #creates the udp listening thread.
        try:
            self.UDPListeningThread = threading.Thread(target=self.UDPListenerThreadFunc, args = ())
            self.UDPListeningThread.daemon = True
        except:
            print("could not create thread!")

        self.UDPListeningThread.start()

    def getConnectedClients(self):
        return self.connectionsList

    def broadcastToAllClients(self, data):
        clientList = self.getConnectedClients()
        data=data.encode(encoding='UTF-8')

        #sends one message to all connected clients using their IP gathered from when they connected.
        for i in range(0, len(clientList)):

            self.UDPsocket.sendto(data, (clientList[i].address[0], clientList[i].address[1]))

    def sendToSingleClient(self, data, client):
        data=data.encode(encoding='UTF-8')

        self.UDPsocket.sendto(data, (client.address[0], client.address[1]))

    def UDPListenerThreadFunc(self):
        while 1:
            # receive data from client
            data, addr = self.UDPsocket.recvfrom(256)
            self.translateAndHandleMessage(data, addr)

    def translateAndHandleMessage(self, data, addr):
        msg = data.decode()

        #If it's a connection request, dont add it to command list
        if(msg == "Qconnecting"):
            if(self.acceptingConnection):
                self.addClientToConnectionList(addr)
        #If its a chatmessage
        elif(msg[0] == "M"):
            self.broadcastToAllClients(msg)

        #if its a command
        elif(msg[0] == "C" or msg[0] == "T" or msg[0] == "E"):
            QCI = QueuedCommandsInfo(addr, msg)
            self.recievedCommandsList.append(QCI)

    def addClientToConnectionList(self, addr):
        ci = ConnectionInfo(addr)
        self.connectionsList.append(ci)
        print ('Got connection from', ci.address)
        text = "You are now connected to the server!"
        text = text.encode()
        self.UDPsocket.sendto(text, (ci.address[0], ci.address[1]))
        print("sent respsonse to client!")
        self.ConnectionListChanged = True

    def CheckIfConnectionListHasChanged(self):
        status = self.ConnectionListChanged
        self.ConnectionListChanged = False
        return status

    def tellClientsToSpawnEnt(self, ent):
        msg = "F"
        msg += ent.__module__ + "." + ent.__class__.__name__
        msg += "/Px"
        msg += str(ent.getCenterX())
        msg += "/Py"
        msg += str(ent.getCenterY())
        print(msg)
        self.broadcastToAllClients(msg)

    def setControllableAtClient(self):
        pass

class ConnectionInfo():
    def __init__(self, address):
        self.address = address
        self.ActiveEntity = None
        self.PlainsMasterTeam = True
        self.Name = "Unknown"

class QueuedCommandsInfo():
    def __init__(self, address, data):
        self.address = address
        self.command = data