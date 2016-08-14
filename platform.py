import entity
import math
import pygame

class Platform(entity.Entity):
    def __init__(self, xPos, yPos, textureName, angle):
        spriteName = textureName
        entity.Entity.__init__(self, spriteName, xPos, yPos)

        #rotate the platform to fit the angle. disabled for now when switching to pyglet.
        self.sprite = self.sprite.get_transform(False,False, angle)

    def update(self):
        entity.Entity.update(self)

    #puts t1 outside of the block it hit so it doesnt intersect
    def onCollision(self, collisionTarget):
        x = collisionTarget.getCenterX() - self.getCenterX()
        xabs = math.pow(x,2)
        xabs = math.sqrt(xabs)

        y = collisionTarget.getCenterY() - self.getCenterY()
        yabs = math.pow(y,2)
        yabs = math.sqrt(yabs)

        #print(collisionTarget.isCollidingRight)
        #collisionTarget.resetAllColisionDirectionFlags()

        #collisionTarget from above or below
        if(yabs > xabs ):
            if(collisionTarget.getCenterY() > self.getCenterY()): #from above
                collisionTarget.setBottomPosition(self.getTopPosition())
                collisionTarget.isCollidingBottom = True
            else:
                collisionTarget.setTopPosition(self.getBottomPosition())
                collisionTarget.isCollidingTop = True

            #makes sure it doesnt stop blocks taht is going the other way than the collision say.
            #for example if the block is moving right, dont stop it if the collision says it hits a right wall.
            #this happens att corners alot so its important to prevent.
            if(collisionTarget.yDistance != 0):
                if(((self.getCenterY() - collisionTarget.getCenterY()) / -collisionTarget.yDistance) > 0):
                    collisionTarget.yDistance = 0
                    collisionTarget.yForce = 0

        #collisionTarget from right or left
        else:
            if(collisionTarget.getCenterX() < self.getCenterX()): #from left
                collisionTarget.setRightPosition(self.getLeftPosition())
                collisionTarget.isCollidingRight = True
            else:
                collisionTarget.setLeftPosition(self.getRightPosition())
                collisionTarget.isCollidingLeft = True


            #makes sure it doesnt stop blocks taht is going the other way than the collision say.
            #for example if the block is moving right, dont stop it if the collision says it hits a right wall.
            #this happens att corners alot so its important to prevent.
            if(collisionTarget.xDistance != 0):
                if(((self.getCenterX() - collisionTarget.getCenterX()) / -collisionTarget.xDistance) < 0):
                    collisionTarget.xDistance = 0
                    collisionTarget.xForce = 0
