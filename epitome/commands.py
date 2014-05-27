#!/usr/bin/env python
"""
This contains calls to each module that are referenced by the command-line-
interface. Each produces a single line of text printed to the master
shell script reference passed in each call.
"""

def invalid_selection():
    print('Invalid selection.')
    return None, None

def selector_int(output):
    # have the user enter a number
    option = raw_input('#: ')

    # ensure response is non-negative
    if int(option) >= 0:
        response = int(option)
    else:
        response, output = invalid_selection()

    return response, output

def selector_list(item_list, output):

    if type(item_list) != list:
        raise TypeError('Input must be a list!')

    # sort the input list
    item_list.sort()

    # print the options, and their numbers
    for i, item in enumerate(item_list):
        print(str(i+1) +': ' + str(item))

    # retrieve the option number
    option = raw_input('option #: ')

    # test the response, response & output = Null if the user makes an error
    try:
        response = item_list[int(option)-1]
    except:
        response, output = invalid_selection()
    if int(option) == 0:
        response, output = invalid_selection()

    return response, output

def selector_dict(item_dict, output):
    
    if type(item_dict) != dict:
        raise TypeError('Input must be a dict!')

    # init list where we store / find the responses
    item_list = []
    
    # generate a sorted list of dict keys
    for item in item_dict:
        item_list.append(item)
    item_list.sort()

    # loop through sorted list
    for i, item in enumerate(item_list):
        print(str(i+1) + ': ' + item + ' ' + item_dict[item])
    
    # retrieve the option number
    option = raw_input('option #: ')

    # test the response, response & output = Null if the user makes an error
    try:
        response = item_list[int(option)-1]
    except:
        response, output = invalid_selection()
    if int(option) == 0: 
        response, output = invalid_selection()

    return response, output

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
    quality, output = selector_list(data_quality, output)

    # get the number of TRs to delete
    print('')
    print('Number of TRs to delete:')
    deltr, output = selector_int(output)

    # get the slice timing
    print('')
    print('Slice-timing pattern: (see AFNI 3dTshift for more help)')
    t_patterns = {'alt+z' : '= alternating in the plus direction', 
                  'alt+z2' : '= alternating, starting at slice #1', 
                  'alt-z' : '= alternating in the minus direction', 
                  'alt-z2' : '= alternating, starting at slice #nz-2', 
                  'seq+z' : '= sequential in the plus direction',
                  'seq-z' : '= sequential in the minus direction'}
    slice_timing, output = selector_dict(t_patterns, output)

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

    import copy

    # init our output variable, which will be returned unharmed if we don't 
    # make any mistakes
    output = copy.copy(input_name)

    # give us some feedback
    print('')
    print('Calculating linear registration pathways.')
    print('')

    # get the data-quality option
    print('Select data quality:')
    data_quality = ['low', 'high']
    quality, output = selector_list(data_quality, output)

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
    cost, output = selector_dict(cost_fxns, output)

    # get registration degrees of freedom
    print('')
    print('Registration degrees of freedom: (see AFNI 3dTshift for help)')
    degrees_of_freedom = ['big_move', 'giant_move']
    reg_dof, output = selector_list(degrees_of_freedom, output)

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

    # did not operate directly on the functional data, so return orig. output
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
