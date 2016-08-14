import C_serverUDPConnector
import threading
import socket

class C_NetworkHandler():

    def __init__(self, UDPlisteningPort):

        self.UDPSERVERPORT = 12347      #This port should be the port the server listens on.
        self.RECUDPPORT = UDPlisteningPort

        self.host = "192.168.0.10"

        self.UDPSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.UDPListeningThread = None

        self.queuedNetworkMessages = []

        self.createUDPListener()


    def createUDPListener(self):

        try:
            self.UDPSocket.bind(("", self.RECUDPPORT))
            print("UDP socket bound!")
        except socket.error as msg:
            print("Bind failed. Error Code : " + str(msg[0]) + " Message " + msg[1])

        #tries connecting to the server on the created socket.
        self.serverConnector = C_serverUDPConnector.C_ServerUDPConnector(self.UDPSERVERPORT, self.host, self.UDPSocket)

        #creates the thread listening on the udp socket.
        try:
            self.UDPListeningThread = threading.Thread(target=self.UDPListenerThreadFunc, args = ())
            self.UDPListeningThread.daemon = True
        except:
            print("could not create thread!")

        self.UDPListeningThread.start()

    def sendMessageToServer(self, data):

        data=data.encode(encoding='UTF-8')
        self.UDPSocket.sendto(data, (self.host, self.UDPSERVERPORT))
        #print(data)


    def UDPListenerThreadFunc(self):
        while 1:
            # receive data from server

            data, addr = self.UDPSocket.recvfrom(256)
            self.queuedNetworkMessages.append(data.decode())
            #print(data.decode())
