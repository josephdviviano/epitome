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
###############################################################################
####### NB: I have no idea what I am doing here, so I am copying numpy. #######

from . import interface
from . import config
from . import utilities
from . import stats

# accessible from epitome name-space, but not imported from epitome import *
from builtins import os, sys