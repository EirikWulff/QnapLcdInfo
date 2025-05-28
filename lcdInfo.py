#!/usr/bin/env python3
import psutil, socket, re, threading, datetime, time, os
from dotenv import load_dotenv
from qnapdisplay import QnapDisplay

Lcd = QnapDisplay()
infoIndex=0
t=None
blankLcdTimeout=30;
load_dotenv()

def getDataArray(network_regex="^eth|^enp|^bond|^vmbr"):
        output = []
        output.append([socket.gethostname(),"Load(5m): "+ str(psutil.getloadavg()[1])])
        output.append(["Last boot:", datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")])
        output.append(["Memory: "+str(psutil.virtual_memory().percent)+"%","Swap: " + str(psutil.swap_memory().percent) + "%"])

        mountpoints = ["/"]
        mountpoints_from_env = os.getenv('MOUNTPOINTS', None)
        if mountpoints_from_env:
                additional_mountpoints = mountpoints_from_env.split('|')
                mountpoints += additional_mountpoints
        
        for mountpoint in mountpoints:
                output.append([mountpoint, "Usage: " + str(psutil.disk_usage(mountpoint).percent) + "%"])

        networks = psutil.net_if_addrs()
        for network in networks:
                if(networks[network][0].netmask and re.search(network_regex,network)):
                        output.append([network, networks[network][0].address])
        return(output)
def timerCallback():
        Lcd.Disable()
def timerReset(t=None):
        if(t):
                t.cancel()
        t = threading.Timer(blankLcdTimeout, timerCallback)
        t.start()
        return t

while(True):
        t = timerReset(t)
        Lcd.Enable()
        data= getDataArray()
        Lcd.Write(0, data[infoIndex][0])
        Lcd.Write(1, data[infoIndex][1])
        if(Lcd.Read() =="Up"):
                delta= -1;
        else:
                delta= +1;
        infoIndex = (infoIndex + delta) % len(data)
