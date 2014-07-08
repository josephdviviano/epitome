#!/usr/bin/env python
"""
Takes input NIFTI 4D data, and applies the specified low-pass filter to each
voxel. To save on computation time, this requires a mask input. All values > 0
in the mask survive.

Usage: <filter_type> <func_name> <mask_name> <cutoff> <path> <run_number>

    filter: one of 'median', 'average', 'kaiser', 'butterworth'.
    func_name: full path of input functional data.
    mask_name: full path of input mask data. 
    cutoff: for median & average, this should be an odd integer number 
            defining the width of the time-domain filter.
            for kaiser & average, this should be a float representing the 
            lowpass cutoff in Hz.
    path: full path of the output directory.
    run_number: a string denoting the zero-padded run number.
"""

import numpy as np
import scipy as sp
import scipy.signal as sig
import nibabel as nib

def loadnii(filename):
    """
    Usage:
        nifti, affine, header, dims = loadnii(filename)

    Loads a Nifti file (3 or 4 dimensions).
    
    Returns: 
        a 2D matrix of voxels x timepoints, 
        the input file affine transform, 
        the input file header, 
        and input file dimensions.
    """

    # load everything in
    nifti = nib.load(filename)
    affine = nifti.get_affine()
    header = nifti.get_header()
    dims = nifti.shape

    # if smaller than 3D
    if len(dims) < 3:
        raise Exception("""
                        Your data has less than 3 dimensions!
                        """)

    # if smaller than 4D
    if len(dims) > 4:
        raise Exception("""
                        Your data is at least a penteract (over 4 dimensions!)
                        """)
    
    # load in nifti and reshape to 2D
    nifti = nifti.get_data()
    if len(dims) == 3:
        dims = tuple(list(dims) + [1])
    nifti = nifti.reshape(dims[0]*dims[1]*dims[2], dims[3])

    return nifti, affine, header, dims

def maskdata(data, mask, rule='>', threshold=[0]):
    """
    Usage:
        data, idx = maskdata(data, mask, rule, threshold)

    Extracts voxels of interest from a 2D data matrix, using a threshold rule
    applied to the mask file, which is assumed to only contain one value per 
    voxel.

    Valid thresholds:
        '<' = keep voxels less than threshold value.
        '>' = keep voxels greater than threshold value.
        '=' = keep voxels equal to threshold value.

    The threshold(s) should be a list of value(s).

    By default, this program finds all voxels that are greater than zero in the
    mask, which is handy for removing non-brain voxels (for example).

    Finally, this program *always* removes voxels with constant-zero values
    regardless of your mask, because they are both annoying and useless.
    If it finds voxels like this, it will tell you about them so you can
    investigate.

    Returns: 
        voxels of interest in data as a collapsed 2D array 
        and a set of indices relative to the size of the original array.
    """

    # ensure the input data and mask are appropriately formatted
    if np.shape(data)[0] != np.shape(mask)[0]:
        print('data = ' + str(data) + ', mask = ' + str(mask))
        raise Exception("""
                        Your data and mask are not in from the same space!
                        """)

    if np.shape(mask)[1] > 1:
        print('mask contains ' + str(np.shape(mask)[1]) + 'values per voxel,')
        raise Exception("""
                        Your mask can't contain multiple values per voxel!
                        """)

    # make sure the rule chosen is kosher
    if any(rule == item for item in ['=', '>', '<']) == False:
        print('threshold rule is ' + str(rule))
        raise Exception("""
                        Your threshold rule must be '=', '>', or '<'!
                        """)

    # make sure the threshold are numeric and non-numpy
    if type(threshold) != list:
        print('threshold datatype is ' + str(type(threshold)))
        raise Exception("""
                        Your threshold(s) must be in a list.
                        """)

    # compute the index
    idx = np.array([])
    threshold = list(threshold)
    for t in threshold:
        # add any new voxels corresponding to a given threshold
        if rule == '=':
            idx = np.unique(np.append(idx, np.where(mask == t)[0]))
        elif rule == '>':
            idx = np.unique(np.append(idx, np.where(mask > t)[0]))
        elif rule == '<':
            idx = np.unique(np.append(idx, np.where(mask < t)[0]))

    # find voxels with constant zeros, remove those from the index
    idx_zeros = np.where(np.sum(data, axis=1) == 0)[0]
    idx = np.setdiff1d(idx, idx_zeros)

    # collapse data using the index
    idx = idx.tolist()
    data = data[idx, :]

    return data, idx

def moving_average(data, N=5):
    # pad the to-be-smoothed vector by the window length on each side
    vector = np.zeros(data.shape[0]+(N*2),)
    vector[N:-N] = data

    # insert the 1st and last value, respectively
    vector[0:N] = data[0]
    vector[-1-N:] = data[-1]

    # convolve the time series with a vector of 1/N
    output = np.convolve(vector, np.ones((N,), ) / N, mode='full')[(N-1):]
    output = output[N:-N]

    return output

def median_filter(func, mask, kernel_size=5):
    """
    Low-passes each time series using a n-d median filter. Useful in cases
    where one cannot assume Gaussian noise and/or would like to preserve 
    edges within the data.

    The default kernel size is extremely conservative, but does a nice job.
    """
    # load in everything
    func, func_aff, func_head, func_dims  = loadnii(func)
    anat, anat_aff, anat_head, anat_dims  = loadnii(anat)
    tmp, idx = maskdata(func, anat)

    # init output array
    filt = np.zeros(tmp.shape)

    # filter data
    for x in np.arange(tmp.shape[0]):
        filt[x, :] = sig.medfilt(tmp[x, :], kernel_size=kernel_size)

    # create a 4D output array
    output = np.zeros(func.shape)
    output[idx, :] = filt
    output = output.reshape(func_dims)
    output_aff = func_aff
    output_head = func_head

    return output, output_aff, output_head

