#!/usr/bin/env python

# backr restor tool in python

import sys
import os
import hashlib
import shutil
from distutils.dir_util import copy_tree
import cPickle as pickle

for q in range(len(sys.argv)):
    if "-h" in sys.argv or "--help" in sys.argv:
        print "restor tool for backr"
        print "usage: restor.py [-h|--help]"
        print "[-h|--help] - print this help"
        exit()

def main():
    # set variables
    cwd = os.getcwd()
    basename = os.path.basename(cwd)

    # get backup location
    if os.path.isfile(".backr-location"):
        with open('.backr-location', 'r') as myfile:
            backup_location = myfile.read()
    else:
        print ".backr-location file not found"
        sys.exit(1)

    qhash = hashlib.sha1(cwd.encode("UTF-8")).hexdigest()[:7]

    basehash = basename + "-" + qhash

    backup_location += "/"
    backup_location += basehash
    backbase = backup_location

    vc_file = backbase+"/backtrack.txt"

    print "listing backups..."
    print
    if os.path.exists(vc_file):
        data = pickle.load(open(vc_file, "rb"))
        possible_backups = ["placeholder"]
        for i in range(0, len(data)):
            print "backup "+str(i)+" in "+data[i]
            if not os.path.exists(data[i]):
                print "    backup deleted or missing!"
            else:
                if possible_backups == ["placeholder"]:
                    possible_backups = [i]
                else:
                    possible_backups += [i]

        # print most recent available backup
        print
        print "most recent available backup:"
        print data[possible_backups[-1]]
        print

        has_number = False
        while not has_number:
            try:
                backup_number = raw_input("Choose a number to restore from: ")
                if backup_number in str(possible_backups):
                    backup_number = int(backup_number)
                    has_number = True
                else:
                    print "That is not an option."
            except ValueError:
                print "Enter a number."
    else:
        print "backtrack file not found in "+backbase
        sys.exit(1)

    restore_from = data[backup_number]

    has_restore_location = False
    while not has_restore_location:
        restore_location = raw_input("Enter a location to restore to: ")
        if os.path.isdir(restore_location):
            print "Will restore to "+restore_location
            has_restore_location = True
        else:
            print restore_location+" does not exist"

    restore_location += "/"
    restore_location += basename
    if not os.path.exists(restore_location):
        os.makedirs(restore_location)
    if not ".tar.gz" in restore_from:
        copy_tree(restore_from, restore_location)
    else:
        shutil.copyfile(restore_from, restore_location+"/"+os.path.basename(restore_from))

    print "Restored to " + restore_location

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print
        print "exit"
        sys.exit(0)
