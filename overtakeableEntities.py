import stearableEntities
import pygame

class OvertakeableEntities(stearableEntities.StearableEntities):

    def __init__(self, spriteName, xPos, yPos):
        stearableEntities.StearableEntities.__init__(self, spriteName, xPos, yPos)
        self.overTaken = False;
        self.takeOverButtonPressed = False

    def update(self, deltaTime):

        stearableEntities.StearableEntities.update(self, deltaTime)

    def takeOverThisEntity(self):
        self.overTaken = True

    def moveLeft(self, force):
        stearableEntities.StearableEntities.moveLeft(self, force)

    def moveRight(self, force):
        stearableEntities.StearableEntities.moveRight(self, force)

    def jump(self, force):
        stearableEntities.StearableEntities.jump(self, force)