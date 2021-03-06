#!/usr/bin/env python3

# Copyright (c) 2020 Anthony Fadly (18fadly.anthony@gmail.com)
# This program is licensed under the Apache License 2.0
# You are free to copy, modify, and redistribute the code.
# See LICENSE file.

# backr backup tool in python

import os
import datetime
import hashlib
import sys
import tarfile
import pickle
import socket
from distutils.dir_util import copy_tree

def get_item_index(array, item):
    for i in range(len(array)):
        if array[i] == item:
            if len(array) > i + 1:
                return i
            else:
                print("error: argument required after " + array[i])
                sys.exit(1)
    return False

# Take Arguments
for i in range(len(sys.argv)):
    if "-h" in sys.argv or "--help" in sys.argv:
        print("backr simple backup tool")
        print("usage: backr.py -s <source> -l <location> [-n|-c] [-w|-e <comment>]")
        print("[-h|--help] - print this help")
        print("[-c|--compress] - use compression")
        print("[-n|--no-compress] - do not use compression")
        print("[-d|--default] - backup to default location, ~/backrs")
        print("[-w|--no-comment] - do not prompt for comment")
        print("[-e|--comment <comment>] - set comment")
        print("[-l|--location <location>] - set location")
        print("location will be ignored if .backr-location file exists")
        print("[-s|--source <source>] - set source dir to backup")
        print("if source is not set, current directory will be used")
        sys.exit(0)
    if "-d" in sys.argv or "--default" in sys.argv:
        prompt_for_location = False
    elif "-l" in sys.argv:
        backup_location = sys.argv[get_item_index(sys.argv,"-l")+1]
        prompt_for_location = False
    elif "--location" in sys.argv:
        backup_location = sys.argv[get_item_index(sys.argv,"--location")+1]
        prompt_for_location = False
    else:
        prompt_for_location = True
    if "-c" in sys.argv or "--compress" in sys.argv:
        use_compression = True
        prompt_for_compression = False
    elif "-n" in sys.argv or "--no-compress" in sys.argv:
        use_compression = False
        prompt_for_compression = False
    else:
        prompt_for_compression = True
    if "-w" in sys.argv or "--no-comment" in sys.argv:
        prompt_for_comment = False
    elif "--comment" in sys.argv:
        comment = sys.argv[get_item_index(sys.argv,"--comment")+1]
        prompt_for_comment = False
    elif "-e" in sys.argv:
        comment = sys.argv[get_item_index(sys.argv,"-e")+1]
        prompt_for_comment = False
    else:
        prompt_for_comment = True
    if "-s" in sys.argv:
        cwd = sys.argv[get_item_index(sys.argv,"-s")+1]
    elif "--source" in sys.argv:
        cwd = sys.argv[get_item_index(sys.argv,"--source")+1]

# Define a function for asking the user yes or no questions
# Taken from: http://stackoverflow.com/questions/3041986/ddg#3041990
def query_yes_no(question):
    default = None
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    prompt = " [y/n] "
    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")

# Define a function for asking the user for a comment
# This comment will be part of a directory name
# In UNIX a filename can contain everything except for "/" or NULL
# And we don't have to worry about NULL because this will be appended to the date
def get_comment():
    while True:
        comment = input("Enter a comment for this backup (or leave blank): ")
        if "/" in comment:
            print("comment cannot contain '/'")
        else:
            return comment

# Define a function to make a tarball, used for the compression feature
def make_tarfile(output_filename, source_dir):
    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))

