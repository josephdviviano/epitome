EPItome-xl -- Kimel Family TIGR Lab
-----------------------------------
This is the source for the Kimel Family TIGR Lab EPItome-xl MRI Pipeline. Mostly written by Joseph D Viviano 2014. It has been modified to work on the local cluster at CAMH's College St. location, and updated with modules to meet the demands of this site.

Quick Start
-----------
This project depends on the following free software: numpy, scipy, matplotlib, nibabel, AFNI, FSL, & sun grid engine.

+ `git clone` this repository to a directory of your choosing.
+ Edit `config` to point to your EPItome-xl directory and your MRI data directory.
+ Intstall using `easy_install epitome`.
+ Add some MRI data to your data directory.
+ Check your work using `epitome check <experiment>`.
+ Generate some pre-processing scripts using `epitome run`.

Detailed Instructions
---------------------
Please see [doc/instructions.md](doc/instructions.md) for all of the gory details, and contact joseph@viviano.ca with any questions. Enjoy the science!
