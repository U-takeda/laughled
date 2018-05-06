#!/usr/bin/env python
import subprocess
import RPi.GPIO as GPIO
import time
import threading
import re
import shutil
import urllib
import datetime
import socket

hostname = socket.gethostname()
servername = "aml195035.local:8000"
actime = 0

#cmd = 'export ALSADEV=plughw:2; julius -h gmmdefs -w class.txt -wsil noise noise noise -input alsa -lv 900 -record ./save'
#cmd = 'export ALSADEV=plughw:2; julius -h gmmdefs -w class.txt -input alsa -lv 900 -record ./save'
cmd = 'julius -h gmmdefs -w class.txt -input alsa -lv 6000 -record ./save'

def LEDon():
        GPIO.output(11, True) 
        time.sleep(1.0)
        GPIO.output(11, False)         
        
def LEDchika():
        GPIO.output(11, True)
        time.sleep(0.1)
        GPIO.output(11, False)
        time.sleep(0.1)
        GPIO.output(11, True)
        time.sleep(0.1)
        GPIO.output(11, False)

def server(so):
	threading.Thread(target=LEDon).start()
	src = open("./save/%s" % filename, "r")
	dst = open("./" + so + "/%s" % filename, "w")
	shutil.copyfileobj(src, dst)
	urllib.urlopen("http://" + servername + "/httpserver/" + so + "/" + hostname + "/" + str(actime) + "/")

if __name__ == '__main__':
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(11, GPIO.OUT)

        p = subprocess.Popen(cmd, shell=True, close_fds=True,
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT)
        while True:
                line = p.stdout.readline()
                #print ("cmd: " + line)
        		
                if re.search(r"recorded to", line):
                        filenameSearch = re.search("(\d\d\d\d\.\d\d\d\d\.\d\d\d\d\d\d\.wav)", line)
                        stoptime = datetime.datetime.now().strftime("%H%M%S.") + "%04d" %(datetime.datetime.now().microsecond // 1000)
                        rectime = re.search("\d\d\d\d\d\d", line)
                        recedtime = rectime.group()
                        actime = float(stoptime) - float(recedtime)
                        #print ("stop" + stoptime)
                        #print ("go" + recedtime)
                        #print ("result" + str(actime))
                        
                        filename = filenameSearch.group(1)
                    	#print ("file: " + filename)

                if re.search(r"sentence1:", line):
                        print ("result: " + line)
                        if re.search(r"laugh", line):
                                server("laugh")

                        if re.search(r"adult", line):
                        		server("voice")
  
                        else:
                                server("noise")