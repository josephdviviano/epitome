#!/usr/bin/env python

def return_paths():
    """
    Returns the paths to the data, pipeline, AFNI, and specifies the number of 
    CPU cores to use.
    """
    # the data directory absolute path
    dir_data = '/srv/MRI/WORKING'
    # the pipeline directory absolute path
    dir_pipe = '/srv/CODE/EPItome-xl'
    # AFNI directory absolute path
    dir_afni = '/usr/local/abin'
    # number of cores to use
    cores = 7

    return dir_data, dir_pipe, dir_afni, cores
