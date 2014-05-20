#!/usr/bin/env python

"""
Generates E-Prime files, and AFNI timing files for Sabrina's brilliant 
experimental paradigm that I named after this Pokemon

http://bulbapedia.bulbagarden.net/wiki/Exeggutor_%28Pok%C3%A9mon%29

You simply feed this program a single number for the number of runs per 
participant. This program must be run once for each participant in the folder
you want the stimulus files to end up in.
"""
import os
import csv
import sys
import random
import numpy as np
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

def load_blocks(directory, run):
    filename = str(run) + '_BlockList.txt'
    blocks = np.genfromtxt(os.path.join(directory, filename),
                           delimiter='\t',
                           dtype=[('Weight', 'i8'),
                                  ('Nested', 'f8'),
                                  ('Procedure', 'S15'),
                                  ('Jitter1', 'i8')])
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
                                  ('Jitter1', 'i8')])
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
    out['events_control'] = np.zeros((runs, 33))
    out['events_inhibit'] = np.zeros((runs, 12))
    out['events_twoback'] = np.zeros((runs, 33))
    out['events_twobkin'] = np.zeros((runs, 33))
    return out

def check_directory(directory):
    if os.path.isdir(directory) == True:
        if os.path.isfile(os.path.join(directory, '1_BlockList.txt')) == True:
            return True
        else:
            return False
    else:
        return False

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
            jitter = (sum(jitter)*2000) + 1000
            # write out the parameters for a given block
            out.writerow(['1'] + 
                          [''] + 
                          [block] + 
                          [jitter])
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

def write_afni_files(directory, runs=4):
    out = make_output_dict(runs)

    if check_directory(directory) == True:
        pass
    else:
        print 'your directory is not correct :('
        #raise

    # loop through runs, writing outputs
    for run in range(runs):

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
        time = 30 # start the timer at 36s (for rest)
        for block in blocks:

            # add the cue time
            time = time + 1.0
            # add jitter from the cue
            jitter = block[3] / 1000.0
            time = time + jitter
            # load in the events
            block_type = block[2] # get the block name
            block_type = block_type[:-1] # strip the trailing number

            # save onset times
            if block_type == 'Control':
                out['blocks_control'][run, j_control] = time
                j_control = j_control + 1
            elif block_type == 'Inhibition':
                out['blocks_inhibit'][run, j_inhibit] = time
                j_inhibit = j_inhibit + 1
            elif block_type == 'Updating':
                out['blocks_twoback'][run, j_twoback] = time
                j_twoback = j_twoback + 1
            elif block_type == 'UpInhib':
                out['blocks_twobkin'][run, j_twobkin] = time
                j_twobkin = j_twobkin + 1

            # now run through the events
            events = load_events(directory, run+1, block[2])
            for event in events:
                # save onset times
                if event[8] == 1:
                    out['events_switch'][run, k_switch] = time
                    k_switch = k_switch + 1
                elif block_type == 'Inhibition' and event[4] == -1: # inhibit
                    out['events_inhibit'][run, k_inhibit] = time
                    k_inhibit = k_inhibit + 1
                elif block_type == 'Control':
                    out['events_control'][run, k_control] = time
                    k_control = k_control + 1
                elif block_type == 'Updating':
                    out['events_twoback'][run, k_twoback] = time
                    k_twoback = k_twoback + 1
                elif block_type == 'UpInhib':
                    out['events_twobkin'][run, k_twobkin] = time
                    k_twobkin = k_twobkin + 1

                # add event length to time
                time = time + 0.5

                # calculate jitter, add to time
                jitter = event[9] / 1000.0
                time = time + jitter

    # strip missing inhibit trials (must convert to strings...)
    out['events_inhibit'] = out['events_inhibit'].astype('str')

    for run in range(runs):
        for idx in [9, 10, 11]:
            if out['events_inhibit'][run][idx] == '0.0':
                out['events_inhibit'][run][idx] = ''

    # save the output files
    np.savetxt(os.path.join(directory, 'blocks_control.1D'),
               out['blocks_control'], delimiter='', fmt='%10.1f')
    np.savetxt(os.path.join(directory, 'blocks_inhibit.1D'),
               out['blocks_inhibit'], delimiter='', fmt='%10.1f')
    np.savetxt(os.path.join(directory, 'blocks_twoback.1D'),
               out['blocks_twoback'], delimiter='', fmt='%10.1f')
    np.savetxt(os.path.join(directory, 'blocks_twobkin.1D'),
               out['blocks_twobkin'], delimiter='', fmt='%10.1f')
    np.savetxt(os.path.join(directory, 'events_control.1D'),
               out['events_control'], delimiter='', fmt='%10.1f')
    np.savetxt(os.path.join(directory, 'events_inhibit.1D'),
               out['events_inhibit'], delimiter=' ', fmt='%5s')
    np.savetxt(os.path.join(directory, 'events_twoback.1D'),
               out['events_twoback'], delimiter='', fmt='%10.1f')
    np.savetxt(os.path.join(directory, 'events_twobkin.1D'),
               out['events_twobkin'], delimiter='', fmt='%10.1f')
    np.savetxt(os.path.join(directory, 'events_switch.1D'),
               out['events_switch'], delimiter='', fmt='%10.1f')

