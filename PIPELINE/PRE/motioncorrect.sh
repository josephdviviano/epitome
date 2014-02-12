#!/bin/bash

## Motion Correct Module: General pre-processing for all fMRI data
#  Orients data to RAI
#  Deletes initial time points
#  Despikes
#  Slice time correction (assumes good headers)
#  Deobliques data
#  Motion correction (outputs motion files for TR censoring a la Power 2012)
#  Scales each run to have mode = 1000
#  Creates session mean deskulled EPIs and masks
#  Calculates various statistics + time series

cd /tmp
for SUB in ${SUBJECTS}; do
    DIR_SESS=`ls -d -- ${DIR_DATA}/${DIR_EXPT}/${SUB}/${DATA_TYPE}/*/`
    for SESS in ${DIR_SESS}; do
        mkdir ${SESS}/PARAMS
        # this used to be here: `ls -d -- ${SESS}/run*/ | sort -n -t n -k 4`
        DIR_RUNS=`ls -d -- ${SESS}/RUN*`
        for RUN in ${DIR_RUNS}; do
            NUM=`basename ${RUN} | sed 's/[^0-9]//g'`
            FILE=`echo ${RUN}/*.nii.gz`

            # 1: Reorient, delete initial timepoints, despike, slice time correct 
            if [ ! -f ${SESS}/func_tshift.${NUM}.nii.gz ]; then
                # ensure all data is in RAI
                3daxialize -prefix ${SESS}/func_tmp_RAI.${NUM}.nii.gz \
                           -axial \
                          ${FILE} 
                
                # delete initial time points
                3dcalc -prefix ${SESS}/func_tmp_del.${NUM}.nii.gz \
                       -a ${SESS}/func_tmp_RAI.${NUM}.nii.gz[${DELTR}..$] \
                       -expr 'a'

                # despike
                3dDespike -prefix ${SESS}/func_tmp_despike.${NUM}.nii.gz \
                          -ssave ${SESS}/PARAMS/spikes.${NUM}.nii.gz \
                          ${SESS}/func_tmp_del.${NUM}.nii.gz

                # slice time correction
                3dTshift -prefix ${SESS}/func_tshift.${NUM}.nii.gz \
                         -verbose -Fourier \
                          ${SESS}/func_tmp_despike.${NUM}.nii.gz
            fi

            # 2: Deoblique, motion correct, and scale data
            if [ ! -f ${SESS}/func_motion.${NUM}.nii.gz ]; then
                3dWarp -prefix ${SESS}/func_tmp_ob.${NUM}.nii.gz \
                       -deoblique -quintic -verb \
                       -newgrid ${DIMS} ${SESS}/func_tshift.${NUM}.nii.gz

                # motion correct to 8th sub-brick of 1st run
                3dvolreg -prefix ${SESS}/func_motion.${NUM}.nii.gz \
                         -base ${SESS}'/func_tmp_ob.01.nii.gz[8]' \
                         -twopass -twoblur 3 -twodup \
                         -Fourier -zpad 2 -float \
                         -1Dfile ${SESS}/PARAMS/motion.${NUM}.1D \
                         -1Dmatrix_save ${SESS}/PARAMS/3dvolreg.${NUM}.aff12.1D \
                          ${SESS}/func_tmp_ob.${NUM}.nii.gz
            fi

            if [ ! -f ${SESS}/func_scaled.${NUM}.nii.gz ]; then
                # scale each run to have mode = 1000
                3dTstat -prefix ${SESS}/func_tmp_mode.${NUM}.nii.gz \
                         ${SESS}/func_motion.${NUM}.nii.gz
                
                3dcalc -prefix ${SESS}/func_scaled.${NUM}.nii.gz \
                       -a ${SESS}/func_motion.${NUM}.nii.gz \
                       -b ${SESS}/func_tmp_mode.${NUM}.nii.gz \
                       -expr 'min(2000, a/b*1000)*step(a)*step(b)'
            fi
            
            # create TS mean for each run
            if [ ! -f ${SESS}/anat_EPI_brain.nii.gz ]; then
                3dTstat -prefix ${SESS}/anat_EPI_tmp_ts_mean.${NUM}.nii.gz \
                         ${SESS}/func_motion.${NUM}.nii.gz
            fi

        done

        ## create session 3D EPI brain + mask (loosened peels)
        if [ ! -f ${SESS}/anat_EPI_brain.nii.gz ]; then
            # create mean over all runs
            3dMean -prefix ${SESS}/anat_EPI_tmp_mean.nii.gz \
                    ${SESS}/anat_EPI_tmp_ts_mean*
            
            3dTstat -prefix ${SESS}/anat_EPI_tmp_vol.nii.gz \
                     ${SESS}/anat_EPI_tmp_mean.nii.gz
            
            3dAutomask -prefix ${SESS}/anat_EPI_mask.nii.gz \
                       -clfrac 0.3 -peels 1 \
                        ${SESS}/anat_EPI_tmp_vol.nii.gz
            
            3dcalc -prefix ${SESS}/anat_EPI_brain.nii.gz \
                   -a ${SESS}/anat_EPI_tmp_vol.nii.gz \
                   -b ${SESS}/anat_EPI_mask.nii.gz \
                   -expr 'a*b'
        fi

        # this used to say: `ls -d -- ${SESS}/run*/ | sort -n -t n -k 4`
        DIR_RUNS=`ls -d -- ${SESS}/RUN*`
        for RUN in ${DIR_RUNS}; do
            NUM=`basename ${RUN} | sed 's/[^0-9]//g'`

            ## % signal change DVARS (Power et. al Neuroimage 2012)
            if [ ! -f ${SESS}/PARAMS/DVARS.${NUM}.1D ]; then
                3dcalc -a ${SESS}/func_scaled.${NUM}.nii.gz \
                       -b 'a[0,0,0,-1]' \
                       -expr '(a - b)^2' \
                       -prefix ${SESS}/func_tmp_backdif.${NUM}.nii.gz
                
                
                3dmaskave -mask ${SESS}/anat_EPI_mask.nii.gz \
                          -quiet ${SESS}/func_tmp_backdif.${NUM}.nii.gz > ${SESS}/PARAMS/tmp_backdif.${NUM}.1D
                
                1deval -a ${SESS}/PARAMS/tmp_backdif.${NUM}.1D \
                       -expr 'sqrt(a)' > ${SESS}/PARAMS/DVARS.${NUM}.1D
                #3dTstat -mean -stdev -prefix %s.backdif2.avg.dvars.stats.1D %s.backdif2.avg.dvars.1D\\\'
            fi

            # Global mean
            if [ ! -f ${SESS}/PARAMS/global_mean.${NUM}.1D ]; then
                3dmaskave -mask ${SESS}/anat_EPI_mask.nii.gz \
                          -quiet ${SESS}/func_scaled.${NUM}.nii.gz > ${SESS}/PARAMS/global_mean.${NUM}.1D
            fi
        done
        rm ${SESS}/anat_EPI_tmp*.nii.gz
        rm ${SESS}/func_tmp*.nii.gz
        rm ${SESS}/PARAMS/tmp*.1D
    done
done
cd ${DIR_PIPE}

## JDV Jan 30 2014