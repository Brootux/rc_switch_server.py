#!/usr/bin/env python
# -*- coding:utf8 -*-

import socket
import os, sys

from LibRemoteSwitch import RemoteSwitch


if __name__ == '__main__':
    # prepare creation of pid file
    pid = str(os.getpid())
    pidfile = "/tmp/rc_switch_server.pid"
    
    # create pid file if ther is none
    if os.path.isfile(pidfile):
        print "server already running, exiting"
        sys.exit(1)
    else:
        file(pidfile, 'w').write(pid)
    
    # setup socket for communication
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serverSocket.bind(("", 6700))
    serverSocket.listen(1)
    
    # change the gpio-pin accpording to your wiring of 433MHz transmitter
    pin = 23
    
    # main server loop
    while(True):
        # Wait for incomming connections
        (clientSocket, address) = serverSocket.accept()
        
        # Change socket to read/write to it like to a file
        cs = clientSocket.makefile()
        
        # Go through all received instructions
        for line in cs.readlines():
            # Separate Instruction into its fields system_code, unit_code, state
            splitLine = line.split(";")
            
            # Check if the correct number of fields was delivered
            if(len(splitLine) != 3):
                print "uncorrect number of fields was delivered, skipping!"
                break
            
            # Split system_code field at field separator "."
            system_code_str = splitLine[0].split(".")
            
            # Check if the correct number of system_code numbers was delivered
            if(len(system_code_str) != 5):
                print "wrong number of system_code numbers was delivered, skipping!"
                break
            
            # Create system_code list
            system_code = []
            
            # Parse system_code to int
            for number in system_code_str:
                system_code.append(int(number))
            
            # Get unit_code
            unit_code = int(splitLine[1])
            
            # Get state
            state = int(splitLine[2])
            
            # Setup switching-unit
            device = RemoteSwitch(unit_code, system_code, pin)
            print "device file created:"
            print device
            print "fields:"
            print "cod2: ", system_code
            print "code: ", unit_code
            print "stat: ", state
            
            # Send switching signal
            if int(state) == 1:
                print "on"
                device.switchOn()
            else:
                print "off"
                device.switchOff()
            
            del device
        
        clientSocket.close()
