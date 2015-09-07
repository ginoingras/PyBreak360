#!/usr/bin/env python
# -*- coding: utf8 -*-
import os, sys, socket

#works only fro windows
IPaddressLocal_all = [ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")]
IPaddressLocal_all.append('127.0.0.1')
IPaddressLocal_all.append('localhost')

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#s.connect(("google.com",80))
s.connect(("8.8.8.8",80)) #work only with external access
IPaddressLocal_all.append(s.getsockname()[0])
print(s.getsockname()[0])
s.close()


print IPaddressLocal_all

#print socket.gethostbyname_ex(socket.gethostname())
#print socket.gethostbyname(socket.gethostname())

