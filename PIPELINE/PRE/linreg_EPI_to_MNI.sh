#!/bin/bash

## Standard Space Module: Prepares data for analysis in standard space
#
#
#

cd /tmp
for SUB in ${SUBJECTS}; do
    DIR_SESS=`ls -d -- ${DIR_DATA}/${DIR_EXPT}/${SUB}/${DATA_TYPE}/*/`
    for SESS in ${DIR_SESS}; do
        # this used to be: `ls -d -- ${SESS}run*/ | sort -n -t n -k 4`
        DIR_RUNS=`ls -d -- ${SESS}/RUN*`
        for RUN in ${DIR_RUNS}; do
            NUM=`basename ${RUN} | sed 's/[^0-9]//g'`

            # smooth data within grey matter boundaries
            if [ ! -f ${SESS}/func_smooth.${NUM}.nii.gz ]; then
                if [ ! -f ${SESS}/func_filtered.${NUM}.nii.gz ]; then
                    3dBlurInMask -prefix ${SESS}/func_smooth.${NUM}.nii.gz \
                                 -FWHM ${BLUR_FWHM} \
                                 -mask ${SESS}/anat_EPI_mask.nii.gz \
                                 -input ${SESS}/func_scaled.${NUM}.nii.gz
                else
                    3dBlurInMask -prefix ${SESS}/func_smooth.${NUM}.nii.gz \
                        -FWHM ${BLUR_FWHM} \
                        -mask ${SESS}/anat_EPI_mask.nii.gz \
                        -input ${SESS}/func_filtered.${NUM}.nii.gz
                fi
            fi


            # register runs with MNI
            if [ ! -f ${SESS}/func_MNI.${NUM}.nii.gz ]; then
                3dAllineate -prefix ${SESS}/func_MNI.${NUM}.nii.gz \
                            -input ${SESS}/func_smooth.${NUM}.nii.gz \
                            -1Dmatrix_apply ${SESS}/mat_EPI_to_TAL.aff12.1D \
                            -master ${DIR_AFNI}/MNI_avg152T1+tlrc \
                            -float -final wsinc5 -mast_dxyz ${DIMS} ${DIMS} ${DIMS}
            fi
        done
        
        # register session masks with MNI
        if [ ! -f ${SESS}/anat_EPI_mask_MNI.nii.gz ]; then
            3dAllineate -prefix ${SESS}/anat_EPI_mask_MNI.nii.gz \
                        -input ${SESS}/anat_EPI_mask.nii.gz \
                        -1Dmatrix_apply ${SESS}/mat_EPI_to_TAL.aff12.1D \
                        -master ${DIR_AFNI}/MNI_avg152T1+tlrc \
                        -float -final NN -mast_dxyz ${DIMS} ${DIMS} ${DIMS}
        fi
    done
    
    # create concatenated runs in order
    if [ ! -f ${DIR_DATA}/${DIR_EXPT}/${SUB}/${DATA_TYPE}/func_MNI_concat_scrubbed.nii.gz ]; then
        INPUT=``
        DIR_SESS=`ls -d -- ${DIR_DATA}/${DIR_EXPT}/${SUB}/${DATA_TYPE}/*/`
        for SESS in ${DIR_SESS}; do
            FILES=`ls ${SESS}/func_scrubbed*`
            INPUT="${INPUT} ${FILES}"
        done    
        
        3dTcat -prefix ${DIR_DATA}/${DIR_EXPT}/${SUB}/${DATA_TYPE}/func_MNI_concat_scrubbed.nii.gz \
               `echo ${INPUT}` 

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

# create experiment wide mask
if [ ! -f ${DIR_DATA}/${DIR_EXPT}/mask_group.nii.gz ]; then
    3dmask_tool -input ${DIR_DATA}/${DIR_EXPT}/*/${DATA_TYPE}/*/anat_EPI_mask_MNI.nii.gz \
                -prefix ${DIR_DATA}/${DIR_EXPT}/mask_group_MNI.nii.gz -frac 1.0
# 3dTcat -prefix ${DIR}/mask_tmp_group.nii.gz -DAFNI_GLOB_SELECTORS=YES ${DIR}/*/task/*/anat_EPI_mask_norm_reg.nii.gz
# 3dTstat -prefix ${DIR}/mask_tmp_group_mean.nii.gz -mean ${DIR}/mask_tmp_group.nii.gz
# 3dCalc -prefix ${DIR}/mask_group.nii.gz -expr 'astep(a, 1)' -a ${DIR}/mask_tmp_group_mean.nii.gz 
fi
cd ${DIR_PIPE}
