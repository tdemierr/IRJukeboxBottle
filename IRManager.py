import os
import lirc

class IRManager:
    irsendconstant = "irsend SEND_ONCE "
    def nextCode(self):
        return lirc.ne

    def sendPower(self):
        os.system(self.irsendconstant + self.ampCode + " " + "Key_Power")
        print "Power"
    def __init__(self, AmpCodes, JukeboxCode):
        self.ampCode=AmpCodes
        self.jukeboxCode=JukeboxCode

