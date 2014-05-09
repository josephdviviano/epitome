#!/usr/bin/env python

import os
import sys
import csv
import fnmatch

import numpy as np
import scipy as sp
import nibabel as nib
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

import ypp_utilities


def TR_drop(path, expt, mode, func_name, mask_name, head_size=50, thresh_FD=0.3, thresh_DV=0.3):
    """
    func__pre = functional data prefix (e.g., 'func_filtered')
    mask_name = mask file name (e.g., 'anat_EPI_mask')
    head_size = head radius in mm (default 50 mm)
    thresh_FD = censor TRs with instantaneous motion > x mm (default 0.3 mm)
    thresh_DV = censor TRs with instantaneous GS fluctuation > x % (def. 0.3 %)

    Defaults taken from Gwig et al. 2013 Cerebral Ctx and are subject to change.
    """
    
    # convert variable types
    head_size = float(head_size)
    thresh_FD = float(thresh_FD)
    thresh_DV = float(thresh_DV)

    # give feedback
    print("")
    print(" ********************** TR Scrubbing Module ********************* ")
    print(" Running experiment " + str(expt) + ", datatype " + str(mode) + ".")
    print(" Framewise displacement threshold     = " + str(thresh_FD) + " mm,")
    print("      DVARS threshold                 = " + str(thresh_DV) + " %,")
    print("      head radius                     = " + str(head_size) + " mm.")
    print(" **************************************************************** ")
    print("")

    # open up a csv
    f = open( path + "/" + expt + "/" + "qc_retained_TRs.csv", "wb")
    f.write('subject \t number of retained TRs \n')

    # get subject numbers
    subjects = ypp_utilities.get_subj(os.path.join(path, expt))

    for subj in subjects:

        directory = os.path.join(path, expt, subj, mode)
        TRs_retained = 0 # keep track of the number of retained TRs

        for sess in os.listdir(directory):
            if os.path.isdir(os.path.join(directory, sess)) == True:
                for fname in os.listdir(os.path.join(directory, sess)):
                    if fnmatch.fnmatch(fname, str(func_name) + '*'):
                        
                        count = fname[-9:-7] #extract the run number

                        # load in masked data
                        data = nib.load(os.path.join(directory, sess, fname))
                        outA = data.get_affine()
                        outH = data.get_header()
                        dims = np.array(data.shape)
                        data = data.get_data()

                        mask = nib.load(os.path.join(directory,
                                                     sess,
                                                     str(mask_name) + '.nii.gz')).get_data()

                        data = np.reshape(data, (dims[0] * dims[1] * dims[2], dims[3]))
                        mask = np.reshape(mask, (dims[0] * dims[1] * dims[2]))
                        data = data[mask > 0, :]

                        for fname in os.listdir(os.path.join(directory, sess, 'PARAMS')):
                            if fnmatch.fnmatch(fname, 'motion.' + str(count) + '*'):
                                FD = np.genfromtxt(os.path.join(directory, sess, 'PARAMS', fname))

                                FD[:,0] = np.radians(FD[:,0])*head_size # roll
                                FD[:,1] = np.radians(FD[:,1])*head_size # pitch
                                FD[:,2] = np.radians(FD[:,2])*head_size # yaw

                                # sum over absolute derivative for the 6 motion paramaters
                                FD = np.sum(np.abs(np.diff(FD, n=1, axis=0)), axis=1)
                                FD = np.insert(FD, 0, 0) # align FD & DVARS

                            if fnmatch.fnmatch(fname, 'DVARS.' + str(count) + '*'):
                                DV = np.genfromtxt(os.path.join(directory, sess, 'PARAMS', fname))
                                DV = (DV) / 1000 # convert to % signal change
                        
                        # mask TRs 2 back and 2 forward from threshold
                        idx_FD = np.where(FD >= thresh_FD)[0]
                        idx_DV = np.where(DV >= thresh_DV)[0] 
                        idx = np.union1d(idx_FD, idx_DV)
                        idx = np.union1d(
                              np.union1d(
                              np.union1d(
                              np.union1d(idx-2, idx-1), idx), idx+1), idx+2)

                        # remove censor idx < 0 and > length of run
                        idx = idx[idx > 0]
                        idx = idx[idx < dims[3]]
                        
                        # find all the kosher TRs
                        idx_retained = np.setdiff1d(np.arange(dims[3]), idx)

                        # 'scrub' the data
                        data = data[:, idx_retained]

                        # keep track of the number of retained TRs
                        dims[3] = len(idx_retained)
                        TRs_retained = TRs_retained + dims[3]

                        # reshape and write 4D output
                        outH.set_data_shape((dims[0], dims[1], dims[2], dims[3]))
                        outF = np.zeros((dims[0]*dims[1]*dims[2], dims[3]))
                        outF[mask > 0, :] = data 
                        outF = np.reshape(outF, (dims[0], dims[1], dims[2], dims[3]))
                        outF = nib.nifti1.Nifti1Image(outF, outA, outH)
                        outF.to_filename(os.path.join(directory, sess, 
                                                    'func_scrubbed.' + str(count) + '.nii.gz'))

                        # update us and continue the loop
                        print('subject ' + subj + ' run ' + str(count) + ' complete')

        # write out files and number of retained TRs
        f.write(str(subj) + '\t' + str(TRs_retained) + '\n')

    f.close() # write out the report

if __name__ == "__main__":
    TR_drop(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], 
            sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8])

