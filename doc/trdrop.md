trdrop
------
Usage: TRdrop <func_prefix> <head_size> <FD_thresh> <DV_thresh>

+ func_prefix -- functional data prefix (eg.,smooth in func_smooth). 
+ head_size -- head radius in mm (def. 50 mm). 
+ thresh_FD -- censor TRs with $\Delta$ motion > $x$ mm (def. 0.3 mm). 
+ thresh_DV -- censor TRs with $\Delta$ GS change > $x$ \% (def. [1000000](http://upload.wikimedia.org/wikipedia/en/1/16/Drevil_million_dollars.jpg). 

This removes motion-corrupted TRs from fMRI scans and outputs shortened versions for connectivity analysis (mostly). By default, DVARS regression is set of OFF by using a very, very high threshold.

Prerequisites: init_epi.
