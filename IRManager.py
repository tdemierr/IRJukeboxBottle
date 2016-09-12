import os
import lirc
import time

class IRManager:
    irsendconstant = "irsend SEND_ONCE "
    keynumber = "KEY_"

    def sendCode(self, device, directives):
        os.system(self.irsendconstant + device + " " + directives)
        time.sleep(.250)
    def nextCode(self):
        return "Test"
    def sendPowerCD(self):
        self.sendCode(self.jukeboxCode, "KEY_POWER")
    def sendPowerAmp(self):
        self.sendCode(self.ampCode, "KEY_POWER")
    def sendChangeCD(self):
        self.sendCode(self.ampCode, "KEY_PLAYER")
    def sendChangeLinePlatine(self):
        self.sendCode(self.ampCode, "KEY_PROG1")
    def sendVolMoins(self):
        self.sendCode(self.ampCode, "KEY_VOLUMEDOWN")
    def sendVolPlus(self):
        self.sendCode(self.ampCode, "KEY_VOLUMEUP")
    def changeDisc(self, code):
        self.sendCode(self.jukeboxCode, "KEY_MEDIA")
        for digit in str(code):
            self.sendCode(self.jukeboxCode, self.keynumber+digit)
        self.sendCode(self.jukeboxCode, "KEY_ENTER")
    def __init__(self, AmpCodes, JukeboxCode):
        self.ampCode=AmpCodes
        self.jukeboxCode=JukeboxCode

