#!/usr/bin/env python

"""
Generates E-Prime files for Sabrina's brilliant experimental paradigm that I 
named after this Pokemon

http://bulbapedia.bulbagarden.net/wiki/Exeggutor_%28Pok%C3%A9mon%29

You simply feed this program a single number for the number of runs per 
participant. This program must be run once for each participant in the folder
you want the stimulus files to end up in.
"""

import csv
import sys
import random
import itertools as it

def unique(seq):
    """
    Returns all unique entries in a list.
    """
    seen = set()
    seen_add = seen.add
    return [ x for x in seq if x not in seen and not seen_add(x)]


def window(seq, n=2):
    """
    Returns a sliding window of width n over data from the iterable
    s -> (s0,s1,...s[n-1]), (s1,s2,...,sn), ...                   
    """
    iteration = iter(seq)
    result = tuple(it.islice(iteration, n))
    if len(result) == n:
        yield result    
    for element in iteration:
        result = result[1:] + (element,)
        yield result

def generate_stimuli(num=3):
    """
    Generates all potential stimuli for the experimental run.
    """
    colours = ['y','b'] * num
    stimuli = unique([''.join(x) for x in list(it.permutations(colours, num))])
    return stimuli 

def create_jitter(n_jitter, n_blocks, n_trials, n_row):
    """
    Creates a list of jitter or no jitter conditions, a test 
    vector to determine whether the jitter clusters together.

    n_jitter = total number of jitter TRs
    n_blocks = total number of blocks
    n_trials = total number of trials / block
    n_row = number of possible jitters in a row
    """
    jitter_on = [1]*n_jitter
    jitter_list = [0]*(n_blocks*n_trials*n_row-n_jitter)
    jitter_list.extend(jitter_on)
    random.shuffle(jitter_list)
    test = window(jitter_list, n_row+1)
    test = list(test)
    return jitter_list, test

def create_template_2(n):
    """
    Creates stimulus template for the control and two-back conditions.
    """
    stim_list = []
    template_0 = [0]*(n/2)
    template_1 = [1]*(n/2)
    template_0.extend(template_1)
    random.shuffle(template_0)
    template = list(template_0)
    return template

def create_template_3(n):
    """
    Creates stimulus template for the inhibit conditions.
    """
    stim_list = []
    template_0 = [0]*(n/3)
    template_1 = [1]*(n/3)
    template_2 = [2]*(n/3)
    template = list(template_0)
    template.extend(template_1)
    template.extend(template_2)
    random.shuffle(template)
    template = list(template)
    return template

def generate_block_names():
    # define block names
    control_names = ['Control1', 'Control2', 'Control3']
    inhibit_names = ['Inhibition1', 'Inhibition2', 'Inhibition3']
    twoback_names = ['Updating1', 'Updating2', 'Updating3']
    twobkin_names = ['UpInhib1', 'UpInhib2', 'UpInhib3']
    # generate random list of blocks
    block_names = list(control_names)
    block_names.extend(inhibit_names)
    block_names.extend(twoback_names)
    block_names.extend(twobkin_names)
    random.shuffle(block_names)
    test = window(block_names, 2)
    test = list(test)
    return block_names, test

