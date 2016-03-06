#!/usr/bin/env python

def run(dir_data, expt, mode):
    output = ''

    print('\nAdding subject-wise regressor spectra QC to the outputs.')

    line = ('. ${DIR_PIPE}/epitome/modules/qc/qc_spectra ' +
            '${DIR_DATA} ${EXPT} ${MODE} ${ID}')

    return line, output
