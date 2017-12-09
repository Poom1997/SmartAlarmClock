import RPi.GPIO as GPIO
import dht11
import time
import datetime

class readTemp:
    def __init__(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.cleanup()
    def getTemp():

        instance = dht11.DHT11(pin=4)

        result = instance.read()
        if result.is_valid():
            #print("Last valid input: " + str(datetime.datetime.now()))
            print("Temperature: %.2d C" % result.temperature)
            print("Humidity: %d %%" % result.humidity)
            return result.temperature,result.humidity
