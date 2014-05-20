"""
The EPItome-xl pipeline. If called from the command line, epitome.interface is
run. This code will generate a large number of scripts to be submitted to
the sun grid engine running on your computer.

I'll add more here later, promise. joseph.d.viviao@gmail.com
"""
###############################################################################
####### NB: I have no idea what I am doing here, so I am copying numpy. #######

from . import interface
from . import config
from . import utilities

# accessible from epitome name-space, but not imported from epitome import *
if sys.version_info[0] >= 3:
    from builtins import os, sys
else:
    from __builtin__ import os, sys