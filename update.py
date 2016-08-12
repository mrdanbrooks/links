#!/usr/bin/env python
# [db] 2016/08/11
# Use with cronjob */5 * * * * ~/.../update.py
# cronjob installed on cs1
import os
import datetime
import requests
import ConfigParser
import subprocess

# Settings - these are files in the same directory as script
configfile = "links.ini"
githubconfigurl = "https://raw.githubusercontent.com/allohakdan/links/master/links.ini"
outputfile = ".htaccess"

# Initialize the directory the script is located in
path = os.path.dirname(os.path.realpath(__file__))


# Determine if the github version of the config file is different from ours 
remote = requests.get(githubconfigurl).text
with open(os.path.join(path,configfile), "r") as f:
    local = "".join(f.readlines())
if remote == local:
    print "No Change"
    exit(0)
print "Update Found"


# Download the new changes
process = subprocess.Popen(["git","pull","origin","master"], cwd=path, stdout=subprocess.PIPE)
print process.communicate()[0]


# Load the configuration file
print "Loading Config file"
if not os.path.exists(os.path.join(path,configfile)):
    raise Exception("%s files does not exist" % configfile)
parser = ConfigParser.ConfigParser()
parser.read(os.path.join(path,configfile))
if not parser.has_section("LINKS"):
    raise Exception("LINKS section must be defined")


# Initialize the output file buffer
buffer = list()
buffer.append("# This file is autogenerated - do not edit directly.")
buffer.append("# Last updated: %s" % str(datetime.datetime.now()))
buffer.append("Options +FollowSymLinks")
buffer.append("RewriteEngine on")
buffer.append("RewriteRule ^.htaccess$ - [r=404,L] # Hide links file")
buffer.append("RewriteRule ^.git$ - [r=404,L] # Hide links file")
#buffer.append("RewriteRule ^links.ini$ - [r=404,L] # Hide links file")

# Copy the links into the output file buffer
# Why use NE - http://stackoverflow.com/a/11380893 
linkrefs = parser.options("LINKS")
for linkref in linkrefs:
    buffer.append("RewriteRule ^%s$ %s [r=302,NE,L]" % (linkref, parser.get("LINKS", linkref)))

# Write the buffer to the output file
with open(os.path.join(path,outputfile), "w") as f:
    for line in buffer:
        f.write(line+"\n")

