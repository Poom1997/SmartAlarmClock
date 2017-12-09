from time import sleep
from Adafruit_CharLCD import Adafruit_CharLCD

class LCDOut:
    def __init__(self):
        pass
    def outPut(str1, str2):
        lcd= Adafruit_CharLCD(rs = 15, en=14, d4 =18, d5 = 23, d6 = 24, d7 =25,cols = 16, lines =2)
        lcd.clear()
        lcd.message(str1 + "\n" + str2)
