cd ~/MRIdata_subjects/TRSE/1104/SourceDICOMs

# anatomicals
#to3d -view orig -'anat' -prefix 1104_flair+orig.nii -session ../afni/ ./flair_3d_1x1x15_27/*.dcm
#to3d -view orig -'anat' -prefix 1104_mprage+orig.nii -session ../afni/ ./MPRAGE/*.dcm

# epis
to3d -view orig -'epan' -time:zt 18 114 1s alt+z2 -anatparent ../afni/1104_mprage+orig.nii -prefix 1104_01+orig.nii -session ../afni/ ./TRSE_Block_1/*.dcm
to3d -view orig -'epan' -time:zt 18 114 1s alt+z2 -anatparent ../afni/1104_mprage+orig.nii -prefix 1104_02+orig.nii -session ../afni/ ./TRSE_Block_2/*.dcm
to3d -view orig -'epan' -time:zt 18 114 1s alt+z2 -anatparent ../afni/1104_mprage+orig.nii -prefix 1104_03+orig.nii -session ../afni/ ./TRSE_Block_3/*.dcm
to3d -view orig -'epan' -time:zt 18 114 1s alt+z2 -anatparent ../afni/1104_mprage+orig.nii -prefix 1104_04+orig.nii -session ../afni/ ./TRSE_Block_4/*.dcm
to3d -view orig -'epan' -time:zt 18 114 1s alt+z2 -anatparent ../afni/1104_mprage+orig.nii -prefix 1104_05+orig.nii -session ../afni/ ./TRSE_Block_5/*.dcm
to3d -view orig -'epan' -time:zt 18 114 1s alt+z2 -anatparent ../afni/1104_mprage+orig.nii -prefix 1104_06+orig.nii -session ../afni/ ./TRSE_Block_6/*.dcm
to3d -view orig -'epan' -time:zt 18 114 1s alt+z2 -anatparent ../afni/1104_mprage+orig.nii -prefix 1104_07+orig.nii -session ../afni/ ./TRSE_Block_7/*.dcm
to3d -view orig -'epan' -time:zt 18 114 1s alt+z2 -anatparent ../afni/1104_mprage+orig.nii -prefix 1104_08+orig.nii -session ../afni/ ./TRSE_Block_8/*.dcm
to3d -view orig -'epan' -time:zt 18 114 1s alt+z2 -anatparent ../afni/1104_mprage+orig.nii -prefix 1104_09+orig.nii -session ../afni/ ./TRSE_Block_9/*.dcm
to3d -view orig -'epan' -time:zt 18 114 1s alt+z2 -anatparent ../afni/1104_mprage+orig.nii -prefix 1104_10+orig.nii -session ../afni/ ./TRSE_Block_10/*.dcm
to3d -view orig -'epan' -time:zt 18 114 1s alt+z2 -anatparent ../afni/1104_mprage+orig.nii -prefix 1104_11+orig.nii -session ../afni/ ./TRSE_Block_11/*.dcm
to3d -view orig -'epan' -time:zt 18 114 1s alt+z2 -anatparent ../afni/1104_mprage+orig.nii -prefix 1104_12+orig.nii -session ../afni/ ./TRSE_Block_12/*.dcm
to3d -view orig -'epan' -time:zt 18 114 1s alt+z2 -anatparent ../afni/1104_mprage+orig.nii -prefix 1104_13+orig.nii -session ../afni/ ./TRSE_Block_13/*.dcm
to3d -view orig -'epan' -time:zt 18 114 1s alt+z2 -anatparent ../afni/1104_mprage+orig.nii -prefix 1104_14+orig.nii -session ../afni/ ./TRSE_Block_14/*.dcm
to3d -view orig -'epan' -time:zt 18 114 1s alt+z2 -anatparent ../afni/1104_mprage+orig.nii -prefix 1104_15+orig.nii -session ../afni/ ./TRSE_Block_15/*.dcm
to3d -view orig -'epan' -time:zt 18 114 1s alt+z2 -anatparent ../afni/1104_mprage+orig.nii -prefix 1104_16+orig.nii -session ../afni/ ./TRSE_Block_16/*.dcm
to3d -view orig -'epan' -time:zt 18 114 1s alt+z2 -anatparent ../afni/1104_mprage+orig.nii -prefix 1104_17+orig.nii -session ../afni/ ./TRSE_Block_17/*.dcm
to3d -view orig -'epan' -time:zt 18 114 1s alt+z2 -anatparent ../afni/1104_mprage+orig.nii -prefix 1104_18+orig.nii -session ../afni/ ./TRSE_Block_18/*.dcm
to3d -view orig -'epan' -time:zt 18 114 1s alt+z2 -anatparent ../afni/1104_mprage+orig.nii -prefix 1104_19+orig.nii -session ../afni/ ./TRSE_Block_19/*.dcm
to3d -view orig -'epan' -time:zt 18 114 1s alt+z2 -anatparent ../afni/1104_mprage+orig.nii -prefix 1104_20+orig.nii -session ../afni/ ./TRSE_Block_20/*.dcm
to3d -view orig -'epan' -time:zt 18 320 1s alt+z2 -anatparent ../afni/1104_mprage+orig.nii -prefix 1104_21+orig.nii -session ../afni/ ./Functional_Localizer/*.dcm
to3d -view orig -'epan' -time:zt 18 300 1s alt+z2 -anatparent ../afni/1104_mprage+orig.nii -prefix 1104_22+orig.nii -session ../afni/ ./Resting_Scan_1/*.dcm
