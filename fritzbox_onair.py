#############################################################################
# FritzboxOnAir
#############################################################################

from subprocess import call
from call_monitor import callmonitor
from phue import Bridge
import psutil
import os

import colorama
from colorama import Fore, Back, Style
from rgb_cie import Converter

import logging

import time

HUEBRIDGEIP = "192.168.178.79"
LIGHTNAME = "OnAir"
PHONENUMBER = "9767518"
LAMP = ""
Volume = ""
IsSkypeActive = False
xy = [0.167, 0.04]
Whitelist=[]


# Executes if calling
def Calling():
    global LAMP
    global xy
    print(Back.GREEN + 'Calling' + Style.RESET_ALL)
    os.system("osascript -e 'set volume output muted true'") # mute system volume
    LAMP.on = True
    LAMP.brightness = 254
    LAMP.transitiontime = 0
    LAMP.xy = xy

# Executes if no calling
def Sleeping():
    global LAMP
    global Volume
    print(Back.CYAN + 'Sleeping' + Style.RESET_ALL)
    os.system("osascript -e 'set volume output muted false'") # unmute system volume
    LAMP.on = False

# Get event from fritzbox
def callBack (self, id, action, details):
    global IsSkypeActive
    global Whitelist

    print("Call: " + str(id) + " - " + action)
    print(str(details))

    # Do nothing at multiple calls
    if (id > 1):
        print("ID1: do nothing")
        return

    # Check if the phonenumber is is in details
    if ("'to': u'" + PHONENUMBER + "'" in str(details) or "'from': u'" + PHONENUMBER + "'" in str(details)):
        # Parse Calling
        if (action == "outgoing" or action == "CALL" or action == "CONNECT" or action == "accepted" or action == "incoming" or action == "RING"):
            if IsSkypeActive == False:
                # Whitelist
                converter = Converter() # for color
                foundInWhitelist = False
                for w in Whitelist:
                    if w in str(details):
                        foundInWhitelist = True
                        break
                if foundInWhitelist == True:
                    print(Fore.LIGHTBLUE_EX + 'Whitelist: True' + Style.RESET_ALL)
                    xy = converter.rgbToCIE1931(0,255,0) # green
                else:
                    print(Fore.LIGHTBLUE_EX + 'Whitelist: False' + Style.RESET_ALL)
                    xy = converter.rgbToCIE1931(255,0,0) # red

                Calling()
        # Parse Sleeping: Checks also if calling is active
        if (action == "closed" or action == "DISCONNECT") and ("CONNECT" in str(details)):
            if IsSkypeActive == False:
                Sleeping()

# Init hue
logging.basicConfig()
print(Fore.LIGHTBLUE_EX + 'Init hue' + Style.RESET_ALL)
Bridge = Bridge(HUEBRIDGEIP)
Bridge.connect() # If the app is not registered and the button is not pressed, press the button and call connect() (this only needs to be run a single time)
Bridge.get_api() # Get the bridge state (This returns the full dictionary that you can explore)
light_names = Bridge.get_light_objects('name') # Get a dictionary with the light name as the key
LAMP = light_names[LIGHTNAME] # Get light object
converter = Converter() # for color

# Whitelist
Whitelist.append("123")
Whitelist.append("456")

# Init call monitor
print(Fore.LIGHTBLUE_EX + 'Init Call monitor' + Style.RESET_ALL)
call = callmonitor() # Create new instance of py-fritz-monitor, Optinal parameters: host, port
call.register_callback (callBack) # Defines a function which is called if any change is detected, unset with call.register_callback (-1)
call.connect() # Connect to fritzbox

print(Fore.LIGHTBLUE_EX + 'Write close to end the script' + Style.RESET_ALL)
while(True):
    # Skype
    time.sleep(10) # only all 10s
    skypeFound = False
    for p in psutil.process_iter():
        if "skype" in p.name().lower():
            skypeFound = True;
            if IsSkypeActive == False:
                print(Fore.LIGHTBLUE_EX + 'Skype open' + Style.RESET_ALL)
                xy = converter.rgbToCIE1931(255,0,0) # red
                Calling()
                IsSkypeActive = True
    if skypeFound == False:
        if IsSkypeActive == True:
            Sleeping()
            IsSkypeActive = False
            print(Fore.LIGHTBLUE_EX + 'Skype close' + Style.RESET_ALL)
