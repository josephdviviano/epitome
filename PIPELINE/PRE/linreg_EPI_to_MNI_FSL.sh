#!/bin/bash

## Standard Space Module: Prepares data for analysis in standard space
#
#
#

cd /tmp
for SUB in ${SUBJECTS}; do
    DIR_SESS=`ls -d -- ${DIR_DATA}/${DIR_EXPT}/${SUB}/${DATA_TYPE}/*/`
    for SESS in `basename ${DIR_SESS}`; do
        
        DIR=`echo ${DIR_DATA}/${DIR_EXPT}/${SUB}/${DATA_TYPE}/${SESS}`
        DIR_T1=`echo ${DIR_DATA}/${DIR_EXPT}/${SUB}/T1/${SESS}`

        # create registration dummy for FSL
        3dresample -dxyz ${DIMS} ${DIMS} ${DIMS} \
                   -prefix ${DIR}/anat_EPI_reg_target.nii.gz \
                   -inset ${DIR_T1}/anat_T1_brain.nii.gz

        DIR_RUNS=`ls -d -- ${DIR}/RUN*`
        for RUN in ${DIR_RUNS}; do
            NUM=`basename ${RUN} | sed 's/[^0-9]//g'`

            # smooth data
            if [ ! -f ${DIR}/func_smooth.${NUM}.nii.gz ]; then
                if [ ! -f ${DIR}/func_filtered.${NUM}.nii.gz ]; then
                    3dBlurInMask -prefix ${DIR}/func_smooth.${NUM}.nii.gz \
                                 -FWHM ${BLUR_FWHM} \
                                 -mask ${DIR}/anat_EPI_mask.nii.gz \
                                 -input ${DIR}/func_scaled.${NUM}.nii.gz
                else
                    3dBlurInMask -prefix ${DIR}/func_smooth.${NUM}.nii.gz \
                                 -FWHM ${BLUR_FWHM} \
                                 -mask ${DIR}/anat_EPI_mask.nii.gz \
                                 -input ${DIR}/func_filtered.${NUM}.nii.gz
                fi
            fi

            # register runs with individual T1s, and MNI
            if [ ! -f ${DIR}/func_T1.${NUM}.nii.gz ]; then
                flirt -in ${DIR}/func_smooth.${NUM}.nii.gz \
                      -ref ${DIR}/anat_EPI_reg_target.nii.gz \
                      -applyxfm -init ${DIR}/mat_EPI_to_T1.mat \
                      -out ${DIR}/func_T1.${NUM}.nii.gz
                      # -interp sinc \
                      # -sincwidth 7 \
                      # -sincwindow blackman \
            fi


            if [ ! -f ${DIR}/func_MNI.${NUM}.nii.gz ]; then
                3dAllineate -prefix ${DIR}/func_MNI.${NUM}.nii.gz \
                            -input ${DIR}/func_T1.${NUM}.nii.gz \
                            -1Dmatrix_apply ${DIR_T1}/mat_T1_to_TAL.1D \
                            -master ${DIR_AFNI}/MNI_avg152T1+tlrc \
                            -float -final wsinc5 \
                            -mast_dxyz ${DIMS} ${DIMS} ${DIMS}
            fi
        done
        
        # register session masks with MNI
        if [ ! -f ${DIR}/anat_EPI_mask_MNI.nii.gz ]; then
            flirt -in ${DIR}/anat_EPI_mask.nii.gz \
                  -ref ${DIR}/anat_EPI_reg_target.nii.gz \
                  -applyxfm -init ${DIR}/mat_EPI_to_T1.mat \
                  -interp nearestneighbour \
                  -out ${DIR}/anat_EPI_mask_T1.nii.gz

            3dAllineate -prefix ${DIR}/anat_EPI_mask_MNI.nii.gz \
                        -input ${DIR}/anat_EPI_mask_T1.nii.gz \
                        -1Dmatrix_apply ${DIR_T1}/mat_T1_to_TAL.1D \
                        -master ${DIR_AFNI}/MNI_avg152T1+tlrc \
                        -float -final NN \
                        -mast_dxyz ${DIMS} ${DIMS} ${DIMS}
        fi
    done
    
    # create concatenated runs in order -- this needs to be fixed!!!
    if [ ! -f ${DIR_DATA}/${DIR_EXPT}/${SUB}/${DATA_TYPE}/func_MNI_concat.nii.gz ]; then
        INPUT=``
        DIR_SESS=`ls -d -- ${DIR_DATA}/${DIR_EXPT}/${SUB}/${DATA_TYPE}/*/`
        for SESS in ${DIR_SESS}; do
            # this used to say `ls ${SESS}/func_smooth* | sort -n -t h -k 2` 
            FILES=`ls ${SESS}/func_MNI*`
            INPUT="${INPUT} ${FILES}"
        done    
        
        3dTcat -prefix ${DIR_DATA}/${DIR_EXPT}/${SUB}/${DATA_TYPE}/func_MNI_concat.nii.gz \
               `echo ${INPUT}`
    fi
done

# create experiment wide mask
if [ ! -f ${DIR_DATA}/${DIR_EXPT}/mask_group.nii.gz ]; then
    3dmask_tool -input ${DIR_DATA}/${DIR_EXPT}/*/${DATA_TYPE}/*/anat_EPI_mask_MNI.nii.gz \
                -prefix ${DIR_DATA}/${DIR_EXPT}/mask_group_MNI.nii.gz -frac 1.0
fi
cd ${DIR_PIPE}

## JDV Jan 30 2014