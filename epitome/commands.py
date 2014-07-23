#!/usr/bin/env python
"""
This contains calls to each module that are referenced by the command-line-
interface. Each produces a single line of text printed to the master
shell script reference passed in each call.
"""

import os, copy
import epitome as epi

###############################################################################
# Helper Functions - Used Internally

# def invalid_selection():
#     print('Invalid selection.')
#     return None, None

def selector_float():
    option = raw_input('#: ') # have the user enter a number

    # ensure response is non-negative
    if option == '':
        option = -1
    
    # check input
    try:
        if float(option) >= float(0):
            response = float(option)
            return response
        else:
            print('*** Input must be positive! ***')
            raise ValueError    
    except:
        print('*** Input must be a float! ***')
        raise ValueError
        #response, output = invalid_selection()    

def selector_int():
    option = raw_input('#: ') # have the user enter a number

    # ensure response is non-negative
    if option == '':
        option = -1
    
    # check input
    try:
        if int(option) >= 0:
            response = int(option)
            return response
        else:
            print('*** Input must be positive! ***')
            raise ValueError
    except:
        print('*** Input must be an integer! ***')
        raise ValueError
        #response, output = invalid_selection()

def selector_list(item_list):
    if type(item_list) != list:
        raise TypeError('Input must be a list!')

    # sort the input list
    item_list.sort()

    # print the options, and their numbers
    for i, item in enumerate(item_list):
        print(str(i+1) +': ' + str(item))

    # retrieve the option number
    option = raw_input('option #: ')

    # check input
    if option == '':
        option = 0
    try:
        response = item_list[int(option)-1]
    except:
        print('*** Option # invalid! ***')
        raise ValueError
        #response, output = invalid_selection()
    if int(option) == 0:
        print('*** Option # invalid! ***')
        raise ValueError
        #response, output = invalid_selection()
    return response

def selector_dict(item_dict):    
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

    # check input
    if option == '':
        option = 0
    try:
        response = item_list[int(option)-1]
    except:
        print('*** Option # invalid! ***')
        raise ValueError
        #response, output = invalid_selection()
    if int(option) == 0:
        print('*** Option # invalid! ***')
        raise ValueError
        #response, output = invalid_selection()
    return response

###############################################################################
# Pre-Processing Scripts

def filter(input_name):
    output = 'filtered'

    print('\nAdding filter module.')

    try:
        print('\nSet detrend order:')
        polort = selector_int()

        print('\nSet mean global signal regression:')
        gs_list = ['off', 'on']
        gs_flag = selector_list(gs_list)

        print('\nSet mean ventricle signal regression:')
        vent_list = ['off', 'on']
        vent_flag = selector_list(vent_list)

        print('\nSet mean draining vessel signal regression:')
        dv_list = ['off', 'on']
        dv_flag = selector_list(dv_list)

        print('\nSet local white matter regression regression:')
        wm_loc_list = ['off', 'on']
        wm_loc_flag = selector_list(wm_loc_list)

        print('\nSet mean white matter regression regression:')
        wm_glo_list = ['off', 'on']
        wm_glo_flag = selector_list(wm_glo_list)

    # if we messed any of these up, we return None
    except ValueError as ve:
        return '', None

    # otherwise we print the command and return it
    line = ('. ${DIR_PIPE}/epitome/modules/pre/filter ' +
                                  str(input_name) + ' ' +
                                  str(polort) + ' ' +
                                  str(gs_flag) + ' ' +
                                  str(vent_flag) + ' ' +
                                  str(dv_flag) + ' ' +
                                  str(wm_loc_flag) + ' ' +
                                  str(wm_glo_flag))
    return line, output

def gen_gcor(input_name):
    output = copy.copy(input_name) # return output unharmed
    
    print('\nAdding global correlation calculation')

    line = ('. ${DIR_PIPE}/epitome/modules/pre/gen_gcor ' + str(input_name))

    return line, output

def gen_regressors(input_name):
    

    output = copy.copy(input_name) # return output unharmed

    print('\nGenerating regressors from ' + str(input_name))

    line = ('. ${DIR_PIPE}/epitome/modules/pre/gen_regressors ' +
                                                  str(input_name))

    return line, output

