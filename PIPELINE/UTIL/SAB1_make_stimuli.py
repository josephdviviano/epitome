import numpy as np
import scipy as sp
import itertools as it
import random

def unique(seq):
    """
    Returns all unique enteries in a list.
    """
    seen = set()
    seen_add = seen.add
    return [ x for x in seq if x not in seen and not seen_add(x)]

def generate_stimuli(num=3):
    """
    Generates all potential stimuli for the experimental run.
    """
    colours = ['y','b'] * num
    stimuli = unique([''.join(x) for x in list(it.permutations(colours, num))])
    return stimuli 

def window(seq, n=2):
    """
    Returns a sliding window of width n over data from the iterable"
    s -> (s0,s1,...s[n-1]), (s1,s2,...,sn), ...                   
    """
    iteration = iter(seq)
    result = tuple(it.islice(iteration, n))
    if len(result) == n:
        yield result    
    for element in iteration:
        result = result[1:] + (element,)
        yield result

def create_jitter(n_jitter, n_blocks, n_trials):
    """
    Creates a list of jitter or no jitter conditions, a test 
    vector to determine whether the jitter clusters together.
    """
    jitter_on = [1]*n_jitter
    jitter_list = [0]*(n_blocks*n_trials-n_jitter)
    jitter_list.extend(jitter_on)
    random.shuffle(jitter_list)
    test = window(jitter_list, 4)
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

#def main():
# generate output dicts
block_stimuli = {}
block_answers = {}

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

# define block names
control_list = ['control_1', 'control_2', 'control_3', 'control_4']
inhibit_list = ['inhibit_1', 'inhibit_2', 'inhibit_3', 'inhibit_4']
twoback_list = ['twoback_1', 'twoback_2', 'twoback_3', 'twoback_4']
twobkin_list = ['twobkin_1', 'twobkin_2', 'twobkin_3', 'twobkin_4']

# generate random list of blocks
block_list = list(control_list)
block_list.extend(inhibit_list)
block_list.extend(twoback_list)
block_list.extend(twobkin_list)
random.shuffle(block_list)

# generate jitter lists
while 1:
    jitter_trials, test = create_jitter(6,11,12)
    if all(sum(tup) == 4 for tup in test) == False: # ensure <= 3 in a row
        break

while 1:
    jitter_switch, test = create_jitter(6,1,12)
    if all(sum(tup) == 4 for tup in test) == False:  # ensure <= 3 in a row
        break

# generate the simuli
for block in block_list:
    
    # control condition
    if any(b in block for b in control_list):
        stimuli_list = [] # init stimuli
        answers_list = [] # init answers
        template = create_template_2(12) # random set of n trials, 2 conditions
        for i in range(len(template)): # iterate through trials
            if template[i] == 0: # yes tial
                stimuli_list.append(random.choice(control_mb)) # add stimulus
                answers_list.append(1) # 'yes'
            elif template[i] == 1: # no trial
                stimuli_list.append(random.choice(control_my)) # add stimulus
                answers_list.append(2) # 'no'
        block_stimuli[block] = stimuli_list # add generated stimulus to dict
        block_answers[block] = answers_list # add generated answers to dict

    # two back condition
    elif any(b in block for b in twoback_list):
        stimuli_list = [] # init stimuli
        answers_list = [] # init answers
        # ensure the first two trials are no trials (because twoback)
        while 1:
            template = create_template_2(12)
            if template[0]+template[1] >= 2:
                break
        # start with 2 no answers at the beginning (because twoback)
        for i in range(2):
            answers_list.append(2) # 'no'
        # fill in the correct stimuli and answers
        for i in range(len(template)-2):
            if template[i+2] == 0: # yes trial
                stimuli_list.append(random.choice(control_mb)) # add stimulus
                answers_list.append(1) # 'yes'
            if template[i+2] == 1: # no trial
                stimuli_list.append(random.choice(control_my)) # add stimulus
                answers_list.append(2) # 'no'
        # finally add on the final two stimuli
        for i in range(2):
            stimuli_list.append(random.choice(stimuli))
        block_stimuli[block] = stimuli_list # add generated stimulus to dict
        block_answers[block] = answers_list # add generated answers to dict

    # inhibit condition
    elif any(b in block for b in inhibit_list):
        stimuli_list = [] # init stimuli
        answers_list = [] # init answers
        template = create_template_3(12) # random set of n trials, 3 conditions
        for i in range(len(template)): # iterate through trials
            if template[i] == 0: # yes tial
                stimuli_list.append(random.choice(inhibit_mb)) # add stimulus
                answers_list.append(1) # 'yes'
            elif template[i] == 1: # no trial
                stimuli_list.append(random.choice(inhibit_my)) # add stimulus
                answers_list.append(2) # 'no'
            elif template[i] == 2: # inhibit trial
                stimuli_list.append(random.choice(inhibit)) # add stimulus
                answers_list.append('') # 'inhibit response'
        block_stimuli[block] = stimuli_list # add generated stimulus to dict
        block_answers[block] = answers_list # add generated answers to dict

    # two-back + inhibit condition
    elif any(b in block for b in twobkin_list):
        stimuli_list = [] # init stimuli
        answers_list = [] # init answers
        # ensure the first two trials are no trials (because twoback)
        while 1:
            template = create_template_3(12)
            if template[0] == 1 and template[1] == 1:
                break
        # start with 2 no answers at the beginning (because twoback)
        for i in range(12):
            if i < 2:
                answers_list.append(2) # 'no'
                if template[i+2] == 0:
                    stimuli_list.append(random.choice(inhibit_mb))
                elif template[i+2] == 1:
                    stimuli_list.append(random.choice(inhibit_my))
                elif template[i+2] == 2:
                    stimuli_list.append(random.choice(inhibit_non))
            elif i >= 2 and i < 10:
                if template[i] == 2 and template[i+2] == 0:
                    stimuli_list.append('yby')
                    answers_list.append('')
                elif template[i] == 2 and template[i+2] == 1:
                    stimuli_list.append(random.choice(['yyb', 'byy']))
                    answers_list.append('')
                elif template[i] == 2 and template[i+2] == 2: # no trial
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
            elif i >= 10:
                if template[i] == 0:
                    stimuli_list.append(random.choice(inhibit_non))
                    answers_list.append(1)
                elif template[i] == 1:
                    stimuli_list.append(random.choice(inhibit_non))
                    answers_list.append(2)
                elif template[i] == 2:
                    stimuli_list.append(random.choice(inhibit))
                    answers_list.append('')
        block_stimuli[block] = stimuli_list # add generated stimulus to dict
        block_answers[block] = answers_list # add generated answers to dict
