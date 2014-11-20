#!/usr/bin/env python

import epitome as epi

def run(input_name):
    output = 'scrubbed'

    print('\nRemoving motion-corrupted TRs.')
    
    print('\nWould you like to use the defaults?')
    print('                           Head Size = 50 mm')
    print('    Framewise Displacement Threshold = 0.3 mm / TR')
    print('                     DVARS Threshold = 3 pct signal change / TR')
    
    try:
        defaults = ['yes', 'no']
        decision = epi.utilities.selector_list(defaults)

        # if the user rejects the defaults or makes a mistake
        if decision == 'no' or None:

            print('\nInput head size (default 50)')
            head_size = epi.utilities.selector_float()

            print('\nInput FD threshold (default 0.3)')
            FD = epi.utilities.selector_float()

            print('\nInput head size (default 1000000)')
            DV = epi.utilities.selector_float()

        else:
            print('\nOK, using the defaults.')
            head_size = 50
            FD = 0.3
            DV = 1000000 # this turns DVARS off, effectively

    # if we messed any of these up, we return None
    except ValueError as ve:
        return '', None

    # otherwise we print the command and return it
    line = ('. ${DIR_PIPE}/epitome/modules/pre/trdrop ' + 
                                  str(input_name) + ' ' +
                                  str(head_size) + ' ' +
                                  str(FD) + ' ' +
                                  str(DV))

    return line, output