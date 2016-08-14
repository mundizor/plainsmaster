import socket               # Import socket module


class C_ServerUDPConnector():

    def __init__(self, serverport, serveradress, socket):
        maxconnectionTries = 3

        #tries to connect to the server. will exit if no server is found.
        for x in range(0, maxconnectionTries):
            try:
                data="Qconnecting"
                data=data.encode(encoding='UTF-8')
                socket.sendto(data, (serveradress, serverport))
                indata, addr = socket.recvfrom(128)
                print(indata)
                break
            except:
                print("could not find server.")
                print("Will quit apllication after %d more tries." % (maxconnectionTries - x - 1))

                if(x >= maxconnectionTries - 1):
                    socket.close()
                    exit()

                print("Trying again.")