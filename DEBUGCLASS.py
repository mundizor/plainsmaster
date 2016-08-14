import pyglet
from pyglet.gl import *


class DEBUGCLASS():

    def __init__(self):
        pass

    #renders a white crosshair at the set coords.
    @staticmethod
    def MarkAtPoint(x, y):

        a1 = x - 32
        a2 = x + 32
        pyglet.graphics.draw(2, pyglet.gl.GL_LINES, ('v3f', (a1, y, 0.0, a2, y, 0.0)))

        a1 = y - 32
        a2 = y + 32
        pyglet.graphics.draw(2, pyglet.gl.GL_LINES, ('v3f', (x, a1, 0.0, x, a2, 0.0)))


    @staticmethod
    def TextAtPoint(x, y, text, size):
        label = pyglet.text.Label(text,
                          font_name='Times New Roman',
                          font_size=size,
                          x=x, y=y,
                          anchor_x='center', anchor_y='center')
        label.draw()