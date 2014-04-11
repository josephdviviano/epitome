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
    rm ${DIR_DATA}/${DIR_EXPT}/${SUB}/${DATA_TYPE}/func_* >& /dev/null

    DIR_SESS=`ls -d -- ${DIR_DATA}/${DIR_EXPT}/${SUB}/${DATA_TYPE}/*/`
    for SESS in ${DIR_SESS}; do
        
        # remove per-session files
        rm ${SESS}/func_smooth* >& /dev/null
        rm ${SESS}/func_noise* >& /dev/null
        rm ${SESS}/func_scrubbed* >& /dev/null
        rm ${SESS}/func_MNI* >& /dev/null
        rm ${SESS}/func_tSNR* >& /dev/null

    done
done
fi
# JDV