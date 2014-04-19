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
dir_ana = '/srv/MRI/ANALYSIS/REST/CONSERV_THRESH/NO_GSREG/DATA'
in_file = 'func_MNI_concat_scrubbed.nii.gz'
ROI_file = '/srv/MRI/ANALYSIS/REST/ROIs_ATOL.nii.gz'

# get us to the right directory
os.system('cd ' + dir_ana)

# labels = ['Dorsal attention A', 
#           'Dorsal attention B', 
#           'Dorsal attention C', 
#           'Dorsal attention D', 
#           'Dorsal attention E', 
#           'Dorsal attention F', 
#           'Default A',
#           'Default B',
#           'Default C',
#           'Default D',
#           'Default E',
#           'Default F']

labels = ['Dorsal attention A', 
          'Dorsal attention B', 
          'Dorsal attention C', 
          'Dorsal attention D', 
          'Dorsal attention E', 
          'Dorsal attention F', 
          'Default A',
          'Default B',
          'Default C',
          'ATOL MPFC',
          'Default E',
          'ATOL PCC']

##

# THIS IS FOR THE 'HARD THREHOLD' ANALYSIS (reject > 1.5 mm FD at any point)
group1 = ['0023', '0025', '0028', '0029', '0030', '0031', 
          '0033', '0034', '0035', '0036', '0037', '0038', 
          '0039', '0040', '0041', '0042', '0043', 
          '060623_4TT00022', '060701_4TT00026', '060712_4TT00031', 
          '060719_4TT00036', '060805_4TT00043', '060805_4TT00044', 
          '060819_4TT00055', '060819_4TT00056', '060902_4TT00063', 
          '060902_4TT00064', '060906_4TT00065', '060906_4TT00066', 
          '060916_4TT00072', '060916_4TT00073', '060919_4TT00074', 
          '060919_4TT00075', '060920_4TT00076', '061003_4TT00082', 
          '061003_4TT00083', '061004_4TT00084', '061004_4TT00085', 
          '061014_4TT00091', '061017_4TT00092', '061017_4TT00093',
          '061018_4TT00094', '061018_4TT00095', '061028_4TT00102', 
          '061028_4TT00103', '061107_4TT00109']

group2 = ['0044', '0046', '0047', '0048', '0050', '0051', 
          '0052', '0055', '0058', '0061', '0062', '0065', 
          '0066', '0067', '0068', '0070', '0071', '0072', 
          '0073', '0074', '0075', '0077', '0078', '0079', 
          '0083', '0084', 
          '061107_4TT00108', '061115_4TT00116', '061115_4TT00117', 
          '061118_4TT00118', '061118_4TT00119', '061125_4TT00121', 
          '061129_4TT00122', '061129_4TT00123', '061206_4TT00129', 
          '061213_4TT00132', '061213_4TT00133', '061220_4TT00136', 
          '061220_4TT00137', '070103_4TT00140', '070103_4TT00141', 
          '070106_4TT00143', '070110_4TT00146', '070113_4TT00147', 
          '070113_4TT00148', '070117_4TT00151', '070117_4TT00152', 
          '070124_4TT00157', '070124_4TT00158', '070131_4TT00163', 
          '070203_4TT00165', '070207_4TT00169', '070214_4TT00174', 
          '070221_4TT00178', '070303_4TT00183', '070303_4TT00184', 
          '070307_4TT00187', '070317_4TT00194', '070317_4TT00195', 
          '070328_4TT00205', '070328_4TT00206', '070331_4TT00208']

## THIS IS FOR HARD_THRESHOLD_ALT (SCRUB AT 1.5mm)

