#!/usr/bin/env python
"""
This looks for most correlated seeds within brain networks

Usage:
  find_maxcorr_in_mask.py [options] <timeseries.nii.gz> <roi_tsmask.nii.gz> <roi_search.nii.gz>

Arguments:
    <timeseries.nii.gz>        Paths to directory containing .mnc images to align and mean
    <roi_tsmask.nii.gz>        Path to template for the ROIs of network regions
    <roi_search.nii.gz>        Name (with full path to the csv of the found nodes)

Options:
  --presmooth FMHM         Run AFNI volume smoothing on the timeseries file before computing correlations
  --brainmask NIFTI        Brainmask to apply to all masks before running, also required for smoothing
  -v,--verbose             Verbose logging
  --debug                  Debug logging in Erin's very verbose style
  -n,--dry-run             Dry run
  -h,--help                Print help

DETAILS
Requires python enviroment with numpy and nibabel:
module load use.own datman/edickie

Requires HCP pipeline environment
module load FSL/5.0.7 freesurfer/5.3.0 connectome-workbench/1.1.1 hcp-pipelines/3.7.0

ROI template example:
ROItemplate='/projects/edickie/code/templates/fsaverage.Yeo2011_7Networksfrom17.32k_fs_LR.ROI.dscalar.nii'
fROItemplate='/projects/edickie/code/templates/fsaverage.Yeo2011_7Networksfrom17.32k_fs_LR.ROI_dscalarfake.nii'

inputfile example:
inputfile= '/projects/edickie/analysis/restcifti/SN110/MNINonLinear/Results/RSN/RSN_Atlas.dtseries.nii'
Work in progress
"""
from docopt import docopt
import numpy as np
import nibabel as nib
import os
import subprocess
import pandas as pd

arguments       = docopt(__doc__)
ts_nii          = arguments['<timeseries.nii.gz>']
souce_roi_nii   = arguments['<roi_tsmask.nii.gz>']
target_roi_nii  = arguments['<roi_search.nii.gz>']
brainmask_nii   = arguments['--brainmask']
presmoothFWHM   = arguments['--presmooth']
VERBOSE         = arguments['--verbose']
DEBUG           = arguments['--debug']
DRYRUN          = arguments['--dry-run']

###
### Erin's little function for running things in the shell
def docmd(cmdlist):
    "sends a command (inputed as a list) to the shell"
    if DEBUG: print ' '.join(cmdlist)
    if not DRYRUN: subprocess.call(cmdlist)

                # 3dBlurInMask \
                #     -prefix ${SESS}/func_volsmooth.${ID}.${NUM}.nii.gz \
                #     -Mmask ${SESS}/anat_tmp_smoothmask.nii.gz \
                #     -FWHM ${FWHM} \
                #     -quiet -float \
                #     -input ${SESS}/${INPUT}.${ID}.${NUM}.nii.gz
if presmoothFWHM==None:
    smoothts_niifile = ts_nii
else:
    if brainmask==None:
        sys.exit("Need to specify a brainmask to do smoothing")
    smoothts_niifile = os.path.join(tmpdir,'ts_sm.nii.gz')
    docmd('3dBlurInMask',
        '-prefix', smoothts_niifile,
        '-Mmask', brainmask,
        '-FWHM', presmoothFWHM,
        'quiet','float',
        '-input', ts_nii)


## read in the dconn file
smoothts_meta = nib.load(smoothts_niifile)
smoothts_data = smoothts_meta.get_data()
dims = smoothts_data.shape
#fc_df = pd.DataFrame(sub_corrmat[0,0,0,0,:,:])

## also read in template
source_roi_meta = nib.load(source_roi_nii)
source_roi_data = source_roi_meta.get_data()

## also read in template
target_roi_meta = nib.load(target_roi_nii)
target_roi_data = target_roi_meta.get_data()

## load the brainmask if given
if brainmask!=None:
    ## load brainmask if it exists
    brainmask_meta = nib.load(brainmask)
    brainmask_data = brainmask_meta.get_data()

    ## masks all three other inputs with the brainmask
    smoothts_data = np.multiply(smoothts_data, brainmask_data)
    source_roi_data = np.multiply(source_roi_data, brainmask_data)
    target_roi_data = np.multiply(target_roi_data, brainmask_data)

## calculate weighted meants for source
# get the seed time series

smoothts_rdata = smoothts_data.reshape((dims[0]*dims[1]*dims[2], dims[3]))
smoothts_rdata = smoothts_data.reshape((dims[0]*dims[1]*dims[2], dims[3]))
src_ts = np.mean(data[idx, :], axis=0)

roi_df = pd.DataFrame(ROInet[0,0,0,0,:,:],index=range(1,ROInet.shape[4]+1))


cols = ['Network','ROI','cifti-index']
result = pd.DataFrame(columns = cols)
thisrow = 1
for network in roi_df.index.values.tolist():
    ### subset matrix to contain rows of only this Network
    network_idx = roi_df.loc[network,roi_df.loc[network,:]>0].index
    ### get a list of ROIs to within the network
    roi_list = roi_df.loc[network,network_idx].unique()
    for roi in roi_list:
        '''
        for each roi find its best vertex and add to table
        '''
        ### get the subarray that contains the ROI
        roi_idx = roi_df.loc[network,roi_df.loc[network,:]==roi].index
        ### calculate the maximal correlation at every vertex with this ROI
        max_indexes = []
        for other_roi in roi_list[roi_list != roi]:
            ## for combination of ROI and other_roi get the indices of the other roi that is most correlated with it
            oroi_idx = roi_df.loc[network,roi_df.loc[network,:]==other_roi].index
            roi_oroi_mat = fc_df.loc[roi_idx,oroi_idx]
            row_maxes = roi_oroi_mat.max(1)
            max_idx = int(row_maxes.loc[row_maxes==row_maxes.max()].index[0])
            max_indexes.append(max_idx)
        ### top picks are those ROIs are those vertices from each other ROI in the network with the highest correlation with it
        toppicks = fc_df.loc[roi_idx,max_indexes]
        ### caculate the median correlation from these top picks
        toppicks_median = toppicks.median(1)
        ### take the highest
        toppick = toppicks_median[toppicks_median==toppicks_median.max()].index[0]
        ### add a row to the result dataframe and fill in the cols
        result = result.append(pd.DataFrame(columns = cols, index = [thisrow]))
        result.Network[thisrow] = network
        result.ROI[thisrow] = int(roi)
        result['cifti-index'][thisrow] = toppick
        thisrow = thisrow + 1


## write the checklist out to a file
result.to_csv(resultsfile, sep=',', columns = cols, index = False)
