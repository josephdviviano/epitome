#!/usr/bin/env python

import epitome.commands as cmd

def init_EPI():    
    output = 'scaled'

    print('\nInitializing functional MRI pre-processing.')

    try:
        # get the data-quality option
        print('\nSelect data quality:')
        data_quality = ['low', 'high']
        quality = cmd.utils.selector_list(data_quality)

        # get the number of TRs to delete
        print('\nNumber of TRs to delete:')
        deltr = cmd.utils.selector_int()

        # get the slice timing
        print('\nSlice-timing pattern: (see AFNI 3dTshift for more help)')
        t_patterns = {'alt+z' : '= alternating in the plus direction', 
                      'alt+z2' : '= alternating, starting at slice #1', 
                      'alt-z' : '= alternating in the minus direction', 
                      'alt-z2' : '= alternating, starting at slice #nz-2', 
                      'seq+z' : '= sequential in the plus direction',
                      'seq-z' : '= sequential in the minus direction'}
        slice_timing = cmd.utils.selector_dict(t_patterns)

        # normalize
        print('\nTime series normalization: (see documentation for help)')
        norm_dict = {'off' : ': deskulling, no normalization',
                     'pct' : ': 1% = 1, normalize to 100 mean voxelwise',
                     'scale':': scale run mean to = 1000, arbitrary units'}
        normalization = cmd.utils.selector_dict(norm_dict)

        # masking
        print('\nEPI masking: acquisition dependent')
        mask_list = ['loose', 'normal', 'tight']
        masking = cmd.utils.selector_list(mask_list)

    # if we messed any of these up, we return None
    except ValueError as ve:
        return '', None

    # otherwise we print the command and return it
    line = ('. ${DIR_PIPE}/epitome/modules/pre/init_EPI ' +
                                      str(quality) + ' ' +
                                      str(deltr) + ' ' +
                                      str(slice_timing) + ' ' +
                                      str(normalization) + ' ' +
                                      str(masking))
    return line, output
