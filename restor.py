#!/usr/bin/env python

# backr restor tool in python

import sys

def main()

for i in range(len(sys.argv)):
    if "-h" in sys.argv or "--help" in sys.argv:
       print "restor tool for backr"
       print "usage: backr.py [-h|--help]"
       exit()
