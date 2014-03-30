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
DIR_EXPT="RSFC2"
#DIR_EXPT="BEBASD"

SUBJECTS=`python ${DIR_PIPE}/ypp_inputs.py ${DIR_DATA} ${DIR_EXPT}`

## Options
DATA_TYPE='REST'
DELTR=4         # number of TRs to delete from the beginning of each run
DIMS=3          # set voxel dimensions post-reslice (iso)
POLORT=4        # degree of legendre polynomials to detrend data against
BLUR_FWHM=6     # blur FWHM
TPATTERN='alt+z' # MRI acquisition specific

## TPATTERN OPTIONS ##
#    alt+z = altplus   = alternating in the plus direction
#    alt+z2            = alternating, starting at slice #1 instead of #0
#    alt-z = altminus  = alternating in the minus direction
#    alt-z2            = alternating, starting at slice #nz-2 instead of #nz-1
#    seq+z = seqplus   = sequential in the plus direction
#    seq-z = seqminus  = sequential in the minus direction
#

export DIR_PIPE
export DIR_DATA
export DIR_AFNI
export DIR_EXPT
export DATA_TYPE
export AFNI_DECONFLICT
export SUBJECTS
export DELTR
export DIMS
export POLORT
export BLUR_FWHM
export TPATTERN

# PIPELINE
#python ${DIR_PIPE}/PRE/freesurfer_T1_export.py ${DIR_DATA} ${DIR_EXPT}
${DIR_PIPE}/PRE/motioncorrect.sh
${DIR_PIPE}/PRE/linreg_calculate.sh
${DIR_PIPE}/PRE/linreg_FSATLAS_to_EPI.sh
${DIR_PIPE}/PRE/create_regressors.sh
${DIR_PIPE}/PRE/filter.sh
${DIR_PIPE}/PRE/linreg_EPI_to_MNI.sh

# QUALITY CONTROL
python ${DIR_PIPE}/QC/mask_check.py ${DIR_DATA} ${DIR_EXPT} ${DATA_TYPE}
python ${DIR_PIPE}/QC/motion_individual_plot.py ${DIR_DATA} ${DIR_EXPT} ${DATA_TYPE}
python ${DIR_PIPE}/QC/reg_check.py ${DIR_DATA} ${DIR_EXPT} ${DATA_TYPE}
#python ${DIR_PIPE}/QC/reg_check_T12MNI.py
#python ${DIR_PIPE}/QC/regressor_spectra.py

##############
# HARD RESET #
##############
#${DIR_PIPE}/UTIL/cleanup_functionals.sh
#${DIR_PIPE}/UTIL/check_runs.sh