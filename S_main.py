import S_lobby
import S_networkHandler
import pyglet
import DEBUGCLASS



class GameWindow(pyglet.window.Window):
    def __init__(self):
        super(GameWindow, self).__init__()

    def on_draw(self):
        self.clear()

        if(Lobby.getIsActive()):
            #render stuff for the lobby here if needed
            DEBUGCLASS.DEBUGCLASS.TextAtPoint(300,300, "Waiting for game to start", 36)
            DEBUGCLASS.DEBUGCLASS.TextAtPoint(300,250, "and clients to connect", 36)
        else:
            Lobby.GM.mainRender()


    def update(dt, Lobby):
        Lobby.update(dt)


window = GameWindow()
NetworkHandler = S_networkHandler.S_NetworkHandler()
Lobby = S_lobby.S_Lobby(NetworkHandler, window)

pyglet.clock.schedule_interval(GameWindow.update, 1/60.0, Lobby)


if __name__ == '__main__':

    pyglet.app.run()

