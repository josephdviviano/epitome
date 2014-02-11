#!/bin/bash

## Pre-processing for fMRI data:
#  
#
#
#

# create experiment wide mask
if [ ! -f ${DIR_DATA}/${DIR_EXPT}/mask_group.nii.gz ]; then
    3dmask_tool -input ${DIR_DATA}/${DIR_EXPT}/*/task/*/anat_EPI_mask_register.nii.gz \
                -prefix ${DIR_DATA}/${DIR_EXPT}/mask_group.nii.gz -frac 1.0
# 3dTcat -prefix ${DIR}/mask_tmp_group.nii.gz -DAFNI_GLOB_SELECTORS=YES ${DIR}/*/task/*/anat_EPI_mask_norm_reg.nii.gz
# 3dTstat -prefix ${DIR}/mask_tmp_group_mean.nii.gz -mean ${DIR}/mask_tmp_group.nii.gz
# 3dCalc -prefix ${DIR}/mask_group.nii.gz -expr 'astep(a, 1)' -a ${DIR}/mask_tmp_group_mean.nii.gz 
fi

for SUB in ${SUBJECTS}; do
    DIR_SESS=`ls -d -- ${DIR_DATA}/${DIR_EXPT}/${SUB}/task/*`
    for SESS in ${DIR_SESS}; do
        # this used to be: `ls -d -- ${SESS}run*/ | sort -n -t n -k 4`
        DIR_RUNS=`ls -d -- ${SESS}/run*`
        for RUN in ${DIR_RUNS}; do
            NUM=`basename ${RUN} | sed 's/[^0-9]//g'`
            # Smooth data
            if [ ! -f ${SESS}/func_smooth${NUM}.nii.gz ]; then
            3dBlurInMask -prefix ${SESS}/func_smooth${NUM}.nii.gz \
                         -FWHM ${BLUR_FWHM} \
                         -mask ${SESS}/anat_EPI_mask_register.nii.gz \
                         -input ${SESS}/func_register${NUM}.nii.gz
            fi
        done
    done
    # create concatenated runs in order -- this needs to be fixed!!!
    if [ ! -f ${DIR_DATA}/${DIR_EXPT}/${SUB}/task/func_concat.nii.gz ]; then
        INPUT=``
        DIR_SESS=`ls -d -- ${DIR_DATA}/${DIR_EXPT}/${SUB}/task/*`
        for SESS in ${DIR_SESS}; do
            # this used to say `ls ${SESS}/func_smooth* | sort -n -t h -k 2` 
            FILES=`ls ${SESS}/func_smooth*`
            INPUT="${INPUT} ${FILES}"
        done    
        
        3dTcat -prefix ${DIR_DATA}/${DIR_EXPT}/${SUB}/task/func_concat.nii.gz `echo ${INPUT}` 

        # 3dresample -prefix ${DIR_DATA}/${DIR_EXPT}/mask_tmp_group_resample.nii.gz \
        #            -rmode NN \
        #            -inset ${DIR_DATA}/${DIR_EXPT}/mask_group.nii.gz \
        #            -master ${DIR}/task/${S}/func_tmp_concat.nii.gz 

        # 3dCalc -prefix ${DIR}/task/${S}/func_tmp_concat.nii.gz \
        #        -expr 'a*b' \
        #        -a ${DIR}/task/${S}/func_tmp_concat.nii.gz \
        #        -b ${DIR_DATA}/${DIR_EXPT}/mask_tmp_group_resample.nii.gz

        # rm ${DIR}/task/${S}/func_tmp_concat.nii.gz
        # rm ${DIR_DATA}/${DIR_EXPT}/mask_tmp_group_resample.nii.gz
    fi

done

## JDV Jan 10 2014
