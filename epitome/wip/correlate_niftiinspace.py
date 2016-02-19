#!/usr/bin/env python
"""
This looks for most correlated seeds within brain networks

Usage:
  correlate_niftyinspace.py [options] <image1.nii.gz> <image2.nii.gz>

Arguments:
    <image1.nii.gz>        Paths to directory containing .mnc images to align and mean
    <image2.nii.gz>        Path to template for the ROIs of network regions

Options:
  --brainmask NIFTI        Brainmask to apply to all masks before running, also required for smoothing
  -v,--verbose             Verbose logging
  --debug                  Debug logging in Erin's very verbose style
  -n,--dry-run             Dry run
  -h,--help                Print help

DETAILS
Requires python enviroment with numpy and nibabel:
module load use.own datman/edickie

Requires HCP pipeline environment
module load FSL/5.0.7 freesurfer/5.3.0 connectome-workbench/1.1.1 hcp-pipelines/3.7.0

ROI template example:
source_roi_nii = 'metaanalytic_coactivation_Bstim_minBstim.nii.gz'
target_roi_nii = 'Lstim_35sphere_bin.nii.gz'
inputfile example:
ts_nii = '/projects/edickie/analysis/epitome/RTMSWM_epi1125_1/RTMSWM_CMH_WM001_01/RST/SESS01/func_MNI-nonlin.hcp.01.nii.gz'
brainmask = '/projects/edickie/analysis/epitome/RTMSWM_epi1125_1/RTMSWM_CMH_WM001_01/RST/SESS01/anat_EPI_mask_MNI-nonlin.nii.gz'
Work in progress
"""
from docopt import docopt
import numpy as np
import nibabel as nib
import os
import subprocess
import pandas as pd

arguments       = docopt(__doc__)
image1          = arguments['<image1.nii.gz>']
image2          = arguments['<image2.nii.gz>']
brainmask       = arguments['--brainmask']
VERBOSE         = arguments['--verbose']
DEBUG           = arguments['--debug']
DRYRUN          = arguments['--dry-run']

###
### Erin's little function for running things in the shell
def docmd(cmdlist):
    "sends a command (inputed as a list) to the shell"
    if DEBUG: print ' '.join(cmdlist)
    if not DRYRUN: subprocess.call(cmdlist)

                # 3dBlurInMask \
                #     -prefix ${SESS}/func_volsmooth.${ID}.${NUM}.nii.gz \
                #     -Mmask ${SESS}/anat_tmp_smoothmask.nii.gz \
                #     -FWHM ${FWHM} \
                #     -quiet -float \
                #     -input ${SESS}/${INPUT}.${ID}.${NUM}.nii.gz


## read in the dconn file
img1_meta = nib.load(image1)
img1_data = img1_meta.get_data()
dims = img1_data.shape

## read in the dconn file
img2_meta = nib.load(image2)
img2_data = img2_meta.get_data()
dims2 = img2_data.shape

if dims != dims2:
    sys.exit("Image1 and Image2 dimensions do not match")

img1_data = img1_data.reshape((dims[0]*dims[1]*dims[2], 1))
img2_data = img2_data.reshape((dims[0]*dims[1]*dims[2], 1))

## load the brainmask if given
if brainmask!=None:
    ## load brainmask if it exists
    brainmask_meta = nib.load(brainmask)
    brainmask_data = brainmask_meta.get_data()
    brainmask_data = brainmask_data.reshape((dims[0]*dims[1]*dims[2]),1)
    brainmask_idx = np.nonzero(brainmask_data)[0]

    ## calc brain corrcoef
    crosscorr = np.corrcoef(img1_data[brainmask_idx, :], img2_data[brainmask_idx, :])[0][1]
else:
    ## calc brain corrcoef
    crosscorr = np.corrcoef(img1_data, img2_data)[0][1]

print("Correlation of {} and {} is {}".format(image1,image2,crosscorr))
