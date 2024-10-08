#!/usr/bin/env python
import ADC0832
import time
import RPi.GPIO as GPIO
 
LED = 4
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED, GPIO.OUT)
 
myPWM = GPIO.PWM(LED,10)
myPWM.start(50)
 
def init():
    ADC0832.setup()
 
def loop():
    while True:
        res = ADC0832.getADC(0)
        vol = 3.3/255 * res
        print ('analog value: %03d  ||  voltage: %.2fV' %(res, vol))
        lux = res*100/255
        myPWM.ChangeDutyCycle(lux)
        time.sleep(0.2)
 
        if res < 128:
            print("dark")
            GPIO.output(LED, GPIO.LOW)
        else:
            print("light")
            GPIO.output(LED, GPIO.HIGH)
            
       
        lux = res * 100 / 255
        myPWM.ChangeDutyCycle(lux)
        print(lux)
        time.sleep(0.2)
 
if __name__ == '__main__':
    init()
    try:
        loop()
    except KeyboardInterrupt:
        ADC0832.destroy()
        print ('The end !')