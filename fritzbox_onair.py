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

HUEBRIDGEIP = "192.168.178.79"
LIGHTNAME = "OnAir"
PHONENUMBER = "9767518"
Volume = ""
IsSkypeActive = False


# Executes if calling
def Calling():
    print(Back.GREEN + 'Calling' + Style.RESET_ALL)
    os.system("osascript -e 'set volume output muted true'") # mute system volume
    Bridge.set_light(LIGHTNAME,'on', True) # turn light on

# Executes if no calling
def Sleeping():
    global Volume
    print(Back.CYAN + 'Sleeping' + Style.RESET_ALL)
    os.system("osascript -e 'set volume output muted false'") # unmute system volume
    Bridge.set_light(LIGHTNAME,'on', False) # turn light off

# Get event from fritzbox
def callBack (self, id, action, details):
    global IsSkypeActive

    print("Call: " + str(id) + " - " + action)
    print(details)

    # Do nothing at multiple calls
    if (id > 1):
        print("ID1: do nothing")
        return

    # Check if the phonenumber is is in details
    if ("'to': u'" + PHONENUMBER + "'" in str(details) or "'from': u'" + PHONENUMBER + "'" in str(details)):
        # Parse Calling
        if (action == "outgoing" or action == "CALL" or action == "CONNECT" or action == "accepted" or action == "incoming" or action == "RING"):
            if IsSkypeActive == False:
                Calling()
        # Parse Sleeping: Checks also if calling is active
        if (action == "closed" or action == "DISCONNECT") and ("CONNECT" in str(details)):
            if IsSkypeActive == False:
                Sleeping()

# Init hue
print(Fore.LIGHTBLUE_EX + 'Init hue' + Style.RESET_ALL)
Bridge = Bridge(HUEBRIDGEIP)
Bridge.connect() # If the app is not registered and the button is not pressed, press the button and call connect() (this only needs to be run a single time)
Bridge.get_api() # Get the bridge state (This returns the full dictionary that you can explore)

# Init call monitor
print(Fore.LIGHTBLUE_EX + 'Init Call monitor' + Style.RESET_ALL)
call = callmonitor() # Create new instance of py-fritz-monitor, Optinal parameters: host, port
call.register_callback (callBack) # Defines a function which is called if any change is detected, unset with call.register_callback (-1)
call.connect() # Connect to fritzbox

print(Fore.LIGHTBLUE_EX + 'Write close to end the script' + Style.RESET_ALL)
while(True):
    # Skype
    skypeFound = False
    for p in psutil.process_iter():
        if "skype" in p.name().lower():
            skypeFound = True;
            if IsSkypeActive == False:
                print(Fore.LIGHTBLUE_EX + 'Skype open' + Style.RESET_ALL)
                Calling()
                IsSkypeActive = True
    if skypeFound == False:
        if IsSkypeActive == True:
            Sleeping()
            IsSkypeActive = False
            print(Fore.LIGHTBLUE_EX + 'Skype close' + Style.RESET_ALL)
