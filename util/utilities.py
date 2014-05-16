#!/usr/bin/env python

import os
import sys

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

def init_shell(path, expt):
    """
    Defines paths, subjects, etc.
    """
    subjects = ypp_utilities.get_subj(os.path.join(path, expt))
    output = '"'

    for subj in subjects:
        output+=str(subj)
        output+=' '
    output+='"'

    os.system('echo ' + str(output))

if __name__ == "__main__":
    init_shell(sys.argv[1], sys.argv[2])
