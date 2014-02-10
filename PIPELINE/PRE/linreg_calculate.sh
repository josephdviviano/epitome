#!/bin/bash

## Linear Registration Module: Calculates pathways between T1s and EPI data 
#  (including standard space)
# Calculates: EPI <--> T1 <--> MNI152
# Generates: EPI template registered to T1 & T1 registered to EPI (sessionwise)

cd /tmp
for SUB in ${SUBJECTS}; do
    DIR_SESS=`ls -d -- ${DIR_DATA}/${DIR_EXPT}/${SUB}/${DATA_TYPE}/*/`
    for SESS in `basename ${DIR_SESS}`; do
        DIR=`echo ${DIR_DATA}/${DIR_EXPT}/${SUB}/${DATA_TYPE}`
        DIR_T1=`echo ${DIR_DATA}/${DIR_EXPT}/${SUB}/T1`
        if [ ! -f ${DIR_T1}/${SESS}/reg_EPI_to_T1.nii.gz ]; then
            
            # Copy EPI and MNI brain into /tmp.
            3dcopy ${DIR}/${SESS}/anat_EPI_brain.nii.gz anat_EPI_brain
            3dcopy ${DIR_AFNI}/MNI_avg152T1+tlrc template

            # If we have a T1 for each session, we register to the session T1. 
            # Otherwise, we go to the first session.
            if [ `ls -l ${DIR} | grep ^d | wc -l` -eq \
                 `ls -l ${DIR_T1} | grep ^d | wc -l` ]; then
                3dcopy ${DIR_T1}/${SESS}/anat_T1_brain.nii.gz anat_T1_brain
            else
                3dcopy ${DIR_T1}/SESS01/anat_T1_brain.nii.gz anat_T1_brain
            fi

            # Talarac individual brain, turning off skullstrip.
            @auto_tlrc -base template+tlrc \
                       -input anat_T1_brain+orig \
                       -no_ss -maxite 300 -OK_maxite \
                       -init_xform AUTO_CENTER

            align_epi_anat.py -anat anat_T1_brain+orig \
                              -epi anat_EPI_brain+orig \
                              -epi_base 0 -epi2anat \
                              -suffix EPI_to_T1 \
                              -anat_has_skull no -epi_strip None \
                              -volreg off -tshift off \
                              -giant_move \
                              -tlrc_apar anat_T1_brain+tlrc \
                              -cost lpc

            # Move outputs from /tmp back into data folders folders.
            mv anat_EPI_brainEPI_to_T1_tlrc_mat.aff12.1D \
               ${DIR}/${SESS}/mat_EPI_to_TAL.aff12.1D
            mv anat_EPI_brainEPI_to_T1_mat.aff12.1D \
               ${DIR}/${SESS}/mat_EPI_to_T1.aff12.1D
            mv anat_T1_brainEPI_to_T1_mat.aff12.1D \
               ${DIR}/${SESS}/mat_T1_to_EPI.aff12.1D
            
            3dcopy anat_T1_brain+tlrc ${DIR}/${SESS}/reg_T1_to_TAL.nii.gz
            
            # If we have a T1 for each session, we register to the session T1. 
            # Otherwise, we go to the first session.
            if [ `ls -l ${DIR} | grep ^d | wc -l` -eq \
                 `ls -l ${DIR_T1} | grep ^d | wc -l` ]; then
                3dcopy anat_EPI_brainEPI_to_T1+orig \
                       ${DIR_T1}/${SESS}/reg_EPI_to_T1.nii.gz
            else
                3dcopy anat_EPI_brainEPI_to_T1+orig \
                       ${DIR_T1}/SESS01/reg_EPI_to_T1.nii.gz
            fi

            # Clean up leftovers in /tmp
            rm anat_*
            rm __tt*
            rm template*
            rm pre.*
        fi

        # Create reg_T1_to_EPI
        if [ ! -f ${DIR}/${SESS}/reg_T1_to_EPI.nii.gz ]; then
            # If we have a T1 for each session, we register to the session T1. 
            # Otherwise, we go to the first session.
            if [ `ls -l ${DIR} | grep ^d | wc -l` -eq \
                 `ls -l ${DIR_T1} | grep ^d | wc -l` ]; then
                3dAllineate -prefix ${DIR}/${SESS}/reg_T1_to_EPI.nii.gz \
                            -input ${DIR_T1}/${SESS}/anat_T1_brain.nii.gz \
                            -1Dmatrix_apply ${DIR}/${SESS}/mat_T1_to_EPI.aff12.1D \
                            -float -final quintic
            else
                3dAllineate -prefix ${DIR}/${SESS}/reg_T1_to_EPI.nii.gz \
                            -input ${DIR_T1}/SESS01/anat_T1_brain.nii.gz \
                            -1Dmatrix_apply ${DIR}/${SESS}/mat_T1_to_EPI.aff12.1D \
                            -float -final quintic
            fi                
        fi
    done
done
cd ${DIR_PIPE}

## JDV Jan 30 2014