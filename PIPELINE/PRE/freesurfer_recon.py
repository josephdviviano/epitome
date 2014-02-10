#!/usr/bin/env python

import subprocess
import os
import fnmatch
import ypp_inputs

oDir, oExp, oSub, oType, oCores = ypp_inputs.init()

stack = []
processes = set()

for subject in oSub:
    directory = os.path.join(oDir, oExp, subject, 'T1')

    for session in os.listdir(directory):
        if os.path.isdir(os.path.join(directory, session)) == True:
            command = 'recon-all -all -notal-check -cw256 -subjid ' + str(oExp) + '_' + str(subject) + '_' + str(session)
            for run in os.listdir(os.path.join(directory, session)):
                if os.path.isdir(os.path.join(directory, session, run)) == True:
                    for filename in os.listdir(os.path.join(directory, session, run)):
                        # add all available filename files to the inputs
                        if filename.endswith(".nii") == True or filename.endswith(".nii.gz") == True:
                            command = command + ' -i ' + os.path.join(directory, session, run, filename)

                # add the qcache flag (for cortical thickness analysis)
                command = command + ' -qcache'
                # create a list of commands
                stack.append(command)
    
# run multiple instances of Freesurfer in parallel
for cmd in stack:
    processes.add(subprocess.Popen(cmd, shell=True))
    if len(processes) >= oCores:
        os.wait()
        processes.difference_update(
            p for p in processes if p.poll() is not None)

#Check if all the child processes were closed
for p in processes:
    if p.poll() is None:
        p.wait();

# JDV Jan 15 2014