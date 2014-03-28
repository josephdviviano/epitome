#!/usr/bin/env python

# Freesurfer T1 Export
# takes the processed T1 from freesurfer to use as a standard anatomical
# this is slow, but provides the highest-quality registration target.
# this also allows us to take advantage of the high-quality freesurfer
# segmentations for nusiance time series regression, if desired

import os
import fnmatch
import ypp_inputs
import ypp_utilities

def T1_export(path, expt):
    
    # get subject numbers
    subjects = ypp_utilities.get_subj(os.path.join(path, expt))

    for subj in subjects:
        directory = os.path.join(path, expt, subj, 'T1')

        for session in os.listdir(directory):
            if os.path.isdir(os.path.join(directory, session)) == True:

                subjID = str(expt) + '_' + str(subj) + '_' + str(session)

                dir_i = os.path.join(path, 'FREESURFER/SUBJECTS', subjID, 'mri')
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
                os.system(cmd3) # convert MGZ APARC atlas to NII
                os.system(cmd4) # orient to RAI orientation
                os.system(cmd5) # convert MGZ APARC2009 atlas to NII
                os.system(cmd6) # orient to RAI orientation

if __name__ == "__main__":
    T1_export((sys.argv[1], sys.argv[2]))

## JDV