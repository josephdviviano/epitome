#!/usr/bin/env python

def run(dir_data, expt, mode):
    output = ''

    print('\nAdding subject-wise motion QC to the outputs.')

    line = ('. ${DIR_PIPE}/epitome/modules/qc/qc_motionind ' +
             '${DIR_DATA} ${EXPT} ${MODE} ${ID}')

    return line, output
