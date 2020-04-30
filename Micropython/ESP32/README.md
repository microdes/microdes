# ReadMe

## Port Connections

You can connect to your board by using the micro USB port 

## Install Dependencies

> sudo apt-get install python3
>
> sudo pip3 install esptool
>
> sudo pip3 install adafruit-ampy
>
> sudo pip3 install pyserial

## Deploy Micropython on Board

First erase the flash:

> esptool.py --port /dev/ttyUSB0 erase_flash

Then upload the firmware:

> esptool.py --chip esp32 --port /dev/ttyUSB0 write_flash -z 0x1000 microdes_ESP32.bin

## Debug

You can use picocom tool to interact with Python Prompt (REPL) of device.

> picocom /dev/ttyUSB0 -b115200

Note: "-b arguement determines the baudrate"


Microdes Team