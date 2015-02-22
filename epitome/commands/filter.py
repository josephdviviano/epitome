#!/usr/bin/env python

import epitome as epi

def run(input_name):
    output = 'filtered'

    print('\nAdding filter module.')

    try:
        print('\nSet detrend order:')
        polort = epi.utilities.selector_int()

        print('\nSet mean global signal regression:')
        gs_list = ['off', 'on']
        gs_flag = epi.utilities.selector_list(gs_list)

        print('\nSet mean ventricle signal regression:')
        vent_list = ['off', 'on']
        vent_flag = epi.utilities.selector_list(vent_list)

        print('\nSet mean draining vessel signal regression:')
        dv_list = ['off', 'on']
        dv_flag = epi.utilities.selector_list(dv_list)

        print('\nSet local white matter regression regression:')
        wm_loc_list = ['off', 'on']
        wm_loc_flag = epi.utilities.selector_list(wm_loc_list)

        print('\nSet mean white matter regression regression:')
        wm_glo_list = ['off', 'on']
        wm_glo_flag = epi.utilities.selector_list(wm_glo_list)

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