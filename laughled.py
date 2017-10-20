#!/usr/bin/env python
import subprocess
import RPi.GPIO as GPIO
import time
import threading
import re
import shutil
import urllib


#cmd = 'export ALSADEV=plughw:2; julius -h gmmdefs -w class.txt -wsil noise noise noise -input alsa -lv 900 -record ./save'
#cmd = 'export ALSADEV=plughw:2; julius -h gmmdefs -w class.txt -input alsa -lv 900 -record ./save'
cmd = 'julius -h gmmdefs -w class.txt -input alsa -record ./save'

def LEDon():
        GPIO.output(11, True)        

def LEDoff():
        GPIO.output(11, False)        
        
def LEDchika():
        GPIO.output(11, True) 
        time.sleep(0.1)
        GPIO.output(11, False)
        time.sleep(0.1)
        GPIO.output(11, True) 
        time.sleep(0.1)
        GPIO.output(11, False)
        
if __name__ == '__main__':
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(11, GPIO.OUT)

        p = subprocess.Popen(cmd, shell=True, close_fds=True,
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT)
        while True:
                line = p.stdout.readline()
                #print "cmd: " + line,
        
                if re.search(r"recorded to", line):
                        filenameSearch = re.search("(\d\d\d\d\.\d\d\d\d\.\d\d\d\d\d\d\.wav)", line)
                        filename = filenameSearch.group(1)
                        print "file: " + filename

                if re.search(r"sentence1:", line):
                        print "result: " + line,
                        if re.search(r"laugh", line):
                                LEDon()
                                urllib.urlopen('http://192.168.152.111:8000/httpserver/laugh/')
                                src = open("./save/%s" % filename, "r")
                                dst = open("./laugh/%s" % filename, "w")
                                shutil.copyfileobj(src, dst)
                                threading.Timer(3, LEDoff).start()
                        else:
                                threading.Thread(target=LEDchika).start()
                                urllib.urlopen('http://192.168.152.111:8000/httpserver/voice')

                                
                if not line and p.poll() is not None:
                        break
                        
        p.wait()
        print "Done."
