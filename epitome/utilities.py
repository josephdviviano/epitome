#!/usr/bin/env python
"""
A collection of utilities for the EPItome-xl pipeline. Mostly for getting 
subject numbers/names, checking paths, etc.
"""

import os, sys
import epitome as epi

def get_subj(dir):
    """
    Gets all folder names (i.e., subjects) in a directory (of subjects).
    """
    subjects = []
    for subj in os.walk(dir).next()[1]:
        if os.path.isdir(os.path.join(dir, subj)) == True:
            subjects.append(subj)
    subjects.sort()
    return subjects

def has_permissions(directory):
    if os.access(directory, 7) == True:
        flag = True
    else:
        print('\nYou do not have write access to directory ' + str(directory))
        print('Please contact a system administrator and try again.\n')
        flag = False

    return flag

def init_shell(path, expt):
    """
    Gets all of the subjects and prints them as a BASH friendly variable.
    """
    subjects = epi.utilities.get_subj(os.path.join(path, expt))
    output = '"'

    for subj in subjects:
        output+=str(subj)
        output+=' '
    output+='"'

    os.system('echo ' + str(output))

if __name__ == "__main__":
    init_shell(sys.argv[1], sys.argv[2])
