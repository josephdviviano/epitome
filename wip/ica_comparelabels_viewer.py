#!/usr/bin/env python
"""
Mash good and bad ica output pics together into on html page of sanity check qc.

Usage:
  ica_comparelabels_viewer.py [options] <input.ica> <labelname1> <labelname2>

Arguments:
    <input.ica>        Top directory for the output file structure
    <labelname1>       Filename containing first set of labels
    <labelname2>       Filename containing second set of labels
Options:
  -v,--verbose             Verbose logging
  --debug                  Debug logging in Erin's very verbose style
  -n,--dry-run             Dry run
  --help                   Print help

DETAILS
Takes the images from the ICA report and combines them into webpages sorted as good and bad.
Written by Erin W Dickie, November 12, 2015
"""
from docopt import docopt
import os
import subprocess
import glob
import sys

arguments       = docopt(__doc__)
inputdir        = arguments['<input.ica>']
icalabels1       = arguments['<labelname1>']
icalabels2       = arguments['<labelname2>']
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

## get the number of ICs from the melodic report
ICpngs = glob.glob(os.path.join(inputdir,'filtered_func_data.ica','report','IC_*_thresh.png'))
numICs = len(ICpngs)

## get the signal and noise components from both files
signal1, noise1 = get_SignalandNoise(icalabels1, numICs)
signal2, noise2 = get_SignalandNoise(icalabels2, numICs)

## make the html filename and title out of the csv filenames
stem1 = os.path.splitext(icalabels1)[0]
stem2 = os.path.splitext(icalabels2)[0]
htmlfilename = "compare_{}_{}.html".format(stem1,stem2)
htmltitle="Comparing ICA labels from {} and {}".format(stem1, stem2)
htmlpage = open(os.path.join(inputdir,htmlfilename),'w')
htmlpage.write('<HTML><TITLE>'+htmltitle+'</TITLE>')
htmlpage.write('<BODY BGCOLOR=#333333>\n')
htmlpage.write('<h1><font color="white">Components for '+ inputdir +'</font></h1>')

## signal in 1, noise in 2
write_html_section(htmlpage, list(set(signal1).intersection(noise2)),
    "Signal in {}, Noise in {}".format(stem1, stem2))

## Noise in 1, signal in 2
write_html_section(htmlpage, list(set(noise1).intersection(signal2)),
    "Noise in {}, Signal in {}".format(stem1, stem2))

## Signal for both
write_html_section(htmlpage, list(set(signal1).intersection(signal2)),
    "Signal in both {} and {}".format(stem1, stem2))

## Signal for both
write_html_section(htmlpage, list(set(noise1).intersection(noise2)),
    "Noise in both {} and {}".format(stem1, stem2))

## finish the file
htmlpage.write('</BODY></HTML>\n')
htmlpage.close() # you can omit in most cases as the destructor will call it
