#!/usr/bin/env python
"""
Mash good and bad ica output pics together into on html page of sanity check qc.

Usage:
  ica_labels_viewer.py [options] <input.ica>

Arguments:
    <input.ica>        Top directory for the output file structure

Options:
  --labelfilename <file>   Name [default: hand_labels_noise.txt] of file that contains labels.
  -v,--verbose             Verbose logging
  --debug                  Debug logging in Erin's very verbose style
  -n,--dry-run             Dry run
  --help                   Print help

DETAILS
Takes the images from the ICA report and combines them into webpages sorted as good and bad.
Written by Erin W Dickie, August 25 2015
"""
from docopt import docopt
import os
import subprocess
import glob
import sys

arguments       = docopt(__doc__)
inputdir        = arguments['<input.ica>']
icalabels       = arguments['--labelfilename']
VERBOSE         = arguments['--verbose']
DEBUG           = arguments['--debug']
DRYRUN          = arguments['--dry-run']

### Erin's little function for running things in the shell
def docmd(cmdlist):
    "sends a command (inputed as a list) to the shell"
    if DEBUG: print ' '.join(cmdlist)
    if not DRYRUN: subprocess.call(cmdlist)

def make_html(IClist,GoodorBad):
    ## write an html page that shows all the V1 pics
    htmlpage = open(os.path.join(inputdir,GoodorBad + '_ica.html'),'w')
    htmlpage.write('<HTML><TITLE>IC '+GoodorBad+' components</TITLE>')
    htmlpage.write('<BODY BGCOLOR=#333333>\n')
    htmlpage.write('<h1><font color="white">'+GoodorBad+' components for '+ inputdir +'</font></h1>')

    for IC in IClist:
        pic = os.path.join(inputdir,'filtered_func_data.ica','report','IC_'+ str(IC) +'_thresh.png')
        icreport = os.path.join(inputdir,'filtered_func_data.ica','report','IC_'+ str(IC) +'.html')
        picrelpath = os.path.relpath(pic,inputdir)
        icreppath = os.path.relpath(icreport,inputdir)
        htmlpage.write('<a href="'+ icreppath + '" style="color: #99CCFF" >')
        htmlpage.write('<img src="' + picrelpath + '" "WIDTH=800" > ')
        htmlpage.write(icreppath+ '</a><br>\n')

    htmlpage.write('</BODY></HTML>\n')
    htmlpage.close() # you can omit in most cases as the destructor will call it


## inputdir='/home/edickie/analysis/colin_fix/featprep/H002_NY_imitate.feat'
## icalabels='hand_labels_noise.txt'
if DEBUG: print arguments

labelpath = os.path.join(inputdir,icalabels)
if os.path.isfile(labelpath):
    text_file = open(labelpath, "r")
    bad_ica = text_file.read().split(',')
    for i in range(len(bad_ica)):
        bad_ica[i] = bad_ica[i].replace('[','')
        bad_ica[i] = bad_ica[i].replace(']','')
        bad_ica[i] = bad_ica[i].replace(' ','')
        bad_ica[i] = bad_ica[i].replace('\n','')
    bad_ica = map(int,bad_ica)
else:
    sys.exit("IC labels file {} not found".format(labelpath))

ICpngs = glob.glob(os.path.join(inputdir,'filtered_func_data.ica','report','IC_*_thresh.png'))

numICs = len(ICpngs)
if  max(bad_ica) > numICs:
    print("We have a problem, more labels than ICs")
    print("Number of ICs: {}".format(numICs))
    print("Labeled Bad ICs {}".format(bad_ica))

good_ica = list(set(range(1,numICs+1)) - set(bad_ica))

make_html(good_ica,'good')
make_html(bad_ica,'bad')
