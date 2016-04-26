#!/usr/bin/env python
"""
Convert the Shen parcellation to dlabel file

"""

import os, sys
import subprocess
import tempfile
import shutil
import numpy as np
import nibabel as nib
import epitome as epi
from epitome.docopt import docopt


def docmd(cmdlist):
    "sends a command (inputed as a list) to the shell"
    if DEBUG: print ' '.join(cmdlist)
    if not DRYRUN: subprocess.call(cmdlist)

## make the tempdir
tempdir = tempfile.mkdtemp()

##
inputrois="~/code/epitome/assets/shen_2mm_268_parcellation.nii.gz"
template_sub=""

## for each number
for i in range(1,269):
    ## cut into binary mask
    docmd(['fslmaths',inputrois,
        '-thr',str(float(i)+0.2),
        '-uthr',str(float(i)+0.2),
        '-bin', os.path.join(tempdir,str(i).zfill(3)+'.nii.gz')])

    ## map that mask to the cifti
    docmd(['epi-result-vol2cifti', str(i).zfill(3)+'.nii.gz',
        template_sub,
        str(i).zfill(3)+'.dscalar.nii'])

## binarize the cifti

   wb_command -cifti-dilate
      <cifti-in> - the input cifti file
      <direction> - which dimension to dilate along, ROW or COLUMN
      <surface-distance> - the distance to dilate on surfaces, in mm
      <volume-distance> - the distance to dilate in the volume, in mm
      <cifti-out> - output - the output cifti file
            [-left-surface] - specify the left surface to use
         <surface> - the left surface file

         [-left-corrected-areas] - vertex areas to use instead of computing
            them from the left surface
            <area-metric> - the corrected vertex areas, as a metric

      [-right-surface] - specify the right surface to use
         <surface> - the right surface file

         [-right-corrected-areas] - vertex areas to use instead of computing
            them from the right surface
            <area-metric> - the corrected vertex areas, as a metric

      [-cerebellum-surface] - specify the cerebellum surface to use
         <surface> - the cerebellum surface file

         [-cerebellum-corrected-areas] - vertex areas to use instead of
            computing them from the cerebellum surface
            <area-metric> - the corrected vertex areas, as a metric

      [-bad-brainordinate-roi] - specify an roi of brainordinates to overwrite,
         rather than zeros
         <roi-cifti> - cifti dscalar or dtseries file, positive values denote
            brainordinates to have their values replaced

      [-nearest] - use nearest value when dilating non-label data

      [-merged-volume] - treat volume components as if they were a single
         component

      For all data values designated as bad, if they neighbor a good value or
      are within the specified distance of a good value in the same kind of
      model, replace the value with a distance weighted average of nearby good
      values, otherwise set the value to zero.  If -nearest is specified, it
      will use the value from the closest good value within range instead of a
      weighted average.

      .The -*-corrected-areas options are intended for dilating on group
      average surfaces, but it is only an approximate correction for the
      reduction of structure in a group average surface.

      If -bad-brainordinate-roi is specified, all values, including those with
      value zero, are good, except for locations with a positive value in the
      ROI.  If it is not specified, only values equal to zero are bad.

## merge the masks
# ## convert to label
# MAKE A CIFTI LABEL FILE FROM A CIFTI FILE
#    wb_command -cifti-label-import
#       <input> - the input cifti file
#       <label-list-file> - text file containing the values and names for labels
#       <output> - output - the output cifti label file
#
#       [-discard-others] - set any values not mentioned in the label list to the
#          ??? label
#
#       [-unlabeled-value] - set the value that will be interpreted as unlabeled
#          <value> - the numeric value for unlabeled (default 0)
#
#       [-drop-unused-labels] - remove any unused label values from the label
#          table
#
#       Creates a cifti label file from a cifti file with label-like values.  You
#       may specify the empty string ('' will work on linux/mac) for
#       <label-list-file>, which will be treated as if it is an empty file.  The
#       label list file must have lines of the following format:
#
#       <labelname>
#       <value> <red> <green> <blue> <alpha>
#
#       Do not specify the "unlabeled" key in the file, it is assumed that 0
#       means not labeled unless -unlabeled-value is specified.  Label names must
#       be on a separate line, but may contain spaces or other unusual characters
#       (but not newline).  Whitespace is trimmed from both ends of the label
#       name, but is kept if it is in the middle of a label.  The values of red,
#       green, blue and alpha must be integers from 0 to 255, and will specify
#       the color the label is drawn as (alpha of 255 means opaque, which is
#       probably what you want).  By default, it will set new label names with
#       names of LABEL_# for any values encountered that are not mentioned in the
#       list file, specify -discard-others to instead set these to the
#       "unlabeled" key.

## remove the tempdirectory
shutil.rmtree(tempdir)
