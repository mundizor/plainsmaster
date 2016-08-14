import entity
import math

class PhysicsEntities(entity.Entity):


    def __init__(self, spriteName, xPos, yPos):
        entity.Entity.__init__(self, spriteName, xPos, yPos)

        self.xPos = entity.Entity.getRect(self).anchor_x
        self.yPos = entity.Entity.getRect(self).anchor_y
        self.weight = 6
        self.gravity = 10
        self.friction = 0.90
        self.airResistance = 0.5
        self.yDistance = 0
        self.xDistance = 0
        self.yForce = 0
        self.xForce = 0

        self.isCollidingRight = False
        self.isCollidingLeft = False
        self.isCollidingBottom = False
        self.isCollidingTop = False


    def update(self, deltaTime):

        self.resetAllColisionDirectionFlags()
        self.physicshandling(deltaTime)

        entity.Entity.update(self)


    def physicshandling(self, deltaTime):

        #adds friction. also adds a bordervalue so it doesnt get too small.
        self.xForce *= self.friction
        if(self.xForce < 0.1 and self.xForce > -0.1):
            self.xForce = 0

        self.yForce += self.gravity * self.weight

        self.yDistance += self.yForce
        self.xDistance += self.xForce
        self.yDistance *= deltaTime
        self.xDistance *= deltaTime

        #removes very small values of distance.
        if(self.xDistance < 0.1 and self.xDistance > -0.1):
            self.xDistance = 0

        #have to ceil Distance otherwise it floors automaticly and the physics gets bad.
        #the rect the value it is added to later is probably an int. fuck python for keeping secrets.
        if(self.xDistance < 0):
            self.xDistance = math.ceil(self.xDistance)
        if(self.yDistance < 0 and self.yDistance > -1):
           self.yDistance = math.floor(self.yDistance)

        entity.Entity.addPosition(self, self.xDistance, -self.yDistance)


    def addForce(self, x, y):
        self.xForce += x
        self.yForce += y

    def resetAllColisionDirectionFlags(self):
        self.isCollidingRight = False
        self.isCollidingLeft = False
        self.isCollidingBottom = False
        self.isCollidingTop = False
