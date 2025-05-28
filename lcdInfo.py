#!/usr/bin/env python3
import psutil, socket, re, threading, datetime, time, os
from dotenv import load_dotenv
from qnapdisplay import QnapDisplay

Lcd = QnapDisplay()
infoIndex=0
t=None
load_dotenv()
blankLcdTimeout=int(os.getenv('SCREEN_TIMEOUT', 10))

def getDataArray(network_regex="^eth|^enp|^bond|^vmbr"):
        output = []
        output.append([socket.gethostname(),"Load(5m): "+ str(psutil.getloadavg()[1])])
        output.append(["Last boot:", datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")])
        output.append(["Memory: "+str(psutil.virtual_memory().percent)+"%","Swap: " + str(psutil.swap_memory().percent) + "%"])

        mountpoints = ["/"]
        additional_mountpoints = os.getenv('MOUNTPOINTS', None)
        mountpoints_names = os.getenv("MOUNTPOINT_NAMES", None)
        if mountpoints_names:
                mountpoints_names = mountpoints_names.split('|')
        if additional_mountpoints:
                additional_mountpoints = additional_mountpoints.split('|')
                mountpoints += additional_mountpoints
        
        mp_index = 0
        for mountpoint in mountpoints:
                if len(mountpoints_names) > (mp_index + 1):
                        display_name = mountpoints_names[mp_index] + " [" + mountpoint + "]"
                else:
                        display_name = mountpoint
                output.append([display_name, "Usage: " + str(psutil.disk_usage(mountpoint).percent) + "%"])
                mp_index += 1

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
