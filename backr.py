#!/usr/bin/env python

# backr backup tool in python

import os

# these are just my notes for what i want it do rn

# take arg or prompt user for whether or not compression should be used
# use_compression = True or False
#q = raw_input("Do you want to use compression? y/n") # get better input
#if q == 'y': # uncomment these later when adding compression (after it already works)
#   use_compression=True
#else:
#    use_compression=False

# determining save location:
# check for saveto file
if os.path.isfile(".backr-location"):
    print ".backr-location exists"
    with open('.backr-location', 'r') as myfile:
        backup_location = myfile.read()
    print "will save to "+backup_location

    # if it does not exist, check for directory with dirname-hash in default location
	    # if this exists then backup_location = default
        # later because there isn't a default yet ^

# else prompt user for backup_location, then check if it exists
    # if exists, use it, else ask user to create
else:
    backup_location = raw_input("Enter a location to save: ")
    if os.path.isdir(backup_location):
        print "will save to " + backup_location
        # add this to new .backr location file
        f = open( '.backr-location', 'w' )
        f.write(backup_location)
        f.close()
    else:
        print backup_location + " does not exist"

# comment for save:
# prompt user for comment to save
comment = raw_input("Enter a comment for this backup (or leave blank): ")
    # make sure comment is a possible dir name
'''
https://stackoverflow.com/questions/295135/turn-a-string-into-a-valid-filename
import unicodedata, re
def slugify(value):
    """
    Normalizes string, converts to lowercase, removes non-alpha characters,
    and converts spaces to hyphens.
    """
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
    value = unicode(re.sub('[^\w\s-]', '', value).strip().lower())
    value = unicode(re.sub('[-\s]+', '-', value))
    print value
q=raw_input("gib: ")
q=q.decode('utf-8')
slugify(q)
'''
        # if not, tell user and ask again

# set some varibles:
# set current dir
# basename folder
# set current time in a possible dir format
# generate a hash of the current dir using something like:

'''
import hashlib, sys

inputt = sys.argv[1]

hash = hashlib.sha1(str(inputt).encode("UTF-8")).hexdigest()
print hash[:10]
'''

# backup folder name will be /location/basename-hash/time/contents

# mkdir backup folder

# cp -r this folder that folder

# if compression was set to true
    # compress all the files in that folder individually

# output

# IMPORTANT, i may want to store all the version numbers in one file instead of multiple

# check for existence for version control folder
     # if it doesn't exist, make it
         # put backup location including time in file called 1
         # put '1' in file called last.txt
     # if it does exist
         # get contents of last.txt
         # backup_number = last +1
         # put location in file called backup number
         # put that number in last.txt

# if compression set to true
    # put the fact that it's compressed in a file
