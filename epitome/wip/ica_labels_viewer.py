#!/usr/bin/env python
"""
Mash good and bad ica output pics together into on html page of sanity check qc.

Usage:
  ica_labels_viewer.py [options] <input.feat>

Arguments:
    <input.feat>        Top directory for the output file structure

Options:
  --labelfilename <file>   Name [default: fix4melview_Standard_thr20.txt] of file that contains labels.
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
inputdir        = arguments['<input.feat>']
icalabels       = arguments['--labelfilename']
VERBOSE         = arguments['--verbose']
DEBUG           = arguments['--debug']
DRYRUN          = arguments['--dry-run']

### Erin's little function for running things in the shell
def docmd(cmdlist):
    "sends a command (inputed as a list) to the shell"
    if DEBUG: print ' '.join(cmdlist)
    if not DRYRUN: subprocess.call(cmdlist)

def write_html_section(htmlhandle, IClist,SectionTitle):
    htmlpage.write('<h2><font color="white">'+SectionTitle+'</font></h2>')
    for IC in IClist:
        pic = os.path.join(inputdir,'filtered_func_data.ica','report','IC_'+ str(IC) +'_thresh.png')
        icreport = os.path.join(inputdir,'filtered_func_data.ica','report','IC_'+ str(IC) +'.html')
        picrelpath = os.path.relpath(pic,inputdir)
        icreppath = os.path.relpath(icreport,inputdir)
        htmlpage.write('<a href="'+ icreppath + '" style="color: #99CCFF" >')
        htmlpage.write('<img src="' + picrelpath + '" "WIDTH=800" > ')
        htmlpage.write(icreppath+ '</a><br>\n')

def get_SignalandNoise(inputlabelfile, numICs) :
    labelpath = os.path.join(inputdir,inputlabelfile)
    if os.path.isfile(labelpath):
        a=open(labelpath,'rb')
        lines = a.readlines()
        if lines:
            first_line = lines[:1]
            last_line = lines[-1]
        bad_ica = last_line.split(',')
        for i in range(len(bad_ica)):
            bad_ica[i] = bad_ica[i].replace('[','')
            bad_ica[i] = bad_ica[i].replace(']','')
            bad_ica[i] = bad_ica[i].replace(' ','')
            bad_ica[i] = bad_ica[i].replace('\n','')
        bad_ica = map(int,bad_ica)
    else:
        sys.exit("IC labels file {} not found".format(labelpath))

    if  max(bad_ica) > numICs:
        print("We have a problem, more labels in {} than ICs".format(inputlabelfile))
        print("Number of ICs: {}".format(numICs))
        print("Labeled Bad ICs {}".format(bad_ica))

    good_ica = list(set(range(1,numICs+1)) - set(bad_ica))
    return(good_ica,bad_ica)

## inputdir='/home/edickie/analysis/colin_fix/featprep/H002_NY_imitate.feat'
## icalabels='hand_labels_noise.txt'
if DEBUG: print arguments

## get the number of ICA components from the report length
ICpngs = glob.glob(os.path.join(inputdir,'filtered_func_data.ica','report','IC_*_thresh.png'))
numICs = len(ICpngs)

## use function to get good and bad
signal, noise = get_SignalandNoise(icalabels, numICs)


## make the html filename and title out of the csv filenames
stem1 = os.path.splitext(icalabels)[0]
htmlfilename = "{}_labels_report.html".format(stem1)
htmltitle="{} ICA labels".format(stem1)
htmlpage = open(os.path.join(inputdir,htmlfilename),'w')
htmlpage.write('<HTML><TITLE>'+htmltitle+'</TITLE>')
htmlpage.write('<BODY BGCOLOR=#333333>\n')
htmlpage.write('<h1><font color="white">Components for '+ inputdir +'</font></h1>')

## Signal for both
write_html_section(htmlpage, signal,
    "Signal Components")

## Signal for both
write_html_section(htmlpage, noise,
    "Noise Components")

## finish the file
htmlpage.write('</BODY></HTML>\n')
htmlpage.close() # you can omit in most cases as the destructor will call it
