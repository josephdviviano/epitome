flirt -in T1/SESS01/anat_T1_brain.nii.gz \
      -ref WH/SESS01/anat_EPI_brain.nii.gz \
      -applyxfm -init WH/SESS01/mat_T1_to_EPI.mat \
      -out WH/SESS01/reg_T1_to_EPI.nii.gz

3dcopy WH/SESS01/reg_T1_to_EPI.nii.gz WH/SESS01/reg_T1_to_EPI
3dcopy T1/SESS01/anat_T1_fs.nii.gz WH/SESS01/anat_T1_fs

cd WH/SESS01/
@SUMA_AlignToExperiment -exp_anat reg_T1_to_EPI+orig \
                        -surf_anat anat_T1_fs+orig \
                        -prefix surf
cd ../..