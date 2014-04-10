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
DIR_EXPT="RSFC1"
#DIR_EXPT="RSFC2"
#DIR_EXPT="BEBASD"

SUBJECTS=`python ${DIR_PIPE}/ypp_inputs.py ${DIR_DATA} ${DIR_EXPT}`

## Options
DATA_TYPE='REST'
DELTR=4              # number of TRs to delete from the beginning of each run
DIMS=3               # set voxel dimensions post-reslice (iso)
POLORT=4             # degree of legendre polynomials to detrend data against
BLUR_FWHM=6          # blur FWHM

# slice time correction
TPATTERN='alt+z'     # MRI acquisition specific slice timing (for correction)

# registration
DATA_QUALITY='low'   # options = 'low' and 'high'
COST='lpc+zz'        # registration cost function
REG_DOF='giant_move' # registration constraints

## TPATTERN OPTIONS ##
#    alt+z = altplus   = alternating in the plus direction
#    alt+z2            = alternating, starting at slice #1 instead of #0
#    alt-z = altminus  = alternating in the minus direction
#    alt-z2            = alternating, starting at slice #nz-2 instead of #nz-1
#    seq+z = seqplus   = sequential in the plus direction
#    seq-z = seqminus  = sequential in the minus direction
#

## DATA QUALITY OPTIONS ##
#    high       = Good internal contrast (default)
#    low        = Poor internal contrast, mostly for old data


## COST FXN OPTIONS ##
#    ls   *OR*  leastsq         = Least Squares [Pearson Correlation]
#    mi   *OR*  mutualinfo      = Mutual Information [H(b)+H(s)-H(b,s)]
#    crM  *OR*  corratio_mul    = Correlation Ratio (Symmetrized*)
#    nmi  *OR*  norm_mutualinfo = Normalized MI [H(b,s)/(H(b)+H(s))]
#    hel  *OR*  hellinger       = Hellinger metric
#    crA  *OR*  corratio_add    = Correlation Ratio (Symmetrized+)
#    crU  *OR*  corratio_uns    = Correlation Ratio (Unsym)
#    sp   *OR*  spearman        = Spearman [rank] Correlation
#    je   *OR*  jointentropy    = Joint Entropy [H(b,s)]
#    lss  *OR*  signedPcor      = Signed Pearson Correlation
#    lpc  *OR*  localPcorSigned = Local Pearson Correlation Signed
#    lpa  *OR*  localPcorAbs    = Local Pearson Correlation Abs
#    lpc+ *OR*  localPcor+Others= Local Pearson Signed + Others
#    ncd  *OR*  NormCompDist    = Normalized Compression Distance
#    lpc+zz                     = Local Pearson Correlation Signed + Magic

## REG_DOF OPTIONS ##
#    big_move           = Smaller moves (if giant gives bad registration)
#    giant_move         = Large search space allowed (generally safe)

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
export COST
export REG_DOF
export DATA_QUALITY

# PIPELINE
#python ${DIR_PIPE}/PRE/freesurfer_T1_export.py ${DIR_DATA} ${DIR_EXPT}
#${DIR_PIPE}/PRE/motioncorrect.sh
#${DIR_PIPE}/PRE/linreg_calculate.sh
#${DIR_PIPE}/PRE/linreg_FSATLAS_to_EPI.sh
#${DIR_PIPE}/PRE/create_regressors.sh
#${DIR_PIPE}/PRE/filter.sh
#${DIR_PIPE}/PRE/linreg_EPI_to_MNI.sh

#${DIR_PIPE}/PRE/calculate_globalcorrelation.sh

${DIR_PIPE}/WIP/headmotion_TRdrop.py ${DIR_DATA} ${DIR_EXPT} ${DATA_TYPE} func_MNI anat_EPI_mask_MNI 50 1.5 32344 
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
#${DIR_PIPE}/UTIL/check_runs.sh

## JDV