def init_EPI():    
    output = 'scaled'

    print('\nInitializing functional MRI pre-processing.')

    try:
        # get the data-quality option
        print('\nSelect data quality:')
        data_quality = ['low', 'high']
        quality = selector_list(data_quality)

        # get the number of TRs to delete
        print('\nNumber of TRs to delete:')
        deltr = selector_int()

        # get the slice timing
        print('\nSlice-timing pattern: (see AFNI 3dTshift for more help)')
        t_patterns = {'alt+z' : '= alternating in the plus direction', 
                      'alt+z2' : '= alternating, starting at slice #1', 
                      'alt-z' : '= alternating in the minus direction', 
                      'alt-z2' : '= alternating, starting at slice #nz-2', 
                      'seq+z' : '= sequential in the plus direction',
                      'seq-z' : '= sequential in the minus direction'}
        slice_timing = selector_dict(t_patterns)

        # normalize
        print('\nTime series normalization: (see documentation for help)')
        norm_dict = {'off' : ': deskulling, no normalization',
                     'pct' : ': 1% = 1, normalize to 100 mean voxelwise',
                     'scale':': scale run mean to = 1000, arbitrary units'}
        normalization = selector_dict(norm_dict)

        # masking
        print('\nEPI masking: acquisition dependent')
        mask_list = ['loose', 'normal', 'tight']
        masking = selector_list(mask_list)

    # if we messed any of these up, we return None
    except ValueError as ve:
        return '', None

    # otherwise we print the command and return it
    line = ('. ${DIR_PIPE}/epitome/modules/pre/init_EPI ' +
                                      str(quality) + ' ' +
                                      str(deltr) + ' ' +
                                      str(slice_timing) + ' ' +
                                      str(normalization) + ' ' +
                                      str(masking))
    return line, output

def linreg_EPI2MNI_AFNI(input_name):
    output = 'MNI'

    # give us some feedback
    print('\nResampling input EPI data to MNI space using AFNI.')

    try:
        # get the reslice dimensions
        print('\nSelect target dimensions (isotropic mm):')
        dims = selector_float()

    # if we messed any of these up, we return None
    except ValueError as ve:
        return '', None

    # otherwise we print the command and return it
    line = ('. ${DIR_PIPE}/epitome/modules/pre/linreg_EPI2MNI_AFNI ' +
                                               str(input_name) + ' ' +
                                               str(dims))
    return line, output

def linreg_EPI2MNI_FSL(input_name):
    output = 'MNI'

    # give us some feedback
    print('\nResampling input EPI data to MNI space using FSL.')

    try:
        # get the reslice dimensions
        print('\nSelect target dimensions (isotropic mm):')
        dims = selector_float()

    # if we messed any of these up, we return None
    except ValueError as ve:
        return '', None

    # otherwise we print the command and return it
    line = ('. ${DIR_PIPE}/epitome/modules/pre/linreg_EPI2MNI_FSL ' +
                                              str(input_name) + ' ' +
                                              str(dims))
    return line, output

def linreg_FS2EPI_AFNI(input_name):
    output = copy.copy(input_name) # return output unharmed

    print('\nMoving Freesurfer atlases to single-subject space using AFNI.')

    line = ('. ${DIR_PIPE}/epitome/modules/pre/linreg_FS2EPI_AFNI')

    return line, output

def linreg_FS2EPI_FSL(input_name):
    output = copy.copy(input_name) # return output unharmed

    print('\nMoving Freesurfer atlases to single-subject space using FSL.')
    
    line = ('. ${DIR_PIPE}/epitome/modules/pre/linreg_FS2EPI_FSL')

    return line, output

def linreg_FS2MNI_FSL(input_name):   
    output = copy.copy(input_name) # return output unharmed

    print('\nMoving Freesurfer atlases to MNI space using FSL.')

    line = ('. ${DIR_PIPE}/epitome/modules/pre/linreg_FS2MNI_FSL')

    return line, output

def linreg_calc_AFNI(input_name):
    output = copy.copy(input_name) # return output unharmed

    print('\nCalculating linear registration pathways using AFNI.')

    try:
        # get the data-quality option
        print('\nSelect data quality:')
        data_quality = ['low', 'high']
        quality = selector_list(data_quality)

        # set the cost function option
        print('\nCost function: (see AFNI align_EPI_anat.py for help)')
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
                     'lpc' : '= Local Pearson Correlation Signed (Default)',
                     'lpa' : '= Local Pearson Correlation Abs',
                     'lpc+' : '= Local Pearson Signed + Others',
                     'ncd' : '= Normalized Compression Distance',
                     'lpc+zz' : '= Local Pearson Correlation Signed + Magic'}
        cost = selector_dict(cost_fxns)

        # get registration degrees of freedom
        print('\nDegrees of freedom: (see AFNI align_EPI_anat.py for help)')
        degrees_of_freedom = ['big_move', 'giant_move']
        reg_dof = selector_list(degrees_of_freedom)

    # if we messed any of these up, we return None
    except ValueError as ve:
        return '', None

    # otherwise we print the command and return it
    line = ('. ${DIR_PIPE}/epitome/modules/pre/linreg_calc_AFNI ' +
                                               str(quality) + ' ' +
                                               str(cost) + ' ' +
                                               str(reg_dof))
    return line, output

