#!/usr/bin/env python
"""
Temporary solution: users must define relevant system-wide options here.
Adding some functions that search for installed software.
"""

import os
import subprocess
import multiprocessing as mp

def find_afni():

    """
    Returns the path of the afni bin/ folder, or None if it isn't
    on your path.
    """
     
    try:
        dir_afni = subprocess.check_output('which afni', shell=True)
        dir_afni = os.path.dirname(dir_afni)
    except:
        dir_afni = None

    return dir_afni

def find_epitome():
    """
    Returns the path of the epitome bin/ folder, or None if it isn't
    on your path.
    """

    try:
        dir_epitome = subprocess.check_output('which epitome', shell=True)
        dir_epitome = os.path.dirname(dir_epitome)[:-4] # also remove '/bin'
    except:
        dir_epitome = None

    return dir_epitome

def find_matlab():
    """
    Returns the path of the matlab folder, or None if it isn't
    on your path.
    """

    try:
        dir_matlab = subprocess.check_output('which matlab', shell=True)
        dir_matlab = '/'.join(dir_matlab.split('/')[:-2])

    except:
        dir_matlab = None
 
    return dir_matlab

def find_fsl():
    """
    Returns the path of the fsl bin/ folder, or None if it isn't
    on your path.
    """
    try:
        dir_fsl = subprocess.check_output('which fsl', shell=True)
        dir_fsl = os.path.dirname(dir_fsl)[:-4]
    except:
        dir_fsl = None

    return dir_fsl

def find_fix():
    """
    Returns the path of the fix bin/ folder, or None if it isn't
    on your path.
    """
    
    try:
        dir_fix = subprocess.check_output('which fix', shell=True)
        dir_fix = os.path.dirname(dir_fsl)[:-4]
    except:
        dir_fix = None

    return dir_fix

def find_data():
    """
    Returns the data path defined by the EPITOME_DATA environment
    variable.
    """

    try:
        dir_data = os.getenv('EPITOME_DATA')
    except:
        dir_data = None

    return dir_data

def return_paths():
    """
    Returns the paths to the data, pipeline, AFNI, and specifies the number of 
    CPU cores to use.

    This function is retained for backwards-compatibility, but I would like to
    move towards the 'find' funct
    """
    
    # the data directory absolute path
    dir_data = find_data()
    
    # the pipeline directory absolute path
    dir_pipe = find_epitome()
    
    # AFNI directory absolute path
    dir_afni = find_afni()
    
    # get the number of CPU cores available 
    # (this will have to change when we improve this code to work in a cluster 
    # environment).
    cores = mp.cpu_count() - 1

    return dir_data, dir_pipe, dir_afni, cores
