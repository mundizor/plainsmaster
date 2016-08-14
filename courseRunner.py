import stearableEntities

class CourseRunner(stearableEntities.StearableEntities):

    def __init__(self, xPos, yPos):
        spriteName = "dew.png"
        stearableEntities.StearableEntities.__init__(self, spriteName, xPos, yPos)
        self.jumpforce = 1000
        self.moveForce = 80

    def update(self, deltaTime):
        stearableEntities.StearableEntities.update(self, deltaTime)

    def moveLeft(self):
        stearableEntities.StearableEntities.moveLeft(self, self.moveForce)

    def moveRight(self):
        stearableEntities.StearableEntities.moveRight(self, self.moveForce)

    def jump(self):
        stearableEntities.StearableEntities.jump(self, self.jumpforce)