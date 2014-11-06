#!/usr/bin/env python

import copy

def nonlinreg_calc_AFNI(input_name):
    output = copy.copy(input_name) # return output unharmed

    print('\nCalculating nonlinear registration pathways.')

    line = ('. ${DIR_PIPE}/epitome/modules/pre/nonlinreg_calc_AFNI')

    return line, output
