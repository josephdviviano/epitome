import os

import numpy as np
import scipy as sp
import scipy.stats as stat
import matplotlib.pyplot as plt

import nibabel as nib
import ypp_utilities

## init some useful variables
dir_ana = '/srv/MRI/ANALYSIS/REST'
dir_mri = '/srv/MRI/WORKING/'
experiments = ['RSFC1'] 

# get us to the right directory
os.system('cd ' + dir_ana)

## Rational: All data are in the MNI space. We have defined all ROIs in MNI 
#  space. For each subject, we downsample the ROIs to EPI resolution, and for 
#  each ROI, find the intersection with the grey matter mask, and collect the 
#  mean time series. We optionally low-pass this time series using a moving 
#  average. Next we generate a correlation matrix per subject, r-to-z transform,
#  and conduct a t-test between the groups at each cell of the graph. We correct
#  for multiple comparisons and star the statistically-different cells.

labels = ['Dorsal attention A', 
          'Dorsal attention B', 
          'Dorsal attention C', 
          'Dorsal attention D', 
          'Dorsal attention E', 
          'Dorsal attention F', 
          'Ventral attention A',
          'Ventral attention B',
          'Ventral attention C',
          'Ventral attention D',
          'Ventral attention E',
          'Ventral attention F',
          'Control A',
          'Control B',
          'Control C',
          'Control D',
          'Control E',
          'Control F',
          'Default A',
          'Default B',
          'Default C',
          'Default D',
          'Default E',
          'Default F',
          'ATOL mPFC']

##

group1 = ['0023','0035','0036','0024','0037','0025','0038','0028','0039',
          '0029','0040','0030','0041','0031','0042','0033','0043','0034']

group2 = ['0046','0061','0073','0084','0047','0062','0074','0048','0064',
          '0075','0050','0065','0076','0051','0066','0077','0052','0067',
          '0078','0054','0068','0079','0055','0070','0081','0058','0071',
          '0082','0044','0060','0072','0083']

group1_iter = 0
group2_iter = 0

##

graph_group1 = np.zeros((len(labels), len(labels), len(group1)))
graph_group2 = np.zeros((len(labels), len(labels), len(group2)))

# loop through the experiments one by one
for exp in experiments:
    subjects = ypp_utilities.get_subj(os.path.join(dir_mri, exp))
    for subj in subjects:

        data_file = os.path.join(dir_mri, exp, subj, 'REST/func_MNI_concat.nii.gz')
        mask_file = os.path.join(dir_mri, exp, subj, 'REST/SESS01/anat_gm.nii.gz')
        mask_bkup = os.path.join(dir_mri, exp, subj, 'REST/SESS01/anat_EPI_mask_MNI.nii.gz')
        tsfm_file = os.path.join(dir_mri, exp, subj, 'REST/SESS01/mat_EPI_to_TAL.aff12.1D')

        # resample mask file to match MNI data
        cmd = ('3dAllineate ' +
                  '-prefix tmp_gm.nii.gz ' +
                  '-input ' + mask_file + ' ' +
                  '-1Dmatrix_apply ' + tsfm_file + ' ' +
                  '-master MNI.nii.gz' + ' ' +
                  '-float ' +
                  '-interp NN ' +
                  '-final NN ' +
                  '-mast_dxyz 3 3 3')
        os.system(cmd)

        # resample ROI file to match mask file
        cmd = ('3dresample ' +
                   '-prefix tmp_ROIs.nii.gz ' +
                   '-master tmp_gm.nii.gz ' +
                   '-inset ROIs.nii.gz')
        os.system(cmd)

        # load in the data, reshapeafy!
        data = nib.load(data_file).get_data()
        mask = nib.load('tmp_gm.nii.gz').get_data()
        bkup = nib.load(mask_bkup).get_data()
        rois = nib.load('tmp_ROIs.nii.gz').get_data()

        dims = data.shape

        timeseries = np.zeros((len(labels), dims[3]))

        data = data.reshape([dims[0]*dims[1]*dims[2], dims[3]])
        mask = mask.reshape(dims[0]*dims[1]*dims[2])
        bkup = bkup.reshape(dims[0]*dims[1]*dims[2])
        rois = rois.reshape(dims[0]*dims[1]*dims[2])

        idx_mask = np.where(mask == 1)[0]
        idx_bkup = np.where(bkup == 1)[0]

        # loop through each roi
        for roi in np.unique(rois[np.where(rois > 0)]):
            idx_roi = np.where(rois == roi)[0]
            idx = np.intersect1d(idx_roi, idx_mask)
            if len(idx) == 0:
                print("!!!!!!!!!!!!!OMGGGGGGGGGGGG!!!!!!!!!!!!!!!!!!!!!!!!!")
                idx = np.intersect1d(idx_roi, idx_bkup)
                test = np.mean(data[idx, :], axis=1)
                idx_test = np.where(test > np.max(data)/100)[0]
                idx = idx[idx_test]
                if len(idx) == 0:
                    print("!!!!!!!!!!!!!GRAHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                    print("!!!!!!!!!!!!!GRAHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                    print("!!!!!!!!!!!!!GRAHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                    print("!!!!!!!!!!!!!GRAHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                    print("!!!!!!!!!!!!!GRAHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                    print("!!!!!!!!!!!!!GRAHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                    print("!!!!!!!!!!!!!GRAHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                    print("!!!!!!!!!!!!!GRAHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            ts = np.mean(data[idx, :], axis=0)
            timeseries[roi-1, :] = ts
        
        # build graph, zero diagonal
        graph = np.corrcoef(timeseries, rowvar=1)
        graph.ravel()[:graph.shape[1]**2:graph.shape[1]+1] = 0

        # r-to-z transform
        for x in range(len(labels)):
            for y in range(len(labels)):
                graph[x,y] = 0.5*np.log((1+graph[x,y])/(1-graph[x,y]))

        # store results
        if subj in group1:
            graph_group1[:, :, group1_iter] = graph
            group1_iter = group1_iter + 1

        if subj in group2:
            graph_group2[:, :, group2_iter] = graph
            group2_iter = group2_iter + 1

        os.system('rm tmp_gm.nii.gz')
        os.system('rm tmp_ROIs.nii.gz')
        #