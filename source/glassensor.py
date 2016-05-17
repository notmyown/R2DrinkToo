import RPi.GPIO as GPIO, time
import strings as s

BLUE = 0
RED = -1
GREEN = 1

class GlasSense:
    inPin = 0
    redPin = 0
    greenPin = 0
    bluePin = 0

    def __init__(self, ip,red,green,blue):
        self.inPin = ip
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.inPin, GPIO.IN)
        GPIO.setup(self.redPin, GPIO.OUT)
        GPIO.setup(self.greenPin, GPIO.OUT)
        GPIO.setup(self.bluePin, GPIO.OUT)
        
    def read(self):
        if GPIO.input(self.inPin)==GPIO.HIGH:
            return GREEN
        return RED
        
    def rgb(self, rgbstate):
        if rgbstate==RED:
            s.debug("Rot");
            GPIO.output(self.redPin, GPIO.HIGH);
            GPIO.output(self.greenPin, GPIO.LOW);
            GPIO.output(self.bluePin, GPIO.LOW);
            return
        if rgbstate==GREEN:
            s.debug("GRÜN");
            GPIO.output(self.redPin, GPIO.LOw);
            GPIO.output(self.greenPin, GPIO.HIGH);
            GPIO.output(self.bluePin, GPIO.LOW);
            return
        s.debug("BLUE");
        GPIO.output(self.redPin, GPIO.LOW);
        GPIO.output(self.greenPin, GPIO.LOW);
        GPIO.output(self.bluePin, GPIO.HIGH);
        
