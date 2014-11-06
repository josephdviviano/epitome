#!/usr/bin/env python

def check_mc_TRs(dir_data, expt, mode):
    output = ''

    print('\nAdding Motion Correction TR checking QC to the outputs.')

    line = ('echo python ${DIR_PIPE}/epitome/modules/qc/check_mc_TRs ' + 
             str(dir_data) + ' ' + str(expt) + ' ' + str(mode) + ' ${ID}')

    return line, output
