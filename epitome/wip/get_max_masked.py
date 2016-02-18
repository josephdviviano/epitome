#!/usr/bin/env python
"""
Outputs a table of peaks for within a mask

Usage:
  get_max_masked.py [options] <image1.nii.gz> <mask.nii.img> <threshold>

Arguments:
    <image1.nii.gz>        Paths to directory containing .mnc images to align and mean
    <mask.nii.img>         Path to template for the ROIs of network regions
    <threshold>            Threshold to apply to image1 before calculating peaks

Options:
  -v,--verbose             Verbose logging
  --debug                  Debug logging in Erin's very verbose style
  -n,--dry-run             Dry run
  -h,--help                Print help

DETAILS
Uses FSLmaths to mask an image then output a table of peaks using FSL's cluster command.
Requires FSL environment

Written by Erin W Dickie, November 30, 2015
"""
from docopt import docopt
import numpy as np
import nibabel as nib
import os
import tempfile
import shutil
import subprocess
import pandas as pd

arguments       = docopt(__doc__)
image1          = arguments['<image1.nii.gz>']
mask            = arguments['<mask.nii.img>']
threshold       = arguments['<threshold>']
VERBOSE         = arguments['--verbose']
DEBUG           = arguments['--debug']
DRYRUN          = arguments['--dry-run']

###
### Erin's little function for running things in the shell
def docmd(cmdlist):
    "sends a command (inputed as a list) to the shell"
    if DEBUG: print ' '.join(cmdlist)
    if not DRYRUN: subprocess.call(cmdlist)

#mkdir a tmpdir for the
tmpdir = tempfile.mkdtemp()

outputdir = os.path.dirname(image1)
image1_stem = os.path.basename(image1)[0:-7]
mask_stem = os.path.basename(mask)[0:-7]
output_stem = os.path.join(outputdir, "clustermax_" + image1_stem + '_in_' + mask_stem)

## mask the map with the MASK

docmd(['fslmaths', image1, '-mul', mask, os.path.join(tmpdir,image1_stem + mask_stem +".nii.gz")])

### run clusterize to get the files
docmd(['cluster', '--in=' + os.path.join(tmpdir,image1_stem + mask_stem +".nii.gz"),
    '--thresh=' + str(threshold),
    '--olmax=' + output_stem + ".txt",
    '--no_table'])
#get rid of the tmpdir
shutil.rmtree(tmpdir)
