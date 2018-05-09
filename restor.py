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
        sys.exit(1)

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
        possible_backups=["placeholder"]
        for i in range(0, len(data)):
            print "backup "+str(i)+" in "+data[i]
            if not os.path.exists(data[i]):
                print ("    backup deleted or missing!")
            else:
                if possible_backups==["placeholder"]:
                    possible_backups=[i]
                else:
                    possible_backups+=[i]
        has_number=False
        while not has_number:
            backup_number=raw_input("Choose a number to restore from: ")
            if backup_number in possible_backups:
                backup_number=int(backup_number)
                has_number=True
            else:
                print "That is not an option."
    else:
        print "backtrack file not found in "+backbase
        sys.exit(1)

    print backup_number
    for i in range(len(possible_backups)):
        if str(backup_number) in possible_backups[i]:
            print possible_backups[i]

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print
        print "exit"
        sys.exit(0)
