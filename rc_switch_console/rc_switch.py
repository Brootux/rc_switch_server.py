#!/usr/bin/env python

from LibRemoteSwitch import RemoteSwitch

if __name__ == '__main__':
    import sys
    
    # change the pin according to your wiring
    pin = 23
    
    if len(sys.argv) < 4:
        print
        print "usage: %s [system_code] [unit_code] [state]" % (sys.argv[0])
        print
        print "example: '%s 0.0.0.0.1 2 1' switches unit 2 of system \"0 0 0 0 1\" on" % (sys.argv[0])
        print
        sys.exit(1)
    
    # get and check user input for system_code
    system_code_str = sys.argv[1].split(".")
    
    if (len(system_code_str) != 5):
        print
        print "Wrong ammount or false setup for system_code!"
        print "system_code has to be five numbers with \".\" between"
        print
        print "example: '%s 0.0.0.0.1 2 1' switches unit 2 of system \"0 0 0 0 1\" on" % (sys.argv[0])
        print
        sys.exit(1)
    
    # get the system code
    system_code = []
    for number in system_code_str:
        system_code.append(int(number))
    
    # get unit code
    unit_code = int(sys.argv[2])
    
    # get target state
    state = int(sys.argv[3])
    
    # create switching device
    device = RemoteSwitch(unit_code, system_code, pin)
    
    # do the switching
    if (state == 1):
        print "Switching ", system_code, unit_code, " on!"
        device.switchOn()
    else:
        print "Switching ", system_code, unit_code, " off!"
        device.switchOff()
