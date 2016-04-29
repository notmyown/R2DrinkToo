import strings as s
import shiftpiMock as shiftpi
#import shiftpi.shiftpi as shiftpi

def enum(**enums):
        return type('Enum', (), enums)

#enumeration of the states of the machine
States = enum(UNKNOWN="UNKNOWN", OK="OK", NOK="NOK")

class BarBot:
    
    PUMP_NUM = 8
    PUMP_INTERVAL = 1000

    def __init__(self):
        s.info("init BarBot")
        #do InitVoddoo
        
    def getPumpNum(self):
        return self.PUMP_NUM
        
    def setPumpNum(self, val):
        self.PUMP_NUM = val
        
    def isReady(self):
        #TODO prüfen ob der BarBot starten kann
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
                    pump = pump - 1
                    pumps[idx] = pump
                    count = count + pump
                else:
                    shiftpi.digitalWrite(idx, shiftpi.LOW)
                idx = idx + 1
            shiftpi.delay(self.PUMP_INTERVAL);
        shiftpi.digitalWrite(shiftpi.ALL, shiftpi.LOW)
        return States.OK
        