#!/usr/bin/env python
# -*- coding:utf8 -*-

import socket, sys

if __name__ == '__main__':
	# Setup for ip and port
	host = "localhost"
    port = 6700
	
	# Create socket instance
    s = socket.socket()
    
    # Connect to rc_switch_server via socket
    s.connect((host, port))
    
    # Simplyfi socket writing
    s = s.makefile()
    
    # Send command to rc_switch_server
    s.write("0.0.0.0.1;1;%s" % sys.argv[1])
    s.flush()
    
    # Close server-connection
    s.close()
