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
        
        if [ ! -f ${DIR_T1}/${SESS}/mat_T1_to_TAL.1D ]; then            
            # Copy EPI and MNI brain into /tmp.
            3dcopy ${DIR_AFNI}/MNI_avg152T1+tlrc template

            # If we have a T1 for each session, we register to the session T1. 
            # Otherwise, we go to the first session.
            if [ `ls -l ${DIR} | grep ^d | wc -l` -eq \
                 `ls -l ${DIR_T1} | grep ^d | wc -l` ]; then
                3dcopy ${DIR_T1}/${SESS}/anat_T1_brain.nii.gz anat_T1_brain
            else
                3dcopy ${DIR_T1}/SESS01/anat_T1_brain.nii.gz anat_T1_brain
            fi

            # T1 to MNI
            @auto_tlrc -base template+tlrc \
                       -input anat_T1_brain+orig \
                       -no_ss -maxite 300 -OK_maxite \
                       -init_xform AUTO_CENTER

            mv anat_T1_brain.Xat.1D ${DIR_T1}/${SESS}/mat_T1_to_TAL.1D

            if [ `ls -l ${DIR} | grep ^d | wc -l` -eq \
                 `ls -l ${DIR_T1} | grep ^d | wc -l` ]; then
                3dcopy anat_T1_brain+tlrc \
                       ${DIR_T1}/${SESS}/reg_T1_to_TAL.nii.gz
            else
                3dcopy anat_T1_brain+tlrc \
                       ${DIR_T1}/SESS01/reg_T1_to_TAL.nii.gz
            fi
        fi
        
        if [ ! -f ${DIR_T1}/${SESS}/reg_EPI_to_T1.nii.gz ]; then
            # EPI to T1
            flirt -in ${DIR}/${SESS}/anat_EPI_brain.nii.gz \
                  -ref ${DIR_T1}/${SESS}/anat_T1_brain.nii.gz \
                  -out ${DIR_T1}/${SESS}/reg_EPI_to_T1.nii.gz \
                  -omat ${DIR}/${SESS}/mat_EPI_to_T1.mat \
                  -dof 12 \
                  -cost corratio \
                  -searchcost mutualinfo \
                  -searchrx -180 180 -searchry -180 180 -searchrz -180 180 \
                  -v
        fi

        if [ ! -f ${DIR}/${SESS}/mat_T1_to_EPI.mat ]; then
            # invert flirt transform
            convert_xfm -omat ${DIR}/${SESS}/mat_T1_to_EPI.mat \
                        -inverse \
                        ${DIR}/${SESS}/mat_EPI_to_T1.mat
        fi

        # Clean up leftovers in /tmp
        rm anat_*
        rm __tt*
        rm template*
        rm pre.*
    done
done
cd ${DIR_PIPE}

## JDV Jan 30 2014