#!/usr/bin/env python
"""
Finds the max value from a map (i.e. seed correlation map)

Usage:
  get_max_from_vertex.py [options] <func.dscalar.nii> --target-vertex FILE --surface FILE

Arguments:
    <func.dscalar.nii>       Paths to directory source image
    --target-vertex INT      Path to template for the ROIs of network regions
    --surface FILE           Surface file .surf.gii to read coordinates from

Options:
  --output-csv-line        Filename for output
  --limit-mm INT           Number of mm to search from target-vertex
  --hemi STR               Specity hemisphere as "L" or "R".
  -v,--verbose             Verbose logging
  --debug                  Debug logging in Erin's very verbose style
  -n,--dry-run             Dry run
  -h,--help                Print help

DETAILS
Finds the max value from a map (i.e. seed correlation map). Uses nibabel to read
the surfaces and "wb_command -surface-geodesic-distance" to get measure the distance
on the surface.

The default will output and report to STDOUT. The "--output-csv-line" option will
output the numbers in one line, easier to concatenate into a csv file for stats.

Written by Erin W Dickie, January 26, 2015
"""
from docopt import docopt
import numpy as np
import nibabel as nib
import os
import sys
import tempfile
import shutil
import subprocess
import pandas as pd
import nibabel.gifti.giftiio

arguments     = docopt(__doc__)
func          = arguments['<func.dscalar.nii>']
limit_mm      = arguments['--limit-mm']
surf          = arguments['--surface']
target_vertex = arguments['--target-vertex']
output_csv_line = arguments['--output-csv-line']
hemi          = arguments['--hemi']
VERBOSE       = arguments['--verbose']
DEBUG         = arguments['--debug']
DRYRUN        = arguments['--dry-run']

###
if DEBUG: print(arguments)
### Erin's little function for running things in the shell
def docmd(cmdlist):
    "sends a command (inputed as a list) to the shell"
    if DEBUG: print ' '.join(cmdlist)
    if not DRYRUN: subprocess.call(cmdlist)

#mkdir a tmpdir for the
tmpdir = tempfile.mkdtemp()

## if hemisphere is not specified, try to grab it from the filenames
if not hemi:
    if ".L." in surf and ".R." not in surf:
        hemi = "L"
    elif ".L." not in surf and ".R." in surf:
        hemi = "R"
    else:
        sys.exit("Can not determine hemiphere from filenames, please specifity with --hemi flag")

if hemi=="L":
    hemi_str = "CORTEX_LEFT"
elif hemi=="R":
    hemi_str = "CORTEX_RIGHT"
else:
    sys.exit("Please specifity --hemi using 'L' or 'R' ")

## separate the cifti file into stuffs
func_surf = os.path.join(tmpdir,'func_surf.func.gii')
docmd(['wb_command', '-cifti-separate', func, 'COLUMN',
    '-metric', hemi_str, func_surf])

## load the functional gifti for one surface
func_nib = nibabel.gifti.giftiio.read(func_surf)
func_data = func_nib.getArraysFromIntent('NIFTI_INTENT_NORMAL')[0].data

## read in the coordinates for this surface
surf_nib = nibabel.gifti.giftiio.read(surf)
surf_coord = surf_nib.getArraysFromIntent('NIFTI_INTENT_POINTSET')[0].data

## read in the stim vertex...
#target_vertex = int(open(L_surf_vertex).read().strip())

## make a surface with distances (which also works as your mask)
surf_distance = os.path.join(tmpdir, 'L_surf_distance.func.gii')
if limit_mm:
    docmd(['wb_command', '-surface-geodesic-distance',
        surf, str(target_vertex), surf_distance, '-limit', str(limit_mm)])
else:
    docmd(['wb_command', '-surface-geodesic-distance',
            surf, str(target_vertex), surf_distance])

## read in the distance file
surf_dist_nib = nibabel.gifti.giftiio.read(surf_distance)
surfdist_data = surf_dist_nib.getArraysFromIntent('NIFTI_INTENT_NORMAL')[0].data

## find the index with maximal FC within the search space
mask_idx = np.where(surfdist_data>0)[0]
FC_vertex = mask_idx[np.argmax(func_data[mask_idx])] ## the vertex index
FC_max = func_data[FC_vertex] ## the maximal FC value

## get the distance on the surface from the surfdist surface file
surfDist = surfdist_data[FC_vertex]

## calculate the euclidean distance from the coordinates
euclDist = np.sqrt(sum(np.square(surf_coord[FC_vertex,:] - surf_coord[target_vertex,:])))

## save the xyz coordinates for both points into variables for output
rTMS_x= surf_coord[target_vertex,0]
rTMS_y= surf_coord[target_vertex,1]
rTMS_z= surf_coord[target_vertex,2]
FC_x= surf_coord[FC_vertex,0]
FC_y= surf_coord[FC_vertex,1]
FC_z= surf_coord[FC_vertex,2]

## make a dict of for the reportness
result_dict={'func' : func,
      'surf' : surf,
      'hemi' : hemi,
      'limit_mm': limit_mm,
      'FC_max': FC_max,
      'euclDist':euclDist,
      'surfDist':surfDist,
      'rTMS_x':rTMS_x,
      'rTMS_y':rTMS_y,
      'rTMS_z':rTMS_z,
      'FC_x':FC_x,
      'FC_y':FC_y,
      'FC_z':FC_z,
      'rTMS_vertex': target_vertex,
      'FC_vertex': FC_vertex}

#docmd(['fslmaths', image1, '-mul', mask, os.path.join(tmpdir,image1_stem + mask_stem +".nii.gz")])
if output_csv_line:
    print("{func},{surf},{hemi},{limit_mm},{FC_max},{euclDist},{surfDist},{rTMS_vertex},{rTMS_x},{rTMS_y},{rTMS_x},{FC_vertex},{FC_x},{FC_y},{FC_z}".format(
      **result_dict))
else:
    print("FC surface: {func}\n"
          "Measure distance on: {surf}\n"
          "Hemisphere: {hemi}\n"
          "Search limit (mm): {limit_mm}\n"
          "Target_vertex (vertex, xyz): {rTMS_vertex},\t{rTMS_x} {rTMS_y} {rTMS_x}\n"
          "FC max vertex (vertex, xyz): {FC_vertex},\t{FC_x} {FC_y} {FC_z}\n"
          "Max Seed Correlation: {FC_max}\n"
          "Euclidean Distance (mm): {euclDist}\n"
          "Distance on Surface (mm): {surfDist}\n".format(**result_dict))

#get rid of the tmpdir
shutil.rmtree(tmpdir)
