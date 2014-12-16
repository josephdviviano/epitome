gen_regressors
--------------
Usage: gen_regressors <func_prefix>

+ func_prefix -- functional data prefix (eg.,smooth in func_smooth).

Creates a series of regressors from fMRI data and a freesurfer segmentation: 

+ white matter + eroded mask
+ ventricles + eroded mask
+ grey matter mask
+ brain stem mask
+ dialated whole-brain mask
+ draining vessels mask
+ local white matter regressors + 1 temporal lag
+ ventricle regressors + 1 temporal lag
+ draining vessel regressors + 1 temporal lag

Prerequisites: init_epi, linreg_calc_afni/fsl, linreg_FS2epi_afni/fsl.

Outputs: set of masks, and regressors in PARAMS/
