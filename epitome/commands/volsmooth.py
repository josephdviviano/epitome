#!/usr/bin/env python

import epitome as epi

def run(input_name):
    output = 'volsmooth'

    print('\nVolumetric smoothing within a defined mask.')

    try:
        print('\nInput mask prefix (default = EPI_mask):')
        mask_prefix = raw_input('Mask Prefix: ')
        if mask_prefix == '':
            mask_prefix = 'EPI_mask'
        
        print('\nInput smoothing kernel FWHM (mm):')
        fwhm = epi.utilities.selector_float()

    # if we messed any of these up, we return None
    except ValueError as ve:
        return '', None

    # otherwise we print the command and return it
    line = ('. ${DIR_PIPE}/epitome/modules/pre/volsmooth ' + 
                                     str(input_name) + ' ' +
                                     str(mask_prefix) + ' ' +
                                     str(fwhm))

    return line, output
