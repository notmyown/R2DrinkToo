import strings as s

import threading as thread
import time

try:
    import shiftpi.shiftpi as shiftpi
except ImportError:
    import shiftpiMock as shiftpi

try:
    import capread
except ImportError:
    import capreadMock as capread


def enum(**enums):
        return type('Enum', (), enums)

#enumeration of the states of the machine
States = enum(UNKNOWN="UNKNOWN", OK="OK", NOK="NOK")

Pins = enum(GLAS_SENS_SEND=1, GLAS_SENS_RECIEVE=2, PUMP_SERIAL=25, PUMP_CLK=24, PUMP_SRCLK=23 )

class BarBotState:
    glas = False
    
    def __init__(self):
        s.info("init BarBotState")
    

class BarBot:
    
    PUMP_NUM = 8
    PUMP_INTERVAL = 1000
    glascapsense = 0
    state = BarBotState()
    sensingthreadrunning = True

    def __init__(self):
        s.info("init BarBot")
        s.info("init  - initialisiere Pumpen")
        shiftpi.pinsSetup({"ser": Pins.PUMP_SERIAL, "rclk": Pins.PUMP_CLK, "srclk": Pins.PUMP_SRCLK})
        s.info("init  - Glas Sensor")
        self.glascapsense = capread.CapSense(Pins.GLAS_SENS_SEND,Pins.GLAS_SENS_RECIEVE)
        s.info("init  - Starte Sensoren")
        self.sensing()
        
        #do InitVoddoo
        
    def shutdown(self):
        self.sensingthreadrunning = False

    def getPumpNum(self):
        return self.PUMP_NUM
        
    def setPumpNum(self, val):
        self.PUMP_NUM = val
        
    def getPumpInterval(self):
        return self.PUMP_INTERVAL
        
    def setPumpInterval(self, val):
        self.PUMP_INTERVAL = val
        
    def isReady(self):
        s.debug("Wert des GlasSensors: " + s.toString(self.state.glas))
        #return False
        return True
    
    def pumping(self, pumps):
        if not self.isReady():
            return States.NOK
        s.info("Starte Pumpen: " + s.toString(pumps))
        count = 1
        while count > 0:
            s.debug(" - Iteration: " + s.toString(pumps))
            count = 0
            idx = 0
            for pump in pumps:
                if pump > 0:
                    shiftpi.digitalWrite(idx, shiftpi.HIGH)
                    pump -= 1
                    pumps[idx] = pump
                    count+= pump
                else:
                    shiftpi.digitalWrite(idx, shiftpi.LOW)
                idx += 1
            shiftpi.delay(self.PUMP_INTERVAL);
        shiftpi.digitalWrite(shiftpi.ALL, shiftpi.LOW)
        return States.OK
    
    def sensing(self):
        s.info("Starte Sensoren")
        #GlasSensor
        sensingthread = thread.Thread(target=self._readGlasSensor)
        sensingthread.setDaemon(True)
        sensingthread.start()
    
    def _readGlasSensor(self):
        while(self.sensingthreadrunning):
            self.state.glas = self.glascapsense.read()
            time.sleep(1)
        s.debug("Exit readGlasSensor")