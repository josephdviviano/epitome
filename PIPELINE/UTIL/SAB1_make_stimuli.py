import itertools as it
import random
import csv

def unique(seq):
    """
    Returns all unique enteries in a list.
    """
    seen = set()
    seen_add = seen.add
    return [ x for x in seq if x not in seen and not seen_add(x)]


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

def generate_block_list():
    # define block names
    control_list = ['control_1', 'control_2', 'control_3']
    inhibit_list = ['inhibit_1', 'inhibit_2', 'inhibit_3']
    twoback_list = ['twoback_1', 'twoback_2', 'twoback_3']
    twobkin_list = ['twobkin_1', 'twobkin_2', 'twobkin_3']
    # generate random list of blocks
    block_list = list(control_list)
    block_list.extend(inhibit_list)
    block_list.extend(twoback_list)
    block_list.extend(twobkin_list)
    random.shuffle(block_list)
    return block_list

def create_stimulus_order():
    # init output dicts
    block_stimuli = {}
    block_answers = {}

    # define block names
    control_list = ['control_1', 'control_2', 'control_3']
    inhibit_list = ['inhibit_1', 'inhibit_2', 'inhibit_3']
    twoback_list = ['twoback_1', 'twoback_2', 'twoback_3']
    twobkin_list = ['twobkin_1', 'twobkin_2', 'twobkin_3']

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

    # generate block list
    block_list = generate_block_list()
    for block in block_list:
        
        stimuli_list = []
        answers_list = []
        
        # control condition
        if any(b in block for b in control_list):
            stimuli_list = [] # init stimuli
            answers_list = [] # init answers
            template = create_template_2(12) # random set of n trials, 2 conditions
            for i in range(len(template)): # iterate through trials
                if template[i] == 0:
                    stimuli_list.append(random.choice(control_mb))
                    answers_list.append(1)
                elif template[i] == 1:
                    stimuli_list.append(random.choice(control_my))
                    answers_list.append(2)

        # two back condition
        elif any(b in block for b in twoback_list):
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
        elif any(b in block for b in inhibit_list):
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
        elif any(b in block for b in twobkin_list):
            # ensure the first two trials are no trials (because twoback)
            while 1:
                template = create_template_3(12)
                if template[0] == 1 and template[1] == 1:
                    break
            # start with 2 no answers at the beginning (because twoback)
            for i in range(len(template)):
                if i < 2:
                    answers_list.append(2) # 'no'
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
        
        block_stimuli[block] = stimuli_list
        block_answers[block] = answers_list
    return block_stimuli, block_answers, block_list

def write_outputs(run):
    # grab the randomized data for a run
    block_stimuli, block_answers, block_list = create_stimulus_order()

    # generate jitters, and ensure jitters happen in chunks < 3 in a row.
    while 1:
        jitter_list, test = create_jitter(6,1,12,3)
        if all(sum(tup) == 4 for tup in test) == False:
            break

    # write out 
    with open(str(run+1) + '_BlockList.txt', 'wb') as csvfile:
        out = csv.writer(csvfile, delimiter='\t')
        out.writerow(['Weight'] + 
                     ['Nested'] + 
                     ['Procedure'] + 
                     ['CueJitter1'] + 
                     ['CueJitter2'] + 
                     ['CueJitter3'])
        for block in block_list:
            # grab the jitters 3 at a time, and sort them
            jitter = []
            for x in range(3):
                jitter.append(jitter_list.pop())
            jitter.sort(reverse=True)
            # write out the parameters for a given block
            out.writerow(['1'] + 
                          [''] + 
                          [block] + 
                          [jitter[0]*2000] + 
                          [jitter[1]*2000] + 
                          [jitter[2]*2000])
    csvfile.close()

    for block in block_list:
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
                         ['NullTrial1'] + 
                         ['NullTrial2'] + 
                         ['NullTrial3'])
            for x, stim in enumerate(block_stimuli[block]):
                # generate jitters in chunks < 3 in a row.
                while 1:
                    jitter_list, test = create_jitter(6,1,12,3)
                    if all(sum(tup) == 4 for tup in test) == False:
                        break
                # grab the jitters 3 at a time, and sort them
                jitter = []
                for x in range(3):
                    jitter.append(jitter_list.pop())
                jitter.sort(reverse=True)
                out.writerow(['1']  + 
                             [''] + 
                             [block] + 
                             [stim + '.bmp'] + 
                             [str(block_answers[block][x])] +
                             ['0'] +
                             ['0'] +
                             ['0'] +
                             ['0'] +
                             [jitter[0]*2000] + 
                             [jitter[1]*2000] + 
                             [jitter[2]*2000])
        csvfile.close()

def main(num_runs=4):
    # loop through runs, writing outputs
    for run in range(num_runs):
        write_outputs(run)