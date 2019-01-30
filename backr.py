#!/usr/bin/env python

# backr backup tool in python

import os
import datetime
import hashlib
import sys
import tarfile
import shutil
from distutils.dir_util import copy_tree
import cPickle as pickle

# Take Arguments
for i in range(len(sys.argv)):
    if "-h" in sys.argv or "--help" in sys.argv:
        print "backr simple backup tool"
        print "usage: backr.py [-h|--help] [-c|--compress] [-d|--default]"
        print "[-h|--help] - print this help"
        print "[-c|--compress] - use compression, do not prompt user"
        print "[-d|--default] - backup to default location (~/backrs, do not prompt user"
        sys.exit(0)
    if "-d" in sys.argv or "--default" in sys.argv:
        prompt_for_location = False
    else:
        prompt_for_location = True
    if "-c" in sys.argv or "--compress" in sys.argv:
        use_compression = True
        prompt_for_compression = False
    else:
        prompt_for_compression = True

# Define a function for asking the user yes or no questions
# Taken from: http://stackoverflow.com/questions/3041986/ddg#3041990
def query_yes_no(question):
    default = None
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    prompt = " [y/n] "
    while True:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
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
        comment = raw_input("Enter a comment for this backup (or leave blank): ")
        if "/" in comment:
            print "comment cannot contain '/'"
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
    if prompt_for_compression:
        use_compression = query_yes_no("Use compression?")

    # Determining save location:
    # Check for .backr_location file with stores save location after first run
    home = os.path.expanduser("~")
    default_location = home+"/backrs"
    if os.path.isfile(".backr-location"):
        with open('.backr-location', 'r') as myfile:
            backup_location = myfile.read()

    # If .backr_location does not exit, prompt the user for a location and save
    # it to the file, later this should be done entirely as an argument to make
    # backr more portable
    else:
        if not prompt_for_location:
            backup_location = default_location
        else:
            backup_location = raw_input("Enter a location to save (or leave blank for default "+default_location+"): ")

            # If the user leaves the location blank, use the default (~/backrs)
            if backup_location == "":
                backup_location = default_location

            # If the user-provided location exists, write it to the file
            if os.path.isdir(backup_location):
                f = open('.backr-location', 'w')
                f.write(backup_location)
                f.close()
            else:

                # Create the folder only if it is ~/backrs
                if backup_location == default_location:
                    os.makedirs(backup_location)
                else:
                    print backup_location + " does not exist"
                    sys.exit(1)

    # Output
    print "will save to "+backup_location

    # Get Comment
    comment = get_comment()

    # Set some varibles:
    # Set current working directory
    cwd = os.getcwd()

    # Set basename directory variable
    basename = os.path.basename(cwd)

    # Set current time in a possible dir format
    time = basename + "-" + datetime.datetime.now().strftime('%G-%b-%d-%I_%M%p_%S') + "-" + comment

    # Generate a hash of the current dir
    qhash = hashlib.sha1(cwd.encode("UTF-8")).hexdigest()[:7]

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

    # Create the basename-time-comment directory
    if not os.path.exists(backup_location):
        os.makedirs(backup_location)

    # cp -r this folder that folder
    copy_tree(cwd, backup_location)

    # if compression was set to true
        # compress all the files in that folder individually
    if use_compression:
        make_tarfile(backbase+"/"+time+".tar.gz", backup_location)
        shutil.rmtree(backup_location)
        print "folder backed up to "+backbase+"/"+time+".tar.gz"
    else:
        print "folder backed up to "+backup_location

    # check for existence for version control file
    vc_file = backbase+"/backtrack.txt"
    if not os.path.exists(vc_file):
        fw = open(vc_file, 'wb')
        if not use_compression:
            data = [backup_location]
        else:
            data = [backbase+"/"+time+".tar.gz"]
        pickle.dump(data, fw)
        fw.close()
    # if it does exist
    else:
        data = pickle.load(open(vc_file, "rb"))
        #backup_number = (len(data)/3)+1
        if not use_compression:
            data += [backup_location]
        else:
            data += [backbase+"/"+time+".tar.gz"]
        fw = open(vc_file, 'wb')
        pickle.dump(data, fw)
        fw.close()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print
        print "exit"
        sys.exit(0)