def create_stimulus_order():
    # init output dicts
    block_stimuli = {}
    block_answers = {}
    block_mb = {}
    block_update = {}
    block_inhibit = {}

    # define block names
    control_names = ['Control1', 'Control2', 'Control3']
    inhibit_names = ['Inhibition1', 'Inhibition2', 'Inhibition3']
    twoback_names = ['Updating1', 'Updating2', 'Updating3']
    twobkin_names = ['UpInhib1', 'UpInhib2', 'UpInhib3']

    # generate the possible stimuli
    stimuli = generate_stimuli(3) # 3 = number of boxes in stimulus array

    # stimulus types: control
    control_mb = ['yby', 'ybb', 'bby', 'bbb'] # should automate this
    control_my = list(set(stimuli) - set(control_mb))

    # stimulus types: inhibit
    inhibit = ['yby', 'byy', 'yyb'] # should automate this
    inhibit_mb = list(set(control_mb) - set(inhibit))
    inhibit_my = list(set(stimuli) - set(inhibit_mb) - set(inhibit))
    inhibit_non = list(set(stimuli) - set(inhibit))

    # generate block list, ensure a switch each time
    while 1:
        block_names, test = generate_block_names()
        counter = 0
        for x in range(len(test)):
            if test[x][0][:-2] == test[x][1][:-2]:
                counter = counter + 1
        if counter == 0:
            break

    for block in block_names:
        
        stimuli_list = [] # correct stimuli
        answers_list = [] # correct answer for task
        mb_list = []      # 1 = trial contains middle blue
        twoback_list = [] # 1 = 2 trials 
        inhibit_list = []
        
        # control condition
        if any(b in block for b in control_names):
            template = create_template_2(12) # random set of n trials, 2 conditions
            for i in range(len(template)): # iterate through trials
                # if this is a yes trial
                if template[i] == 0:
                    stimuli_list.append(random.choice(control_mb))
                    answers_list.append(1)
                # if this is a no trial
                elif template[i] == 1:
                    stimuli_list.append(random.choice(control_my))
                    answers_list.append(2)

        # two back condition
        elif any(b in block for b in twoback_names):
            # ensure the first two trials are no trials (because twoback)
            while 1:
                template = create_template_2(12)
                if template[0]+template[1] >= 2:
                    break
            # start with 2 no answers at the beginning (because twoback)
            for i in range(2):
                answers_list.append(2)
            # fill in the correct stimuli and answers
            for i in range(len(template)-2):
                if template[i+2] == 0:
                    stimuli_list.append(random.choice(control_mb))
                    answers_list.append(1)
                if template[i+2] == 1:
                    stimuli_list.append(random.choice(control_my))
                    answers_list.append(2)
            # finally add on the final two stimuli
            for i in range(2):
                stimuli_list.append(random.choice(stimuli))

        # inhibit condition
        elif any(b in block for b in inhibit_names):
            template = create_template_3(12)
            for i in range(len(template)):
                if template[i] == 0:
                    stimuli_list.append(random.choice(inhibit_mb))
                    answers_list.append(1)
                elif template[i] == 1:
                    stimuli_list.append(random.choice(inhibit_my))
                    answers_list.append(2)
                elif template[i] == 2:
                    stimuli_list.append(random.choice(inhibit))
                    answers_list.append('')

        # two-back + inhibit condition
        elif any(b in block for b in twobkin_names):
            # ensure the first two trials are no trials (because twoback)
            while 1:
                template = create_template_3(12)
                if template[0] == 1 and template[1] == 1:
                    break
            # start with 2 no answers at the beginning (because twoback)
            for i in range(len(template)):
                if i < 2:
                    answers_list.append(2)
                    if template[i+2] == 0:
                        stimuli_list.append(random.choice(inhibit_mb))
                    elif template[i+2] == 1:
                        stimuli_list.append(random.choice(inhibit_my))
                    elif template[i+2] == 2:
                        stimuli_list.append(random.choice(inhibit_non))
                # fill in the correct stimuli and answers
                elif i >= 2 and i < len(template)-2:
                    if template[i] == 2 and template[i+2] == 0:
                        stimuli_list.append('yby')
                        answers_list.append('')
                    elif template[i] == 2 and template[i+2] == 1:
                        stimuli_list.append(random.choice(['yyb', 'byy']))
                        answers_list.append('')
                    elif template[i] == 2 and template[i+2] == 2:
                        stimuli_list.append(random.choice(inhibit))
                        answers_list.append('')
                    elif template[i+2] == 0:
                        stimuli_list.append(random.choice(inhibit_mb))
                        answers_list.append(template[i]+1)
                    elif template[i+2] == 1:
                        stimuli_list.append(random.choice(inhibit_my))
                        answers_list.append(template[i]+1)
                    elif template[i+2] == 2:
                        stimuli_list.append(random.choice(inhibit_non))
                        answers_list.append(template[i]+1)
                    else:
                        print str(template[i]) + ' & i+2: ' + str(template[i+2])
                # fill in the correct answers and appropriate stimuli
                elif i >= len(template)-2:
                    if template[i] == 0:
                        stimuli_list.append(random.choice(inhibit_non))
                        answers_list.append(1)
                    elif template[i] == 1:
                        stimuli_list.append(random.choice(inhibit_non))
                        answers_list.append(2)
                    elif template[i] == 2:
                        stimuli_list.append(random.choice(inhibit))
                        answers_list.append('')

        # now fill in those pesky answers (I hate you, Sabrina :D)
        for i in range(12):
            if i <=1:
                twoback_list.append(0)
            elif any(s in stimuli_list[i-2] for s in control_mb):
                twoback_list.append(1)
            else:
                twoback_list.append(0)
            if any(s in stimuli_list[i] for s in control_mb):
                mb_list.append(1)
            else:
                mb_list.append(0)
            if any(s in stimuli_list[i] for s in inhibit):
                inhibit_list.append(1)
            else:
                inhibit_list.append(0)
        
        block_stimuli[block] = stimuli_list
        block_answers[block] = answers_list
        block_mb[block] = mb_list
        block_update[block] = twoback_list
        block_inhibit[block] = inhibit_list
    return block_stimuli, block_answers, block_mb, block_update, block_inhibit, block_names