def mean_filer(func, mask, kernel_size=5):
    """
    Low-passes each time series using a 1d moving average filter. Useful in
    cases where one wants to suppress Gaussian noise.

    The default kernel size is extremely conservative, but does a nice job.
    """
    # load in everything
    func, func_aff, func_head, func_dims  = loadnii(func)
    anat, anat_aff, anat_head, anat_dims  = loadnii(anat)
    tmp, idx = maskdata(func, anat)

    # init output array
    filt = np.zeros(tmp.shape)

    # filter data
    for x in np.arange(tmp.shape[0]):
        filt[x, :] = moving_average(tmp[x, :], N=kernel_size)

    # create a 4D output array
    output = np.zeros(func.shape)
    output[idx, :] = filt
    output = output.reshape(func_dims)
    output_aff = func_aff
    output_head = func_head

    return output, output_aff, output_head

def kaiser_filter(func, anat, cutoff=0.1):
    """
    Low-passes each time series using a bi-directional FIR kaiser filter.
    Useful in cases where the preservation of phase information is more
    important than strong attenuation of high frequencies.

    The default cutoff is the traditional resting-state cutoff.
    """
    # load in everything
    func, func_aff, func_head, func_dims  = loadnii(func)
    anat, anat_aff, anat_head, anat_dims  = loadnii(anat)
    tmp, idx = maskdata(func, anat)

    # init output array
    filt = np.zeros(tmp.shape)

    # get sampling rate, nyquist frequency
    TR_len = func_head.values()[15][4]
    if TR_len > 1000:
        TR_len = TR_len / 1000.0
    samp_rate = 1.0/TR_len
    nyq = samp_rate/2.0

    # return a kaiser window with 60 Hz attenuation over a 0.1 Hz transition
    width = 0.1
    ripple_db = 60.0
    numtap, beta = sig.kaiserord(ripple_db, width)
    
    # enforce odd filter order
    if np.remainder(numtap, 2.0) == 0:
        numtap = numtap -1

    # design and apply lowpass filter
    b = sig.firwin(numtap, cutoff/nyq, window=('kaiser', beta))
    a = [1.0]

    for x in np.arange(tmp.shape[0]):
        filt[x, :] = sig.filtfilt(b, a, tmp[x, :], axis=0)

    # create a 4D output array
    output = np.zeros(func.shape)
    output[idx, :] = filt
    output = output.reshape(func_dims)
    output_aff = func_aff
    output_head = func_head

    return output, output_aff, output_head

def butterworth_filter(func, anat, cutoff=0.1):
    """
    Low-passes each time series using a low order, bi-directional FIR
    butterworth filter. Useful in cases where you are particularly worried
    about the impact of discontinuities in your data on the behavior of your
    filter.

    The default cutoff is the traditional resting-state cutoff.
    """
    # load in everything
    func, func_aff, func_head, func_dims  = loadnii(func)
    anat, anat_aff, anat_head, anat_dims  = loadnii(anat)
    tmp, idx = maskdata(func, anat)

    # init output array
    filt = np.zeros(tmp.shape)

    # get sampling rate, nyquist frequency
    TR_len = func_head.values()[15][4]
    if TR_len > 1000:
        TR_len = TR_len / 1000.0
    samp_rate = 1.0/TR_len
    nyq = samp_rate/2.0

    # design and apply lowpass filter
    b, a = sig.butter(3, cutoff/nyq)
    a = [1.0]

    for x in np.arange(tmp.shape[0]):
        filt[x, :] = sig.filtfilt(b, a, tmp[x, :], axis=0)

    # create a 4D output array
    output = np.zeros(func.shape)
    output[idx, :] = filt
    output = output.reshape(func_dims)
    output_aff = func_aff
    output_head = func_head

    return output, output_aff, output_head

def write_output(path, num, out, aff, head):
    """
    Writes a NIFTI file to the specified path with the specified run number.
    """
    out = nib.nifti1.Nifti1Image(out, aff, head)
    out.to_filename(os.path.join(path, 'func_lowpass.' + str(num) + '.nii.gz'))

if __name__ == "__main__":
    
    # type checking
    sys.argv[1] = str(sys.argv[1])
    sys.argv[2] = str(sys.argv[2])
    sys.argv[3] = str(sys.argv[3])
    sys.argv[4] = float(sys.argv[4])
    sys.argv[5] = str(sys.argv[5])
    sys.argv[6] = str(sys.argv[6])

    if sys.argv[1] == 'median':
        o, a, h = median_filter(sys.argv[2], sys.argv[3], sys.argv[4])
        write_output(sys.argv[5], sys.argv[6], o, a, h)
    
    elif sys.argv[1] == 'average':
        o, a, h = mean_filter(sys.argv[2], sys.argv[3], sys.argv[4])
        write_output(sys.argv[5], sys.argv[6], o, a, h)
    
    elif sys.argv[1] == 'kaiser':
        o, a, h = kaiser_filter(sys.argv[2], sys.argv[3], sys.argv[4])
        write_output(sys.argv[5], sys.argv[6], o, a, h)
    
    elif sys.argv[1] == 'butterworth':
        o, a, h = butterworth_filter(sys.argv[2], sys.argv[3], sys.argv[4])
        write_output(sys.argv[5], sys.argv[6], o, a, h)
    
    else:
        print('*** INVALID FILTER SELECTION! ***')