#!/usr/bin/env python

def check_runs(dir_data, expt, mode):
    output = ''

    print('\nAdding NIFTI dimension-checking QC to the outputs.')

    line = ('echo bash ${DIR_PIPE}/epitome/modules/qc/check_runs ' + 
             str(dir_data) + ' ' + str(expt))

    return line, output
