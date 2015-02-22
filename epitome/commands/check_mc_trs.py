#!/usr/bin/env python

def run(dir_data, expt, mode):
    output = ''

    print('\nAdding Motion Correction TR checking QC to the outputs.')

    line = ('echo python ${DIR_PIPE}/epitome/modules/qc/check_mc_trs ' + 
             str(dir_data) + ' ' + str(expt) + ' ' + str(mode) + ' ${ID}')

    return line, output
