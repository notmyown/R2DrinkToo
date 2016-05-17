import strings as s

BLUE = 0
RED = -1
GREEN = 1

class GlasSense:
    inPin = 0

    def __init__(self, ip):
        self.inPin = ip
        
    def read(self):
        return -1
        
    def rgb(self, rgbstate):
        if rgbstate==RED:
            s.debug("ROT");
            return
        if rgbstate==GREEN:
            s.debug("GRÜN");
            return
        s.debug("BLAU");