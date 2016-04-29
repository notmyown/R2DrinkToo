import strings as s
from time import sleep

ALL  = -1
HIGH = 1
LOW  = 0

def digitalWrite(pin, mode):
    if pin > 0:
        s.debug("Setze PIN " + s.toString(pin) + " auf " + s.toString(mode))
    
def delay(millis):
    millis_to_seconds = float(millis)/1000
    return sleep(millis_to_seconds)