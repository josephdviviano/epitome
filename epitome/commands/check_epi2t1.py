#!/usr/bin/env python

def run(dir_data, expt, mode):
    output = ''

    print('\nAdding EPI-to-T1 registration checking QC to the outputs.')

    line = ('echo python ${DIR_PIPE}/epitome/modules/qc/check_epi2t1 ' + 
             str(dir_data) + ' ' + str(expt) + ' ' +  str(mode))

    return line, output
