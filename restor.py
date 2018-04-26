#!/usr/bin/env python

# backr restor tool in python

import sys, os, hashlib
import cPickle as pickle

for i in range(len(sys.argv)):
    if "-h" in sys.argv or "--help" in sys.argv:
       print "restor tool for backr"
       print "usage: backr.py [-h|--help]"
       exit()

def main():
    # set veriables
    dir=os.getcwd()
    basename=os.path.basename(dir)

    # get backup location
    if os.path.isfile(".backr-location"):
        with open('.backr-location', 'r') as myfile:
            backup_location = myfile.read()
    else:
        print ".backr-location file not found"
        sys.exit(0)

    hash = hashlib.sha1(dir.encode("UTF-8")).hexdigest()
    hash = hash[:7]

    basehash = basename
    basehash += "-"
    basehash += hash

    backup_location += "/"
    backup_location += basehash
    backbase=backup_location

    vc_file=backbase+"/backtrack.txt"

    print "listing backups..."
    print
    if os.path.exists(vc_file):
        data=pickle.load( open( vc_file, "rb" ))
        for i in range(0, len(data), 3):
            print "backup "+str((i/3)+1)+" in "+data[i+1][16:]
    else:
        print "backtrack file not found in "+backbase

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print
        print "exit"
        sys.exit(0)