# Main Function
def main():
    # use_compression was defined by an argument in the initial for loop
    global use_compression
    global comment
    global backup_location
    global cwd
    if prompt_for_compression:
        use_compression = query_yes_no("Use compression?")

    # Set current working directory
    try:
        cwd
    except NameError:
        cwd = os.getcwd()
    else:
        if not os.path.exists(cwd):
            print("Error: " + cwd + " not found")
            sys.exit(1)

    # Determining save location:
    # Check for .backr_location file with stores save location after first run
    home = os.path.expanduser("~")
    default_location = home+"/backrs"
    if os.path.isfile(cwd + "/.backr-location"):
        with open(cwd + '/.backr-location', 'r') as myfile:
            backup_location = myfile.read()

    # If .backr_location does not exit, prompt the user for a location and save
    # it to the file, later this should be done entirely as an argument to make
    # backr more portable
    else:
        if not prompt_for_location:
            try:
                backup_location
            except NameError:
                backup_location = default_location
        else:
            print("Enter a save location")
            print("Leave blank for default "+default_location)
            print("The path will be created if it does not exist")
            backup_location = input("> ")

            # If the user leaves the location blank, use the default (~/backrs)
            if backup_location == "":
                backup_location = default_location

        # Write it to the file
        f = open(cwd + '/.backr-location', 'w')
        f.write(backup_location)
        f.close()

    # Output
    print("will save to "+backup_location)

    # Get Comment
    if prompt_for_comment:
        comment = get_comment()
    else:
        try:
            comment
        except NameError:
            comment = ""

    # Set some variables:
    # Set basename directory variable
    basename = os.path.basename(cwd)

    # Set current time in a possible dir format
    if comment == "":
        time = basename + "-" + datetime.datetime.now().strftime('%G-%b-%d-%I_%M%p_%S')
    else:
        time = basename + "-" + datetime.datetime.now().strftime('%G-%b-%d-%I_%M%p_%S') + "-" + comment

    # Generate a hash of the current dir and system hostname
    hostname = socket.gethostname()
    host_and_cwd = hostname + ":" + cwd
    qhash = hashlib.sha1(host_and_cwd.encode("UTF-8")).hexdigest()[:7]

    # Set basehash var to basename and hash
    basehash = basename + "-" + qhash

    # Backup folder name will be /location/basename-hash/time
    # Add basehash to backup_location
    backup_location += "/" + basehash

    # We'll need a variable set to backup_location at the point later
    backbase = backup_location

    # At this point we know the save location like ~/backrs exists
    # We need to create the folder specifically for this folder
    # This creates ~/backrs/basename-hash
    if not os.path.exists(backup_location):
        os.makedirs(backup_location)

    # At time to backup_location to create a folder for this specific backup
    # backup_location is now, for example ~/backrs/basename-hash/basename-time-comment
    # Remember that "time" variable contains basename-time-comment
    backup_location += "/" + time

    # If use_compression was set, make a tarball of the backup
    # Output varies depending on whether or not it was compressed
    if use_compression:
        make_tarfile(backbase+"/"+time+".tar.gz", cwd)
        print("folder backed up to "+backbase+"/"+time+".tar.gz")
    else:
        # This line does the actual backup it creates the backup location folder
        # and copies the current directory to the backup location
        copy_tree(cwd, backup_location)
        print("folder backed up to "+backup_location)

    # We use a file called backtrack.txt to keep track of how many backups
    # there are and their locations, this is necessary for restor.py
    # It is stored in the backbase, eg ~/backrs/basename-hash
    vc_file = backbase+"/backtrack.txt"

    # If the file does not exist we create it using pickle
    # We only write the backup location or, if compressed, the tarball location
    if not os.path.exists(vc_file):
        fw = open(vc_file, 'wb')
        if not use_compression:
            data = [backup_location]
        else:
            data = [backbase+"/"+time+".tar.gz"]
        pickle.dump(data, fw)
        fw.close()

    # If backtrack.txt already exists we use pickle to set its contents to the data var which we will add to
    else:
        data = pickle.load(open(vc_file, "rb"))
        if not use_compression:
            data += [backup_location]
        else:
            data += [backbase+"/"+time+".tar.gz"]
        fw = open(vc_file, 'wb')
        pickle.dump(data, fw)
        fw.close()

# Use the except KeyboardInterrupt on main trick to allow the user to C-c anytime
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('\n' + "exit")
        sys.exit(0)
