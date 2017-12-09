from LCD_Screen import LCDOut as LCD
from temp_Sensor import readTemp as ts
import RPi.GPIO as GPIO
from os import path
import speech_recognition as sr
import espeak
import time
import os

AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "test.wav")

class Speech:
    
    def record(self):
        os.system("arecord -D hw:1,0 -r 24000 -f S16_LE --duration=4 test.wav")
        
    def speak(self, a):
        tmp = a.split()
        st = ''
        for i in range (0, len(tmp)):
            st = st + tmp[i] + '_'
        print(st)
        os.system("espeak " + st)

    def set_alarm(self):
        LCD.outPut("Hour?","tell me")
        time.sleep(2)
        while True:
            h = self.listen()
            if h.isdigit() and int(h) < 24 and int(h) >=0:
                break
            if(h == "cancel"):
                return()
            LCD.outPut("Invalid Number","Try Again")
            self.speak("Invalid value " + h)
            blink_LED(21,2)
            LCD.outPut("Hour?","tell me")
            time.sleep(1)
        print(h)    
        LCD.outPut("Minute?","tell me")
        time.sleep(2)
        while True:
            m = self.listen()
            if m.isdigit() and int(m) < 60 and int(m) >=0:
                break
            if(m == "cancel"):
                return()
            LCD.outPut("Invalid Number","Try Again")
            self.speak("Invalid value " + m)
            blink_LED(21,2)
            LCD.outPut("Minute?","tell me")
            time.sleep(1)
        print(m)    
        file = open("alarm.txt","w")
        file.write(h.zfill(2) + '\n')
        file.write(m.zfill(2) + '\n')
        file.write("Enabled")
        file.close()
        self.speak("Alarm Activated")
        time.sleep(2)
        LCD.outPut("Alarm Activated","")
        GPIO.output(20,True)
        self.speak("Alarm set at" + str(h) +":"+ str(m))
        time.sleep(2)

    def enableAlarm(self):
        file = open("alarm.txt","r")
        h = file.readline()
        m = file.readline()
        file.close()
        file = open("alarm.txt","w")
        file.write(h)
        file.write(m)
        file.write("Enabled")
        file.close()
        LCD.outPut("Alarm Activated","")
        GPIO.output(20,True)
        time.sleep(1)
        self.speak("Alarm set at" + str(h) +"."+ str(m))
        time.sleep(2)
        
    def disableAlarm(self):
        file = open("alarm.txt","r")
        h = file.readline()
        m = file.readline()
        file.close()
        file = open("alarm.txt","w")
        file.write(h)
        file.write(m)
        file.write("Disabled")
        file.close()
        LCD.outPut("Alarm Deactivated","")
        GPIO.output(20,False)
        time.sleep(2)
    
    def listen(self):
        GPIO.output(7,True)
        GPIO.output(21,False)
        LCD.outPut("Speak Command..", " Listening... ")
        self.record()
        GPIO.output(7,False)
        LCD.outPut("Recognizing..", "  Please Wait!  ")

        r = sr.Recognizer()
        with sr.AudioFile(AUDIO_FILE) as source:
            audio = r.record(source) # read the entire audio file

        try:
            # for testing purposes, we're just using the default API key
            # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
            # instead of `r.recognize_google(audio)`
            print("Google Speech Recognition thinks you said " + "\"" + r.recognize_google(audio) + "\"")
        except sr.UnknownValueError:
            LCD.outPut("Unknown", "Command.....")
            blink_LED(21,5)
            GPIO.output(21,True)
            return("unknown")
        except sr.RequestError as e:
            LCD.outPut("Unknown", "Error......")
            blink_LED(21,7)
            GPIO.output(21,True)
            return("cancel")
        except sr.ValueError as e:
            while True:
                LCD.outPut("Connection Error","No Internet!")
                blink_LED(21,7)
                LCD.outPut(" Please Connect ","to the Internet!")
                blink_LED(21,7)
                LCD.outPut(" Please Restart ","the Device!")
                blink_LED(21,7)
            return("cancel")

        text = r.recognize_google(audio)
        return text
        
    def transcribe(self, text = ""):
        if(text == ""):
            text = self.listen()
        if "morning" in text:
            LCD.outPut("Hi There!", "Good Morning!")
            self.speak("Hello")
            text = "what time temperature"
            if(text == ""):
                return()

        if "what" in text or "what's" in text:
            if "time" in text:
                t = time.localtime()
                a = ""
                a = a +  str(t[2]).zfill(2) + "-"
                a = a +  str(t[1]).zfill(2) + "-"
                a = a +  str(t[0]) + " "
                a = a +  str(t[3]).zfill(2) + ":"
                a = a +  str(t[4]).zfill(2)
                print(a)
                # 06-12-2016 14:56
                month = ['January','Febuary','March','April','May','June',
                         'July','August','September','October','November',
                         'December']
                thisTime = a.split(' ')
                date = thisTime[0].split('-')
                outText = "It is "
                outText += str(int(date[0])) + " "
                outText += str(month[int(date[1])-1]) + " "
                outText += date[2] + " "

                clockTime = thisTime[1].split(':')
                ampm = 'AM'
                if int(clockTime[0]) > 12:
                    ampm = 'PM'
                    clockTime[0] = int(clockTime[0]) % 12
                if int(clockTime[0]) == 0:
                    clockTime[0] = '12'

                outText += str(clockTime[0]) + " " + str(clockTime[1]) + " " + ampm
                print(outText)
                
                self.speak(outText)
                if(text != "what time temperature"):
                    return()
                
            if "temperature" in text:
                b = ts.getTemp()
                while(b == None):
                    b = ts.getTemp()
                b = "the temperature is"+ str(b[0]).zfill(2) +"degrees"
                self.speak(b)
                return()

        elif "set" in text:
            if "alarm" in text:    
                self.set_alarm()

        elif "cancel" in text:
            return()        

        elif "turn off" in text or "disable" in text or "deactivate" in text and "alarm" in text:
            self.disableAlarm()
            self.speak("Alarm Deactivated")
            return()

        elif "turn on" in text or "enable" in text or "activate" in text and "alarm" in text:
            self.enableAlarm()
            self.speak("Alarm Activated")
            return()

        elif "shutdown" in text or "activate override shutdown" in text or "initiate override shutdown" in text or "terminate" in text:
            LCD.outPut("Shutting Down","  Good Bye! ")
            self.speak("Shutting Down and Good Bye")
            time.sleep(2)
            LCD.outPut("If all LED are off","Disconnect power.")
            os.system("sudo shutdown -h now")
        else:
            text = "unknown"

        if(text == "cancel" or text == "unknown"):
            LCD.outPut("Unknown Command","  :(  ")
            self.speak("I dont understand you")
            blink_LED(21,3)
            GPIO.output(21,False)
            return()

def blink_LED(name, second):
    state = True
    GPIO.output(name,state)
    for i in range(0,second*2):
        state = not state
        time.sleep(0.5)
        GPIO.output(name,state)
        
