import os
import lirc

class IRManager:
    irsendconstant = "irsend SEND_ONCE "
    def nextCode(self):
        return "Test"
    def sendPowerCD(self):
        os.system(self.irsendconstant + self.JukeboxCode + " " + "Key_Power")
    def sendPowerAmp(self):
        os.system(self.irsendconstant + self.ampCode + " " + "Key_Power")
    def sendChangeCD(self):
        os.system(self.irsendconstant + self.ampCode + " " + "KEY_PLAYER")
    def sendChangeLinePlatine(self):
        os.system(self.irsendconstant + self.JukeboxCode + " " + "KEY_PROG1")
    def sendVolMoins(self):
        os.system(self.irsendconstant+ self.ampCode + " " + "KEY_VOLUMEDOWN")
    def sendVolPlus(self):
        os.system(self.irsendconstant + self.ampCode + " " + "KEY_VOLUMEUP")
    def __init__(self, AmpCodes, JukeboxCode):
        self.ampCode=AmpCodes
        self.jukeboxCode=JukeboxCode

