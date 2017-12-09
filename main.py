from temp_Sensor import readTemp as ts
from LCD_Screen import LCDOut as LCD
import RPi.GPIO as GPIO
from speech import Speech as SP
import urllib.request
import time
import os

#Declare Global Variables
VOICE_COMMAND = 9
SNOOZE = 19
DISMISS = 13
VOICE_LED = 7
POWER = 1
SNOOZE_LED = 12
ALARM_LED = 16
ALARM_SET_LED = 20
FAULT_LED = 21
GPIO.setmode(GPIO.BCM)
        
#Input
GPIO.setup(VOICE_COMMAND,GPIO.IN) #Voice Command
GPIO.setup(SNOOZE,GPIO.IN) #Snooze Alarm
GPIO.setup(DISMISS,GPIO.IN) #Dismiss Alarm

#Output
GPIO.setup(VOICE_LED,GPIO.OUT) #Voice Command LED
GPIO.setup(POWER,GPIO.OUT) #Power LED
GPIO.setup(SNOOZE_LED,GPIO.OUT) #AlarmSnooze LED
GPIO.setup(ALARM_LED,GPIO.OUT) #Alarming LED
GPIO.setup(ALARM_SET_LED,GPIO.OUT) #AlarmSet LED
GPIO.setup(FAULT_LED,GPIO.OUT) #Fault LED

GPIO.output(VOICE_LED,False)
GPIO.output(POWER,False)
GPIO.output(ALARM_LED,False)
GPIO.output(SNOOZE_LED,False)
GPIO.output(ALARM_SET_LED,False)
        
def initialize():
    try:
        #Initialize Pins and LED
        updateScreen("Initializing.......","DISPLAY","  Please Wait!  ")
        os.system("cd /home/pi/Desktop/Assembly_Project/assembly")
        os.system("sudo ./light")
        time.sleep(3)
        #Set all LED to Off
        GPIO.output(VOICE_LED,False)
        GPIO.output(POWER,False)
        GPIO.output(ALARM_LED,False)
        GPIO.output(SNOOZE_LED,False)
        GPIO.output(ALARM_SET_LED,False)
        
        #Check for Internet Connection
        updateScreen("Connecting......","DISPLAY","  Please Wait!  ")
##        req = urllib.request.Request('http://google.com')
##        urllib.request.urlopen(req)
##        updateScreen("Syncing Time....","DISPLAY","  Please Wait!  ")
##        os.system("sudo /etc/init.d/ntp stop")
##        os.system("sudo ntpd -q -g")
##        os.system("sudo /etc/init.d/ntp start")
##        print("Time Synced")
        
        #Start Main Programming Thread
        GPIO.output(FAULT_LED,False)
        GPIO.output(POWER,True)
        mainPgrm()

    #No Internet Connection Error Handling   
    except urllib.error.URLError as e:
        GPIO.output(FAULT_LED,True)
        print("Connection Error")
        updateScreen("Connection Error","DISPLAY","No Internet!")
        blink_LED(FAULT_LED,3)
        updateScreen(" Please Connect ","DISPLAY","to the Internet!")
        blink_LED(FAULT_LED,7)
        updateScreen(" Reconnecting.. ","DISPLAY","to the Internet!")
        blink_LED(FAULT_LED,5)
        GPIO.output(FAULT_LED,True)
        initialize()

def blink_LED(name, second):
    state = True
    GPIO.output(name,state)
    for i in range(0,second*2):
        state = not state
        time.sleep(0.5)
        GPIO.output(name,state)
        
def updateTime():
        tme = time.localtime()
        a = ""
        a = a +  str(tme[2]).zfill(2) + "-"
        a = a +  str(tme[1]).zfill(2) + "-"
        a = a +  str(tme[0]) + " "
        a = a +  str(tme[3]).zfill(2) + ":"
        a = a +  str(tme[4]).zfill(2)
        return a, tme
    
def updateScreen(a, b=None, c=None):
    if(b != "DISPLAY"):
        while(b==None):
            b = ts.getTemp()
        c = ("TEMP:" + str(b[0]).zfill(2) + "'C HM:" + str(b[1]).zfill(2) + "%")
    LCD.outPut(a, c)
    GPIO.output(POWER,False)
    time.sleep(1)
    GPIO.output(POWER,True)

def Voice_Button():
    updateScreen("InitializeSpeech","DISPLAY","  Please Wait!  ")
    SP().transcribe()
    time_Str, raw= updateTime()
    updateScreen(time_Str)

def getAlarm():
    file = open("alarm.txt","r")
    alarm = file.readlines()
    file.close()
    return alarm

def alarm_Activate():
    while True:
        LCD.outPut("WAKE UP!!!!!","RISE AND SHINE!!")
        os.system("sudo aplay /home/pi/Desktop/Assembly_Project/ALARM.wav")
        GPIO.output(ALARM_LED,True)
        if (GPIO.input(DISMISS)):
            GPIO.output(ALARM_LED,False)
            LCD.outPut("Alarm Dismissed","Wakey Wakey!")
            time.sleep(2)
            SP().transcribe("morning")
            return()
        elif(GPIO.input(SNOOZE)):
            GPIO.output(ALARM_LED,False)
            os.system("espeak " + "snoozing_for_five_minutes")
            for i in range(0,299):
                LCD.outPut("Snoozing! " + str(300-i),"You are Lazy!")
                blink_LED(SNOOZE_LED,1)
                if(GPIO.input(DISMISS)):
                    GPIO.output(SNOOZE_LED,False)
                    LCD.outPut("Alarm Dismissed","Wakey Wakey!")
                    time.sleep(2)
                    SP().transcribe("morning")
                    return()
        time.sleep(1)
        GPIO.output(ALARM_LED,False)
        time.sleep(1)
            
def mainPgrm():
    oldMin = 0
    alarm = getAlarm()
    print(alarm)
    while True:
        try:
            time_Str, raw= updateTime()
            if(oldMin != raw[4]):
                alarm = getAlarm()
                oldMin = raw[4]
                print("Screen Updated " + time_Str + ":" + str(raw[5]).zfill(2))
                if(alarm[2] == 'Enabled'):
                    GPIO.output(ALARM_SET_LED,True)
                    if(alarm[0] == str(raw[3]).zfill(2) + '\n' and alarm[1] == str(raw[4]).zfill(2) + '\n'):
                        alarm_Activate()
                        SP().disableAlarm()
                        GPIO.output(SNOOZE_LED, False)
                else:
                    GPIO.output(ALARM_SET_LED,False)
                updateScreen(time_Str)
                
            if (GPIO.input(VOICE_COMMAND)):
                Voice_Button()
                
        except IndexError as e:
            file = open("alarm.txt","w")
            file.write("00\n")
            file.write("00\n")
            file.write("Enabled")
            file.close()
            LCD.outPut("Alarm Error!","Alarm Reset!!!")
            blink_LED(FAULT_LED,5)
            LCD.outPut("Alarm Error!","Restarting....")
            blink_LED(FAULT_LED,5)
            initialize()
            
 
           
initialize()
