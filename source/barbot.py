import strings as s

import threading as thread
import time

try:
    import shiftpi.shiftpi as shiftpi
except ImportError:
    import shiftpiMock as shiftpi

try:
    import glassensor
except ImportError:
    import glassensorMock as glassensor


def enum(**enums):
        return type('Enum', (), enums)

#enumeration of the states of the machine
States = enum(UNKNOWN="UNKNOWN", OK="OK", NOK="NOK", NOGLAS="NOGLAS")

Pins = enum(GLAS_SENS=2, PUMP_SERIAL=25, PUMP_CLK=24, PUMP_SRCLK=23 )

class BarBotState:
    glas = False
    
    def __init__(self):
        s.info("init BarBotState")
    

class BarBot:
    
    PUMP_NUM = 8
    PUMP_INTERVAL = 1000
    glassense = 0
    state = BarBotState()
    sensingthreadrunning = True

    def __init__(self):
        s.info("init BarBot")
        state = BarBotState()
        s.info("init  - initialisiere Pumpen")
        shiftpi.pinsSetup({"ser": Pins.PUMP_SERIAL, "rclk": Pins.PUMP_CLK, "srclk": Pins.PUMP_SRCLK})
        s.info("init  - Glas Sensor")
        self.glassense = glassensor.GlasSense(Pins.GLAS_SENS)
        s.info(" - setze auf Blue")
        self.glassense.rgb(glassensor.BLUE)
        s.info("init  - Starte Sensoren")
        
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
        return self.state.glas
    
    def state(self):
        return self.state
    
    def pumping(self, pumps):
        if not self.isReady():
            self.glassense.rgb(glassensor.RED)
            s.info(" - setze auf Rot")
            return States.NOK
        s.info("Starte Pumpen: " + s.toString(pumps))
        s.info(" - setze auf Grün")
        self.glassense.rgb(glassensor.GREEN)
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
        s.info(" - setze auf Blue")
        self.glassense.rgb(glassensor.BLUE)
        return States.OK