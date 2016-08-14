import pyglet
from pyglet.window import mouse

class Button(pyglet.event.EventDispatcher):

    #xPos and yPos are the buttons top left corner.
    def __init__(self, textureName, xPos, yPos, func, *args):
        self.textureName = "Textures/Buttons/" + textureName
        self.buttonFunc = func

        self.sprite = pyglet.resource.image(self.textureName)
        self.yPos = yPos
        self.xPos = xPos

        self.args = args

    def render(self):
        self.sprite.blit(self.xPos, self.yPos)

    def on_mouse_press(self, x,y,button, modifiers):
        #if you click on the button with left mouse it runs the button function
        if(button == mouse.LEFT):
            if(x < self.xPos + self.sprite.width and x > self.xPos):
                if(y < self.yPos + self.sprite.height and y > self.yPos):
                    self.buttonFunc(*self.args)



