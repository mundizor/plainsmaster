class S_ClientMessageTranslator:
    def __init__(self):
        pass


    @staticmethod
    def translateSpawnPosAndEnemytype(msg):
        msg = msg[2:]

        xpos, msg = S_ClientMessageTranslator.translateUntilSign(msg, "y")
        ypos, msg = S_ClientMessageTranslator.translateUntilSign(msg, "T")
        moduleName, msg = S_ClientMessageTranslator.translateUntilSign(msg, ".")
        className = msg

        return xpos, ypos, moduleName, className


    @staticmethod
    def translateUntilSign(msg, stopsign):
        looopnr = 0
        brokenOutString = ""

        for i in msg:
            looopnr+=1
            if(i == stopsign):
                break
            brokenOutString += i

        msg = msg[looopnr:]

        return brokenOutString, msg