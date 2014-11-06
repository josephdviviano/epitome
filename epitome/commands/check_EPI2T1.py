#!/usr/bin/env python

def check_EPI2T1(dir_data, expt, mode):
    output = ''

    print('\nAdding EPI-to-T1 registration checking QC to the outputs.')

    line = ('echo python ${DIR_PIPE}/epitome/modules/qc/check_EPI2T1 ' + 
             str(dir_data) + ' ' + str(expt) + ' ' +  str(mode))

    return line, output
