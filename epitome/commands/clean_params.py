#!/usr/bin/env python

import os
import epitome as epi

def run(expt, clean):

    dir_data, dir_pipe, dir_afni, cores = epi.config.return_paths() 

    print('\n *** Adding PARAMS PURGE to the cleanup Queue! ***')

    fname = os.path.join(dir_data, expt, clean)
    line = ('. ' + str(dir_pipe) + 
            '/epitome/modules/cleanup/clean_params >> ' + fname)
    os.system(line)
