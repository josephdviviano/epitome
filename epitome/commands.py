#!/usr/bin/env python
"""
This contains calls to each module that are referenced by the command-line-
interface. Each produces a single line of text printed to the master
shell script reference passed in each call.
"""

def invalid_selection():
    print('Invalid selection.')
    return None, None

def selector_float(output):
    option = raw_input('#: ') # have the user enter a number

    # ensure response is non-negative
    if option == '':
        option = -1
    if float(option) >= float(0):
        response = float(option)
    else:
        response, output = invalid_selection()

    return response, output    

def selector_int(output):
    option = raw_input('#: ') # have the user enter a number

    # ensure response is non-negative
    if option == '':
        option = -1
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
    if option == '':
        option = 0
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
    if option == '':
        option = 0
    try:
        response = item_list[int(option)-1]
    except:
        response, output = invalid_selection()
    if int(option) == 0: 
        response, output = invalid_selection()

    return response, output

def filter(input_name):
    output = 'filtered'

    print('')
    print('Adding filter module.')

    print('')
    print('Set detrend order:')
    polort, output = selector_int(output)

    print('Set global signal regression:')
    gs_list = ['off', 'on']
    gs_flag, output = selector_list(gs_list, output)

    # if we messed any of these up, we return None
    if output == None:
        print('Please try again')
        line = ''
    # otherwise we print the command and return it
    else:
        line = ('. ${DIR_PIPE}/epitome/modules/pre/filter ' +
                                      str(input_name) + ' ' +
                                      str(polort) + ' ' +
                                      str(gs_flag))
    return line, output

def gen_gcor(input_name):
    import copy

    output = copy.copy(input_name) # return output unharmed
    
    print('')
    print('Adding global correlation calculation')

    line = ('. ${DIR_PIPE}/epitome/modules/pre/gen_gcor ' + str(input_name))

    return line, output

def gen_regressors(input_name):
    import copy

    output = copy.copy(input_name) # return output unharmed

    print('')
    print('Generating regressors from' + str(input_name))

    line = ('. ${DIR_PIPE}/epitome/modules/pre/gen_regressors ' +
                                                  str(input_name))

    return line, output

def init_EPI():    
    output = 'scaled'

    print('')
    print('Initializing functional MRI pre-processing.')


    # get the data-quality option
    print('')
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
    return line, output

def linreg_EPI2MNI_AFNI(input_name):
    output = 'MNI'

    # give us some feedback
    print('')
    print('Resampling input EPI data to MNI space using AFNI.')

    # get the reslice dimensions
    print('')
    print('Select target dimensions (isotropic mm):')
    dims, output = selector_float(output)

    # if we messed any of these up, we return None
    if output == None:
        print('Please try again')
        line = ''
    # otherwise we print the command and return it
    else:
        line = ('. ${DIR_PIPE}/epitome/modules/pre/linreg_EPI2MNI_AFNI ' +
                                                   str(input_name) + ' ' +
                                                   str(dims))
    return line, output

def linreg_EPI2MNI_FSL(input_name):
    output = 'MNI'

    # give us some feedback
    print('')
    print('Resampling input EPI data to MNI space using FSL.')

    # get the reslice dimensions
    print('')
    print('Select target dimensions (isotropic mm):')
    dims, output = selector_float(output)

    # if we messed any of these up, we return None
    if output == None:
        print('Please try again')
        line = ''
    # otherwise we print the command and return it
    else:
        line = ('. ${DIR_PIPE}/epitome/modules/pre/linreg_EPI2MNI_FSL ' +
                                                  str(input_name) + ' ' +
                                                  str(dims))
    return line, output

def linreg_FS2EPI_AFNI(input_name):
    import copy

    output = copy.copy(input_name) # return output unharmed

    print('')
    print('Moving Freesurfer atlases to single-subject space using AFNI.')

    line = ('. ${DIR_PIPE}/epitome/modules/pre/linreg_FS2EPI_AFNI')

    return line, output

def linreg_FS2EPI_FSL(input_name):
    import copy

    output = copy.copy(input_name) # return output unharmed

    print('')
    print('Moving Freesurfer atlases to single-subject space using FSL.')
    
    line = ('. ${DIR_PIPE}/epitome/modules/pre/linreg_FS2EPI_FSL')

    return line, output

def linreg_FS2MNI_FSL(input_name):   
    import copy

    output = copy.copy(input_name) # return output unharmed

    print('')
    print('Moving Freesurfer atlases to MNI space using FSL.')

    line = ('. ${DIR_PIPE}/epitome/modules/pre/linreg_FS2MNI_FSL')

    return line, output


def linreg_calc_AFNI(input_name):
    import copy

    output = copy.copy(input_name) # return output unharmed

    print('')
    print('Calculating linear registration pathways using AFNI.')

    # get the data-quality option
    print('')
    print('Select data quality:')
    data_quality = ['low', 'high']
    quality, output = selector_list(data_quality, output)

    # set the cost function option
    print('')
    print('Cost function: (see AFNI align_EPI_anat.py for help)')
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
    print('Degrees of freedom: (see AFNI align_EPI_anat.py for help)')
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
    return line, output

