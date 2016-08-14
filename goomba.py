import overtakeableEntities

class Goomba(overtakeableEntities.OvertakeableEntities):

    def __init__(self, xPos, yPos):
        spriteName = "goomba.png"
        overtakeableEntities.OvertakeableEntities.__init__(self, spriteName, xPos, yPos)
        self.moveForce = 80
        self.jumpForce = 1000

    def update(self, deltaTime):


        #if the unit is not overtaken by a player, add force to it.
        if(self.overTaken == False):

            #if the goomba collides with a wall make it change direction
            if(self.isCollidingLeft == True or self.isCollidingRight == True):
                self.moveForce *= -1

            self.addForce(self.moveForce,0)

        overtakeableEntities.OvertakeableEntities.update(self, deltaTime)

    def moveLeft(self):
        overtakeableEntities.OvertakeableEntities.moveLeft(self, self.moveForce)

    def moveRight(self):
        overtakeableEntities.OvertakeableEntities.moveRight(self, self.moveForce)

    def jump(self):
        overtakeableEntities.OvertakeableEntities.jump(self, self.jumpForce)

