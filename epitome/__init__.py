"""
The EPItome-xl pipeline. If called from the command line, epitome.interface is
run. This code will generate a large number of scripts to be submitted to
the sun grid engine running on your computer.

I'll add more here later, promise. joseph.d.viviao@gmail.com
"""
###############################################################################
####### NB: I have no idea what I am doing here, so I am copying numpy. #######

import os, sys

from . import interface
from . import config
from . import utilities

# Warn the user if s/he is using Python 3...
if sys.version_info[0] >= 3:
    print """ Warning, I haven't tested this with Python 3 yet! """

if __name__ == "__main__":
    epitome.interface()