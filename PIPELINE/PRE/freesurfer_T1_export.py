#!/usr/bin/env python

# Freesurfer T1 Export
# takes the processed T1 from freesurfer to use as a standard anatomical
# this is slow, but provides the highest-quality registration target.
# this also allows us to take advantage of the high-quality freesurfer
# segmentations for nusiance time series regression, if desired

import os
import sys
import fnmatch
import ypp_inputs
import ypp_utilities

def T1_export(path, expt):
    
    # get subject numbers
    subjects = ypp_utilities.get_subj(os.path.join(path, expt))
 
    # get directory of sessions
    for subj in subjects:
        directory = os.path.join(path, expt, subj, 'T1')
        
        # get all sessions
        for session in os.listdir(directory):
            if os.path.isdir(os.path.join(directory, session)) == True:
                #export all FREESURFER data per session
                run_commands(path, directory, expt, subj, session)

def run_commands(path, directory, expt, subj, session):
    
    subjID = str(expt) + '_' + str(subj) + '_' + str(session)
    dir_i = os.path.join(path, 'FREESURFER/SUBJECTS', subjID, 'mri')
    dir_o = os.path.join(directory, session)

    # convert freesurfer T1 to NII
    if os.path.isfile(dir_o + '/anat_T1_fs.nii.gz') == False:
        cmd1 = ('mri_convert ' +
                '--in_type mgz ' +
                '--out_type nii ' +
                '-odt float ' +
                '-rt nearest ' + 
                '--input_volume ' + dir_i + '/brain.mgz ' + 
                '--output_volume ' + dir_o + '/anat_T1_fs.nii.gz')
        os.system(cmd1) 
    
    # orient to RAI orientation
    if os.path.isfile(dir_o + '/anat_T1_brain.nii.gz') == False:
        cmd2 = ('3daxialize ' +
                '-prefix ' + dir_o + '/anat_T1_brain.nii.gz ' +
                '-axial '  + dir_o + '/anat_T1_fs.nii.gz')
        os.system(cmd2)
    
    # convert MGZ APARC atlas to NII
    if os.path.isfile(dir_o + '/anat_aparc_fs.nii.gz') == False:
        cmd3 = ('mri_convert ' + 
                '--in_type mgz ' +
                '--out_type nii ' +
                '-odt float ' +
                '-rt nearest ' + 
                '--input_volume ' + dir_i + '/aparc+aseg.mgz ' +
                '--output_volume ' + dir_o + '/anat_aparc_fs.nii.gz')
        os.system(cmd3)
    
    # orient to RAI orientation
    if os.path.isfile(dir_o + '/anat_aparc_brain.nii.gz') == False:
        cmd4 = ('3daxialize ' +
                '-prefix ' + dir_o + '/anat_aparc_brain.nii.gz ' +
                '-axial '  + dir_o + '/anat_aparc_fs.nii.gz')
        os.system(cmd4)

    # convert MGZ APARC2009 atlas to NII
    if os.path.isfile(dir_o + '/anat_aparc2009_fs.nii.gz') == False:
        cmd5 = ('mri_convert ' +
                '--in_type mgz ' +
                '--out_type nii ' +
                '-odt float ' +
                '-rt nearest ' + 
                '--input_volume ' + dir_i + '/aparc.a2009s+aseg.mgz ' + 
                '--output_volume ' + dir_o + '/anat_aparc2009_fs.nii.gz')
        os.system(cmd5)

    # orient to RAI orientation
    if os.path.isfile(dir_o + '/anat_aparc2009_brain.nii.gz') == False:
        cmd6 = ('3daxialize ' +
                '-prefix ' + dir_o + '/anat_aparc2009_brain.nii.gz ' + 
                '-axial '  + dir_o + '/anat_aparc2009_fs.nii.gz')
        os.system(cmd6)

if __name__ == "__main__":
    T1_export(sys.argv[1], sys.argv[2])

## JDV