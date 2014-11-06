#!/usr/bin/env python

def check_masks(dir_data, expt, mode):
    output = ''

    print('\nAdding mask-checking QC to the outputs.')

    line = ('echo python ${DIR_PIPE}/epitome/modules/qc/check_masks ' + 
             str(dir_data) + ' ' + str(expt) + ' ' + str(mode))

    return line, output
