# FritzboxOnAir
### Callmonitor of fritzbox with Mac and Hue integration
If a you take a call, or receive a call, the audio volume of the mac is set to zero, and the given Hue light will light up.

After calling, the light turns off, and the volumne increase to the value before calling 🦄

# Installing
* Enable call monitor of fritzbox with `#96*5*#` (disabling `#96*4*#`)
* Install [volume-osx](https://pypi.python.org/pypi/volume-osx)
* Install [colorama](https://pypi.python.org/pypi/colorama)
* Set your IP address of your hue bridge to variable HUEBRIDGEIP
* Set your light name to variable LIGHTNAME
* Set your internal phone number to the variable PHONENUMBER
* Register your script to the hue bridge: Press the button and run the script
* Startup
    - Open crontab: `export VISUAL=nano; crontab -e`
    - Set your script to run on reboot: `@reboot python3 "/my/path/fritzbox_onair.py"`

# Sources
* Thanks HcDevel for the great [fritzbox library](https://github.com/HcDevel/py-fritz-monitor)
* Thanks russianidiot for the possibility to [mute my Mac](https://github.com/russianidiot/volume-osx.sh.cli)
* Thanks studioimaginaire for [light up](https://github.com/studioimaginaire/phue)
