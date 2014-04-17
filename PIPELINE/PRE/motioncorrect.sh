#!/bin/bash

## Motion Correct Module: General pre-processing for all fMRI data
#  Orients data to RAI
#  Deletes initial time points
#  Despikes
#  Slice time correction (assumes good headers)
#  Deobliques data
#  Motion correction (outputs motion files for TR censoring a la Power 2012)
#  Creates session mean deskulled EPIs and masks
#  Scales each run to have mode = 1000, removing obviously non-brain data
#  Calculates various statistics + time series

echo '*************************************************************************'
echo '    Motion Correction and General Pre-processing for all fMRI data'
echo ''
echo '    Running with the following options:'
echo '        EXPERIMENT           :' ${DIR_EXPT}
echo '        DATA TYPE            :' ${DATA_TYPE}
echo '        # OF TRs TO REMOVE   :' ${DELTR}
echo '        FINAL DIMENSIONS (mm):' ${DIMS}
echo '        DETREND ORDER        :' ${POLORT}
echo '        BLUR FWHM            :' ${BLUR_FWHM}
echo '        SLICE TIMING         :' ${TPATTERN}
echo '        DATA QUALITY         :' ${DATA_QUALITY}
echo '        REGISTRATION COST FXN:' ${COST}
echo '        REGISTRATION DOF     :' ${REG_DOF}
echo ''
echo '*************************************************************************'

cd /tmp

