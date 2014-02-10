#!/bin/bash

## Warn the user and ask to continue
read -p "About to delete processed functional data! Press Y/y to continue." \
        -n 1 -r
echo # (optional) move to a new line
if [[ $REPLY =~ ^[Yy]$ ]]
then

## Let's Dance https://www.youtube.com/watch?v=N4d7Wp9kKjA ##
for SUB in ${SUBJECTS}; do

    # remove any multisession files
    rm ${DIR_DATA}/${DIR_EXPT}/${SUB}/${DATA_TYPE}/func_*

    DIR_SESS=`ls -d -- ${DIR_DATA}/${DIR_EXPT}/${SUB}/${DATA_TYPE}/*/`
    for SESS in ${DIR_SESS}; do
        
        # remove per-session files
        rm -r ${SESS}/PARAMS/
        rm ${SESS}/anat_*
        rm ${SESS}/func_*
        rm ${SESS}/mat_*
        rm ${SESS}/reg_*
        
    done

    DIR_SESS=`ls -d -- ${DIR_DATA}/${DIR_EXPT}/${SUB}/T1/*/`
    for SESS in ${DIR_SESS}; do

        rm ${SESS}/reg_*
        rm ${SESS}/anat_*

    done
done
fi
# JDV Jan 30 2014