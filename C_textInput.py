import pyglet

class Rectangle(object):
    '''Draws a rectangle into a batch.'''
    def __init__(self, x1, y1, x2, y2, batch):
        self.vertex_list = batch.add(4, pyglet.gl.GL_QUADS, None,
            ('v2i', [x1, y1, x2, y1, x2, y2, x1, y2]),
            ('c4B', [200, 200, 220, 255] * 4)
        )

class TextWidget(object):
    def __init__(self, text, x, y, width, batch, height, name):
        self.name = name
        self.document = pyglet.text.document.UnformattedDocument(text)
        self.document.set_style(0, len(self.document.text),
            dict(color=(0, 0, 0, 255))
        )
        font = self.document.get_font()

        self.layout = pyglet.text.layout.IncrementalTextLayout(
            self.document, width, height, multiline=False, batch=batch)
        self.caret = pyglet.text.caret.Caret(self.layout)

        self.layout.x = x
        self.layout.y = y

        # Rectangular outline
        pad = 2
        self.rectangle = Rectangle(x - pad, y - pad,
                                   x + width + pad, y + height + pad, batch)

    def hit_test(self, x, y):
        return (0 < x - self.layout.x < self.layout.width and
                0 < y - self.layout.y < self.layout.height)

class textOutputBox():
    def __init__(self, batch, boxwidth, boxheight, xpos, ypos):

        self.boxwidth = boxwidth
        self.boxheight = boxheight
        self.batch = batch

        self.doc = pyglet.text.decode_text('Hello world!'.ljust(self.boxwidth))
        self.doc.set_style(0, 12, dict(font_name='Arial', font_size=12,
                                    color=(0,0,0,255)))
        self.layout = pyglet.text.layout.ScrollableTextLayout(self.doc,
                                            width=500,
                                            height=self.boxheight, multiline=True, batch=batch)
        self.layout.x = xpos
        self.layout.y = ypos
        self.layout.view_y = 0

        self.rectangle = Rectangle(self.layout.x, self.layout.y, self.layout.x + self.boxwidth, self.layout.y + self.boxheight, self.batch)

    def addTextLine(self, text):
        self.doc.insert_text(-1, text.ljust(self.boxwidth))
        self.layout.view_y = -self.layout.content_height

#this could should be re used for ingame chat system later.
class TextInputHandler():
    def __init__(self, widgets, batch, text_cursor, textOutputBox, networkhandler):
        self.widgets = widgets
        self.batch = batch
        self.text_cursor = text_cursor
        self.textOutputBox = textOutputBox
        self.networkhandler = networkhandler

    def on_draw(self):
        self.batch.draw()

    def on_mouse_motion(self, x, y, dx, dy, window):
        for widget in self.widgets:
            if widget.hit_test(x, y):
                window.set_mouse_cursor(self.text_cursor)
                break
        else:
            window.set_mouse_cursor(None)

    def on_mouse_press(self, x, y, button, modifiers):
        for widget in self.widgets:
            if widget.hit_test(x, y):
                self.set_focus(widget)
                break
        else:
            self.set_focus(None)

        if self.focus:
            self.focus.caret.on_mouse_press(x, y, button, modifiers)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if self.focus:
            self.focus.caret.on_mouse_drag(x, y, dx, dy, buttons, modifiers)

    def on_text(self, text):
        if self.focus:
            self.focus.caret.on_text(text)

    def on_text_motion(self, motion):
        if self.focus:
            self.focus.caret.on_text_motion(motion)

    def on_text_motion_select(self, motion):
        if self.focus:
            self.focus.caret.on_text_motion_select(motion)

    def on_key_press(self, symbol, modifiers):
        #if the player presses enter in active text field it gets sent to the server.
        if symbol == pyglet.window.key.ENTER:
            if(self.focus == None):
                return

            #if theres a / before the chat message its a command and not a message
            if(self.focus.document.text[0] == "/"):

                self.networkhandler.sendMessageToServer("C" + self.focus.document.text[1:])
            else:
                self.networkhandler.sendMessageToServer("M" + self.focus.document.text)
            self.focus.document.text = ""

        elif symbol == pyglet.window.key.ESCAPE:
            pyglet.app.exit()

    def set_focus(self, focus):
        if self.focus:
            self.focus.caret.visible = False
            self.focus.caret.mark = self.focus.caret.position = 0

        self.focus = focus
        if self.focus:
            self.focus.caret.visible = True
            self.focus.caret.mark = 0
            self.focus.caret.position = len(self.focus.document.text)

#this class is specific for the lobby. to make an ingame chat, make a class simialr to this and inherit from textinputhandler.
class LobbyTextInputHandler(TextInputHandler):
    def __init__(self, window, networkhandler):

        self.textBoxOfset = 40
        self.boxesBottomPos = 20

        self.chatboxYPos = self.boxesBottomPos
        self.nameBoxYPos = self.chatboxYPos + self.textBoxOfset
        self.chatoutputBoxYPos = self.nameBoxYPos + self.textBoxOfset

        self.xPos = 150
        self.chathistoryYPos = 160
        self.chathistoryBoxheight = 150
        self.width = 400

        self.batch = pyglet.graphics.Batch()
        self.labels = [
            pyglet.text.Label('Chat history', x=10, y=self.chatoutputBoxYPos + self.chathistoryBoxheight, anchor_y='top',
                              color=(255, 255, 255, 255), batch=self.batch),
            pyglet.text.Label('Name', x=10, y=60, anchor_y='bottom',
                              color=(255, 255, 255, 255), batch=self.batch),
            pyglet.text.Label('Chat', x=10, y=20,
                              anchor_y='bottom', color=(255, 255, 255, 255),
                              batch=self.batch)
        ]
        self.widgets = [
            TextWidget("Player2", self.xPos, self.nameBoxYPos, self.width - 10, self.batch, 20, "name"),
            TextWidget('', self.xPos, self.chatboxYPos, self.width - 10, self.batch, 20, "chat")
        ]
        self.text_cursor = window.get_system_mouse_cursor('text')

        self.focus = None
        self.set_focus(self.widgets[0])

        self.textOutputBox = textOutputBox(self.batch, self.width, self.chathistoryBoxheight, self.xPos, self.chatoutputBoxYPos)

        super(LobbyTextInputHandler, self).__init__(self.widgets, self.batch, self.text_cursor, self.textOutputBox, networkhandler)

    def on_text(self, text):
        #dont print enter on screen. it just adds 3 spaces. this if case returns if it gets enter as input
        if(ord(text) == 13):
            return

        if(self.focus == None):
            return

        if(self.focus.name == "name"):
            self.playerName = self.focus.document.text

        super(LobbyTextInputHandler, self).on_text(text)

    def on_key_press(self, symbol, modifiers):
        if(self.focus == None):
                return

        if(self.focus.name == "name"):
            return



        super(LobbyTextInputHandler, self).on_key_press(symbol, modifiers)
