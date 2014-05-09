#!/usr/bin/env python

import subprocess
import os
import fnmatch
import ypp_utilities

def FS_recon(root, expt, mode, core):

    # get subject numbers
    subjects = ypp_utilities.get_subj(os.path.join(root, expt))
    
    # init commandstack and multiprocessing capability
    stack = []
    processes = set()

    # loop through all subjects
    for subj in subjects:
        path = os.path.join(root, expt, subj, 'T1')

        for sess in os.listdir(path):
            if os.path.isdir(os.path.join(path, sess)) == True:
                if os.path.isdir(os.path.join(str(root) + '/FREESURFER/SUBJECTS', str(expt) + '_' + str(subj) + '_' + str(sess))) == False:
                    command = 'recon-all -all -notal-check -cw256 -subjid ' + str(expt) + '_' + str(subj) + '_' + str(sess)
                    for run in os.listdir(os.path.join(path, sess)):
                        if os.path.isdir(os.path.join(path, sess, run)) == True:
                            for filename in os.listdir(os.path.join(path, sess, run)):
                                # add all available filename files to the inputs
                                if filename.endswith(".nii") == True or filename.endswith(".nii.gz") == True:
                                    command = command + ' -i ' + os.path.join(path, sess, run, filename)

                    # add the qcache flag (for cortical thickness analysis)
                    command = command + ' -qcache'
                    # create a list of commands
                    stack.append(command)
                else:
                    pass

    # run multiple instances of Freesurfer in parallel
    for cmd in stack:
        processes.add(subprocess.Popen(cmd, shell=True))
        if len(processes) >= core:
            os.wait()
            processes.difference_update(
                p for p in processes if p.poll() is not None)

    #Check if all the child processes were closed
    for p in processes:
        if p.poll() is None:
            p.wait();

if __name__ == "__main__":
    FS_recon(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