# group1 = ['0023', '0025', '0028', '0029', '0030', '0031', 
#           '0033', '0034', '0035', '0036', '0037', '0038', 
#           '0039', '0040', '0041', '0042', '0043', 
#           '060623_4TT00022', '060701_4TT00025', '060701_4TT00026', 
#           '060712_4TT00031', '060712_4TT00032', '060719_4TT00035', 
#           '060719_4TT00036', '060722_4TT00038', '060805_4TT00043', 
#           '060805_4TT00044', '060809_4TT00046', '060819_4TT00055', 
#           '060819_4TT00056', '060823_4TT00057', '060823_4TT00058', 
#           '060902_4TT00063', '060902_4TT00064', '060906_4TT00065', 
#           '060906_4TT00066', '060916_4TT00072', '060916_4TT00073', 
#           '060919_4TT00074', '060919_4TT00075', '060920_4TT00076', 
#           '061003_4TT00082', '061003_4TT00083', '061004_4TT00084', 
#           '061004_4TT00085', '061014_4TT00091', '061017_4TT00092', 
#           '061017_4TT00093', '061018_4TT00094', '061018_4TT00095', 
#           '061028_4TT00102', '061028_4TT00103', '061107_4TT00109', 
#           '061115_4TT00116']

# group2 = ['0044', '0046', '0047', '0048', '0050', '0051', 
#          '0052', '0054', '0055', '0058', '0060', '0061', 
#          '0062', '0064', '0065', '0066', '0067', '0068', 
#          '0070', '0071', '0072', '0073', '0074', '0075', 
#          '0076', '0077', '0078', '0079', '0081', '0082', 
#          '0083', '0084', 
#          '061107_4TT00108', '061115_4TT00117', '061118_4TT00118', 
#          '061118_4TT00119', '061125_4TT00121', '061129_4TT00122', 
#          '061129_4TT00123', '061206_4TT00129', '061213_4TT00132', 
#          '061213_4TT00133', '061220_4TT00136', '061220_4TT00137', 
#          '070103_4TT00140', '070103_4TT00141', '070106_4TT00142', 
#          '070106_4TT00143', '070110_4TT00145', '070110_4TT00146', 
#          '070113_4TT00147', '070113_4TT00148', '070117_4TT00151', 
#          '070117_4TT00152', '070124_4TT00157', '070124_4TT00158', 
#          '070131_4TT00163', '070131_4TT00164', '070203_4TT00165', 
#          '070207_4TT00169', '070214_4TT00174', '070221_4TT00177', 
#          '070221_4TT00178', '070303_4TT00183', '070303_4TT00184', 
#          '070307_4TT00186', '070307_4TT00187', '070314_4TT00193', 
#          '070317_4TT00194', '070317_4TT00195', '070328_4TT00205', 
#          '070328_4TT00206', '070331_4TT00208']

# THIS WAS FOR THE STRICT ANALYSIS (FD=0.3, DVARS=3)
# group1 = ['0023', '0024', '0025', '0028', '0030', '0031', 
#           '0033', '0034', '0035', '0036', '0037', '0038', '0039',
#           '0040', '0041', '0042', '0043',
#           '060623_4TT00022', '060701_4TT00025', '060701_4TT00026',
#           '060712_4TT00031', '060712_4TT00032', '060719_4TT00035',
#           '060719_4TT00036', '060722_4TT00038', '060805_4TT00043', 
#           '060805_4TT00044', '060809_4TT00046', '060819_4TT00055', 
#           '060819_4TT00056', '060823_4TT00057', '060823_4TT00058', 
#           '060902_4TT00063', '060902_4TT00064', '060906_4TT00065', 
#           '060906_4TT00066', '060916_4TT00072', '060916_4TT00073', 
#           '060919_4TT00074', '060919_4TT00075', '060920_4TT00076', 
#           '061003_4TT00082', '061003_4TT00083', '061004_4TT00084', 
#           '061004_4TT00085', '061014_4TT00091', '061017_4TT00092', 
#           '061017_4TT00093', '061018_4TT00094', '061018_4TT00095', 
#           '061028_4TT00102', '061028_4TT00103', '061107_4TT00109', 
#           '061115_4TT00116']

# group2 = ['0044', '0047', '0048', '0050', '0051', '0052', '0062',
#           '0064', '0068', '0073', '0076', '0077', '0084',
#           '061118_4TT00118', '070307_4TT00187', '061129_4TT00123', 
#           '070113_4TT00147', '070317_4TT00195', '070317_4TT00194', 
#           '070103_4TT00141', '070131_4TT00163', '061107_4TT00108', 
#           '061118_4TT00119', '061213_4TT00132', '070214_4TT00174', 
#           '070124_4TT00158', '070303_4TT00183', '061129_4TT00122', 
#           '061213_4TT00133', '061206_4TT00129', '070117_4TT00151', 
#           '070328_4TT00205', '070207_4TT00169', '070124_4TT00157']

