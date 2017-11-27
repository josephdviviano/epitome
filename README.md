epitome
-------
epitome is a collection of scriptit modules for pre-processing MRI data, as well as a bundle of command-line tools for processing and analysing.

These tools will be of interest to researchers who want to prototype new analysis strategies in a confirgurable environment with little up-front cost.

Written by Joseph D. Viviano 2014-17.

> As long as our brain is a mystery, the universe, the reflection of the structure of the brain will also be a mystery.
> -- Santiago Ramón y Cajal

**Shortcuts:**

+ [Setup](#setup)
+ [Introduction](#introduction)
+ [Dependencies](#dependencies)
+ [Bundled Files](#bundled-files)
+ [Overview](#overview)
+ [Workflows](#workflows)
+ [Writing Modules](#writing-modules)

Setup
-----
+ install [scriptit](https://github.com/josephdviviano/scriptit)

epitome does not have any direct dependencies, but the scripts it generates rely heavily on well-developed MRI pacakges. The more esoteric packages come bundled with this code, and some custom analysis packages are bundled with epitome under bin/

Quickstart:

+ `git clone` this repository to a directory of your choosing.
+ Set `SCRIPTIT_DATA` to point to an MRI data directory.
+ Set `SCRIPTIT_MODULES` to point to `epitome/modules`.
+ Set `PATH` to point to `epitome/bin`.
+ Set `PYTHONPATH` to point to `epitome`.
+ Set `SUBJECTS_DIR` to point to the desired freesurfer subjects folder.
+ Set `HCP_DATA` to point to a directory that will hold data in the HCP folder.
+ Check your work using `scriptit check`.
+ Create an experiment and some subjects using `sit-folder`.
+ Put some NIFTI data into these subject's RUN folders.
+ Check your work using `scriptit verify <experiment>`
+ Generate a pre-processing pipeline using `scriptit generate`.
+ Render this pipeline to a BASH script using `scriptit render`.

Currently, epitome requires the user to have installed and configured the following packages to be in their path:

+ [FSL](http://fsl.fmrib.ox.ac.uk/fsl/fslwiki/)
+ [AFNI](http://afni.nimh.nih.gov/)
+ [Freesurfer](http://freesurfer.net/)
+ [Matlab (with Stats and Signals toolboxes) and/or Matlab Compiler](http://afni.nimh.nih.gov/sscc/dglen/CompiledMatlab)
+ [Numpy](http://www.numpy.org/)
+ [Scipy](http://www.scipy.org/)
+ [MatPlotLib](http://matplotlib.org/)
+ [NiBabel](http://nipy.org/nibabel/)
+ [Scikit Learn](http://scikit-learn.org/stable/)

Optional:

+ [FSL FIX 1.61: ica_fix](http://fsl.fmrib.ox.ac.uk/fsl/fslwiki/FIX)
+ [Bioread 0.9.3: epi-physio](https://pypi.python.org/pypi/bioread/0.9.3)
+ [gradunwarp: unwarp](https://github.com/Washington-University/gradunwarp)
+ [Connectome Workbench](http://www.humanconnectome.org/software/connectome-workbench.html)
+ [HCP Pipeline Scripts and Atlases](http://www.humanconnectome.org/documentation/HCP-pipelines/index.html)
+ [Ciftify](https://github.com/edickie/ciftify)

Introduction
------------
epitome is a program designed for the flexible construction of MRI pre-processing pipelines, with a focus on functional MRI images and their associated problems. Its primary function is to take BASH modules and chain them together in any way the user desires to create a set of batch-processing scripts for an MRI experiment. These modules are not necessarily dependent on one another, allowing users of this package to easily extend the functionality of epitome by simply depositing a shell script into the appropriate module folder and writing the associated python wrapper command (and documentation!)

The goal of this design is to allow multiple levels of control for users of different skills with the same interface. epitome facilitates the construction of very robust pre-processing scripts that can be run on your computer or in a distributed computing environment by only answering a few high-level questions, hopefully making it easy for beginners to get started. The scripts that are output by these commands are otherwise fully tweak-able and well commented -- they encourage experimentation. These modified modules could eventually evolve into new features altogether, which are easily added to the existing pool.

This system is also designed to facilitate easy-to-reproduce research, as these scripts can be easily re-purposed for new experiments that follow the epitome folder structure. In this way, the outputs of epitome act as your lab notebook, and can be shared with collaborators or reviewers.

This manual will progress to more advanced topics in the end. First, I will explain the basic use of epitome. Next, I'll explain the modules one-by-one, follow with a description of a few common pre-processing tasks. I'll then  and finish with an explanation on how to add new modules.

Dependencies
------------
epitome contains a small number of programs that actually manipulate data, but also makes heavy use of widely-used MRI analysis tools and a number of python distributions. The user is assumed to have properly installed and configured FSL, AFNI, Freesurfer, and the python packages numpy, scipy, and matplotlib. For physiological noise regression, you must have the MATLAB compiler runtime installed, along with AFNI's [McRetroTS](http://afni.nimh.nih.gov/sscc/dglen/McRetroTS) scripts installed in /opt/MATLAB/MATLAB_Compiler_Runtime/ and /opt/mcretro/, respectively.

epitome comes packaged with AFNI's [McRetroTS](http://afni.nimh.nih.gov/sscc/dglen/McRetroTS) scripts in bin/. Version downloaded: 2012.12.17.1431   McRetroTS_linux64pkg.zip on Nov 5th 2014.

The program itself was built and tested on the Ubuntu 12.04/14.04 OS. I imagine it will work well in any Linux environment. It should run on Mac OS X as well, but this remains unverified. There will be no support for Windows.

Bundled Files
-------------
epitome comes with some bundled files under `assets/`. Some of these files are used by the pipeline directly, and others are files that the user might find useful at the analysis stage (for example, whole brain atlases). A full list follows, with indication as to whether the database interacts directly with these files, or whether they are only there for convienience.

+ .labels files -- files containing MNI coordinates for ROI-based analysis. Can be used with AFNI's `3dUndump` to create 3D ROI mask NIFTIs.
+ MNI152_T1_1mm_brain.nii.gz -- the epitome pipeline's MNI brain (from FSL 5.0.7) [used by epitome].
+ MNI152_T1_1mm_brain_mask_dil.nii.gz -- the dialated MNI brain mask (from FSL 5.0.7) [used by epitome].
+ MNI152_T1_1mm.nii.gz -- a copy of the MNI brain with the skull intact (from FSL 5.0.7).
+ MNI_avg152T1.nii.gz -- a copy of the MNI brain from AFNI (downloaded November 2014), used in previous versions of epitome.
+ shen_?mm_268_parcellation.nii.gz -- a 264 ROI brain atlas in MNI space (equally-sized ROIs, covers entire cortex, subcortex).

Overview
--------
epitome comes with a few command-line interfaces. epitome is used to inspect data in the MRI directory, returns information on the currently-available modules, can be used to construct new pipelines, and to remove unwanted data from the MRI directory cleanly. `epi-physio` is a tool built to parse physiological data from the BIOPAK 150 unit installed at York University (Toronto), and might need to be adapted / extended to work with other units. `epi-folder` is used to generate an appropriate folder structure in the MRI directory for the epitome pipeline to work on.

The MRI directory itself must be organized as follows:

    /EPITOME
        /EXPERIMENTS
            /SUBJECTS
                /MODE
                    /SESS
                        /RUN

The Freesurfer subject directory does not need to be inside the epitome folder structure.

The folder structure is integral to epitome -- if it is flawed, the pipeline will fail in [mysterious ways](https://www.youtube.com/watch?v=TxcDTUMLQJI). The structure itself is designed to be thought of as a tree. At the roots of the tree are the individual files collected at the scanner. As we ascend the tree, files are combined across sessions, image modalities, and subjects, so one finds experiment-wide outputs at the highest levels. The `epi-folder` program will help you set up these folders appropriately.

**EXPERIMENTS**

This is a set of folders containing entire experiments. There are no important naming conventions, but it seems advisable (for consistency) to make the folder names all capitals, and short (e.g., `LINGASD` for 'language study on those with autism spectrum disorder').

**SUBJECTS**

Once again, these are simply folders with participant names. They follow no convention, but should be consistent for your own sake.

**MODE**

Image modality folders separate images of different kinds: anatomicals, epi's collected using differing sequences, or epi's of different task-types (e.g., rest vs. two-back matching). The T1 directory *must* exist for each subject at the very minimum in `SESS01`.

This is a good place to separate scans you would like to have analyzed in different ways, or to test multiple pre-processing strategies on the same set of subjects. For example, it may be that your `TASK` set is being prepared for a GLM or partial least squares analysis, and should be processed more minimally than your REST data, which will undergo things such as low-pass filtering and nuisance variable regression. In another example, it may be that you are curious about how your choice of pre-processing steps influences your results. Here, you could have a set of identical scans under `REST_1` and `REST_2`. You could build two sets of pipelines using epitome with the unique identifiers `1` and `2`, and run them on each modality separately.

epitome has no modules built for DTI scans at the moment, but they could easily be added here under their own DTI modality. Note that a set of DTI-friendly modules would need to be built for these kinds of scans.

**SESS**

The session folders are used to separate scans taken on different days. They must begin with `SESS` and end with a zero-padded 2-digit number (e.g., `02`). epitome does not currently support experiments where participants were scanned on more than 99 days.

These session folders are currently used to match epis with the T1 taken on the same day. Best practice is to collect a T1 with every epi scan. The pipeline is also able to use the T1 collected on the first day as the target for all sessions. This will be automatically decided by the pipeline: if the number of T1s does not equal the number of sessions, only the first T1 will be used.

**While it is normally advisable for the sessions to align chronologically, in the case that the only T1 collected was _not on the first day_, it should still be entered as `SESS01`.**

**RUN**

Each `RUN` folder should contain one and only one .nii or .nii.gz formatted file. Appropriate companion files should also be entered here: physiological noise recordings (extension .PHYS, and/or custom slice timing files (extension .1D). If more than one NIFTI file is in this folder, the pipeline will fail. Any other files kept in this folder will remain untouched, so this is a fine place to keep run-specific notes.

Workflows
---------
epitome give you the ability to chain modular BASH scripts together to generate a great number of MRI pre-processing pathways, and in doing so, gives you the power to create very bad pipelines. Here, I detail a few reasonable workflows.

**basic: GLM, PLS, etc.**

Here, we are interested in doing a set of basic tasks before running a GLM analysis on some task-based MRI design. We've already placed the anatomical and functional NIFTI (and .phys files, if appropriate) into their RUN folders and have run epitome run. Every run begins with `init_epi`.

    init_epi high 0 on alt+z off normal

Here, we are telling epitome that we are working with high contrast data, want to remove 0 TRs from the beginning of each run, use despiking, have acquired our data in the alternating plus direction, we are turning off time series normalization, and would like a brain mask of normal tightness, which is a reasonable default.

    linreg_calc_AFNI high lpc giant_move

Here we are calculating all of our registration pathways, from epi space, to single-subject T1 space (and therefore, Freesurfer space), and finally group-level MNI space, using linear registrations. Some reference images and transformation pathways are output, but we haven't actually moved the data yet.

    linreg_FS2epi_AFNI

This will put all of our Freesurfer-derived segmentations in single-subject epi space, which we can use to generate regressors.

    volsmooth scaled epi_mask 6.0

This will smooth the epi data within the defined mask (anat_epi_mask.nii.gz in this case) using a full-width half-maximum (FWHM) of 6 mm. The input data is still scaled, since this is the first actual manipulation of the outputs from init_epi.

    linreg_epi2MNI_AFNI volsmooth 3.0

Finally, this will transform each smoothed run up into MNI space with a isotropic voxel resolution of 3 mm^2.

**functional connectivity**

Functional connectivity analysis benefits from the application of tissue-based regressors pre-analysis. Here we generate the mean, mean derivative, and mean square, of the white matter & ventricle time series, along with the motion paramaters.

    init_epi high 0 on alt+z off normal
    linreg_calc_AFNI high lpc giant_move
    linreg_FS2epi_AFNI

    filter scaled 4 on off on on off off off off EPI_mask

*Optional:* In some cases it may be advantageous to remove motion-corrupted TRs from your data, especially if you are comparing two groups you suspect move in different ways. This can be done with the TR drop module. We're just going to use the default settings here.

    trscrub 50 0.5 100000

Here, we are detrending the scaled data against the head motion parameters, Legendre polynomials up to the 4th order, the mean white matter signal, the local white matter signal, the mean cerebral spinal fluid signal, and the mean draining vessel signal. For all of these signals, we also regress against the 1st temporal lag.

    lowpass filtered EPI_mask average 3

Next, we low-pass the data using a moving-average filter of span 3. Most of the information in BOLD data is of fairly low frequency, so the hope is that low-passing the data will remove some high-frequency noise from the signals. There are multiple options that could be used here, but no one ever got fired for using a moving average filter, so I suggest it here as a fair default.

    volsmooth lowpass EPI_mask 6.0
    linreg_epi2MNI_AFNI volsmooth 3.0

**surface analysis / smoothing for volume analysis**

When studying the cortex, it is often desirable to look at the data on a surface. This prevents the blurring of signals between sulci and gyri, allows for finer localization of function, and permits some interesting co-registration methods. For simplicity, we will do this to data intended for a simple GLM analysis.

    init_epi high 0 on alt+z off normal
    linreg_calc_AFNI high lpc giant_move
    linreg_FS2epi_AFNI

    vol2surf scaled

This will projects the epi data contained within the white-matter boundaries of the Freesurfer segmentation to a AFNI-based surface space. This must be run on epi data in single-subject T1 space, otherwise we won't end up projecting the cortex to the surface model, but rather some random selection of brain and non-brain matter!

    surfsmooth surface 10.0

This will smooth along the cortical surface with a FWHM of 10mm. Generally, surface-smoothed data can be subjected to larger smoothing kernels, as they do not mix signals coming from cortically-distant regions as readily in this format.

    surf2vol smooth scaled

This will project the surface data in smooth back into volume format in the same space as the scaled data, from whence it came. Many of the spatial-specificity advantages of surface-based analysis are now available in volume space, ensuring compatibility with many traditional analysis programs.

Writing Modules
---------------
epitome, as it stands, has very few novel features over traditional pipelining programs. However, its strength lies with ease of extensibility. Here, I will detail how one would create a new module to be included in the epitome pipeline.

Modules take the form of either BASH scripts, or stand alone programs (such is the case with most QC modules at the moment) with a few stylistic conventions. They are `active' so long as they are kept in a .../epitome/modules/XXX directory, and will be accessed by the pipeline according to their type. `freesurfer' and `pre' modules are accessed first by epitome run, followed by those in `qc'. At the moment, the two freesurfer modules are not optional.

The modules themselves use a [here-doc trick](http://tldp.org/LDP/abs/html/here-docs.html) to set variables defined on the command line first, and then `cat` the remaining script to STDOUT. Therefore, running a properly formatted module should not run anything, but should simply print it's contents out to the command line. There are a few reserved variables used in most, if not all, modules.

+ DIR_SESS: A listing of all the sessions within a image modality.
+ SESS: A variable denoting the current session.
+ DIR_RUNS: A listing of all the runs within a session.
+ RUN: A variable denoting the current run.
+ NUM: The run number.
+ ID: The unique identifier of a epitome run, defined globally.

A module will typically loop through sessions, and then runs, taking an input file prefix (such as func_scaled), performing a number of operations on that file (producing intermediate files worth keeping, or in other cases, temporary files that will be removed by the module's end), and sometimes outputting a single functional file with a new prefix (such as func_lowpass). The anatomy of a call to an output file follows the convention

    filename.ID.NUM.extension.

For NIFTI files, filename is typically func_prefix or anat_prefix, for 4D and 3D files, respectively. Regressors, QC metrics, and other parameter files are typically stored in a special PARAMS folder. Registrations are stored with the reg_X_to_Y convention, and the extension appropriate to the program that generated them (be it AFNI or FSL).

A well-written module will never try to do anything that has already been done. Therefore, blocks of code are wrapped in an

    if [ -f filename.ID.NUM.extension ]; then; commands; fi

loop. This is not mandatory, but highly recommended. It allows one to re-run the pipeline with a few tweaks, and the code will only act on files missing from the output structure.

Finally, variables can be defined within the module to allow the user to set them before running the module via the command line. Each command-line argument should correspond to a variable at the top of the module, which is then referenced in the appropriate locations throughout the script. Since the variables are defined before each module, the name-space between modules does not need to be maintained. However, for consistency, it is best to select variable names that are specific and unlikely to have shared meanings in other areas of the pipeline.

