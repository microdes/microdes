# microdes
Vulnerability Scanning Tool for Microcontrollers

## About

Microdes is released under GNU General Public License v3.0. Microdes license allows free usage by end users.

Microdes tool is aimed for turning any kind of microcontroller into a vulnerability scanning tool.
 
## Important

Current release of the Microdes tool is a test version.

This release is not completely stable and has limitations.

Ip range is limited by 192.168.0.1/24.

Only first 1000 ports will be scanned.

Only VSFTPD 2.3.4 vulnerability could be detected.

## Usage

Firstly you should install Micropython to your microcontroller. You can find device specific releases of micropython under Micropython file. You can find device specific installation guides under device files.

Run microdes.py file with required arguements:

> python3 microdes.py -H |server-ip| -p |server-port| -wN |Wireless Name| -wP |Wireless Password|

Two different Python files will be generated after running the microdes.py file. These files are server.py and main.py.

Run server.py

> python3 server.py

Upload the main.py to microcontroller

> ampy --port serial-port-name put main.py 

Note: "Board automatically runs main.py file after boot"

Microdes Team




