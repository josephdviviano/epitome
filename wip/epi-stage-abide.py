#!/usr/bin/env python
"""
For a abide subject list, makes relevant link for epitome run

Usage:
  epi-stage-abide [options] <abide_inputdir> <epi_data_dir>

Arguments:
  <abide_inputdir>  Top directory for abide input files
  <epi_data_dir>    Top directory for the epitome project tree structure

Options:
  --fslreorient2std        Runs fslreorient2std on the input files (default is to symlink)
  --subjectlist FILE       Text file containing a list of subject
  -v,--verbose             Verbose logging
  --debug                  Debug logging in Erin's very verbose style
  -n,--dry-run             Dry run
  --help                   Print help

DETAILS
Links to the ABIDE inputs to create the file structure

Written by Erin W Dickie, Febuary 2016
"""

from epitome.docopt import docopt
import pandas as pd
import epitome as epi
import glob
import os
import sys
import subprocess
import datetime


arguments       = docopt(__doc__)
inputdir        = arguments['<abide_inputdir>']
outputdir       = arguments['<epi_data_dir>']
FSL2STD       = arguments['--fslreorient2std']
subjlistfile    = arguments['--subjectlist']
DEBUG           = arguments['--debug']
DRYRUN          = arguments['--dry-run']

if DEBUG: print arguments


### Erin's little function for running things in the shell
def docmd(cmdlist):
    "sends a command (inputed as a list) to the shell"
    if DEBUG: print ' '.join(cmdlist)
    if not DRYRUN: subprocess.call(cmdlist)

# need to find the t1 weighted scan and update the checklist
def find_and_copy_tagnii(colname,pattern):
    """
    for a particular scan type, will look for new files in the inputdir
    and copy them to the output structure
    """
    for i in range(0,len(checklist)):
    	#if link doesn't exist
        subject =  checklist['id'][i]
        site = subject.split('_')[0]
    	targetdir = os.path.join(outputdir, site, subject,colname, 'SESS01', 'RUN01')
    	if os.path.exists(targetdir)==False:
            niidir = os.path.join(inputdir,checklist['id'][i],checklist['id'][i],'scans')
    	    #if mnc name not in checklist
            if pd.isnull(checklist[colname][i]):
                niifiles = glob.glob(niidir + pattern)
                if DEBUG: print "Found {} {} in {}".format(len(niifiles),colname,niidir)
                if len(niifiles) == 1:
                    checklist[colname][i] = ';'.join(niifiles)
                elif len(niifiles) > 1:
                    checklist['notes'][i] = "> {} {} found".format(expected_count,archive_tag)
                elif len(niifiles) < 1:
                    checklist['notes'][i] = "No {} found.".format(colname)
            # make the link
            if pd.isnull(checklist[colname][i])==False:
                niifiles = checklist[colname][i].split(';')
                for niifile in niifiles:
                    niipath = os.path.abspath(os.path.join(niidir,niifile))
                    nii_base = os.path.basename(niipath)
                    targetpath = os.path.abspath(os.path.join(targetdir,nii_base))
                    docmd(['mkdir','-p',targetdir])
                    if FSL2STD:
                        docmd(['fslreorient2std', niipath, targetdir])
                    else:
                        os.symlink(niipath, targetpath)


####set checklist dataframe structure here
#because even if we do not create it - it will be needed for newsubs_df (line 80)
def loadchecklist(checklistfile,subjectlist):
    """
    Reads the checklistfile (normally called ENIGMA-DTI-checklist.csv)
    if the checklist csv file does not exit, it will be created.

    This also checks if any subjects in the subjectlist are missing from the checklist,
    (checklist.id column)
    If so, they are appended to the bottom of the dataframe.
    """

    cols = ['id', 'T1', 'RST', 'date_ran','qc_rator', 'qc_rating', 'notes']

    if DEBUG: print("cols: {}".format(cols))

    # if the checklist exists - open it, if not - create the dataframe
    if os.path.isfile(checklistfile):
    	checklist = pd.read_csv(checklistfile, sep=',', dtype=str, comment='#')
    else:
    	checklist = pd.DataFrame(columns = cols)

    # new subjects are those of the subject list that are not in checklist.id
    newsubs = list(set(subjectlist) - set(checklist.id))

    # add the new subjects to the bottom of the dataframe
    newsubs_df = pd.DataFrame(columns = cols, index = range(len(checklist),len(checklist)+len(newsubs)))
    newsubs_df.id = newsubs
    checklist = checklist.append(newsubs_df)

    # return the checklist as a pandas dataframe
    return(checklist)



######## NOW START the 'main' part of the script ##################
## make the putput directory if it doesn't exist
outputdir = os.path.abspath(outputdir)

## find those subjects in input who have not been processed yet
if subjlistfile:
    subids = pd.read_csv(subjlistfile, header=None, sep="\n")
    subids = subids[0].tolist()
else:
    subids = epi.utilities.get_subj(inputdir)

## create an checklist for the FA maps
checklistfile = os.path.normpath(outputdir+'/epitome-checklist.csv')
checklist = loadchecklist(checklistfile,subids)

## look for new subs using FA_tag and tag2
find_and_copy_tagnii('T1', '/anat/resources/NIfTI/files/mprage.nii')
find_and_copy_tagnii('RST', '/rest/resources/NIfTI/files/rest.nii')

## write the checklist out to a file
checklist.to_csv(checklistfile, sep=',', index = False)
