import threading
import socket

class S_ClientUDPConnector():

    def __init__(self, port):

        self.UDPSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)    # Create a socket object
        host = socket.gethostname() # Get local machine name
        self.UDPSocket.bind((host, port))        # Bind to the port

        self.activeThread = None

    def createListeningThread(self, connectionsList):
        #creates a thread that listenes for a client to connect
        try:
            self.activeThread = threading.Thread(target=self.listenForClient, args = (connectionsList,))
        except:
            print("could not create thread!")

        self.activeThread.start()

    def listenForClient(self, connectionsList):
        try:
            #waiting for connectons. maximum 1.
            print("waiting for message from client")
            data, addr = self.UDPSocket.recvfrom(128)    # Establish connection with client.
            print("1")
            ci = ConnectionInfo(addr)
            print("2")
            connectionsList.append(ci)
            print ('Got connection from', ci.address)
            text = "You are now connected to the server!"
            text = text.encode()
            self.UDPSocket.sendto(text, (ci.address[0], ci.address[1]))
            print("sent respsonse to client!")

        except:
            print("Socket got closed!")


    def isActiveThreadAlive(self):
        #if the thread is not yet created return that it is dead.
        if(self.activeThread == None):
            return False

        #return the alive state of thread.
        return self.activeThread.isAlive()


    def killListeningSocket(self):
        self.UDPSocket.close()

#class to hold connection info.
class ConnectionInfo():
    def __init__(self, address):
        self.address = address
        self.ActiveEntity = None
