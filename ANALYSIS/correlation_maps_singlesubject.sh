#!/bin/bash

# generates seed-based correlation maps at the subject level for each ROI

if [ "$#" -eq 0 ]; then
	echo " I need to know where your ROI file is! "
	exit
fi

MASK=${1}

cd /tmp
for SUB in ${SUBJECTS}; do
	3dROIstats \
	    -mask ${MASK} \
	    -1Dformat \
	    -nzmean \
	    ${DIR_DATA}/${DIR_EXPT}/${SUB}/${DATA_TYPE}/func_MNI_concat.nii.gz
