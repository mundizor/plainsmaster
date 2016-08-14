import pyglet
import DEBUGCLASS

class Entity:

    def __init__(self, spriteName, xPos, yPos):
        self.sprite = pyglet.resource.image(spriteName)
        self.rect = self.sprite.get_image_data()
        self.rect.anchor_x = xPos
        self.rect.anchor_y = yPos
        self.sprite.anchor_x = self.sprite.width / 2
        self.sprite.anchor_y = self.sprite.height / 2

    def update(self):
        pass

    def render(self, camera):
        #makes sure everything renders relative to the camera.
        #right now + 0 is the camera part. put camera calculations at +0
        cx = camera.getCamPosX()
        cy = camera.getCamPosY()
        self.sprite.blit(self.rect.anchor_x + cx, self.rect.anchor_y + cy)
        DEBUGCLASS.DEBUGCLASS.MarkAtPoint(self.getCenterX() + cx,self.getCenterY() + cy)

    def onCollision(self, collisionTarget):
        pass

    def getRect(self):
        return self.rect

    def getCenterX(self):
        return self.rect.anchor_x

    def getCenterY(self):
        return self.rect.anchor_y

    def setCenterPosition(self, cx, cy):
        self.rect.anchor_x = cx
        self.rect.anchor_y = cy

    def setBottomPosition(self, pos):
        self.rect.anchor_y = pos + (self.rect.height / 2)

    def setTopPosition(self, pos):
        self.rect.anchor_y = pos - (self.rect.height / 2)

    def setLeftPosition(self, pos):
        self.rect.anchor_x = pos + (self.rect.width / 2)

    def setRightPosition(self, pos):
        self.rect.anchor_x = pos - (self.rect.width / 2)

    def getBottomPosition(self):
        return self.getCenterY() - (self.rect.height / 2)

    def getTopPosition(self):
        return self.getCenterY() + (self.rect.height / 2)

    def getRightPosition(self):
        return self.getCenterX() + (self.rect.width / 2)

    def getLeftPosition(self):
        return self.getCenterX() - (self.rect.width / 2)

    def addPosition(self, cx, cy):
        self.rect.anchor_x += cx
        self.rect.anchor_y += cy