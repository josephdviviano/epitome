![epitome -- an MRI metapipeline](assets/logo.png "epitome -- a MRI metapipeline and analysis suite")

epitome is a MRI pipeline for generating pipelines out of BASH 'modules'. It is intended to produce highly-portable BASH analysis scripts out of small code chunks that non-programmers can contribute, while exposing the underbelly of the system for more experienced programmers to work on.

epitome is also a package of tools for conducting network analysis (and other types analysis) on fMRI data. These features are intended to eventually play nicely with [NetworkX](https://networkx.github.io/) and replicate at least the base functionality of the [BCT (brain connectivity toolbox)](https://sites.google.com/site/bctnet/) in the Python environment.

Written by Joseph D. Viviano and Erin W Dickie, 2014-16.

> As long as our brain is a mystery, the universe, the reflection of the structure of the brain will also be a mystery.
> -- Santiago Ramón y Cajal

*Current under active development at the TIGRLab (CAMH), and is regularly updated with modules to meet the demands of this site.*

**Shortcuts:**

+ [Setup](#setup)
+ [Introduction](#introduction)
+ [Dependencies](#dependencies)
+ [Bundled Files](#bundled-files)
+ [Overview](#overview)
+ [Usage](#usage)
+ [Modules](#modules)
+ [Workflows](#workflows)
+ [Writing Modules](#writing-modules)

Setup
-----
epitome does not have any direct dependencies, but the scripts it generates rely heavily on well-developed MRI pacakges. The more esoteric packages come bundled with this code, and some custom analysis packages are bundled with epitome under bin/

Quickstart:

+ `git clone` this repository to a directory of your choosing.
+ Create an MRI data directory somewhere.
+ Add some MRI data to your data directory.
+ Add epitome/bin to your PATH.
+ Add epitome to your PYTHONPATH.
+ Set `EPITOME_DATA` to point to your MRI data folder.
+ Set `EPITOME_CLONE` to point to a directoy that will contain copies of epitome.
+ Set `SUBJECTS_DIR` to point to the desired freesurfer subjects folder.
+ Check your work using `epitome check`.
+ Create an experiment and some subjects using `epi-folder`.
+ Put some NIFTI data into these subject's RUN folders.
+ Check your work using `epitome verify <experiment>`
+ Generate some pre-processing scripts using `epitome run`.

If you want to run use Human Connectome Project (HCP) Tools, there are some additional steps:
+ Set `HCP_DATA` to point to a directory that will hold data in the HCP folder structure

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

+ [Grid Engine: epi-queue](http://gridscheduler.sourceforge.net/) or [PBS](http://www.adaptivecomputing.com/products/open-source/torque/)
+ [FSL FIX 1.61: ica_fix](http://fsl.fmrib.ox.ac.uk/fsl/fslwiki/FIX)
+ [Bioread 0.9.3: epi-physio](https://pypi.python.org/pypi/bioread/0.9.3)
+ [gradunwarp: unwarp](https://github.com/Washington-University/gradunwarp)
+ [Connectome Workbench](http://www.humanconnectome.org/software/connectome-workbench.html) if running in "HCP mode"
+ [HCP Pipeline Scripts and Atlases](http://www.humanconnectome.org/documentation/HCP-pipelines/index.html) if running in "HCP mode"

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

Usage
-----
epitome contains a set of helper subroutines and two main functions: `run' and `clean'. Typing epitome into your command line after installation should show each function and a brief description of each, so I won't reiterate that here. I will mention that `epitome check <experiment>` allows you to check the total number of raw NIFTIs in the `RUN` folders of each image modality. This allows you to quickly find empty `RUN` folders, and ensure you have properly imported all of your data.

**epitome run**

This walks you through the construction of a pipeline for a single image modality within a single experiment. Every run of epitome begins with a run of Freesurfer on all T1s, and `init_epi`, which does the most basic kinds of MRI pre-processing. Following that, you are free to chain together modules as you see fit.

Each pipeline is generated from a local copy of the epitome repo in the `EPITOME_CLONE` directory (if undefined, this will be `~/epitome`). This is to prevent software updates from interfering with any ongoing project. This also means you can make local hacks to a copy of the pipeline and not disturb your other projects, or other users. Ideally, some of these hacks will end up being integrated back into the main branch of epitome. Before each run of the pipeline, you will be required to pick between an old branch of the pipeline (so try to name them reasonably), or `***NEW***`, which will work from a copy of the master epitome repo.

IMPORTANT for cluster users: the `EPITOME_CLONE` folder should be available to every node of the queue that will be used to process your data, otherwise certian calls made by the `cmd` scripts will fail.

In order to retain the modular and easily-customized structure of epitome, this program allows you to shoot yourself in the foot. In fact, if you aren't clear on what to do, you are more likely to make a malformed pipeline than you are to making a good one. Therefore, I recommend reading the Pipeline section of this manual at least once, and perhaps skimming the Presets section following, to get a sense of reasonable usage.

The pipeline will allow you to chain together various modules in order until you give it the stop command, when it will switch over to asking you to submit a set of desired QC outputs. Internally, this program is simply looking through the `epitome/modules/qc` directory instead of `epitome/modules/pre`. These QC outputs will only properly work once all of your subjects are pre-processed, as they output single PDFs detailing some feature of the entire experiment.

Finally, a few outputs will be deposited in your experiment directory: a `master` script, a `proclist` script, and a set of `cmd` scripts. A copy of all the current modules at the time of running will be deposited in an epitome directory in your home folder. The master script generates everything else from these copied modules, and can be edited by-hand to produce new pipelines. In fact, those who know what they are doing can generate new pipelines directly from an old master script, instead of interacting with the command line interface again. The cmd scripts are the actual set of commands run on each participant. These are essentially the module script files concatenated in the way defined by the user with the appropriate variables filled in. These files are meant to be well-commented, and should be easily edited by-hand for those adventurous types who would like to tweak various settings, try new methods, or debug beguiling problems, on a subject-wise basis. Alternatively, the modules in your home folder can be edited, the master script re-run, and the changes will be applied to every subject's cmd script. The proclist is simply a set of calls to these various scripts in order. It can be called directly, to run the subjects serially, or submitted to a batch queuing system to be analyzed in a cluster environment.

epitome scripts are written to never re-do done work. Therefore, to replace a bad set of outputs with good ones, one must first delete the bad outputs. This can be done by hand, or via a set of helper cleanup scripts, detailed below.

**epitome clean**

Produces scripts for deleting files from subject's `SESS` folders. Generally, it is good practice to inspect the outputs of epitome first, and if problems are identified, to work backwards through the pipeline until the problem arises to determine the origin of the issue. After the outputs have been vetted, use these cleanup scripts to remove unnessicary files.

**epitome help**

Prints the help for the selected module (stored as markdown files in `doc/`).

**epi-folder**

This simple tool will help you generate folders properly-formatted for epitome. It is run on a per-subject basis, but a clever user could manually duplicate a single folder structure for as many participants as needed. These folders will automatically be generated in the designated working directory.

**epi-physio**

epitome will automatically regress physiological noise out of your data, if you place it (appropriately named) in each RUN folder. The BioPak system outputs a single giant set of physiological data for the entirety of an MRI session. This program will take in this single file and split it into a set of heart rate and respiration time series for each run. These output files are placed in your current working directory and will need to be sorted manually.

**epi-queue**

epitome eventually generates a `proclist`, a set of commands that must be executed in order to generate the desired outputs. This proclist can be run manually, if desired, but can also be submitted to the sun-grid queuing system by using epi-queue. This is generally preferred, as multiple users attempting to run proclists simultaneously might overload the system.

**everything else**

For the usage of all other epitome command-line tools, run the appropriate program with the `--help` flag (e.g., `epi-fft --help`).


Modules
-------
Modules can be easily chained together manually, or by using the command-line interface included with the pipeline. New modules are simply bash scripts which call various programs, including FSL, Freesurfer, AFNI, and custom python program. Any script found in the modules directories will be added to the command line interface automatically, but will not work properly unless a matching python wrappper function is added to `epitome/commands`.

**freesurfer**

Right now, freesurfer's `recon-all` is run on every participant before further processing. This is to produce surface files that can be used for cortical smoothing / data visualization, and the automatic generation of tissue masks which can be used for the generation of nuisance regressors.

**hcp**
After running, freesurfer's `recon-all` on every participant. The hcpexport module will convert the outputs of freesurfer into a the nifti (for volume) and gifti (for surface) files organized into the folder structure of the Human Connectome Project. This directory structure is useful if using later hcp tools analyze your functional data or other data modalities (i.e. cortical thickness). This step also converts freesurfer derived masks into a format that is easier for epitome to use (nifti format) and does a non-linear (FSL based) registration of all these files into MNI space. These useful files get copied into the T1 directory so that epiotome can use them.

**pre-processing**

This contains the lion's share of the pipeline. Every run of epitome begins with `init_epi`, which contains a non-contentious set of pre-processing steps for EPI images. The following stages can be chained together at will to preform de-noising, spatial transformations, projections to surface-space, and spatial smoothing.

**quality control**

These programs run experiment-wide, and therefore are run after all /pre modules have completed for every subject. They produce reports that give a broad overview of the data quality at different stages of pre-processing, encouraging visual inspection of the data and hopefully reducing the amount of time spent hunting for the source of bugs when they do arise.

**cleanup**

These programs are run separately using epitome clean. They generally provide the ability to eliminate faulty outputs or intermediate files from experiments. Due to their destructive nature, these scripts must be executed by hand and each step must be manually confirmed. They are therefore not amiable to unattended scripting, although one could easily write their own with some know-how.

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

**python wrapper**

With modules written, an advanced user could write a master BASH script by hand to make use of it. However, most users will want to make use of the python-based command line interface, which will require you to write a small wrapper function: `.../epitome/commands/foo.py`.

Each function should have the same name as the associated module and wrapper function, and accept a single variable input_name. This denotes the filename prefix that the module will operate on.

Next, you should define the output prefix (e.g., lowpass). This will be passed on to the next module, assuming the user does not make any errors inputing the various module options.

Finally, the function should ask the user a single question for each command-line argument. I have built 4 `selector` functions for integers, floats, lists, and dictionaries. These final two allow the user to select from a set of options, with or without an accompanying description. The first two allow the use to input a numerical value for appropriate settings, for example, smoothing kernel size in millimeters.

This set of questions should be wrapped in a try-except loop, checking for `ValueErrors`. If the user inputs an inappropriate option, the function will throw an error and return the special type `None`, which will prompt epitome to ignore the current call to the function and ask the user to try again. If all is well, the collected variables should be passed to the line variable, which contains a BASH formatted string that will be printed to the master script.

The following is a code block demonstrating this structure (based on `epitome/commands/surfsmooth.py`):

    import epitome as epi

    def surfsmooth(input_name):
        output = 'smooth'
        print('\nSmoothing functional data on a cortical surface.')

        # have the user input one floating-point number, and error out if the user makes a mistake
        try:
            print('\nInput smoothing kernel FWHM (mm):')
            fwhm = epi.utils.selector_float()
        except ValueError as ve:
            return '', None

        # return a single line for the master script with the appropriate command-line arguments set
        line = '. ${DIR_PIPE/epitome/modules/pre/surfsmooth {} {}'.format(input_name, fwhm)
        return line, output

**documentation**

This is a very important part of module-building. Documentation for a given module is supplied in the doc/ folder, in a markdown document sharing the name of the module itself. This will be viewable on both GitHub, any future web-hosted manual location, and will also be used to generate the command-line help. Remember -- epitome modules should always be useful to advanced users who simply want to write their own master BASH script, and therefore, the documentation should contain enough information so that they can perform this task manually. Hopefully the current set of documentation is a sufficient guide for future development.
