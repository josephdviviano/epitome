volsmooth
---------
Usage: volsmooth <func_prefix> <mask_prefix> <FWHM>

+ func_prefix -- functional data prefix (eg., smooth in func_smooth).
+ mask_prefix -- mask data prefix (eg., epi_mask in anat_epi_mask).
+ func_prefix -- functional data prefix (eg.,smooth in func_smooth).

Re-samples a mask containing one or more labels to the functional data and smooths within unique values. All zero values in the mask are zeroed out in the output. The output of this can be combined with the outputs of surfsmooth \& surf2vol using combine_volumes.

Prerequisites: init_epi, linreg_calc_afni, linreg_epi2T1_afni, vol2surf.
