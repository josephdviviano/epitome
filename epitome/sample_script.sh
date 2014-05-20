#!/bin/bash

# a simple file containing the participants to be analyzed

## Setup
export DIR_PIPE='/srv/CODE/PIPELINE'
export DIR_DATA='/srv/MRI/WORKING'
export DIR_AFNI='/usr/local/abin'
export CORES=7

export AFNI_DECONFLICT=OVERWRITE
export SUBJECTS=`python ${DIR_PIPE}/ypp_inputs.py ${DIR_DATA} ${DIR_EXPT}`

## Options
export DIR_EXPT="TRSEEN"
export DATA_TYPE='LOCALIZER'
export DELTR=0              # TRs to delete from the beginning of each run
export DIMS=3               # voxel dimensions post-reslice (iso)
export POLORT=4             # detrend degree
export BLUR_FWHM=6          # blur FWHM
export TPATTERN='alt+z'     # MRI acquisition specific slice timing
export DATA_QUALITY='high'  # options = 'low' and 'high'
export COST='lpc+zz'        # registration cost function
export REG_DOF='giant_move' # registration constraints

# PIPELINE
#python ${DIR_PIPE}/PRE/freesurfer_T1_export.py ${DIR_DATA} ${DIR_EXPT}
${DIR_PIPE}/PRE/motioncorrect.sh
${DIR_PIPE}/PRE/linreg_calculate.sh
#${DIR_PIPE}/PRE/linreg_FSATLAS_to_EPI.sh
#${DIR_PIPE}/PRE/create_regressors.sh
#${DIR_PIPE}/PRE/filter.sh
#${DIR_PIPE}/PRE/filter_gsreg.sh
${DIR_PIPE}/PRE/linreg_EPI_to_MNI.sh

#${DIR_PIPE}/WIP/headmotion_TRdrop.py ${DIR_DATA} ${DIR_EXPT} ${DATA_TYPE} func_MNI anat_EPI_mask_MNI 50 0.3 65403 
#${DIR_PIPE}/PRE/calculate_globalcorrelation.sh

#path, expt, mode, func_name, mask_name, head_size=50, thresh_FD=1.5, thresh_DV=30000

# QUALITY CONTROL
#python ${DIR_PIPE}/QC/mask_check.py ${DIR_DATA} ${DIR_EXPT} ${DATA_TYPE}
#python ${DIR_PIPE}/QC/motion_individual_plot.py ${DIR_DATA} ${DIR_EXPT} ${DATA_TYPE}
#python ${DIR_PIPE}/QC/reg_check.py ${DIR_DATA} ${DIR_EXPT} ${DATA_TYPE}
#python ${DIR_PIPE}/QC/reg_check_T12MNI.py
#python ${DIR_PIPE}/QC/regressor_spectra.py

##############
# HARD RESET #
##############
#${DIR_PIPE}/UTIL/cleanup_everything.sh
#${DIR_PIPE}/UTIL/cleanup_MNI.sh
#${DIR_PIPE}/UTIL/cleanup_registration.sh
#${DIR_PIPE}/UTIL/cleanup_postmotioncorrect.sh
#${DIR_PIPE}/UTIL/check_runs.sh
