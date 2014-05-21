"""
The EPItome-xl pipeline. If called from the command line, epitome.interface is
run. This code will generate a large number of scripts to be submitted to
the sun grid engine running on your computer.

I'll add more here later, promise. joseph.d.viviao@gmail.com
"""
###############################################################################
####### NB: I have no idea what I am doing here, so I am copying numpy. #######

from . import config
from . import utilities

# if __name__ == "__main__":
#     epitome.interface()