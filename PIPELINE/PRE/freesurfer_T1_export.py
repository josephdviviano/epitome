#!/usr/bin/env python

# Freesurfer T1 Export
# takes the processed T1 from freesurfer to use as a standard anatomical
# this is slow, but provides the highest-quality registration target.
# this also allows us to take advantage of the high-quality freesurfer
# segmentations for nusiance time series regression, if desired

import os
import fnmatch
import ypp_inputs

Od, Oe, Os, Ot, Oc = ypp_inputs.init()

for subject in Os:
    directory = os.path.join(Od, Oe, subject, 'T1')

    for session in os.listdir(directory):
        if os.path.isdir(os.path.join(directory, session)) == True:

            subjID = str(Oe) + '_' + str(subject) + '_' + str(session)

            dir_i = os.path.join(Od, 'FREESURFER/SUBJECTS', subjID, 'mri')
            dir_o = os.path.join(directory, session)

            cmd1 = ('mri_convert --in_type mgz ' +
                               '--out_type nii' +
                               ' -odt float ' +
                               ' -rt nearest ' + 
                               ' --input_volume ' + dir_i + '/brain.mgz' + 
                               ' --output_volume ' + dir_o + '/anat_T1_fs.nii.gz')
            cmd2 = ('3daxialize -prefix ' + dir_o + '/anat_T1_brain.nii.gz' +
                              ' -axial '  + dir_o + '/anat_T1_fs.nii.gz')

            cmd3 = ('mri_convert --in_type mgz' +
                               ' --out_type nii' +
                               ' -odt float' +
                               ' -rt nearest' + 
                               ' --input_volume ' + dir_i + '/aparc+aseg.mgz' +
                               ' --output_volume ' + dir_o + '/anat_aparc_fs.nii.gz')
            cmd4 = ('3daxialize -prefix ' + dir_o + '/anat_aparc_brain.nii.gz' +
                              ' -axial '  + dir_o + '/anat_aparc_fs.nii.gz')

            cmd5 = ('mri_convert --in_type mgz' +
                               ' --out_type nii' +
                               ' -odt float' +
                               ' -rt nearest' + 
                               ' --input_volume ' + dir_i + '/aparc.a2009s+aseg.mgz' + 
                               ' --output_volume ' + dir_o + '/anat_aparc2009_fs.nii.gz')
            cmd6 = ('3daxialize -prefix ' + dir_o + '/anat_aparc2009_brain.nii.gz' + 
                             ' -axial '  + dir_o + '/anat_aparc2009_fs.nii.gz')

            os.system(cmd1) # convert freesurfer T1 to NII
            os.system(cmd2) # orient to RAI orientation
            os.system(cmd3) # convert freesurfer APARC segmentation to NII
            os.system(cmd4) # orient to RAI orientation
            os.system(cmd5) # convert freesurfer APARC2009 segmentation to NII
            os.system(cmd6) # orient to RAI orientation

## JDV Jan 30 2013