
class CapSense:
    timeout = 10000
    total = 0
    DEBUG = 1
    inPin = 0
    outpin= 0

    
    def __init__(self, ip, op):
        self.inPin = ip
        self.outpin = op
        
    def read(self):
        self.total += 1
        return self.total
        
        #TEstFunktion aus dem Beipiel von https://bitbucket.org/boblemarin/raspberrypi-capacitive-sensor
    def test(self):
        # init LEDs sequence
        leds = [27,22,23,24,25,10,8,7]
        
        for i in leds:
            GPIO.setup( i,GPIO.OUT )
        
        for l in range(0,10):
            for i in leds:
                GPIO.output( i,GPIO.HIGH )
            time.sleep(0.1)
            for i in leds:
                GPIO.output( i,GPIO.LOW )
            time.sleep(0.1)
        
        # loop
        while True:
            total = 0
            for j in range(0,10):
                total += self.read(18,17);
            for j in range(len(leds)):
                if ( (total-40) / 16 > j ):
                    GPIO.output( leds[j],GPIO.HIGH )
                else:
                    GPIO.output( leds[j],GPIO.LOW )
        
            
        # clean before you leave
        GPIO.cleanup()
