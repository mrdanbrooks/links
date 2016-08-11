#!/usr/bin/env python
# [db] 2016/08/11
import os
import requests
import subprocess

# Read the most recent links file
actual = requests.get("https://raw.githubusercontent.com/mrdanbrooks/links/master/links").text
# print actual


# Read the current links file
expected = None
path = os.path.dirname(os.path.realpath(__file__))
with open(path+"/links","r") as current:
    expected = "".join(current.readlines())
# print expected


if expected != actual:
    print "Update Found"
    process = subprocess.Popen(["git","pull","origin","master"], cwd=path, stdout=subprocess.PIPE)
    print process.communicate()[0]
else:
    print "No Updates"


#     import difflib
#     expected=expected.splitlines(1)
#     actual=actual.splitlines(1)
#     diff=difflib.unified_diff(expected,actual)
#     print ''.join(diff)


