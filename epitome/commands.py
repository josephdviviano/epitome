#!/usr/bin/env python
"""
This contains calls to each module that are referenced by the command-line-
interface. Each produces a single line of text printed to the master
shell script reference passed in each call.
"""

def invalid_selection():
    print('Invalid selection.')
    return None

def filter(input_name):
    print('')
    print('Adding filter module')

    return line, output
def gen_gcor(input_name):
    return line, output

def init_EPI():
    
    # init our output variable
    output = ''

    # give us some feedback
    print('')
    print('Initializing functional MRI pre-processing.')
    print('')

    # get the data-quality option
    print('Select data quality:')
    data_quality = ['low', 'high']
    for i, qual in enumerate(data_quality):
        print(str(i+1) +': ') + str(qual)
    response = input('option #: ')

    # test the response
    try:
        quality = data_quality[int(response-1)]
    except:
        output = invalid_selection()
    if response == 0:
        output = invalid_selection()

    # get the number of TRs to delete
    print('')
    print('Number of TRs to delete:')
    response = input('delete TRs: ')

    # test the response
    if int(response) >= 0:
        deltr = int(response)
    else:
        output = invalid_selection()

    # get the slice timing
    print('')
    print('Slice-timing pattern: (see AFNI 3dTshift for more help)')
    t_patterns = {'alt+z' : '= alternating in the plus direction', 
                  'alt+z2' : '= alternating, starting at slice #1', 
                  'alt-z' : '= alternating in the minus direction', 
                  'alt-z2' : '= alternating, starting at slice #nz-2', 
                  'seq+z' : '= sequential in the plus direction',
                  'seq-z' : '= sequential in the minus direction'}

    i = 0
    pattern_list = []
    for pattern in t_patterns:
        pattern_list.append(pattern)
        print(str(i+1) + ': ' + pattern + ' ' + t_patterns[pattern])
        i = i + 1 # iterate
    response = input('option #: ')

    # test the response
    try:
        slice_timing = pattern_list[int(response-1)]
    except:
        output = invalid_selection()
    if response == 0: 
        output = invalid_selection()

    # if we messed any of these up, we return None
    if output == None:
        print('Please try again')
        line = ''
    # otherwise we print the command and return it
    else:
        line = ('. ${DIR_PIPE}/epitome/modules/pre/init_EPI ' +
                                          str(quality) + ' ' +
                                          str(deltr) + ' ' +
                                          str(slice_timing))
        output = 'scaled'
    return line, output

def linreg_EPI2MNI_AFNI(input_name):
    return line, output
def linreg_EPI2MNI_FSL(input_name):
    return line, output
def linreg_FS2EPI_AFNI(input_name):
    return line, output
def linreg_FS2EPI_FSL(input_name):
    return line, output
def linreg_FS2MNI_FSL(input_name):
    return line, output
def linreg_FS2MNI_FSL(input_name):
    return line, output
def linreg_calc_AFNI(input_name):

    # init our output variable, which will be returned unharmed if we don't 
    # make any mistakes
    output = input_name

    # give us some feedback
    print('')
    print('Calculating linear registration pathways.')
    print('')

    # get the data-quality option
    print('Select data quality:')
    data_quality = ['low', 'high']
    for i, qual in enumerate(data_quality):
        print(str(i+1) + ': ' + str(qual)
    response = input('option #: ')

    # test the response
    try:
        quality = data_quality[int(response-1)]
    except:
        output = invalid_selection()
    if response == 0:
        output = invalid_selection()

    # set the cost function option
    print('')
    print('Registration cost function: (see AFNI align_EPI_anat.py for help)')
    cost_fxns = {'ls' : '= Least Squares [Pearson Correlation]', 
                 'mi' : '= Mutual Information [H(b)+H(s)-H(b,s)]', 
                 'crM' : '= Correlation Ratio (Symmetrized*)', 
                 'nmi' : '= Normalized MI [H(b,s)/(H(b)+H(s))]', 
                 'hel' : '= Hellinger metric',
                 'crA' : '= Correlation Ratio (Symmetrized+)',
                 'crU' : '= Correlation Ratio (Unsym)',
                 'sp' : '= Spearman [rank] Correlation',
                 'je' : '= Joint Entropy [H(b,s)]',
                 'lss' : '= Signed Pearson Correlation',
                 'lpc' : '= Local Pearson Correlation Signed',
                 'lpa' : '= Local Pearson Correlation Abs',
                 'lpc+' : '= Local Pearson Signed + Others',
                 'ncd' : '= Normalized Compression Distance',
                 'lpc+zz' : '= Local Pearson Correlation Signed + Magic'}
    
    i = 0
    cost_list = []
    for cost in cost_fxns:
        cost_list.append(cost)
        print(str(i+1) + ': ' + cost + ' ' + cost_fxns[cost])
        i = i + 1 # iterate

    response = input('Cost function: ')

    # test the response
    try:
        cost = cost_list[int(response-1)]
    except:
        output = invalid_selection()
    if response == 0: 
        output = invalid_selection()

    # get registration degrees of freedom
    print('')
    print('Registration degrees of freedom: (see AFNI 3dTshift for help)')
    degrees_of_freedom = ['big_move', 'giant_move']

    for i, reg_dof in enumerate(degrees_of_freedom):
        print(str(i+1) + ': ' + str(reg_dof))
    response = input('option #: ')

    # test the response
    try:
        reg_dof = degrees_of_freedom[int(response-1)]
    except:
        output = invalid_selection()
    if response == 0: 
        output = invalid_selection()

    # if we messed any of these up, we return None
    if output == None:
        print('Please try again')
        line = ''
    # otherwise we print the command and return it
    else:
        line = ('. ${DIR_PIPE}/epitome/modules/pre/linreg_calc_AFNI ' +
                                                   str(quality) + ' ' +
                                                   str(cost) + ' ' +
                                                   str(reg_dof))

    # we return the output given, because we did not operate directly on the
    # functional data
    return line, output

def linreg_calc_FSL(input_name):
    return line, output
def surf2vol(input_name):
    return line, output
def surfsmooth(input_name):
    return line, output
def TRdrop(input_name):
    return line, output
def vol2surf(input_name):
    return line, output

def del_everything():
    return line, output
def del_postmc():
    return line, output
def del_registration():
    return line, output
def del_MNI():
    return line, output

def check_masks():
    return line, output
def check_EPI2T1():
    return line, output
def check_T12MNI():
    return line, output
def check_runs():
    return line, output
def check_motionind():
    return line, output
def check_spectra():
    return line, output
