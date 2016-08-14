import physicsEntities
import pygame

class StearableEntities(physicsEntities.PhysicsEntities):
    def __init__(self, spriteName, xPos, yPos):
        physicsEntities.PhysicsEntities.__init__(self, spriteName, xPos, yPos)
        self.wPressed = False

    def update(self, deltaTime):
        physicsEntities.PhysicsEntities.update(self, deltaTime)

    def moveLeft(self, force):
        self.addForce(-force,0)

    def moveRight(self, force):
        self.addForce(force,0)

    def jump(self, force):
        #only allow jump if the entity is standing on the ground.
        if(self.yDistance == 0):
            self.addForce(0,-force)
