#!/usr/bin/env python

def check_T12MNI(dir_data, expt, mode):
    output = ''

    print('\nAdding T1-to-MNI registration checking QC to the outputs.')

    line = ('echo python ${DIR_PIPE}/epitome/modules/qc/check_T12MNI ' + 
             str(dir_data) + ' ' + str(expt) + ' ' + str(mode))

    return line, output
