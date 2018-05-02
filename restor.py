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
        possible_backups=[0]
        for i in range(0, len(data), 3):
            i_number=str((i/3)+1)
            i_backup=data[i+1][16:]
            print "backup "+i_number+" in "+i_backup #data[i+1][16:]
            if not os.path.exists(i_backup):
                print ("    backup deleted or missing!")
            else:
                if possible_backups==[0]:
                    possible_backups=[i_number]
                else:
                    possible_backups+=[i_number]
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

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print
        print "exit"
        sys.exit(0)
