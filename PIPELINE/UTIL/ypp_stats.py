"""
A collection of statisical routines useful for large data sets.
"""

def FDR_mask(p=[], q=0.05, iid='yes', crit='no'):

    """
    Calculates the Benjamini & Hochberg (1995) correction for multiple 
    hypothesis testing from a list of p-values, and creates a binary mask
    where p-values are significant. Also optionally reports the critical
    p-value. Requires numpy.

    See http://www.jstor.org/stable/2346101 for details.

    - `p`   : a nD list or numpy array of p values.
    - `q`   : maximum acceptibe proportion of false positives. Default = 0.05.
    - `iid' : if iid='yes', uses liberal test assuming positive dependence
              or independence between tests. if iid='no', uses conservative
              test with no assumptions. Default = 'yes'.
    - `crit`: if crit='yes', also returns the critical p-value . Default = 'no'.
    """

    import numpy as np

    # initialize numpy array with > 2 p values
    if isinstance(p, np.ndarray) == False:
        p = np.array(p)

    if p.size < 2:
        print('p-value vector must have multiple values!')
        raise SystemExit

    q = float(q)

    # if p is > 1D, reshape to 1D
    if len(p.shape) > 1:
        dim = np.shape(p)
        shape = 1
        for d in dim:
            shape = shape * d
        p = p.reshape(shape)

    size = float(len(p)) # number of comparisons
    idx = np.argsort(p) # sort p values for test
    dat = p[idx]
    del(idx)
    
    # find threshold
    vec = np.arange(size) + float(1)
    if iid == 'yes':
        threshold = vec / size * q
    if iid == 'no':
        threshold = vec / size * q / np.sum([1 / vec])
    del(vec)

    # find largest p value below threhold
    H0_rej = dat <= threshold
    try:
        crit_p = np.max(dat[H0_rej])
    except:
        print('Nothing is significant')
        crit_p = 0
    del(dat, threshold)

    # create & reshape binary output mask
    mask = np.zeros(size) 
    if crit_p > 0:
        mask[p <= crit_p] = 1

    if 'dim' in locals():
        shape = []
        for d in dim:
            shape.append(d)
        mask.reshape(shape)

    if crit == 'yes':
        return (mask, crit_p)
    else: 
        return mask

def FDR_threshold(p=[], q=0.05, iid='yes'):

    """
    Calculates the Benjamini & Hochberg (1995) correction for multiple 
    hypothesis testing from a list of p-values, and returns the threshold only.
    NaNs are ignored for the calculation.

    See http://www.jstor.org/stable/2346101 for details.

    - `p`   : a nD list or numpy array of p values.
    - `q`   : maximum acceptibe proportion of false positives. Default = 0.05.
    - `iid' : if iid='yes', uses liberal test assuming positive dependence
              or independence between tests. if iid='no', uses conservative
              test with no assumptions. Default = 'yes'.
    """

    import numpy as np

    # initialize numpy array with > 2 p values
    if isinstance(p, np.ndarray) == False:
        p = np.array(p)

    if p.size < 2:
        print('p-value vector must have multiple values!')
        raise SystemExit

    q = float(q)

    # if p is > 1D, reshape to 1D
    if len(p.shape) > 1:
        dim = p.shape
        shape = 1
        for d in dim:
            shape = shape * d
        p = p.reshape(shape)

    # remove NaNs
    p = p[np.where(np.isnan(p) == False)[0]]

    # sort the p-vector
    size = float(len(p)) # number of comparisons
    idx = np.argsort(p) # sort p values for test
    dat = p[idx]
    del(idx)
    
    # find threshold
    vec = np.arange(size) + float(1)
    if iid == 'yes':
        threshold = vec / size * q
    if iid == 'no':
        threshold = vec / size * q / np.sum([1 / vec])
    del(vec)

    # find largest p value below threhold
    H0_rej = dat <= threshold
    try:
        crit_p = np.max(dat[H0_rej])
        print('p-threshold = ' + str(crit_p))
    except:
        crit_p = 0
        print('the only thing significant here is how much you stink!')
    del(dat, threshold)

    return crit_p