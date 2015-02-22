#!/usr/bin/env python

def run(dir_data, expt, mode):
    output = ''

    print('\nAdding T1-to-MNI registration checking QC to the outputs.')

    line = ('echo python ${DIR_PIPE}/epitome/modules/qc/check_t12mni ' + 
             str(dir_data) + ' ' + str(expt) + ' ' + str(mode))

    return line, output
