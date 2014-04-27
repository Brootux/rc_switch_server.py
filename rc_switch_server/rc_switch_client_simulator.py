#!/usr/bin/env python
# -*- coding:utf8 -*-

import socket, sys

if __name__ == '__main__':
	
    s = socket.socket()
    
    host = "localhost"
    port = 6700
    
    s.connect((host, port))
    
    s = s.makefile()
    
    s.write("0.0.0.0.1;1;%s" % sys.argv[1])
    s.flush()
    
    s.close()
