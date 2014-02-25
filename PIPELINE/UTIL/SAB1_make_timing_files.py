import itertools as it
import random
import csv
import numpy as np

def load_blocks(run):
    blocks = np.genfromtxt(str(run) + '_BlockList.txt', 
                               delimiter='\t',
                               dtype=[('Weight','i8'),
                                      ('Nested','f8'), 
                                      ('Procedure','S15'),
                                      ('Jitter1','i8'),
                                      ('Jitter2','i8'),
                                      ('Jitter3','i8')])
    blocks = blocks[1:] # strip header
    return blocks

def load_events(run, blocktype):
    events = np.genfromtxt(str(run) + '_' + str(blocktype) + '.txt',
                           delimiter='\t',
                           dtype=[('Weight','i8'),
                                  ('Nested','f8'), 
                                  ('Procedure','S15'),
                                  ('Stimuli','S15'),
                                  ('Ans','i8'),
                                  ('MB', 'i8'),
                                  ('Upd', 'i8'),
                                  ('Inhib', 'i8'),
                                  ('Switch', 'i8'),
                                  ('Jitter1','i8'),
                                  ('Jitter2','i8'),
                                  ('Jitter3','i8')])
    events = events[1:] # strip header
    return events

def write_outputs(run):

def main(num_runs=4):

    # init some name variables
    control_names = ['control_1', 'control_2', 'control_3']
    inhibit_names = ['inhibit_1', 'inhibit_2', 'inhibit_3']
    twoback_names = ['twoback_1', 'twoback_2', 'twoback_3']
    twobkin_names = ['twobkin_1', 'twobkin_2', 'twobkin_3']

    # event matricies
    events_control = np.zeros(4,36)
    events_inhibit = np.zeros(4,36)
    events_twoback = np.zeros(4,36)
    events_twobkin = np.zeros(4,36)

    # block matricies
    blocks_control = np.zeros(4,3)
    blocks_inhibit = np.zeros(4,3)
    blocks_twoback = np.zeros(4,3)
    blocks_twobkin = np.zeros(4,3)

    # loop through runs, writing outputs
    for run in range(num_runs):

        blocks = load_blocks(run+1)
        time = 0 # start the timer
        for i, block in enumerate(blocks):
            # add the cue time
            time = time + 2
            # add jitter from the cue
            jitter = (block[3] + block[4] + block[5]) / 1000 
            time = time + jitter
            # load in the events
            events = load_events(run+1, block[2])
            





        write_outputs(run)