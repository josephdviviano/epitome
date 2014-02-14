#!/bin/bash

## Brings T1-associated files to single participant / single session space

cd /tmp
for SUB in ${SUBJECTS}; do
    DIR_SESS=`ls -d -- ${DIR_DATA}/${DIR_EXPT}/${SUB}/${DATA_TYPE}/*/`
    for SESS in `basename ${DIR_SESS}`; do
        
        DIR=`echo ${DIR_DATA}/${DIR_EXPT}/${SUB}/${DATA_TYPE}/${SESS}`
        DIR_T1=`echo ${DIR_DATA}/${DIR_EXPT}/${SUB}/T1/${SESS}`
        
        +# register GM to MNI
        if [ ! -f ${DIR}/anat_aparc_MNI.nii.gz ]; then
            3dAllineate -prefix ${DIR}/anat_aparc_MNI.nii.gz \
                        -input ${DIR_T1}/anat_aparc_brain.nii.gz \
                        -1Dmatrix_apply ${DIR_T1}/mat_T1_to_TAL.1D \
                        -master ${DIR_AFNI}/MNI_avg152T1+tlrc \
                        -float -interp NN -final NN
        fi

        # register GM to MNI
        if [ ! -f ${DIR}/anat_aparc2009_MNI.nii.gz ]; then
            3dAllineate -prefix ${DIR}/anat_aparc2009_MNI.nii.gz \
                        -input ${DIR_T1}/anat_aparc2009_brain.nii.gz \
                        -1Dmatrix_apply ${DIR_T1}/mat_T1_to_TAL.1D \
                        -master ${DIR_AFNI}/MNI_avg152T1+tlrc \
                        -float -interp NN -final NN
        fi
        
        # register GM to MNI
        if [ ! -f ${DIR}/anat_gm_MNI.nii.gz ]; then
            3dAllineate -prefix ${DIR}/anat_gm_MNI.nii.gz \
                        -input ${DIR}/anat_gm.nii.gz \
                        -1Dmatrix_apply ${DIR_T1}/mat_T1_to_TAL.1D \
                        -master ${DIR_AFNI}/MNI_avg152T1+tlrc \
                        -mast_dxyz ${DIMS} ${DIMS} ${DIMS} \
                        -float -interp NN -final NN
        fi

    done
done
cd ${DIR_PIPE}

## JDV Jan 30 2014