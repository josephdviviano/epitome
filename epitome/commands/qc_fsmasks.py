#!/usr/bin/env python

def run(dir_data, expt, mode):
    output = ''

    print('\nAdding mask-checking QC to the outputs.')

    line = ('. ${DIR_PIPE}/epitome/modules/qc/qc_fsmasks ' +
            '${DIR_DATA} ${EXPT} ${MODE}')

    return line, output
