#!/usr/bin/env python
"""
This contains calls to each module that are referenced by the command-line-
interface. Each produces a single line of text printed to the master
shell script reference passed in each call.
"""

def invalid_selection():
    print('Invalid selection.')
    return None

def filter(input):
    print('')
    print('Adding filter module')

    return line, output
def gen_gcor(input):
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

def linreg_EPI2MNI_AFNI(input):
    return line, output
def linreg_EPI2MNI_FSL(input):
    return line, output
def linreg_FS2EPI_AFNI(input):
    return line, output
def linreg_FS2EPI_FSL(input):
    return line, output
def linreg_FS2MNI_FSL(input):
    return line, output
def linreg_FS2MNI_FSL(input):
    return line, output
def linreg_calc_AFNI(input):
    return line, output
def linreg_calc_FSL(input):
    return line, output
def surf2vol(input):
    return line, output
def surfsmooth(input):
    return line, output
def TRdrop(input):
    return line, output
def vol2surf(input):
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
