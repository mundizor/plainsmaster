from pyglet.gl import *

class Camera(object):

    def __init__(self, win, target=None):
        self.targetZoom = 300
        self.NoneTargetZoom = 1000

        self.win = win
        self.zoom = self.NoneTargetZoom

        self.target = target

        self.camX = 0
        self.camY = 0

        self.lastFramePosx = self.camX
        self.lastFramePosy = self.camY

        if(target):
            #if the client has a traget, zoom in.
            self.zoom = self.targetZoom

            self.camX -=self.target.getCenterX()
            self.camY -=self.target.getCenterY()

            self.lastFramePosx = self.target.getCenterX()
            self.lastFramePosy = self.target.getCenterY()


    def worldProjection(self):
         glMatrixMode(GL_PROJECTION)
         glLoadIdentity()
         widthRatio = self.win.width / self.win.height
         gluOrtho2D(
             -self.zoom * widthRatio,
             self.zoom * widthRatio,
             -self.zoom,
             self.zoom)


    def hudProjection(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(0, self.win.width, 0, self.win.height)

    def render(self):

        if(self.target == None):
            return

        x = self.target.getCenterX() - self.lastFramePosx
        y = self.target.getCenterY() - self.lastFramePosy

        self.lastFramePosx = self.target.getCenterX()
        self.lastFramePosy = self.target.getCenterY()

        self.camX -= x
        self.camY -= y

    def getCamPosX(self):
        return self.camX

    def getCamPosY(self):
        return self.camY

    def addCamPos(self, xdist, ydist):
        self.camX += xdist
        self.camY += ydist

    def SetNewTarget(self, target):
        self.target = target

        if(target == None):
            self.zoom = self.NoneTargetZoom
        else:
            self.zoom = self.targetZoom