gr_iter = 0

gr = copy.copy(group1)
gr2 = copy.copy(group2)
gr.extend(gr2)

##

graph_z_gr = np.zeros((len(labels), len(labels), len(gr)))
subject_list = []

# loop through the subjects
for subj in gr:

    subject_list.append(subj)

    data_file = os.path.join(dir_ana, subj, str(in_file))
    mask_file = os.path.join(dir_ana, subj, 'anat_gm.nii.gz')
    mask_bkup = os.path.join(dir_ana, subj, 'anat_EPI_mask_MNI.nii.gz')
    tsfm_file = os.path.join(dir_ana, subj, 'mat_EPI_to_TAL.aff12.1D')

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
               '-inset ' + str(ROI_file))
    os.system(cmd)

    # load in the data, reshapeafy!
    data = nib.load(data_file).get_data()
    mask = nib.load('tmp_gm.nii.gz').get_data()
    bkup = nib.load(mask_bkup).get_data()
    rois = nib.load('tmp_ROIs.nii.gz').get_data()

    dims = data.shape

    timeseries = np.zeros((len(labels), dims[3]))
    ROI_count = np.zeros((len(labels), 1))

    data = data.reshape([dims[0]*dims[1]*dims[2], dims[3]])
    mask = mask.reshape(dims[0]*dims[1]*dims[2])
    bkup = bkup.reshape(dims[0]*dims[1]*dims[2])
    rois = rois.reshape(dims[0]*dims[1]*dims[2])

    idx_mask = np.where(mask == 1)[0]
    idx_bkup = np.where(bkup == 1)[0]

    # loop through each roi
    for roi in np.unique(rois[np.where(rois > 0)]):
        idx_roi = np.where(rois == roi)[0]
        idx_mean = np.where(np.mean(data, axis=1) > 950)[0]
        idx = np.intersect1d(np.intersect1d(idx_roi, idx_mask), idx_mean)
        if len(idx) == 0:
            timeseries[roi-1, :] = np.repeat(np.nan, dims[3])
            pass
        ts = np.mean(data[idx, :], axis=0)

        #low pass the data
        # ts = sp.signal.medfilt(ts, kernel_size=3)

        timeseries[roi-1, :] = ts

    # keep track of successful seeds
    for ind, test in enumerate(timeseries[:, 0]): 
        if np.isnan(test) == False:
            ROI_count[ind] = ROI_count[ind] + 1
    
    # build graph, zero diagonal
    graph_r = np.corrcoef(timeseries, rowvar=1)
    graph_r.ravel()[:graph_r.shape[1]**2:graph_r.shape[1]+1] = 0

    # r-to-z transform graph
    graph_z = np.zeros((len(labels), len(labels)))
    for x in range(len(labels)):
        for y in range(len(labels)):
            graph_z[x,y] = 0.5*np.log((1+graph_r[x,y])/(1-graph_r[x,y]))

    # keep track of successful correlations
    graph_count = np.zeros((len(labels), len(labels)))
    for x in range(len(labels)):
        for y in range(len(labels)):
            if x != y:
                graph_count[x, y] = np.min([ROI_count[x], ROI_count[y]])

    graph_z_gr[:, :, gr_iter] = graph_z
    gr_iter = gr_iter + 1

    os.system('rm tmp_gm.nii.gz')
    os.system('rm tmp_ROIs.nii.gz')
    #


column_names = ['subject']
# come up with column names
for x in range(len(labels)):
    for y in range(len(labels)):
        if x < y:
            column_names.append(str(labels[x] + '*' + labels[y]))

# open a CSV file
with open('subject_zscores.txt', 'wb') as csvfile:
    out = csv.writer(csvfile, delimiter='\t')
    
    # write header
    out.writerow(column_names)

    counter = 0
    # write each row (1 per subject)
    for subj in np.arange(len(gr)):
        rowdata = [str(gr[subj])]
        for x in range(len(labels)):
            for y in range(len(labels)):
                if x < y:
                    rowdata.append(str(graph_z_gr[x, y, subj]))
        out.writerow(rowdata)

csvfile.close()

