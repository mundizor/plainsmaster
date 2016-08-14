class CollisionHandler():

    def __init__(self):
        pass

    def findCollidingBlocks(self, activeEntity, courseArray):
        collidingBlocks = []
        for blockItr in courseArray:
            if( self.checkForCollision(activeEntity, blockItr)):
                collidingBlocks.append(blockItr)

        #runs the collision function for all the platforms the entity colided with.
        for blockItr in collidingBlocks:
            blockItr.onCollision(activeEntity)

    def checkForCollision(self, b1, b2):

        b1x = b1.getCenterX() - b1.rect.width / 2
        b2x = b2.getCenterX() - b2.rect.width / 2
        b1y = b1.getCenterY() - b1.rect.height / 2
        b2y = b2.getCenterY() - b2.rect.height / 2
        if (b1x < b2x + b2.rect.width and
        b1x + b1.rect.width > b2x and
        b1y < b2y + b2.rect.height and
        b1.rect.height + b1y > b2y):
            return True


        return False