# loop through subjects, sessions, and runs, respectively
for SUB in ${SUBJECTS}; do
    DIR_SESS=`ls -d -- ${DIR_DATA}/${DIR_EXPT}/${SUB}/${DATA_TYPE}/*/`

    for SESS in ${DIR_SESS}; do
        mkdir ${SESS}/PARAMS
        DIR_RUNS=`ls -d -- ${SESS}/RUN*`

        for RUN in ${DIR_RUNS}; do
            NUM=`basename ${RUN} | sed 's/[^0-9]//g'`
            FILE=`echo ${RUN}/*.nii.gz`

            # 1: Reorient, delete initial TRs, despike, slice time correct 
            if [ ! -f ${SESS}/func_tshift.${NUM}.nii.gz ]; then
                # ensure all data is in RAI
                3daxialize \
                    -prefix ${SESS}/func_tmp_RAI.${NUM}.nii.gz \
                    -axial \
                    ${FILE} 
                
                # retain 1st TR
                if [ ${DATA_QUALITY} = 'low' ]; then
                    if [ ${NUM} = 01 ]; then
                        # strip off the pre-stabilization TR
                        3dcalc \
                            -prefix ${SESS}/anat_EPI_tmp_initTR.nii.gz \
                            -a ${SESS}/func_tmp_RAI.${NUM}.nii.gz[0] \
                            -expr 'a'
                    fi
                fi

                # delete initial time points
                3dcalc \
                    -prefix ${SESS}/func_tmp_del.${NUM}.nii.gz \
                    -a ${SESS}/func_tmp_RAI.${NUM}.nii.gz[${DELTR}..$] \
                    -expr 'a'

                # despike
                3dDespike \
                    -prefix ${SESS}/func_tmp_despike.${NUM}.nii.gz \
                    -ssave ${SESS}/PARAMS/spikes.${NUM}.nii.gz \
                     ${SESS}/func_tmp_del.${NUM}.nii.gz

                # RetroICORR correction for physiological noise, if exists
                if [ -f ${RUN}/*.phys ]; then
                    # get the relevant variables
                    X=`fslhd 130013_3T_rfMRI_REST1_LR.nii.gz \
                             | sed -n 6p | cut -c 5-`
                    Y=`fslhd 130013_3T_rfMRI_REST1_LR.nii.gz \
                             | sed -n 7p | cut -c 5-`
                    Z=`fslhd 130013_3T_rfMRI_REST1_LR.nii.gz \
                             | sed -n 8p | cut -c 5-`
                    SLICE=`perl -e "@xyz=(${X},${Y},${Z}); \
                                    @slice=(sort{$a<=>$b}@xyz)[0]; \
                                    print @slice"`
                    SAMP=`cat 130013_3T_rfMRI_REST1_LR_Physio_log.txt | wc -l`
                    NTRS=`fslhd 130013_3T_rfMRI_REST1_LR.nii.gz \
                             | sed -n 9p | cut -c 5-`
                    TR=`fslhd 130013_3T_rfMRI_REST1_LR.nii.gz \
                             | sed -n 22p | cut -c 9-`
                    
                    # compute sampling rate of physio recording
                    UNITS=`fslhd 130013_3T_rfMRI_REST1_LR.nii.gz \
                                 | sed -n 14p | cut -c 11- | xargs`
                    # convert ms to seconds, if necessary
                    if [ ${UNITS} = 's' ]; then
                        TIME=`perl -e "print ${NTRS} \* ${TR}"`
                    elif [ ${UNITS} = 'ms' ]; then
                        TIME=`perl -e "print ${NTRS} * ${TR} / 1000"`
                    fi 
                    FS=`perl -e "print ${SAMP} / ${TIME}"`
                    # McRetroTS Respfile Cardfile VolTR Nslices PhysFS Graph
                    McRetroTS resp.phys card.phys ${TR} ${SLICE} ${FS} 0
   
                else
                    # just skip this stage & match ouput file names
                    mv ${SESS}/func_tmp_despike.${NUM}.nii.gz \
                       ${SESS}/func_tmp_retroic.${NUM}.nii.gz
                fi

                # slice time correction (can include specified timings)
                if [ -f ${RUN}/slice_timing.1D ]; then
                    3dTshift \
                        -prefix ${SESS}/func_tshift.${NUM}.nii.gz \
                        -verbose \
                        -Fourier \
                        -tpattern @ ${RUN}/slice_timing.1D \
                        ${SESS}/func_tmp_retroic.${NUM}.nii.gz
                else
                    3dTshift \
                        -prefix ${SESS}/func_tshift.${NUM}.nii.gz \
                        -verbose -Fourier \
                        -tpattern ${TPATTERN} \
                        ${SESS}/func_tmp_retroic.${NUM}.nii.gz
                fi
            fi

            # 2: Deoblique, motion correct, and scale data
            if [ ! -f ${SESS}/func_motion.${NUM}.nii.gz ]; then
                # deoblique run
                3dWarp \
                    -prefix ${SESS}/func_ob.${NUM}.nii.gz \
                    -deoblique \
                    -quintic \
                    -verb \
                    -gridset ${SESS}/func_tshift.01.nii.gz \
                    ${SESS}/func_tshift.${NUM}.nii.gz

                # motion correct to 9th sub-brick of 1st run
                3dvolreg \
                    -prefix ${SESS}/func_motion.${NUM}.nii.gz \
                    -base ${SESS}'/func_ob.01.nii.gz[8]' \
                    -twopass \
                    -twoblur 3 \
                    -twodup \
                    -Fourier \
                    -zpad 2 \
                    -float \
                    -1Dfile ${SESS}/PARAMS/motion.${NUM}.1D \
                    -1Dmatrix_save ${SESS}/PARAMS/3dvolreg.${NUM}.aff12.1D \
                    ${SESS}/func_ob.${NUM}.nii.gz

                # make a registration volume for low-quality data if required
                if [ ${DATA_QUALITY} = 'low' ] && [ ${NUM} = 01 ]; then
                    # deoblique registration volume
                    3dWarp \
                        -prefix ${SESS}/anat_EPI_tmp_initTR_ob.nii.gz \
                        -deoblique \
                        -quintic \
                        -verb \
                        -gridset ${SESS}/func_tshift.01.nii.gz \
                        ${SESS}/anat_EPI_tmp_initTR.nii.gz

                    # align registration volume with the motion correction TR
                    3dvolreg \
                        -prefix ${SESS}/anat_EPI_initTR.nii.gz \
                        -base ${SESS}'/func_ob.01.nii.gz[8]' \
                        -twopass \
                        -twoblur 3 \
                        -twodup \
                        -Fourier \
                        -zpad 2 \
                        -float \
                        ${SESS}/anat_EPI_tmp_initTR_ob.nii.gz
                fi
            fi
            
            # create TS mean for each run
            if [ ! -f ${SESS}/anat_EPI_brain.nii.gz ]; then
                3dTstat \
                    -prefix ${SESS}/anat_EPI_tmp_ts_mean.${NUM}.nii.gz \
                    ${SESS}/func_motion.${NUM}.nii.gz
            fi

        done

        ## create session 3D EPI brain + mask (loosened peels)
        if [ ! -f ${SESS}/anat_EPI_brain.nii.gz ]; then
            # create mean over all runs
            3dMean \
                -prefix ${SESS}/anat_EPI_tmp_mean.nii.gz \
                ${SESS}/anat_EPI_tmp_ts_mean*
            
            3dTstat \
                -prefix ${SESS}/anat_EPI_tmp_vol.nii.gz \
                ${SESS}/anat_EPI_tmp_mean.nii.gz
            
            3dAutomask \
                -prefix ${SESS}/anat_EPI_mask.nii.gz \
                -clfrac 0.3 \
                -peels 1 \
                ${SESS}/anat_EPI_tmp_vol.nii.gz
            
            3dcalc \
                -prefix ${SESS}/anat_EPI_brain.nii.gz \
                -a ${SESS}/anat_EPI_tmp_vol.nii.gz \
                -b ${SESS}/anat_EPI_mask.nii.gz \
                -expr 'a*b'

            if [ ${DATA_QUALITY} = 'low' ]; then
                3dcalc \
                    -prefix ${SESS}/anat_EPI_initTR_brain.nii.gz \
                    -a ${SESS}/anat_EPI_initTR.nii.gz \
                    -b ${SESS}/anat_EPI_mask.nii.gz \
                    -expr 'a*b'
            fi

        fi

        DIR_RUNS=`ls -d -- ${SESS}/RUN*`
        for RUN in ${DIR_RUNS}; do
            NUM=`basename ${RUN} | sed 's/[^0-9]//g'`

            if [ ! -f ${SESS}/func_scaled.${NUM}.nii.gz ]; then
                # scale each run to have mode = 1000
                3dTstat \
                    -prefix ${SESS}/func_tmp_median.${NUM}.nii.gz \
                    -median \
                    ${SESS}/func_motion.${NUM}.nii.gz

                3dmaskave \
                    -median \
                    -quiet \
                    -mask ${SESS}/anat_EPI_brain.nii.gz \
                    ${SESS}/func_tmp_median.${NUM}.nii.gz \
                    > ${SESS}/tmp_median.1D

                MEDIAN=`cat ${SESS}/tmp_median.1D`
                3dcalc \
                    -prefix ${SESS}/func_scaled.${NUM}.nii.gz \
                    -a ${SESS}/func_motion.${NUM}.nii.gz \
                    -b ${SESS}/func_tmp_median.${NUM}.nii.gz \
                    -c ${SESS}/anat_EPI_mask.nii.gz \
                    -expr "a*(1000/b)*astep(a, ${MEDIAN}*0.10)*c" \
                    -datum float
                rm ${SESS}/tmp_median.1D
            fi

            # % signal change DVARS (Power et. al Neuroimage 2012)
            if [ ! -f ${SESS}/PARAMS/DVARS.${NUM}.1D ]; then
                3dcalc \
                    -a ${SESS}/func_scaled.${NUM}.nii.gz \
                    -b 'a[0,0,0,-1]' \
                    -expr '(a - b)^2' \
                    -prefix ${SESS}/func_tmp_backdif.${NUM}.nii.gz
                
                
                3dmaskave \
                    -mask ${SESS}/anat_EPI_mask.nii.gz \
                    -quiet ${SESS}/func_tmp_backdif.${NUM}.nii.gz \
                    > ${SESS}/PARAMS/tmp_backdif.${NUM}.1D
                
                1deval \
                    -a ${SESS}/PARAMS/tmp_backdif.${NUM}.1D \
                    -expr 'sqrt(a)' \
                    > ${SESS}/PARAMS/DVARS.${NUM}.1D
            fi

            # Global mean
            if [ ! -f ${SESS}/PARAMS/global_mean.${NUM}.1D ]; then
                3dmaskave \
                    -mask ${SESS}/anat_EPI_mask.nii.gz \
                    -quiet ${SESS}/func_scaled.${NUM}.nii.gz \
                    > ${SESS}/PARAMS/global_mean.${NUM}.1D
            fi
        done
        rm ${SESS}/anat_EPI_tmp*.nii.gz >& /dev/null
        rm ${SESS}/func_tmp*.nii.gz >& /dev/null
        rm ${SESS}/PARAMS/tmp*.1D >& /dev/null
    done
done
cd ${DIR_PIPE}
