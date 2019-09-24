#!/usr/bin/env python3

# Copyright (c) 2019 Aiden Holmes (aidenholmes@teknik.io)
# This program is licensed under the Apache License 2.0
# You are free to copy, modify, and redistribute the code.
# See LICENSE file.

# backr restor tool in python

import sys
import os
import hashlib
import shutil
import pickle
from distutils.dir_util import copy_tree

def get_item_index(array, item):
    for i in range(len(array)):
        if array[i] == item:
            return i
    return False

for q in range(len(sys.argv)):
    if "-h" in sys.argv or "--help" in sys.argv:
        print("restor tool for backr")
        print("usage: restor.py [-h|--help]")
        print("[-h|--help] - print this help")
        print("[-s|--source <source>] - set dir to restore")
        print("[-l|--location <location>] - set location to restore to")
        sys.exit()
    if "-s" in sys.argv:
        cwd = sys.argv[get_item_index(sys.argv,"-s")+1]
    elif "--source" in sys.argv:
        cwd = sys.argv[get_item_index(sys.argv,"--source")+1]
    if "-l" in sys.argv:
        restore_location = sys.argv[get_item_index(sys.argv,"-l")+1]
    elif "--location" in sys.argv:
        restore_location = sys.argv[get_item_index(sys.argv,"--location")+1]

def main():
    # set variables
    global cwd
    global restore_location
    try:
        cwd
    except NameError:
        cwd = os.getcwd()
    basename = os.path.basename(cwd)

    # get backup location
    if os.path.isfile(cwd + "/.backr-location"):
        with open(cwd + '/.backr-location', 'r') as myfile:
            backup_location = myfile.read()
    else:
        print(".backr-location file not found")
        sys.exit(1)

    qhash = hashlib.sha1(cwd.encode("UTF-8")).hexdigest()[:7]
    backup_location += "/" + basename + "-" + qhash
    backbase = backup_location

    vc_file = backbase+"/backtrack.txt"

    print("listing backups..." + '\n')
    if os.path.exists(vc_file):
        data = pickle.load(open(vc_file, "rb"))
        possible_backups = ["placeholder"]
        for i in range(0, len(data)):
            print("backup "+str(i)+" in "+data[i])
            if not os.path.exists(data[i]):
                print("    backup deleted or missing!")
            else:
                if possible_backups == ["placeholder"]:
                    possible_backups = [i]
                else:
                    possible_backups += [i]

        # print most recent available backup
        print('\n' + "most recent available backup:")
        if isinstance(possible_backups[-1], int):
            print(str(data[possible_backups[-1]]) + '\n')
        else:
            print("no possible backups" + '\n')

        has_number = False
        while not has_number:
            try:
                backup_number = input("Choose a number to restore from: ")
                if backup_number in str(possible_backups):
                    backup_number = int(backup_number)
                    has_number = True
                else:
                    print("That is not an option.")
            except ValueError:
                print("Enter a number.")
    else:
        print("backtrack file not found in "+backbase)
        sys.exit(1)

    restore_from = data[backup_number]

    has_restore_location = False
    while not has_restore_location:
        try:
            restore_location
        except NameError:
            restore_location = input("Enter a location to restore to: ")
        if os.path.isdir(restore_location):
            print("Will restore to "+restore_location)
            has_restore_location = True
        else:
            print(restore_location+" does not exist")
            del restore_location

    restore_location += "/"
    restore_location += basename
    if not os.path.exists(restore_location):
        os.makedirs(restore_location)
    if not ".tar.gz" in restore_from:
        copy_tree(restore_from, restore_location)
    else:
        shutil.copyfile(restore_from, restore_location+"/"+os.path.basename(restore_from))

    print("Restored to " + restore_location)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('\n' + "exit")
        sys.exit(0)
