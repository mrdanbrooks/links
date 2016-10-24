#!/usr/bin/env bash

# http://stackoverflow.com/a/246128
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
# The following line is no longer needed
# cd $DIR && git pull origin master

# Check to see if update indicator file exists
if [[ ! -e $DIR/../cgi_bin/update.txt ]]; then
   echo "Update File Not Found"
   exit 1
fi

# if indicator file has a 1 in it, then we should update
if [[ `cat $DIR/../cgi_bin/update.txt` == 1 ]]; then
   echo "Update Requested"
   /usr/bin/python $DIR/update.py
   if [[ $? == 0 ]]; then
       echo "Dismissing Update"
       echo "0" > $DIR/../cgi_bin/update.txt
   else
       echo "Will try again later"
   fi
#else
#   echo "No update"
fi