def linreg_calc_FSL(input_name):
    output = copy.copy(input_name) # return output unharmed

    print('\nCalculating linear registration pathways.')

    try:
        # get the data-quality option
        print('\nSelect data quality:')
        data_quality = ['low', 'high']
        quality = selector_list(data_quality)

        # set the cost function option
        print('\nRegistration cost function: (see FSL FLIRT for help)')
        cost_fxns = {'mutualinfo' : '= Mutual Information [H(b)+H(s)-H(b,s)]', 
                     'leastsq' : '=  Least Squares [Pearson Correlation]',
                     'corratio' : '= Correlation Ratio', 
                     'normcorr' : '= Normalized Correlation', 
                     'labeldiff' : '= FSL magic!',
                     'bbr' : '= FSL magic!'}

        cost = selector_dict(cost_fxns)

        # get registration degrees of freedom
        print('\nRegistration degrees of freedom: (see FSL FLIRT for help)')
        degrees_of_freedom = [6, 7, 9, 12]
        reg_dof = selector_list(degrees_of_freedom)

    # if we messed any of these up, we return None
    except ValueError as ve:
        return '', None

    # otherwise we print the command and return it
    line = ('. ${DIR_PIPE}/epitome/modules/pre/linreg_calc_FSL ' +
                                               str(quality) + ' ' +
                                               str(cost) + ' ' +
                                               str(reg_dof))
    return line, output

def lowpass(input_name):
    import numpy as np

    output = 'lowpass'

    print('\nLow-passing each voxel time series.')
    
    try:
        print('\nInput mask prefix (default = EPI_mask):')
        mask_prefix = raw_input('Mask Prefix: ')
        if mask_prefix == '':
            mask_prefix = 'EPI_mask'

        print('\nWhich filter type would you like to use (see documentation)?')
        filter_list = ['median', 'average', 'kaiser', 'butterworth']
        filter_type = selector_list(filter_list)

        if filter_type in ['median', 'average']:
            flag = 0

            # ensures input length is odd
            while flag == 0:
                print('\nSelect window length (must be odd, default = 3):')
                lowpass_param = selector_int()

                if np.remainder(lowpass_param, 2) != 0:
                    flag = 1
                else:
                    print('Window length must be odd!')
        
        elif filter_type in ['kaiser', 'butterworth']:
            
            print('\nInput cutoff frequency in Hz (default = 0.1 Hz):')
            lowpass_param = selector_float()

    # if we messed any of these up, we return None
    except ValueError as ve:
        return '', None

    # otherwise we print the command and return it
    line = ('. ${DIR_PIPE}/epitome/modules/pre/lowpass ' +
                                           str(input_name) + ' ' + 
                                           str(mask_prefix) + ' ' +
                                           str(filter_type) + ' ' +
                                           str(lowpass_param))
    return line, output

def TRdrop(input_name):
    output = 'scrubbed'

    print('\nRemoving motion-corrupted TRs.')
    
    print('\nWould you like to use the defaults?')
    print('                           Head Size = 50 mm')
    print('    Framewise Displacement Threshold = 0.3 mm / TR')
    print('                     DVARS Threshold = 3 pct signal change / TR')
    
    try:
        defaults = ['yes', 'no']
        decision = selector_list(defaults)

        # if the user rejects the defaults or makes a mistake
        if decision == 'no' or None:

            print('\nInput head size (default 50)')
            head_size, output = selector_float(output)

            print('\nInput FD threshold (default 0.3)')
            FD, output = selector_float(output)

            print('\nInput head size (default 1000000)')
            DV, output = selector_float(output)

        else:
            print('\nOK, using the defaults.')
            head_size = 50
            FD = 0.3
            DV = 1000000 # this turns DVARS off, effectively

    # if we messed any of these up, we return None
    except ValueError as ve:
        return '', None

    # otherwise we print the command and return it
    line = ('. ${DIR_PIPE}/epitome/modules/pre/TRdrop ' + 
                                  str(input_name) + ' ' +
                                  str(head_size) + ' ' +
                                  str(FD) + ' ' +
                                  str(DV))

    return line, output

def surf2vol(input_name):   
    output = 'ctx'

    print('\nProjecting surface data to volume space.')

    line = ('. ${DIR_PIPE}/epitome/modules/pre/surf2vol ' + str(input_name))

    return line, output

def surfsmooth(input_name):    
    output = 'smooth'

    print('\nSmoothing functional data on a cortical surface.')

    try:
        print('\nInput smoothing kernel FWHM (mm):')
        fwhm, output = selector_float(output)

    # if we messed any of these up, we return None
    except ValueError as ve:
        return '', None

    # otherwise we print the command and return it
    line = ('. ${DIR_PIPE}/epitome/modules/pre/surfsmooth ' +
                                      str(input_name) + ' ' +
                                      str(fwhm))

    return line, output