def linreg_calc_FSL(input_name):
    import copy

    output = copy.copy(input_name) # return output unharmed

    print('')
    print('Calculating linear registration pathways.')

    # get the data-quality option
    print('')
    print('Select data quality:')
    data_quality = ['low', 'high']
    quality, output = selector_list(data_quality, output)

    # set the cost function option
    print('')
    print('Registration cost function: (see FSL FLIRT for help)')
    cost_fxns = {'mutualinfo' : '= Mutual Information [H(b)+H(s)-H(b,s)]', 
                 'leastsq' : '=  Least Squares [Pearson Correlation]',
                 'corratio' : '= Correlation Ratio', 
                 'normcorr' : '= Normalized Correlation', 
                 'labeldiff' : '= FSL magic!',
                 'bbr' : '= FSL magic!'}

    cost, output = selector_dict(cost_fxns, output)

    # get registration degrees of freedom
    print('')
    print('Registration degrees of freedom: (see FSL FLIRT for help)')
    degrees_of_freedom = [6, 7, 9, 12]
    reg_dof, output = selector_list(degrees_of_freedom, output)

    # if we messed any of these up, we return None
    if output == None:
        print('Please try again')
        line = ''
    # otherwise we print the command and return it
    else:
        line = ('. ${DIR_PIPE}/epitome/modules/pre/linreg_calc_FSL ' +
                                                   str(quality) + ' ' +
                                                   str(cost) + ' ' +
                                                   str(reg_dof))
    return line, output

def surf2vol(input_name):   
    output = 'ctx'

    print('')
    print('Projecting surface data to volume space.')

    line = ('. ${DIR_PIPE}/epitome/modules/pre/surf2vol ' + str(input_name))

    return line, output

def surfsmooth(input_name):    
    output = 'smooth'

    print('')
    print('Smoothing functional data on a cortical surface.')

    print('')
    print('Input smoothing kernel FWHM (mm):')
    fwhm, output = selector_float(output)

    # if we messed any of these up, we return None
    if output == None:
        print('Please try again')
        line = ''
    # otherwise we print the command and return it
    else:
        line = ('. ${DIR_PIPE}/epitome/modules/pre/surfsmooth ' +
                                          str(input_name) + ' ' +
                                          str(fwhm))
    return line, output

def vol2surf(input_name):
    output = 'surface'

    print('')
    print('Projecting data to cortical surface.')

    line = ('. ${DIR_PIPE}/epitome/modules/pre/vol2surf ' + str(input_name))

    return line, output

def TRdrop(input_name):
    output = 'scrubbed'

    print('')
    print('Removing motion-corrupted TRs.')
    
    print('')
    print('Would you like to use the defaults?')
    print('                           Head Size = 50 mm')
    print('    Framewise Displacement Threshold = 0.3 mm / TR')
    print('                     DVARS Threshold = 3 pct signal change / TR')
    defaults = ['yes', 'no']
    decision, garbage = selector_list(defaults, output)

    # if the user rejects the defaults or makes a mistake
    if decision == 'no' or None:

        print('')
        print('Input head size (default 50)')
        head_size, output = selector_float(output)

        print('')
        print('Input FD threshold (default 0.3)')
        FD, output = selector_float(output)

        print('')
        print('Input head size (default 0.3)')
        DV, output = selector_float(output)

    else:
        print('')
        print('OK, using the defaults.')
        head_size = 50
        FD = 0.3
        DV = 0.3

    line = ('. ${DIR_PIPE}/epitome/modules/pre/TRdrop ' + 
                                  str(input_name) + ' ' +
                                  str(head_size) + ' ' +
                                  str(FD) + ' ' +
                                  str(DV))

    return line, output

def check_masks(dir_data, expt, mode):
    output = ''

    print('')
    print('Adding mask-checking QC to the outputs.')

    line = ('. ${DIR_PIPE}/epitome/modules/qc/check_masks ' + 
                                        str(dir_data) + ' ' +
                                        str(expt) + ' ' +
                                        str(mode))

    return line, output

def check_EPI2T1(dir_data, expt, mode):
    output = ''

    print('')
    print('Adding EPI-to-T1 registration checking QC to the outputs.')

    line = ('. ${DIR_PIPE}/epitome/modules/qc/check_EPI2T1 ' + 
                                         str(dir_data) + ' ' +
                                         str(expt) + ' ' +
                                         str(mode))

    return line, output

def check_T12MNI(dir_data, expt, mode):
    output = ''

    print('')
    print('Adding T1-to-MNI registration checking QC to the outputs.')

    line = ('. ${DIR_PIPE}/epitome/modules/qc/check_T12MNI ' + 
                                         str(dir_data) + ' ' +
                                         str(expt) + ' ' +
                                         str(mode))

    return line, output

def check_runs(dir_data, expt, mode):
    output = ''

    print('')
    print('Adding NIFTI dimension-checking QC to the outputs.')

    line = ('. ${DIR_PIPE}/epitome/modules/qc/check_runs ' + 
                                       str(dir_data) + ' ' +
                                       str(expt) + ' ' +
                                       str(mode))

    return line, output

def check_motionind(dir_data, expt, mode):
    output = ''

    print('')
    print('Adding subject-wise motion QC to the outputs.')

    line = ('echo python ${DIR_PIPE}/epitome/modules/qc/check_motionind ' + 
             str(dir_data) + ' ' + str(expt) + ' ' + str(mode))

    return line, output

def check_spectra(dir_data, expt, mode):
    output = ''

    print('')
    print('Adding subject-wise regressor spectra QC to the outputs.')

    line = ('echo python ${DIR_PIPE}/epitome/modules/qc/check_spectra ' + 
            str(dir_data) + ' ' + str(expt) + ' ' +  str(mode))

    return line, output

def del_everything():
    return line, output
def del_postmc():
    return line, output
def del_registration():
    return line, output
def del_MNI():
    return line, output
