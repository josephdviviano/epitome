SUB='01'

# make TR in register with EPI data (ugly, should use AFNI)
flirt -interp sinc -sincwidth 7 -sincwindow blackman \
      -in ${SUB}/T1/SESS01/anat_T1_brain.nii.gz \
      -ref ${SUB}/WH/SESS01/anat_EPI_brain.nii.gz \
      -applyxfm -init ${SUB}/WH/SESS01/mat_T1_to_EPI.mat \
      -out ${SUB}/WH/SESS01/reg_T1_to_EPI.nii.gz

# Make SUMA directory and export from freesurfer
@SUMA_Make_Spec_FS -sid s${SUB}

mv -r SUMA /blah/blah/SUMA

# Copy registered T1 image into SUMA directory
3dcopy ${SUB}/WH/SESS01/reg_T1_to_EPI.nii.gz ${SUB}/SUMA/reg_T1_to_EPI


# align surface to EPI data
cd ${SUB}/SUMA

@SUMA_AlignToExperiment -exp_anat reg_T1_to_EPI+orig \
                        -surf_anat FLICKER120_01_SESS01_SurfVol+orig \
                        -align_centers

mv *Alnd_Exp+orig.BRIK SURFACE.BRIK
mv *Alnd_Exp+orig.HEAD SURFACE.HEAD

# load it up

afni -niml &
suma -spec FLICKER120_01_SESS01_both.spec -sv FLICKER120_01_SESS01_SurfVol+orig &