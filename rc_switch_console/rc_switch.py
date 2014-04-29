#!/usr/bin/env python

from LibRemoteSwitch import RemoteSwitch
import sys

if __name__ == '__main__':
    # Change the pin according to your wiring  of 433MHz transmitter
    # Hint:
    #       You should rerun gpio export [GPIO-Pin] out and/or
    #       manipulate the gpio-export command in /etc/rc.local when
    #       using another GPIO-Pin!
    pin = 23
    
    # Check if the correct number of fields was given
    if len(sys.argv) < 4:
        print
        print "usage: %s [system_code] [unit_code] [state]" % (sys.argv[0])
        print
        print "example: '%s 0.0.0.0.1 2 1' switches unit 2 of system \"0 0 0 0 1\" on" % (sys.argv[0])
        print
        sys.exit(1)
    
    # Get user input for system_code
    system_code_str = sys.argv[1].split(".")
    
    # Check if the correct number of system_code numbers was delivered
    if (len(system_code_str) != 5):
        print
        print "Wrong ammount or false setup for [system_code]!"
        print "system_code has to be five numbers with \".\" between"
        print
        print "example: '%s 0.0.0.0.1 2 1' switches unit 2 of system \"0 0 0 0 1\" on" % (sys.argv[0])
        print
        sys.exit(1)
    
    # Create system_code list
    system_code = []
    
    # Parse system_code to int
    for number in system_code_str:
        system_code.append(int(number))
    
    # Get unit_code
    unit_code = int(sys.argv[2])
    
    if(unit_code > 31 or unit_code < 0):
		print
        print "Wrong setup for [unit_code]!"
        print "unit_code can just lie between 0 and 31!"
        print
        sys.exit(1)
    
    # Get state
    state = int(sys.argv[3])
    
    if(state > 1 or state < 0):
		print
        print "Wrong setup for [state]!"
        print "state can just lie between 0 and 1!"
        print
        sys.exit(1)
    
    # Setup switching-unit
    device = RemoteSwitch(unit_code, system_code, pin)
    
    # Send switching signal
    if (state == 1):
        print "Switching ", system_code, unit_code, " on!"
        device.switchOn()
    else:
        print "Switching ", system_code, unit_code, " off!"
        device.switchOff()
