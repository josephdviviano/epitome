#!/usr/bin/env python
"""
Temporary solution: users must define relevant system-wide options here.
"""

import multiprocessing as mp

def return_paths():
    """
    Returns the paths to the data, pipeline, AFNI, and specifies the number of 
    CPU cores to use.
    """
    # the data directory absolute path
    dir_data = '/srv/MRI/WORKING'
    # the pipeline directory absolute path
    dir_pipe = '/srv/CODE/epitome'
    # AFNI directory absolute path
    dir_afni = '/usr/local/abin'
    # get the number of CPU cores available 
    # (this will have to change when we improve this code to work in a cluster 
    # environment).
    cores = mp.cpu_count() - 1

    return dir_data, dir_pipe, dir_afni, cores


