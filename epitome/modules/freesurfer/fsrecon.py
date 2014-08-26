#!/usr/bin/env python

import os, sys
import fnmatch
import subprocess

import epitome as epi

def check_if_exists(root, expt, subj, sess):
    """
    Checks if a freesurfer directory already exists, returns truth.
    """
    if os.path.isdir(os.path.join(
        str(root) + '/FREESURFER/SUBJECTS', 
        str(expt) + '_' + str(subj) + '_' + str(sess))) == False:
        return False

    else:
        return True

def generate_stack(root, expt):
    """
    Returns a stack of freesurfer recon-all commands to run, with great 
    uglyness.
    """
    stack = []

    # get subject numbers
    subjects = epi.utilities.get_subj(os.path.join(root, expt))

    # loop through all subjects
    for subj in subjects:
        path = os.path.join(root, expt, subj, 'T1')

        for sess in os.listdir(path):
            if os.path.isdir(os.path.join(path, sess)) == True:
                if check_if_exists(root, expt, subj, sess) == False:
                    
                    cmd = ('recon-all -all -notal-check -cw256 -subjid ' + 
                            str(expt) + '_' + str(subj) + '_' + str(sess))
                    
                    for run in os.listdir(os.path.join(path, sess)):
                        if os.path.isdir(os.path.join(path, sess, run)) == True:
                            for filename in os.listdir(os.path.join(path, sess, run)):
                                
                                # add all available filename files to the inputs
                                if filename.endswith(".nii") == True or filename.endswith(".nii.gz") == True:
                                    cmd = cmd + ' -i ' + os.path.join(path, sess, run, filename)

                    # add the qcache flag (for cortical thickness analysis)
                    cmd = cmd + ' -qcache'
                    
                    # create a list of cmds
                    stack.append(cmd)
                else:
                    pass
    
    return stack

def FS_recon(root, expt, mode, proc):

    stack = generate_stack(root, expt)

    # This would per
    # # run multiple instances of Freesurfer in parallel
    # processes = set()
    # for cmd in stack:
    #     processes.add(subprocess.Popen(cmd, shell=True))
    #     if len(processes) >= core:
    #         os.wait()
    #         processes.difference_update(
    #             p for p in processes if p.poll() is not None)

    # #Check if all the child processes were closed
    # for p in processes:
    #     if p.poll() is None:
    #         p.wait();

    f = open(proc, 'wb')

    for cmd in stack:
        f.write(str(cmd) + '\n')

    f.write('\n')
    f.close()

if __name__ == "__main__":
    # check input types
    root = str(sys.argv[1])
    expt = str(sys.argv[2])
    mode = str(sys.argv[3])
    proc = str(sys.argv[4])

    # submit arguments to the program
    FS_recon(root, expt, mode, proc)
