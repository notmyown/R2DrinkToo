#!/user/bin/env python

import RPi.GPIO as GPIO, time

class CapSense:
    timeout = 10000
    total = 0
    DEBUG = 1
    inPin = 0
    outpin= 0
    
    def __init__(self, ip, op):
        self.inPin = ip
        self.outpin = op
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

    def read(self):
        
        total = 0
        
        # set Send Pin Register low
        GPIO.setup(self.outPin, GPIO.OUT)
        GPIO.output(self.outPin, GPIO.LOW)
        
        # set receivePin Register low to make sure pullups are off 
        GPIO.setup(self.inPin, GPIO.OUT)
        GPIO.output(self.inPin, GPIO.LOW)
        GPIO.setup(self.inPin, GPIO.IN)
        
        # set send Pin High
        GPIO.output(self.outPin, GPIO.HIGH)
        
        # while receive pin is LOW AND total is positive value
        while( GPIO.input(self.inPin) == GPIO.LOW and total < self.timeout ):
            total+=1
        
        if ( total > self.timeout ):
            return -2 # total variable over timeout
            
         # set receive pin HIGH briefly to charge up fully - because the while loop above will exit when pin is ~ 2.5V 
        GPIO.setup( self.inPin, GPIO.OUT )
        GPIO.output( self.inPin, GPIO.HIGH )
        GPIO.setup( self.inPin, GPIO.IN )
        
        # set send Pin LOW
        GPIO.output( self.outPin, GPIO.LOW ) 
    
        # while receive pin is HIGH  AND total is less than timeout
        while (GPIO.input(self.inPin)==GPIO.HIGH and total < self.timeout) :
            total+=1
        
        if ( total >= self.timeout ):
            return -2
        else:
            return total