def vol2surf(input_name):
    output = 'surface'

    print('\nProjecting data to cortical surface.')

    line = ('. ${DIR_PIPE}/epitome/modules/pre/vol2surf ' + str(input_name))

    return line, output

def volsmooth(input_name):
    output = 'volsmooth'

    print('\nVolumetric smoothing within a defined mask.')

    try:
        print('\nInput mask prefix (default = EPI_mask):')
        mask_prefix = raw_input('Mask Prefix: ')
        if mask_prefix == '':
            mask_prefix = 'EPI_mask'
        
        print('\nInput smoothing kernel FWHM (mm):')
        fwhm = selector_float()

    # if we messed any of these up, we return None
    except ValueError as ve:
        return '', None

    # otherwise we print the command and return it
    line = ('. ${DIR_PIPE}/epitome/modules/pre/volsmooth ' + 
                                     str(input_name) + ' ' +
                                     str(mask_prefix) + ' ' +
                                     str(fwhm))

    return line, output

###############################################################################
# QC Scripts

def check_masks(dir_data, expt, mode):
    output = ''

    print('\nAdding mask-checking QC to the outputs.')

    line = ('echo python ${DIR_PIPE}/epitome/modules/qc/check_masks ' + 
             str(dir_data) + ' ' + str(expt) + ' ' + str(mode))

    return line, output

def check_EPI2T1(dir_data, expt, mode):
    output = ''

    print('\nAdding EPI-to-T1 registration checking QC to the outputs.')

    line = ('echo python ${DIR_PIPE}/epitome/modules/qc/check_EPI2T1 ' + 
             str(dir_data) + ' ' + str(expt) + ' ' +  str(mode))

    return line, output

def check_T12MNI(dir_data, expt, mode):
    output = ''

    print('\nAdding T1-to-MNI registration checking QC to the outputs.')

    line = ('echo python ${DIR_PIPE}/epitome/modules/qc/check_T12MNI ' + 
             str(dir_data) + ' ' + str(expt) + ' ' + str(mode))

    return line, output

def check_runs(dir_data, expt, mode):
    output = ''

    print('\nAdding NIFTI dimension-checking QC to the outputs.')

    line = ('echo bash ${DIR_PIPE}/epitome/modules/qc/check_runs ' + 
             str(dir_data) + ' ' + str(expt))

    return line, output

def check_motionind(dir_data, expt, mode):
    output = ''

    print('\nAdding subject-wise motion QC to the outputs.')

    line = ('echo python ${DIR_PIPE}/epitome/modules/qc/check_motionind ' + 
             str(dir_data) + ' ' + str(expt) + ' ' + str(mode) + ' ${ID}')

    return line, output

def check_spectra(dir_data, expt, mode):
    output = ''

    print('\nAdding subject-wise regressor spectra QC to the outputs.')

    line = ('echo python ${DIR_PIPE}/epitome/modules/qc/check_spectra ' + 
            str(dir_data) + ' ' + str(expt) + ' ' +  str(mode) + ' ${ID}')

    return line, output

###############################################################################
# Cleanup Scripts

def del_everything(expt, clean):

    dir_data, dir_pipe, dir_afni, cores = epi.config.return_paths() 

    print('\n *** Adding DELETE EVERYTHING to the cleanup Queue! ***')

    fname = os.path.join(dir_data, expt, clean)
    line = ('. ' + str(dir_pipe) + 
            '/epitome/modules/cleanup/del_everything >> ' + fname)
    os.system(line)

def del_postmc(expt, clean):

    dir_data, dir_pipe, dir_afni, cores = epi.config.return_paths() 

    print('\n *** Adding DELETE POST MOTION CORRECT to the cleanup Queue! ***')

    fname = os.path.join(dir_data, expt, clean)
    line = ('. ' + str(dir_pipe) + 
            '/epitome/modules/cleanup/del_postmc >> ' + fname)
    os.system(line)

def del_reg(expt, clean):

    dir_data, dir_pipe, dir_afni, cores = epi.config.return_paths() 

    print('')
    print(' *** Adding DELETE REGISTRATIONS to the cleanup Queue! ***')

    fname = os.path.join(dir_data, expt, clean)
    line = ('. ' + str(dir_pipe) + 
            '/epitome/modules/cleanup/del_registration >> ' + fname)
    os.system(line)

def del_MNI(expt, clean):

    dir_data, dir_pipe, dir_afni, cores = epi.config.return_paths() 

    print('')
    print(' *** Adding DELETE MNI to the cleanup Queue! ***')

    fname = os.path.join(dir_data, expt, clean)
    line = ('. ' + str(dir_pipe) +
            '/epitome/modules/cleanup/del_MNI >> ' + fname)
    os.system(line)
