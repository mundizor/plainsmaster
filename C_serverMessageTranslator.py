class C_ServerMessageTranslator:
    def __init__(self):
        pass


    @staticmethod
    def translatePositionMessage(msg):
        xPosString = ""
        yPosString = ""
        indexString = ""

        #deletes the PX from the start of the string.
        msg = msg[2:]

        loopnr = 0
        for i in msg:
            loopnr += 1
            if(i == 'y'):
                break
            xPosString += i

        msg = msg[loopnr:]

        loopnr = 0
        for i in msg:
            loopnr += 1
            if(i == 'i'):
                break
            yPosString += i

        msg = msg[loopnr:]

        indexString = msg

        x = int(float(xPosString))
        y = int(float(yPosString))
        index = int(indexString)

        return index, x, y

    @staticmethod
    def translateEntitySpawningMessage(msg):
        #finds the module name
        moduleName = ""
        loopnr = 0
        for i in msg:
            loopnr += 1
            if(i == '.'):
                break
            moduleName += i

        msg = msg[loopnr:]

        #finds the classname
        className = ""
        loopnr = 0
        for i in msg:
            loopnr += 1
            if(i == '/'):
                break
            className += i

        msg = msg[loopnr:]

        #removes the "Px" from the start of the message
        msg = msg[2:]

        #finds the xposition
        xPosString = ""
        loopnr = 0
        for i in msg:
            loopnr += 1
            if(i == '/'):
                break
            xPosString += i

        msg = msg[loopnr:]

        #removes the "Py" from the start of the message
        msg = msg[2:]
        yPosString = msg

        x = int(float(xPosString))
        y = int(float(yPosString))

        return moduleName, className, x, y

    @staticmethod
    def translateNumberInTeams(msg):
        NRT = ""

        msg = msg[1:]
        looopnr = 0
        for i in msg:
            looopnr+=1
            if(i == "F"):
                break
            NRT += i

        NRF = msg[looopnr:]

        return NRT, NRF


