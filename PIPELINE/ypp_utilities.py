#!/usr/bin/env python

import os

def get_subj(dir):
    """
    Gets all folder names in a directory.
    """
    subjects = []
    for subj in os.walk(dir).next()[1]:
        if os.path.isdir(os.path.join(dir, subj)) == True:
            subjects.append(subj)
    subjects.sort()
    return subjects