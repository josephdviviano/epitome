filter
------
Usage: filter <func_prefix> <det> <gs> <vent> <dv> <wm_loc> <wm_glo>

+ func_prefix -- functional data prefix (eg.,smooth in func_smooth). 
+ det -- polynomial order to detrend each voxel against. 
+ std -- if == on, does standard basic time-series filtering (mean white matter and csf regression).
+ gs -- if == on, regress mean global signal from each voxel (careful...). 
+ anaticor -- if == on, regress 15mm local white matter signal from data. 
+ compcor -- if == on, regress top 3 principal components from both the white matter and csf from the data.
+ dv -- if == on, regress mean draining vessel signal from each voxel. 

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

This computes detrended nuisance time series, fits each run with a computed noise model, and subtracts the fit. Computes temporal SNR. This program always regresses the motion parameters \& their first lags, as well as physiological noise regressors generated my McRetroTS if they are available. The rest are optional.

Prerequisites: init_epi, linreg_calc_afni/fsl, linreg_FS2epi_afni/fsl.

Outputs: set of masks, and regressors in PARAMS/,  filtered
