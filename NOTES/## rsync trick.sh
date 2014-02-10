##rsync trick
files=`ls */task_fmri/*/func_concat.nii.gz`
for f in ${files}; do rsync -Rv ${f} ~/Desktop/SAB1_OUT/; done;

files=`ls */task_fmri/*/func_smooth*.nii.gz`
for f in ${files}; do rsync -Rv ${f} ~/Desktop/SAB1_OUT/; done;

files=`ls */task_fmri/*/anat_EPI_mask_register.nii.gz`
for f in ${files}; do rsync -Rv ${f} ~/Desktop/SAB1_OUT/; done;