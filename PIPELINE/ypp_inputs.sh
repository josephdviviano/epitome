#!/bin/bash

# a simple file containing the participants to be analyzed

## Directories ##
DIR_PIPE='/srv/CODE/PIPELINE'
DIR_DATA='/srv/MRI/WORKING'
DIR_AFNI='/usr/local/abin'
AFNI_DECONFLICT=OVERWRITE
CORES=7

#DIR_EXPT="TRSE"
#DIR_EXPT="SAB1"
#DIR_EXPT="ATOL"
#DIR_EXPT="TRSEEN"
#DIR_EXPT="RSFC1"
#DIR_EXPT="RSFC2"
DIR_EXPT="BEBASD"

SUBJECTS=`python ${DIR_PIPE}/ypp_inputs.py ${DIR_DATA} ${DIR_EXPT}`

## Options
DATA_TYPE='TASK'
DELTR=4     # number of TRs to delete from the beginning of each run
DIMS=3      # set voxel dimensions post-reslice (iso)
POLORT=4    # degree of legendre polynomials to detrend data against
BLUR_FWHM=6 # blur FWHM

export DIR_PIPE
export DIR_DATA
export DIR_AFNI
export DATA_TYPE
export AFNI_DECONFLICT
export DIR_EXPT
export SUBJECTS
export DELTR
export DIMS
export POLORT
export BLUR_FWHM

# PIPELINE
#python ${DIR_PIPE}/PRE/freesurfer_T1_export.py ${DIR_DATA} ${DIR_EXPT}
#${DIR_PIPE}/PRE/motioncorrect.sh
#${DIR_PIPE}/PRE/linreg_calculate.sh
#${DIR_PIPE}/PRE/linreg_FSATLAS_to_EPI.sh
#${DIR_PIPE}/PRE/create_regressors.sh
#${DIR_PIPE}/PRE/filter.sh
#${DIR_PIPE}/PRE/linreg_EPI_to_MNI.sh

#${DIR_PIPE}/UTIL/cleanup_functionals.sh
#${DIR_PIPE}/UTIL/check_runs.sh

#python ${DIR_PIPE}/QC/mask_check.py
#python ${DIR_PIPE}/QC/motion_individual_plot.py
python ${DIR_PIPE}/QC/reg_check.py ${DIR_DATA} ${DIR_EXPT} ${DATA_TYPE}
#python ${DIR_PIPE}/QC/reg_check_T12MNI.py
#python ${DIR_PIPE}/QC/regressor_spectra.py
