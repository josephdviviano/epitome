#!/usr/bin/env python

import os
import csv
import sys
import random
import numpy as np
import itertools as it

"""
Generates AFNI GLM rapid-event timing files for Sabrina's brilliant
experimental paradigm I named after this Pokemon

http://bulbapedia.bulbagarden.net/wiki/Exeggutor_%28Pok%C3%A9mon%29

This program requires you supply it with a path to the input stimulus timing
files and the number of experimental runs.
"""

def load_blocks(directory, run):
    filename = str(run) + '_BlockList.txt'
    blocks = np.genfromtxt(os.path.join(directory, filename),
                           delimiter='\t',
                           dtype=[('Weight', 'i8'),
                                  ('Nested', 'f8'),
                                  ('Procedure', 'S15'),
                                  ('Jitter1', 'i8'),
                                  ('Jitter2', 'i8'),
                                  ('Jitter3', 'i8')])
    blocks = blocks[1:] # strip header
    return blocks

def load_events(directory, run, blocktype):
    filename = str(run) + '_' + str(blocktype) + '.txt'
    events = np.genfromtxt(os.path.join(directory, filename),
                           delimiter='\t',
                           dtype=[('Weight', 'i8'),
                                  ('Nested', 'f8'), 
                                  ('Procedure', 'S15'),
                                  ('Stimuli', 'S15'),
                                  ('Ans', 'i8'),
                                  ('MB', 'i8'),
                                  ('Upd', 'i8'),
                                  ('Inhib', 'i8'),
                                  ('Switch', 'i8'),
                                  ('Jitter1', 'i8'),
                                  ('Jitter2', 'i8'),
                                  ('Jitter3', 'i8')])
    events = events[1:] # strip header
    return events

def make_output_dict(runs=4):
    # init output
    out = {}

    # block matricies
    out['blocks_control'] = np.zeros((runs, 3))
    out['blocks_inhibit'] = np.zeros((runs, 3))
    out['blocks_twoback'] = np.zeros((runs, 3))
    out['blocks_twobkin'] = np.zeros((runs, 3))

    # event matricies
    out['events_switch'] = np.zeros((runs, 12))
    out['events_control'] = np.zeros((runs, 36))
    out['events_inhibit'] = np.zeros((runs, 12))
    out['events_twoback'] = np.zeros((runs, 36))
    out['events_twobkin'] = np.zeros((runs, 36))
    return out

def check_directory(directory):
    if os.path.isdir(directory) == True:
        if os.path.isfile(os.path.join(directory, '1_BlockList.txt')) == True:
            return True
        else:
            return False
    else:
        return False

def write_afni_files(directory, runs=4):
    out = make_output_dict(runs)

    if check_directory(directory) == True:
        pass
    else:
        print 'your directory is not correct :('
        #raise

    # loop through runs, writing outputs
    for i, run in enumerate(range(runs)):

        # block indicies
        j_control = 0
        j_inhibit = 0
        j_twoback = 0
        j_twobkin = 0

        # event indicies
        k_switch = 0
        k_control = 0
        k_inhibit = 0
        k_twoback = 0
        k_twobkin = 0

        blocks = load_blocks(directory, run+1)
        time = 0 # start the timer
        for block in blocks:

            # add the cue time
            time = time + 2
            # add jitter from the cue
            jitter = (block[3] + block[4] + block[5]) / 1000
            time = time + jitter
            # load in the events
            block_type = block[2] # get the block name
            block_type = block_type[:-1] # strip the trailing number

            # save onset times
            if block_type == 'Control':
                out['blocks_control'][i, j_control] = time
                j_control = j_control + 1
            elif block_type == 'Inhibition':
                out['blocks_inhibit'][i, j_inhibit] = time
                j_inhibit = j_inhibit + 1
            elif block_type == 'Updating':
                out['blocks_twoback'][i, j_twoback] = time
                j_twoback = j_twoback + 1
            elif block_type == 'UpInhib':
                out['blocks_twobkin'][i, j_twobkin] = time
                j_twobkin = j_twobkin + 1

            # now run through the events
            events = load_events(directory, run+1, block[2])
            for event in events:
                # save onset times
                if event[8] == 1:
                    out['events_switch'][i, k_switch] = time
                    k_switch = k_switch + 1
                if block_type == 'Control':
                    out['events_control'][i, k_control] = time
                    k_control = k_control + 1
                elif block_type == 'Inhibition' and event[4] == -1: # inhibit
                    out['events_inhibit'][i, k_inhibit] = time
                    k_inhibit = k_inhibit + 1
                elif block_type == 'Updating':
                    out['events_twoback'][i, k_twoback] = time
                    k_twoback = k_twoback + 1
                elif block_type == 'UpInhib':
                    out['events_twobkin'][i, k_twobkin] = time
                    k_twobkin = k_twobkin + 1

                # add event length to time
                time = time + 2

                # calculate jitter, add to time
                jitter = (event[9] + event[10] + event[11]) / 1000
                time = time + jitter

        # save the output files
        np.savetxt(os.path.join(directory, 'blocks_control.1D'),
                   out['blocks_control'], delimiter='', fmt='%10.2f')
        np.savetxt(os.path.join(directory, 'blocks_inhibit.1D'),
                   out['blocks_inhibit'], delimiter='', fmt='%10.2f')
        np.savetxt(os.path.join(directory, 'blocks_twoback.1D'),
                   out['blocks_twoback'], delimiter='', fmt='%10.2f')
        np.savetxt(os.path.join(directory, 'blocks_twobkin.1D'),
                   out['blocks_twobkin'], delimiter='', fmt='%10.2f')
        np.savetxt(os.path.join(directory, 'events_control.1D'),
                   out['events_control'], delimiter='', fmt='%10.2f')
        np.savetxt(os.path.join(directory, 'events_inhibit.1D'),
                   out['events_inhibit'], delimiter='', fmt='%10.2f')
        np.savetxt(os.path.join(directory, 'events_twoback.1D'),
                   out['events_twoback'], delimiter='', fmt='%10.2f')
        np.savetxt(os.path.join(directory, 'events_twobkin.1D'),
                   out['events_twobkin'], delimiter='', fmt='%10.2f')
        np.savetxt(os.path.join(directory, 'events_switch.1D'),
                   out['events_switch'], delimiter='', fmt='%10.2f')

if __name__ == "__main__":
    # maybe this will also become a command-line thing, right now we 
    # only consider the present working directory
    directory = os.getcwd()
    if len(sys.argv) < 2:
        print('Dir:' + str(directory) + ', runs: 4.')
        write_afni_files(directory)
    elif len(sys.argv) == 2:
        print('Dir: ' + str(directory) + ', runs: ' + str(sys.argv[1]))
        write_afni_files(directory, sys.argv[1])
    else:
        print('Too many inputs! I only need 1 (the number of runs!)')