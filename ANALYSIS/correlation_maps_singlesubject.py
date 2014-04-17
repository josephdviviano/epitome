import os
import copy

import numpy as np
import scipy as sp
import scipy.stats as stat
import matplotlib.pyplot as plt

from statsmodels.formula.api import ols
from statsmodels.graphics.api import interaction_plot, abline_plot
from statsmodels.stats.anova import anova_lm
import statsmodels.api as sm
import pandas as pd

import nibabel as nib
import ypp_utilities
import ypp_stats

## init some useful variables
dir_ana = '/srv/MRI/ANALYSIS/REST'
dir_mri = '/srv/MRI/WORKING/'
experiments = ['RSFC1', 'RSFC2']
#in_file = 'func_MNI_concat.nii.gz'
in_file = 'func_MNI_concat_scrubbed.nii.gz'
ROI_file = 'ROIs_noATOL.nii.gz'

# get us to the right directory
os.system('cd ' + dir_ana)

## Rational: All we're doing here is calculating the whole-brain correlation
#  map from each seed defined by the ROI mask with every other voxel in the
#  brain, defined as the intersection of the two group-masks.

labels = ['d_attn_A', 
          'd_attn_B', 
          'd_attn_C', 
          'd_attn_D', 
          'd_attn_E', 
          'd_attn_F', 
          'def_A',
          'def_B',
          'def_C',
          'def_D',
          'def_E',
          'def_F']

# labels = ['d_attn_A', 
#           'd_attn_B', 
#           'd_attn_C', 
#           'd_attn_D', 
#           'd_attn_E', 
#           'd_attn_F', 
#           'def_A',
#           'def_B',
#           'def_C',
#           'ATOL_MPFC',
#           'def_E',
#           'ATOL_PCC']

groups = {
    '1': ['0023', '0024', '0025', '0028', '0030', '0031', 
          '0033', '0034', '0035', '0036', '0037', '0038', '0039',
          '0040', '0041', '0042', '0043',
          '060623_4TT00022', '060701_4TT00025', '060701_4TT00026',
          '060712_4TT00031', '060712_4TT00032', '060719_4TT00035',
          '060719_4TT00036', '060722_4TT00038', '060805_4TT00043', 
          '060805_4TT00044', '060809_4TT00046', '060819_4TT00055', 
          '060819_4TT00056', '060823_4TT00057', '060823_4TT00058', 
          '060902_4TT00063', '060902_4TT00064', '060906_4TT00065', 
          '060906_4TT00066', '060916_4TT00072', '060916_4TT00073', 
          '060919_4TT00074', '060919_4TT00075', '060920_4TT00076', 
          '061003_4TT00082', '061003_4TT00083', '061004_4TT00084', 
          '061004_4TT00085', '061014_4TT00091', '061017_4TT00092', 
          '061017_4TT00093', '061018_4TT00094', '061018_4TT00095', 
          '061028_4TT00102', '061028_4TT00103', '061107_4TT00109', 
          '061115_4TT00116'],
    '2': ['0044', '0047', '0048', '0050', '0051', '0052', '0062',
          '0064', '0068', '0073', '0076', '0077', '0084',
          '061118_4TT00118', '070307_4TT00187', '061129_4TT00123', 
          '070113_4TT00147', '070317_4TT00195', '070317_4TT00194', 
          '070103_4TT00141', '070131_4TT00163', '061107_4TT00108', 
          '061118_4TT00119', '061213_4TT00132', '070214_4TT00174', 
          '070124_4TT00158', '070303_4TT00183', '061129_4TT00122', 
          '061213_4TT00133', '061206_4TT00129', '070117_4TT00151', 
          '070328_4TT00205', '070207_4TT00169', '070124_4TT00157']
         }

for i, exp in enumerate(experiments):
    
    mask_file = os.path.join(dir_mri, exp, 'mask_group_MNI.nii.gz')

    # resample mask file to match MNI data
    cmd = ('3dresample ' +
              '-prefix tmp_mask.nii.gz ' +
              '-input ' + mask_file + ' ' +
              '-master MNI.nii.gz' + ' ' +
              '-rmode NN ' +
              '-dxyz 3 3 3')
    os.system(cmd)

    # reshapeafy
    mask = nib.load('tmp_mask.nii.gz').get_data()
    dims = mask.shape
    mask = mask.reshape(dims[0]*dims[1]*dims[2])

    # either add the new mask to the master, or create the master
    if i == 0:
        master = mask
        
        # resample ROI file to match mask file
        cmd = ('3dresample ' +
                   '-prefix tmp_ROIs.nii.gz ' +
                   '-master tmp_mask.nii.gz ' +
                   '-inset ' + str(ROI_file))
        os.system(cmd)

    else:
        master = master + mask
    os.system('rm tmp_mask.nii.gz')

# find voxels shared by all participants
idx_m = np.where(master == len(experiments))[0]

# load in the ROIs
rois = nib.load('tmp_ROIs.nii.gz')
outA = rois.get_affine()
outH = rois.get_header()
rois = rois.get_data()
outH.set_data_shape((dims[0], dims[1], dims[2], 2))
rois = rois.reshape(dims[0]*dims[1]*dims[2])
os.system('rm tmp_ROIs.nii.gz')

# load in the subjects
for grp in groups:
    for exp in experiments:
        subjects = ypp_utilities.get_subj(os.path.join(dir_mri, exp))
        for subj in (subj for subj in subjects if subj in groups[grp]):
            data_file = os.path.join(dir_mri, exp, subj, 'REST/' + str(in_file))
            data = nib.load(data_file).get_data()
            dims = data.shape
            data = data.reshape([dims[0]*dims[1]*dims[2], dims[3]])

            # loop through each roi
            for roinum, roi in enumerate(np.unique(rois[np.where(rois > 0)])):
                
                if grp == '1':
                    filename = os.path.join(dir_ana, 'group1/' + 
                                                     str(subj) + 
                                                     '_r-z_' + 
                                                     str(labels[roinum]) + 
                                                     '.nii.gz')
                elif grp == '2':
                    filename = os.path.join(dir_ana, 'group2/' + 
                                                     str(subj) + 
                                                     '_r-z_' + 
                                                     str(labels[roinum]) + 
                                                     '.nii.gz')

                if os.path.isfile(filename) == False:
                
                    # create output array
                    out = np.zeros([dims[0]*dims[1]*dims[2], 2])
                    
                    # get the mean time series
                    idx_roi = np.where(rois == roi)[0]
                    idx_mu = np.where(np.mean(data, axis=1) > 950)[0]
                    idx = np.intersect1d(np.intersect1d(idx_roi, idx_m), idx_mu)
                    
                    # skip empty ROIs
                    if len(idx) == 0:
                        pass
                    
                    # gather the mean time series
                    ts = np.mean(data[idx, :], axis=0)
                    
                    # look through each time series, calculating r + z
                    for i in np.arange(len(idx_m)):
                        out[idx_m[i], 0] = np.corrcoef(ts, 
                                                       data[idx_m[i], :], 
                                                       rowvar=0)[1,0]
                        out[idx_m[i], 1] = 0.5*np.log((1+out[idx_m[i], 0])/
                                                      (1-out[idx_m[i], 0]))

                    # reshape to 3D
                    out = out.reshape([dims[0], dims[1], dims[2], 2])

                    # write out the file to the ANALYSIS folder
                    out = nib.nifti1.Nifti1Image(out, outA, outH)
                    out.to_filename(filename)

                    print 'Wrote ' + str(filename)
