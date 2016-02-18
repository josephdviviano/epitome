#!/usr/bin/env python
"""
Make qc page that overlays the fix structural on the mean epi.

Usage:
  epi-over-fixmask-qc.py [options] <outputdir>

Arguments:
    <outputdir>        Top directory for the output file structure

Options:
  --debug                  Debug logging in Erin's very verbose style
  -n,--dry-run             Dry run
  --help                   Print help

DETAILS
Make qc page that overlays the fix structural on the mean epi.

Requires datman python enviroment, FSL and imagemagick.

Written by Erin W Dickie, Nov 17 2015
"""
from docopt import docopt
import pandas as pd
import os
import subprocess
import tempfile
import shutil
import glob
import sys

arguments       = docopt(__doc__)
outputdir       = arguments['<outputdir>']
DEBUG           = arguments['--debug']
DRYRUN          = arguments['--dry-run']

if DEBUG: print arguments

## check that FSL has been loaded - if not exists
FSLDIR = os.getenv('FSLDIR')
if FSLDIR==None:
    sys.exit("FSLDIR environment variable is undefined. Try again.")

### Erin's little function for running things in the shell
def docmd(cmdlist):
    "sends a command (inputed as a list) to the shell"
    if DEBUG: print ' '.join(cmdlist)
    if not DRYRUN: subprocess.call(cmdlist)

def gif_gridtoline(input_gif,output_gif):
    '''
    uses imagemagick to take a grid from fsl slices and convert to one line (like in slicesdir)
    '''
    docmd(['convert',input_gif, '-resize', '384x384',input_gif])
    docmd(['convert', input_gif,\
        '-crop', '100x33%+0+0', os.path.join(tmpdir,'sag.gif')])
    docmd(['convert', input_gif,\
        '-crop', '100x33%+0+128', os.path.join(tmpdir,'cor.gif')])
    docmd(['convert', input_gif,\
        '-crop', '100x33%+0+256', os.path.join(tmpdir,'ax.gif')])
    docmd(['montage', '-mode', 'concatenate', '-tile', '3x1', \
        os.path.join(tmpdir,'sag.gif'),\
        os.path.join(tmpdir,'cor.gif'),\
        os.path.join(tmpdir,'ax.gif'),\
        os.path.join(output_gif)])

def mask_overlay(background_nii,mask_nii, overlay_gif):
    '''
    use slices from fsl to overlay the mask on the background (both nii)
    then make the grid to a line for easier scrolling during QC
    '''
    docmd(['slices', background_nii, mask_nii, '-o', os.path.join(tmpdir,'BOmasked.gif')])
    gif_gridtoline(os.path.join(tmpdir,'BOmasked.gif'),overlay_gif)



## find the files that match the resutls tag...first using the place it should be from doInd-enigma-dti.py
## find those subjects in input who have not been processed yet and append to checklist
## glob the dtifitdir for FA files to get strings

# if no subids given - just glob the whole DTI fit ouput
addfeatdirs = glob.glob(outputdir + '/*.feat')
if DEBUG : print("Outputs found: {}".format(addfeatdirs))

QCdir = os.path.join(outputdir,'QC')
#mkdir a tmpdir for the
tmpdirbase = tempfile.mkdtemp()
# tmpdirbase = os.path.join(QCdir,'tmp')
# dm.utils.makedirs(tmpdirbase)

# make the output directories
QC_reg_dir = os.path.join(QCdir,'fix_reg')
docmd(['mkdir','-p',QC_reg_dir])

maskpics = []
V1pics = []
for featdir in addfeatdirs:
    ## manipulate the full path to the FA map to get the other stuff

    basename = os.path.basename(featdir).replace('.feat','')
    tmpdir = os.path.join(tmpdirbase,basename)
    docmd(['mkdir','-p',tmpdir])
    basename = os.path.basename(featdir).replace('.feat','')
    mean_func = os.path.join(featdir,'mean_func.nii.gz')
    fix_brain = os.path.join(featdir,'fix','hr2exf.nii.gz')

    maskpic = os.path.join(QC_reg_dir,basename + 'highres_overlay.gif')
    maskpics.append(maskpic)
    if os.path.exists(maskpic) == False:
        mask_overlay(mean_func,fix_brain, maskpic)


## write an html page that shows all the BET mask pics
qchtml = open(os.path.join(QCdir,'qc_registration.html'),'w')
qchtml.write('<HTML><TITLE>FSL fix reg</TITLE>')
qchtml.write('<BODY BGCOLOR=#333333>\n')
qchtml.write('<h1><font color="white">FSL registration for fix QC page</font></h1>')
for pic in maskpics:
    relpath = os.path.relpath(pic,QCdir)
    qchtml.write('<a href="'+ relpath + '" style="color: #99CCFF" >')
    qchtml.write('<img src="' + relpath + '" "WIDTH=800" > ')
    qchtml.write(relpath + '</a><br>\n')
qchtml.write('</BODY></HTML>\n')
qchtml.close() # you can omit in most cases as the destructor will call it


#get rid of the tmpdir
shutil.rmtree(tmpdirbase)
