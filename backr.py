#!/usr/bin/env python

# backr backup tool in python

import os, datetime, hashlib, sys
from distutils.dir_util import copy_tree
import cPickle as pickle

# take args
for i in range(len(sys.argv)):
    if "-c" in sys.argv or "--compress" in sys.argv:
        use_compression=True
        prompt_for_compression=False
    else:
        prompt_for_compression=True

# http://stackoverflow.com/questions/3041986/ddg#3041990
def query_yes_no(question):
    default=None
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

if prompt_for_compression:
    use_compression=query_yes_no("Use compression?")

# determining save location:
# check for saveto file
home = os.path.expanduser("~")
default_location=home+"/backrs"
if os.path.isfile(".backr-location"):
    with open('.backr-location', 'r') as myfile:
        backup_location = myfile.read()
    print "will save to "+backup_location
# else prompt user for backup_location, then check if it exists
    # if exists, use it, else ask user to create
else:
    backup_location = raw_input("Enter a location to save (or leave blank for default): ")
    if backup_location=="":
        backup_location=default_location
    if os.path.isdir(backup_location):
        print "will save to " + backup_location
        # add this to new .backr location file
        f = open( '.backr-location', 'w' )
        f.write(backup_location)
        f.close()
    else:
        print backup_location + " does not exist"
        exit()

# comment for save:
# prompt user for comment to save
def get_comment():
    has_comment=0
    while(has_comment==0):
        comment = raw_input("Enter a comment for this backup (or leave blank): ")
        # make sure comment is a possible dir name
        if "/" in comment:
            print "comment cannot contain '/'"
        else:
            return comment
            has_comment=1
comment=get_comment()

# set some varibles:
dir=os.getcwd()
#print dir
# basename folder
basename=os.path.basename(dir)
#print basename
# set current time in a possible dir format
time=datetime.datetime.now().strftime('%G-%b-%d-%I:%M%p:%S')
time+="-"
time+=comment
#print time
# generate a hash of the current dir
hash = hashlib.sha1(dir.encode("UTF-8")).hexdigest()
hash = hash[:7]

basehash = basename
basehash += "-"
basehash += hash

# backup folder name will be /location/basename-hash/time/contents

backup_location += "/"
backup_location += basehash
backbase=backup_location

# mkdir backup folder

if not os.path.exists(backup_location):
    os.makedirs(backup_location)

backup_location += "/"
backup_location += time

if not os.path.exists(backup_location):
    os.makedirs(backup_location)

# cp -r this folder that folder
copy_tree(dir, backup_location)

# if compression was set to true
    # compress all the files in that folder individually
if use_compression:
    os.system("gzip -rf "+backup_location) # old backr way
    # TODO do compression in python not with gzip
    #for filename in os.listdir(backup_location):
    #    print filename

print "folder backed up to "+backup_location

# IMPORTANT, i may want to store all the version numbers in one file instead of multiple

# check for existence for version control file
vc_file=backbase+"/backtrack.txt"
if not os.path.exists(vc_file):
    fw = open(vc_file,'wb')
    data = ["1",backup_location,use_compression]
    pickle.dump(data, fw)
    fw.close()
# if it does exist
else:
    #fw = open(vc_file,'wb')
    # get contents of last.txt
    tracks=pickle.load( open( vc_file, "rb" ))
    print tracks
    # backup_number = last +1
    # put location in file called backup number
    # put that number in last.txt
    #fw.close()

# if compression set to true
    # put the fact that it's compressed in a file
