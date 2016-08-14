import C_lobby
import pyglet

from pyglet.window import key

class GameWindow(pyglet.window.Window):
    def __init__(self):
        super(GameWindow, self).__init__()

    def on_draw(self):
        self.clear()

        Lobby.render()

    def on_mouse_press(self, x, y, button, modifiers):
        Lobby.on_mouse_press(x,y,button,modifiers)

    def on_key_press(self, symbol, modifiers):
        Lobby.lobbyInputHandler.textinputer.on_key_press(symbol, modifiers)

    def on_mouse_motion(self, x, y, dx, dy):
        Lobby.on_mouse_motion(x, y, dx, dy, self)

    def on_text(self, text):
        Lobby.lobbyInputHandler.textinputer.on_text(text)

    def on_text_motion(self, motion):
        Lobby.lobbyInputHandler.textinputer.on_text_motion(motion)

    def on_text_motion_select(self, motion):
        Lobby.lobbyInputHandler.textinputer.on_text_motion_select(motion)

    def update(dt):
        Lobby.update(dt)



#initializes window and keyboard
window = GameWindow()
keys = key.KeyStateHandler()
window.push_handlers(keys)

Lobby = C_lobby.C_Lobby(keys, window, 12346)

pyglet.clock.schedule_interval(GameWindow.update, 1/60.0)

if __name__ == '__main__':

    pyglet.app.run()

