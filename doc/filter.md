filter
------
Usage: filter <func_prefix> <det> <gs> <vent> <dv> <wm_loc> <wm_glo>

+ func_prefix -- functional data prefix (eg.,smooth in func_smooth). 
+ det -- polynomial order to detrend each voxel against. 
+ gs -- if == on, regress mean global signal from each voxel. 
+ vent -- if == on, regress mean ventricle signal from each voxel. 
+ dv -- if == on, regress mean draining vessel signal from each voxel. 
+ wm_loc -- if == on, regress local white matter from target voxels. 
+ wm_glo -- if == on, regress global white matter for all voxels.

This computes detrended nuisance time series, fits each run with a computed noise model, and subtracts the fit. Computes temporal SNR. This program always regresses the motion parameters \& their first lags, as well as physiological noise regressors generated my McRetroTS if they are available. The rest are optional, and generally advisable save global mean regression.

Prerequisites: init_epi, linreg_calc_afni/fsl, linreg_FS2epi_afni/fsl, gen_regressors.

Outputs: filtered
