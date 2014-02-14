# remove all registration-related files
for s in *; do
    rm ${s}/REST/func_mni_concat.nii.gz
    rm ${s}/REST/SESS??/reg_*
    rm ${s}/REST/SESS??/mat_*
    rm ${s}/REST/SESS??/anat_EPI_mask_mni.nii.gz
    rm ${s}/REST/SESS??/func_mni*
    rm ${s}/T1/SESS??/reg_*
done
# JDV Jan 30 2014