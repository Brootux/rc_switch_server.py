rc_switch_server.py
===================

Server and local-command to easily control rc-switches on Raspberry Pi (RPI).

# Description

This project delivers two components to control elro (or elro-based) remote-control switches (rc-switches):

  * a local command that can control the rc-switches directly (local-command)
  * a server-deamon to control the rc-switches via TCP/IP

So fo example, an Android/IOS/WindowsPhone-App could be written (not done yet) or you can use a home-automation visualization (visu) to control the switches via server-deamon.

Hint:
This projcect is based on the following tutorial http://www.raspberrypi.org/forums/viewtopic.php?f=32&t=32177 . It automates the steps from the tutorial and extends it by setting up a server-deamon.

# Installation
## Hardware setup

The preconfigured setup will require to connect your 433MHz-Transmitter to GPIO-pin-23 of your Raspberry Pi (RPI Pinout, http://www.hobbytronics.co.uk/raspberry-pi-gpio-pinout).

If you connect the Transmitter to another pin, you can later change the pin in software easily!

## Software setup

* Clone this git-repository
  * `git clone https://github.com/Brootux/rc_switch_server.py.git`
  * change into the new directory `cd rc_switch_server.py`
* run the installRCS.sh bash-script (as root or with sudo)
  * `./installRCS.sh`
  * maybe you have to run `sudo chmod 755 installRCS.sh` first!
* You can now use the local-command (rc_switch.py) and server-deamon sould run (you can control that by typing `ss -a`, an entry like `*:6700` should be there)
* Do the last steps, recommended by the install script:
  * Add in `/etc/rc.local` BEFORE the `exit 0` the line `sudo -u pi /usr/local/bin/gpio export 23 out`
  * Restart RPI by `sudo shutdown -r now`


# Command syntax
## Local-Command

The local command excepts the following syntax:

`rc_switch.py [system_code] [unit_code] [on/off]`

The system_code has to be five numbers with dots between them. On/Off means 1/0.

Examples:
  * `rc_switch.py 0.1.0.0.0 1 1` (switch A of system-code 01000 on)
  * `rc_switch.py 0.1.0.0.0 1 0` (switch A of system-code 01000 off)

Hints:
  * You can change hardware-pin of your 433Mhz-Transmitter for local-command in the file `/usr/local/bin/rc_switch.py` after installation!
  * You should rerun `gpio export [GPIO-Pin] out` and/or manipulate the gpio-export command in `/etc/rc.local` when using another GPIO-Pin!


## Server-Command

The server-deamon can be controled via the `service` command:
  * `sudo service rc_switch_server start`
  * `sudo service rc_switch_server stop`

The server-deamon defaultly listens on the following ip/port configuration:
  * ip = `0.0.0.0` (can be accessed from outside of the pi)
  * port = `6700`

Hints:
  * You can change ip/port in the file `/usr/local/rc_switch_server/server.py` after installation!
  * You can change the hardware-pin of your 433Mhz-Transmitter for server-deamon in this file too!
  * You should rerun `gpio export [GPIO-Pin] out` and/or manipulate the gpio-export command in `/etc/rc.local` when using another GPIO-Pin!

## Server-Clients

Any Client, that wants to control a rc-switch has to send a string in the following format to the server-deamon:

`[system_code];[unit_code];[on/off]`

The system_code has to be five numbers with dots between them. On/Off means 1/0, examples:
  * `"0.1.0.0.0;1;1"` (switch A of system-code 01000 on)
  * `"0.1.0.0.0;1;0"` (switch A of system-code 01000 off)

You can turn on/off more than one switch by sending multiple lines, examples:
  * `"0.1.0.0.0;1;1\n0.1.0.0.0;2;1"` (switch A and B of system-code 01000 on)
  * `"0.1.0.0.0;1;1\n0.1.0.0.0;2;0"` (switch A of system-code 01000 on and B of system-code 01000 off)

Hints:
  * There is a example implementation for a client in `/usr/local/rc_switch_server/rc_switch_client_simulator.py` wich takes 1 argument (on/off) and connects to server running on local host. The default system_code and unit_code are 00001 and 1!
