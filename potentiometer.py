#!/usr/bin/env python
import ADC0832
import time
import RPi.GPIO as GPIO

# Set up the LED pin and PWM frequency
LED_PIN = 4  # Pin connected to LED (alarm LED)
PWM_FREQ = 1000  # 1kHz frequency for PWM

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LED_PIN, GPIO.OUT)  # Set up alarm LED pin

    # Set up PWM for the LED
    global pwm_led
    pwm_led = GPIO.PWM(LED_PIN, PWM_FREQ)
    pwm_led.start(0)  # Start with 0% duty cycle (LED off)

    ADC0832.setup()

def loop():
    while True:
        # Read ADC value from potentiometer
        res = ADC0832.getADC(0)  # ADC channel 0
        vol = 3.3 / 255 * res  # Convert to voltage
        print('Digital value: %03d  ||  Voltage: %.2fV' % (res, vol))

        # Scale ADC value (0-255) to PWM duty cycle (0-100%)
        duty_cycle = res * 100 / 255
        pwm_led.ChangeDutyCycle(duty_cycle)  # Adjust LED brightness

        # Check luminosity level and control the alarm LED
        if res < 10:  # Assuming the ADC value correlates directly to Lux
            print("dark")
            GPIO.output(LED_PIN, GPIO.LOW)  # Turn off alarm LED
        else:
            print("light")
            GPIO.output(LED_PIN, GPIO.HIGH)  # Turn on alarm LED

        time.sleep(0.2)  # Small delay for smoother updates

def destroy():
    pwm_led.stop()  # Stop PWM
    GPIO.cleanup()  # Clean up GPIO

if __name__ == '__main__':
    try:
        setup()
        loop()
    except KeyboardInterrupt:
        destroy()
        print('The end!')
