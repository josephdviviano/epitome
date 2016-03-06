#!/usr/bin/env python

def run(dir_data, expt, mode):
    output = ''

    print('\nAdding T1-to-MNI registration checking QC to the outputs.')

    line = ('. ${DIR_PIPE}/epitome/modules/qc/qc_t12mni ' +
            '${DIR_DATA} ${EXPT} ${MODE}')

    return line, output
