#!/usr/bin/env python

import epitome as epi

def linreg_EPI2T1_FSL(input_name):
    output = 'T1'

    # give us some feedback
    print('\nResampling input EPI data to T1 space using AFNI.')

    try:
        # get the reslice dimensions
        print('\nSelect target dimensions (isotropic mm):')
        dims = epi.utilities.selector_float()

    # if we messed any of these up, we return None
    except ValueError as ve:
        return '', None

    # otherwise we print the command and return it
    line = ('. ${DIR_PIPE}/epitome/modules/pre/linreg_EPI2T1_FSL ' +
                                               str(input_name) + ' ' +
                                               str(dims))
    return line, output
