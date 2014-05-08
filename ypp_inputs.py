#!/usr/bin/env python

import os
import sys
import ypp_utilities

# defines paths, subjects, etc.

def init():
    path = '/srv/MRI/WORKING'
    mode = 'TASK'
    core = 7

    #expt = 'BEBASD'
    #expt = 'RSFC1'
    #expt = 'ATOL'
    #expt = 'TRSE'
    expt = 'RSFC2'
    # expt = 'TRSEEN'                              # experiment directory

    return path, expt, subj, mode, core

def init_shell(path, expt):
    subjects = ypp_utilities.get_subj(os.path.join(path, expt))
    output = '"'

    for subj in subjects:
        output+=str(subj)
        output+=' '
    output+='"'

    os.system('echo ' + str(output))

if __name__ == "__main__":
    init_shell(sys.argv[1], sys.argv[2])