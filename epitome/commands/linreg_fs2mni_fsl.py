#!/usr/bin/env python

import copy 

def linreg_FS2MNI_FSL(input_name):   
    output = copy.copy(input_name) # return output unharmed

    print('\nMoving Freesurfer atlases to MNI space using FSL.')

    line = ('. ${DIR_PIPE}/epitome/modules/pre/linreg_FS2MNI_FSL')

    return line, output
