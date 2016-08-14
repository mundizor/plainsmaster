import platform
class LevelLoader:
    def __init__(self):
        self.StringLevelArray = []
        self.loadLevel()

        self.textureFolder = "Textures/Ground Textures/"
        self.textureName = "standard floor tile.png"

        self.dummyplatform = platform.Platform(0, 0, self.textureFolder + self.textureName, 0)
        self.platformWidth = self.dummyplatform.rect.width
        self.platformHeight = self.dummyplatform.rect.height
        self.dummyplatform = None

    #ska senare ladda in ifrån en text-fil ist.
    def loadLevel(self):
        self.StringLevelArray.append("P--------------PPP-----------P")
        self.StringLevelArray.append("P-------------------------P--P")
        self.StringLevelArray.append("P----------------------------P")
        self.StringLevelArray.append("P----------------------------P")
        self.StringLevelArray.append("P-----PPPP-P-----------------P")
        self.StringLevelArray.append("P----------P---PPP-----------P")
        self.StringLevelArray.append("P----------------------------P")
        self.StringLevelArray.append("PPPPPPPPPPPPPPPPPPPPPPPPPPPPPP")

    def createLevel(self, createdCourseArray, originPos):
        for i in enumerate(self.StringLevelArray):
            for j in enumerate(self.StringLevelArray[i[0]]):
                if(j[1] == "-" or j[1] == "T"):
                    pass
                elif(j[1] == "P"):
                    xPos = originPos[0] + (self.platformWidth * j[0])
                    yPos = originPos[1] - (self.platformHeight * i[0])
                    textureName, spinAngle = self.getTexture(i[0],j[0])
                    createdCourseArray.append(platform.Platform(xPos, yPos, textureName, spinAngle))


    def getTexture(self, i, j):

        L = self.getCharToTheLeft(i,j)
        R = self.getCharToTheRight(i,j)
        U = self.getCharAbove(i,j)
        D = self.getCharBelow(i,j)

        angle = 0
        textureFolder = self.textureFolder
        textureName = self.textureName

        if(U == "-" and D == "-" and L == "-" and R == "-"):
            textureName = "floor tile full grass around.png"

        elif(U == "P" and D == "P" and L == "P" and R == "P"):
            textureName = "floor tile no grass.png"

        elif(U == "P" and D == "-" and L == "-" and R == "-"):
            textureName = "floor tile three parts grass.png"
        elif(U == "-" and D == "P" and L == "-" and R == "-"):
            textureName = "floor tile three parts grass.png"
            angle = 180
        elif(U == "-" and D == "-" and L == "P" and R == "-"):
            textureName = "floor tile three parts grass.png"
            angle = 270
        elif(U == "-" and D == "-" and L == "-" and R == "P"):
            textureName = "floor tile three parts grass.png"
            angle = 90

        elif(U == "-" and D == "P" and L == "P" and R == "P"):
            textureName = "standard floor tile.png"
        elif(U == "P" and D == "-" and L == "P" and R == "P"):
            textureName = "standard floor tile.png"
            angle = 180
        elif(U == "P" and D == "P" and L == "-" and R == "P"):
            textureName = "standard floor tile.png"
            angle = 270
        elif(U == "P" and D == "P" and L == "P" and R == "-"):
            textureName = "standard floor tile.png"
            angle = 90

        elif(U == "P" and D == "-" and L == "P" and R == "-"):
            textureName = "floor tile corner connector.png"
            angle = 270
        elif(U == "P" and D == "-" and L == "-" and R == "P"):
            textureName = "floor tile corner connector.png"
            angle = 180
        elif(U == "-" and D == "P" and L == "-" and R == "P"):
            textureName = "floor tile corner connector.png"
            angle = 90
        elif(U == "-" and D == "P" and L == "P" and R == "-"):
            textureName = "floor tile corner connector.png"
            angle = 0

        elif(U == "P" and D == "P" and L == "-" and R == "-"):
            textureName = "floor tile two parts grass.png"
        elif(U == "-" and D == "-" and L == "P" and R == "P"):
            textureName = "floor tile two parts grass.png"
            angle = 90

        return textureFolder + textureName, angle

    def getCharToTheLeft(self,i, j):
        if(j == 0):
            return "-"

        return self.StringLevelArray[i][j - 1]

    def getCharToTheRight(self,i, j):
        if(j == len(self.StringLevelArray[i])-1):
            return "-"

        return self.StringLevelArray[i][j + 1]

    def getCharAbove(self,i,j):
        if(i == 0):
            return "-"

        return self.StringLevelArray[i - 1][j]

    def getCharBelow(self,i,j):
        if(i == len(self.StringLevelArray)-1):
            return "-"

        return self.StringLevelArray[i + 1][j]