#!/usr/bin/env python

import fnmatch
import os
import csv
import glob
import operator
import numpy as np
import scipy as sp
from scipy.stats import ttest_ind
import matplotlib.pyplot as plt
import ypp_inputs

## Options: will eventually be set at command line
head_r = 50   # head diamater in mm
FD_t = 2    #
DV_t = 10   #
quality = 0  # set to 1 for dpi = 300, eps output
blacklist = []  # participants to exclude

##

def factors(n):    
    """
    Returns all factors of n.
    """
    return set(reduce(list.__add__, 
                ([i, n//i] for i in range(1, int(n**0.5) + 1) if n % i == 0)))

def get_subj(dir):
    """
    Gets all folder names in a directory.
    """
    subjects = []
    for subj in os.walk(dir).next()[1]:
        if os.path.isdir(os.path.join(dir, subj)) == True:
            subjects.append(subj)
    return subjects

def compute_FD(f, head_radius):
    """
    Computes FD vector from AFNI 3dVolreg 6-param .1D file read using
    numpy's genfromtxt.

    f is a string pointing to the .1D file.
    head_radius is an integer in mm.

    1) Convert degrees (roll, pitch, yaw) to mm using head radius
    2) Takes the same of the absoloute first difference
    Returns a vector of mm/TR.
    
    """
    f = np.genfromtxt(f)
    f[:,0] = np.radians(f[:,0]) * head_radius
    f[:,1] = np.radians(f[:,1]) * head_radius
    f[:,2] = np.radians(f[:,2]) * head_radius
    f = np.abs(np.diff(f, n=1, axis=0))
    f = np.sum(f, axis=1)
    return f

def square_factors(fac, num):
    """
    Finds the two most square factors of a number from a list of factors.
    Factors returned with the smallest first.
    """
    candidates = []
    for x in fac:
        for y in fac:
            if x*y == num:
                candidates.append(abs(x-y))
    most_square = np.min(candidates)
    for x in fac:
        for y in fac:
            if x*y == num:
                if x-y == most_square:
                    factor = [x, y]
    if factor[0] > factor[1]:
        factor = factor[::-1]
    return factor

def figure_quality(q):
    """
    Sets figure quality to be very high if q >=1.
    """
    if quality >= 1:
        size = 12
        dpi = 300
    else:
        size = 8
        dpi = 72
    return size, dpi 

def main():
    """
    This plots a trace of the framewise displacement measure and DVARS measure 
    for each participant (Power et al. 2012). Participants are sorted in the 
    plot from best to worst behaved, and thresholds are printed to facilitate 
    qualitative participant rejection, if that's how you roll.
    """

    # declare all variables
    Od, Oe, Os, Ot, Oc = ypp_inputs.init()
    ax_x = 0
    ax_y = 0
    flag = 0
    FD_all = np.array([])
    DV_all = np.array([])
    dict_FD = {}

    # get subject numbers
    subjects = get_subj(os.path.join(Od, Oe))

    # get number of subjects
    n_subj = len(subjects)

    # sort subjects by FD lowest to highest
    for subj in subjects:
        FD = np.array([])
        for session in os.walk(os.path.join(Od, Oe, subj, Ot)).next()[1]:
            d = os.path.join(Od, Oe, subj, Ot, session)
            for run in np.arange(len(glob.glob(d + '/RUN*'))) + 1:     
                f = compute_FD(os.path.join(d, 'PARAMS/motion.' +
                                               '%02d' % run +'.1D'), head_r)      
                # per subject
                FD = np.append(FD, f)
            
            #take total FD over all runs      
            dict_FD[subj] = np.sum(FD) / len(FD)

    # sort dict on normalized FD sum
    subjects = sorted(dict_FD.iteritems(), key=operator.itemgetter(1))

    # find the most square set of factors for n_subj
    while flag == 0:
        
        # get all candidate factors for the current number of subjects
        f_subj = factors(n_subj)
        factor = square_factors(f_subj, n_subj)
        
        # check if solution is 'square enough'
        if float(factor[1]) / float(factor[0]) <= 1.5:
            flag = 1
       
        # if not, try again with a larger number
        else:
            n_subj = n_subj + 1

    # init figure
    figure_size, figure_dpi = figure_quality(quality)

    fig_FD, ax_FD = plt.subplots(nrows=factor[0], 
                                 ncols=factor[1], 
                                 figsize=(figure_size, figure_size), 
                                 dpi=figure_dpi, 
                                 facecolor='white')
    fig_DV, ax_DV = plt.subplots(nrows=factor[0], 
                                 ncols=factor[1], 
                                 figsize=(figure_size, figure_size), 
                                 dpi=figure_dpi, 
                                 facecolor='white')

    for subj in subjects:
        
        # skip the blacklist, otherwise find framewise displacement and DVARS
        if any(s in subj[0] for s in blacklist):
            pass 
        else:
            FD = np.array([])
            DV = np.array([])
            breaks = np.array([0])
            for session in os.walk(os.path.join(Od, Oe, subj[0], Ot)).next()[1]:
                d = os.path.join(Od, Oe, subj[0], Ot, session)
                for run in np.arange(len(glob.glob(d + '/RUN*'))) + 1:     
                    # framewise displacement
                    f = compute_FD(os.path.join(d, 'PARAMS/motion.' +
                                                   '%02d' % run +'.1D'), head_r)         
                    FD = np.append(FD, f, axis=1) # per subject
                    FD_all= np.append(FD_all, f) # across all subjects
                    run_length = len(FD)
                    breaks = np.append(breaks, run_length) # list of run breaks

                    # DVARS
                    f = np.genfromtxt(os.path.join(d, 'PARAMS/DVARS.' + 
                                                      '%02d' % run + '.1D'))
                    f = f[1:] / 10 # remove leading 0, conv. to % signal
                    DV = np.append(DV, f) # per subject 
                    DV_all = np.append(DV_all, f) # across all subjects
            
            t = np.arange(len(DV)) # time axis
            
            # plot FD, DVARS, thresholds, and runs for each subject
            for b in breaks:
                ax_FD[ax_y][ax_x].axvline(x=b, ymin=0, ymax=100, color='black')
            ax_FD[ax_y][ax_x].axhline(y=FD_t, xmin=0, xmax=1, color='red')
            ax_FD[ax_y][ax_x].plot(t, FD.T, lw=1, label=subj[0], color='blue')
            ax_FD[ax_y][ax_x].set_xlim((-3, len(t) + 3))
            ax_FD[ax_y][ax_x].set_title(str(subj[0]), fontsize=10)
            for b in breaks:
                ax_DV[ax_y][ax_x].axvline(x=b, ymin=0, ymax=100, color='black')
            ax_DV[ax_y][ax_x].axhline(y=DV_t, xmin=0, xmax=1, color='red')
            ax_DV[ax_y][ax_x].plot(t, DV.T, lw=1, label=subj[0], color='green')
            ax_DV[ax_y][ax_x].set_xlim((-3, len(t) + 3))
            ax_DV[ax_y][ax_x].set_title(str(subj[0]), fontsize=10)

            ax_x = ax_x + 1  # this keeps us moving through the grid of plots
            if ax_x > factor[1]-1:
                ax_x = 0
                ax_y = ax_y + 1

    ax_x = 0 # reset the axis for a second go
    ax_y = 0
    for subj in np.arange(n_subj):
        if subj < len(subjects):
            # common y axis maximum
            ax_FD[ax_y][ax_x].set_ylim((0, np.max(FD_all))) 
            ax_DV[ax_y][ax_x].set_ylim((0, np.max(DV_all)))

            # remove unnecessary detail
            ax_FD[ax_y][ax_x].set_frame_on(False) # remove frame
            ax_DV[ax_y][ax_x].set_frame_on(False)
            ax_FD[ax_y][ax_x].axes.get_yaxis().set_visible(False) # rm y axis
            ax_DV[ax_y][ax_x].axes.get_yaxis().set_visible(False)
            ax_FD[ax_y][ax_x].get_xaxis().tick_bottom() # remove x ticks
            ax_DV[ax_y][ax_x].get_xaxis().tick_bottom()
            ax_FD[ax_y][ax_x].axes.get_xaxis().set_ticks([]) # remove x labels
            ax_DV[ax_y][ax_x].axes.get_xaxis().set_ticks([])
            
            # add in x line at bottom
            xmin, xmax = ax_FD[ax_y][ax_x].get_xaxis().get_view_interval()
            ymin, ymax = ax_FD[ax_y][ax_x].get_yaxis().get_view_interval()
            ax_FD[ax_y][ax_x].add_artist(plt.Line2D((xmin, xmax), 
                                                    (ymin, ymin), 
                                                     color='black', 
                                                     linewidth=1))
            xmin, xmax = ax_DV[ax_y][ax_x].get_xaxis().get_view_interval()
            ymin, ymax = ax_DV[ax_y][ax_x].get_yaxis().get_view_interval()
            ax_DV[ax_y][ax_x].add_artist(plt.Line2D((xmin, xmax), 
                                                    (ymin, ymin), 
                                                     color='black', 
                                                     linewidth=1))
        # delete empty plots
        if subj >= len(subjects):
            ax_FD[ax_y][ax_x].axis('off')
            ax_DV[ax_y][ax_x].axis('off')

        # this keeps us moving through the grid of plots
        ax_x = ax_x + 1
        if ax_x > factor[1]-1:
            ax_x = 0
            ax_y = ax_y + 1

    fig_FD.suptitle('Framewise Displacement (mm/TR), threshold = ' +
                                                     str(FD_t) + ' mm/TR')
    fig_DV.suptitle('DVARS (% signal change/TR), line = ' +
                                                     str(DV_t) + '%/TR')
    
    fig_FD.subplots_adjust(hspace=0.7) # add some breathing room
    fig_DV.subplots_adjust(hspace=0.7)

    fig_FD.savefig(os.path.join(Od, Oe, 'qc_FD_individual.pdf')) # save pdf
    fig_DV.savefig(os.path.join(Od, Oe, 'qc_DVARS_individual.pdf'))
    if quality >= 1:
        fig_FD.savefig(os.path.join(Od, Oe, 'qc_FD_individual.eps')) # save eps
        fig_DV.savefig(os.path.join(Od, Oe, 'qc_DVARS_individual.eps'))

    print('Printed plots to ' + str(os.path.join(Od, Oe)) + '.')

## JDV Jan 29 2014

# labels for x-y axis (not really needed)
# ax_FD[ax_y][ax_x].set_xlabel('Time (TRs)')
# ax_FD[ax_y][ax_x].set_ylabel('FD (mm/TR)')
# ax_DV[ax_y][ax_x].set_xlabel('Time (TRs)')
# ax_DV[ax_y][ax_x].set_ylabel('DVARS (\% signal)')

# old stuff...
# ax[0].tick_params(axis='both', which='both', size=10)
# ax[0].set_xlim([0, len(t)-1])
# xTicks = np.linspace(0, len(t), 5)
# xTicks[-1] = xTicks[-1] - 1
# ax[0].set_xticks(xTicks)
# ax[0].set_xticklabels((xTicks+1).astype(np.int))