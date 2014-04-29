#!/usr/bin/env python
# -*- coding:utf8 -*-

import socket
import os, sys

from LibRemoteSwitch import RemoteSwitch


if __name__ == '__main__':
	# Change the pin according to your wiring  of 433MHz transmitter
	# Hint:
    #       You should rerun gpio export [GPIO-Pin] out and/or
    #       manipulate the gpio-export command in /etc/rc.local when
    #       using another GPIO-Pin!
    pin = 23
    ip = ""
    port = 6700
	
    # Prepare creation of pid file
    pid = str(os.getpid())
    pidfile = "/tmp/rc_switch_server.pid"
    
    # Create pid file if ther is none
    if os.path.isfile(pidfile):
        print "server already running, exiting"
        sys.exit(1)
    else:
        file(pidfile, 'w').write(pid)
    
    # Setup socket for communication
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serverSocket.bind((ip, port))
    serverSocket.listen(1)
    
    
    
    # Main server loop
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
				print
                print "incorrect number of fields was delivered, skipping!"
                print "hint: format is \"[system_code];[unit_code];[state]\""
                break
            
            # Split system_code field at field separator "."
            system_code_str = splitLine[0].split(".")
            
            # Check if the correct number of system_code numbers was delivered
            if(len(system_code_str) != 5):
				print
                print "wrong system_code was delivered, skipping!"
                break
            
            # Create system_code list
            system_code = []
            
            # Parse system_code to int
            for number in system_code_str:
                system_code.append(int(number))
            
            # Get unit_code
            unit_code = int(splitLine[1])
            
            if(unit_code > 31 or unit_code < 0):
				print
                print "wrong unit_code was delivered, skipping!"
                break
            
            # Get state
            state = int(splitLine[2])
            
            if(state > 1 or state < 0):
                print "wrong state was delivered, skipping!"
                break
            
            # Print out the received fields
            print
            print "received fields:"
            print "sender:\t\"%s\"" % (str(address))
            print "syst_code:\t", system_code
            print "unit_code:\t", unit_code
            print "state:\t", state
            
            # Setup switching-unit
            device = RemoteSwitch(unit_code, system_code, pin)
            
            # Send switching signal
            if int(state) == 1:
                print "switching on"
                device.switchOn()
            else:
                print "switching off"
                device.switchOff()
            
            # Free the RemoteSwitch-Library
            del device
        
        # Close connection to client
        clientSocket.close()
