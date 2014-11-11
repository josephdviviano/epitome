#!/usr/bin/env python

import copy

def run(input_name):
    output = copy.copy(input_name) # return output unharmed

    print('\nGenerating regressors from ' + str(input_name))

    line = ('. ${DIR_PIPE}/epitome/modules/pre/gen_regressors ' +
                                                  str(input_name))

    return line, output
