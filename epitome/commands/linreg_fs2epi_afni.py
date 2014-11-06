#!/usr/bin/env python

import copy 

def linreg_FS2EPI_AFNI(input_name):
    output = copy.copy(input_name) # return output unharmed

    print('\nMoving Freesurfer atlases to single-subject space using AFNI.')

    line = ('. ${DIR_PIPE}/epitome/modules/pre/linreg_FS2EPI_AFNI')

    return line, output