def init(directory, num_runs=4):    
    # loop through runs, writing outputs
    for run in range(num_runs):
        write_outputs(run)
    
    # and generate AFNI files
    write_afni_files(directory, num_runs)

if __name__ == "__main__":
    
    # get current directory (could become command line thing)
    directory = os.getcwd()
    
    # print very important text
    print("""                                                    
			                                                           
			"Exeggutor, go!"  

			               :::~                                         
			                  :+++~=             ~~++=                  
			                    :+??=     ::    ???                     
			           =~~~~~=    +??+:   +:  ~??+                      
			         :::::++++++:  :+++  ::  +??+       ~::::           
			                    +??++++= + :++++   :+???+               
			           ~~~~:::   ???:+~~ = :++++  :+??+                 
			       :::     ~~~~~~: +~~=~~=~~~~~ ~~~+  +?????+~~         
			                 :===~~ ~~==~=~~~~=:~~= ~~??????+++~:       
			           =+?????+++~~ :=~~:=~~~~~=~~~~~+          :+:     
			         ~???::     +~~~~:~~~~~~~~~~~~=     :               
			       ~+:      :+++++  ~~~~~~~~~~~:~~~~~~+++??~            
			      ::       :++ ++::++++:~~~~~~::  :::: ??????+=         
			             :I?????~III???++ ~~:????++       : +++:        
			                ::~?IIIII??+++~:???????:          :++:      
			                ~:~I+II~~~+?++:???+~??? 7~          ::      
			                :?7 +II7  7?++??~77+???+++                  
			                 +++IIII????+++??????++: :                  
			                       ~+ ~+++:+++++++::++                  
			                    +: +++:+++ ++++++++++?                  
			                       ++++  ~~~~ ++++?                     
			                     ~~=~~~~~~~~~~~                         
			                    ,===~~==~~~~~~~,                        
			            ~       ~=======,,,,,~~~                        
			          ~   ~:=~==~=~====~~~~~~~~,                        
			           7~~~~,=,====~===~~~~~~~,~                        
			           ???+~~~~~, ~~~~~~~~,~~~~~                        
			           +???~~~~~:  ~~~~~~,~~~~~~                        
			            ???=~~            ,,,,,~                        
			              +~            ~,~==~~~                        
			                            ~~,,~~,                         
			                             ~=====~                        
			                                   7      

            "Exeggutor used generate E-Prime stimulus files!"

            "It's super effective!"
            
	     """)
    if len(sys.argv) < 2:
        print('Using default number of runs (4).')
        init(directory)
   
    elif len(sys.argv) == 2:
        print('Using ' + str(sys.argv[1]) + ' number of runs.')
        init(directory, int(sys.argv[1]))
    
    else:
        print('Gave me too many inputs! I only need 1 (the number of runs)')
