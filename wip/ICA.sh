#!/bin/bash

## This will run ICA on your raw data, which is useful when looking for bad runs /
## scanner artifacts. This won't actually do anything to you data, but you could
## regress "bad" components after identifing them (by eye... yuck) using fsl_regfilt

for SUB in ${SUBJECTS}; do
    
    DIR_SESS=`ls -d -- ${DIR_DATA}/${DIR_EXPT}/${SUB}/task/*/`
    for SESS in ${DIR_SESS}; do
    	
    	DIR_RUNS=`ls -d -- ${SESS}/run*/`
        NUM=1 # counter for numbering files
        for RUNS in ${DIR_RUNS}; do
        	FILE=`echo ${RUNS}run*.nii.gz`

        	# run MELODIC, output some images of components (saves space)
        	if [ ! -f ${SESS}melodic.${NUM}.ica/ ]; then
        	melodic -i ${FILE} -o ${SESS}melodic.${NUM} --dimest=lap --Oorig --Ostats
            fi 
            
            NUM=$((NUM + 1))
        done
    done
done

## JDV Jan 9 2014