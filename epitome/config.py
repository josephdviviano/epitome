#!/usr/bin/env python
"""
Temporary solution: users must define relevant system-wide options here.
"""

import os
import subprocess
import multiprocessing as mp


def find_afni():
    dir_afni = subprocess.check_output('which afni', shell=True)
    dir_afni = os.path.dirname(dir_afni)

    return dir_afni

def find_epitome():
    dir_epitome = subprocess.check_output('which EPItome', shell=True)
    # also removed '/bin'
    dir_epitome = os.path.dirname(dir_epitome)[-4]

    return dir_epitome

def return_paths():
    """
    Returns the paths to the data, pipeline, AFNI, and specifies the number of 
    CPU cores to use.
    """
    
    # the data directory absolute path
    dir_data = '/srv/MRI/WORKING'
    
    # the pipeline directory absolute path
    dir_pipe = find_epitome()
    
    # AFNI directory absolute path
    dir_afni = find_afni()
    
    # get the number of CPU cores available 
    # (this will have to change when we improve this code to work in a cluster 
    # environment).
    cores = mp.cpu_count() - 1

    return dir_data, dir_pipe, dir_afni, cores
