import C_textInput
import button

class C_LobbyInputHandler():
    def __init__(self, window, networkhandler):
        self.networkHandler = networkhandler
        self.textinputer = C_textInput.LobbyTextInputHandler(window, self.networkHandler)

        self.buttonList = []


    def createButton(self, name, x, y, func):
        self.buttonList.append(button.Button(name, x, y, func))

    def on_draw(self):
        self.textinputer.on_draw()

        for i in self.buttonList:
            i.render()

    def on_mouse_press(self, x, y, button, modifiers):
        self.textinputer.on_mouse_press(x,y,button,modifiers)

        for i in self.buttonList:
            i.on_mouse_press(x,y,button,modifiers)

    def on_mouse_motion(self, x, y, dx, dy, window):
        self.textinputer.on_mouse_motion(x, y, dx, dy, window)