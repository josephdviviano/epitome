#!/usr/bin/env python

import epitome as epi

def run(input_name):
    output = 'filtered'

    print('\nAdding filter module.')

    try:
        print('\nSet detrend order:')
        polort = epi.utilities.selector_int()

        print('\nSet mean global signal regression:')
        gs = epi.utilities.selector_list(['off', 'on'])

        print('\nSet mean ventricle signal regression:')
        vent = epi.utilities.selector_list(['off', 'on'])

        print('\nSet mean draining vessel signal regression:')
        dv = epi.utilities.selector_list(['off', 'on'])

        print('\nSet local white matter regression:')
        wm_loc = epi.utilities.selector_list(['off', 'on'])

        print('\nSet mean white matter regression:')
        wm_glo = epi.utilities.selector_list(['off', 'on'])

        print('\nSet top principal component regression:')
        top_pc = epi.utilities.selector_list(['off', 'on'])

    # if we messed any of these up, we return None
    except ValueError as ve:
        return '', None

    # otherwise we print the command and return it
    line = ('. ${DIR_PIPE}/epitome/modules/pre/filter {input_name} {polort} '
               '{gs} {vent} {dv} {wm_loc} {wm_glo} {top_pc}').format(
                              input_name=str(input_name),
                              polort=str(polort),
                              gs=gs,
                              vent=vent,
                              wm_loc=wm_loc,
                              wm_glo=wm_glo,
                              top_pc=top_pc)

    return line, output