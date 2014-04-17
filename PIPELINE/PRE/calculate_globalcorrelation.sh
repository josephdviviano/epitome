#!/bin/bash

## calculate global correlation for each concatenated run

cd /tmp

for SUB in ${SUBJECTS}; do
    for FILE in `ls ${DIR_DATA}/${DIR_EXPT}/${SUB}/${DATA_TYPE}/*.nii.gz`; do
        FNAME=`basename ${FILE}`
        if [ ! -f ${DIR_DATA}/${DIR_EXPT}/${SUB}/${DATA_TYPE}/${FNAME}.gcorr ]; then
            @compute_gcor \
                -input ${FILE} \
                -verb 0 \
                -mask ${DIR_DATA}/${DIR_EXPT}/${SUB}/${DATA_TYPE}/SESS01/anat_EPI_mask_MNI.nii.gz \
                > ${DIR_DATA}/${DIR_EXPT}/${SUB}/${DATA_TYPE}/${FNAME}.gcorr
        fi
    done
done

cd ${DIR_PIPE}
