#!/usr/bin/env python

"""
###############################################################################

                       _  _ ___
                      |_ |_) | _|_  _  ._ _   _ __ \/ |  
                      |_ |  _|_ |_ (_) | | | (/_   /\ |_ 

Usage:

    epitome list               -- returns a list of all available modules.
    epitome check              -- returns installation paths.
    epitome check <experiment> -- checks directory structure for a given 
                                  experiment.
    epitome <module> -help     -- returns usage for a single module.
    epitome run                -- boots up the user interface (which prints
                                  out a set of processing scripts).

#######################################################################jdv2014#

"""

import os
import sys
import config

def print_modules():
    print """I'm printing some modules!"""


def check_paths():
    print """I'm checking some paths!"""

def check_directories(exp):
    print """I'm checking the directory structure for """ + str(exp) + '!'

def print_help(module):
    print """I'm printing the help file for """ + str(module) + '!'

def run_epitome():
    print """I'm running EPItome-XL!"""

# this is the command-line usage bit
if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == 'list':
        print_modules()
    
    # a set of convenience functions
    elif len(sys.argv) == 2 and sys.argv[1] == 'check':
        check_paths()
    elif len(sys.argv) == 3 and sys.argv[1] == 'check':
        check_directories(sys.argv[2]) 
    elif len(sys.argv) > 3 and sys.argv[1] == 'check':
        print 'epitome check only works with 1 experiment at a time!'

    # for printing help
    elif len(sys.argv) == 3 and sys.argv[2] == '-help':
        print_help(sys.argv[1])

    # for running the command-line interface
    elif len(sys.argv) == 2 and sys.argv[1] == 'run':
        run_epitome()

    # return the usage if the user does a silly thing
    else:
        print __doc__
