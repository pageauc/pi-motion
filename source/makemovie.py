#!/usr/bin/python
print "initializing ...."
import StringIO
import subprocess
import os
import time
import csv
from datetime import datetime
import cgi, cgitb
print "makemovie - create google_drive *.jpg listing to makemovie.txt" 
ls_params = " -t -r ./google_drive/*.jpg > makemovie.txt"
exit_status = subprocess.call("ls %s " % ls_params, shell=True)
print "makemovie - Creating makemovie.avi from file listing in makemovie.txt"
print "makemovie - This will take a while ......."
mencoder_params = "-nosound -ovc lavc -lavcopts vcodec=mpeg4:aspect=4/3:vbitrate=8000000 -vf scale=1296:972 -o makemovie.avi -mf type=jpeg:fps=20 mf://@makemovie.txt"
exit_status = subprocess.call("mencoder %s" % mencoder_params, shell=True)
print "makemovie - makemovie.avi created"