def write_outputs(run):
    # grab the randomized data for a run
    block_stimuli, block_answers, block_mb, block_update, block_inhibit, block_names = create_stimulus_order()

    # generate jitters, and ensure jitters happen in chunks < 3 in a row.
    while 1:
        jitter_list, test = create_jitter(6,1,12,3)
        if all(sum(tup) == 4 for tup in test) == False:
            break

    # write out stimuli
    with open(str(run+1) + '_BlockList.txt', 'wb') as csvfile:
        out = csv.writer(csvfile, delimiter='\t')
        out.writerow(['Weight'] + 
                     ['Nested'] + 
                     ['Procedure'] + 
                     ['CueJitter1'])
        for block in block_names:
            # grab the jitters 3 at a time, and sort them
            jitter = []
            for x in range(3):
                jitter.append(jitter_list.pop())
            #jitter.sort(reverse=True)
            jitter = sum(jitter)
            # write out the parameters for a given block
            out.writerow(['1'] + 
                          [''] + 
                          [block] + 
                          [1000 + (jitter*2000)])
    csvfile.close()

    for block in block_names:
        with open(str(run+1) + '_' + block + '.txt', 'wb') as csvfile:
            out = csv.writer(csvfile, delimiter='\t')
            out.writerow(['Weight'] + 
                         ['Nested'] + 
                         ['Procedure'] + 
                         ['Stimuli'] + 
                         ['Ans'] + 
                         ['MB'] + 
                         ['Upd'] + 
                         ['Inhib'] + 
                         ['Switch'] + 
                         ['NullTrial1'])
            # generate jitters in chunks < 3 in a row.
            while 1:
                jitter_list, test = create_jitter(6,1,12,3)
                if all(sum(tup) == 4 for tup in test) == False:
                    break
            for i, stim in enumerate(block_stimuli[block]):
                # is this a switch trial?
                if i == 0:
                    switch = 1
                else:
                    switch = 0
                # grab the jitters 3 at a time, and sort them
                jitter = []
                for x in range(3):
                    jitter.append(jitter_list.pop())
                #jitter.sort(reverse=True)
                jitter = sum(jitter)

                # rename the blocks --> subprocesses
                if block[:-1] == 'Updating':
                    subproc = 'UpdProc' + block[-1:]
                elif block[:-1] == 'Control':
                    subproc = 'ContProc' + block[-1:]
                elif block[:-1] == 'Inhibition':
                    subproc = 'InhibProc' + block[-1:]
                elif block[:-1] == 'UpInhib':
                    subproc = 'UpInhibProc' + block[-1:]

                # write out the information
                out.writerow(['1']  + 
                             [''] + 
                             [subproc] + 
                             [stim + '.bmp'] + 
                             [str(block_answers[block][i])] + 
                             [str(block_mb[block][i])] + 
                             [str(block_update[block][i])] + 
                             [str(block_inhibit[block][i])] + 
                             [str(switch)] + 
                             [1500 + (jitter*2000)])
        csvfile.close()

def init(num_runs=4):
    # loop through runs, writing outputs
    for run in range(num_runs):
        write_outputs(run)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Using default number of runs (4).')
        init()
    elif len(sys.argv) == 2:
        print('Using ' + str(sys.argv[1]) + ' number of runs.')
        init(int(sys.argv[1]))
    else:
        print('Gave me too many inputs! I only need 1 (the number of runs)')