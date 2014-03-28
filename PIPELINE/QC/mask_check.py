#!/usr/bin/env python

import os
import datetime

import nibabel as nib
import numpy as np
from scipy import ndimage as nd

import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

import ypp_inputs
import ypp_utilites

def main():
    """
    Prints the central slice of the T1 and co-registered + deskulled EPI, 
    including an edge-detected version of the T1 (requires AFNI).
    """

    # declare all variables
    path, expt, subjects, mode, core = ypp_inputs.init()

    # get subject numbers
    subjects = ypp_utilities.get_subj(os.path.join(path, expt))
    #subjects = ['211']
    # loop through all subjects
    pdf = PdfPages(os.path.join(path, expt, 'qc_masks.pdf'))
    for subj in subjects:

        anat = os.path.join(path, expt, subj, mode, 'SESS01/anat_EPI_brain.nii.gz')
        wm = os.path.join(path, expt, subj, mode, 'SESS01/anat_wm_ero.nii.gz')
        dv = os.path.join(path, expt, subj, mode, 'SESS01/anat_dv_ero.nii.gz')
        gm = os.path.join(path, expt, subj, mode, 'SESS01/anat_gm.nii.gz')
        vent = os.path.join(path, expt, subj, mode, 'SESS01/anat_vent_ero.nii.gz')

        # load in data
        anat = nib.load(anat).get_data()
        wm = nib.load(wm).get_data()
        dv = nib.load(dv).get_data()
        gm = nib.load(gm).get_data()
        vent = nib.load(vent).get_data()

        # reorient the data to radiological
        anat = np.transpose(anat, (2,0,1))
        anat = np.rot90(anat, 2)
        wm = np.transpose(wm, (2,0,1))
        wm = np.rot90(wm, 2)
        dv = np.transpose(dv, (2,0,1))
        dv = np.rot90(dv, 2)
        gm = np.transpose(gm, (2,0,1))
        gm = np.rot90(gm, 2)
        vent = np.transpose(vent, (2,0,1))
        vent = np.rot90(vent, 2)

        # get size ratio between over + underlay
        dsfactor = [a/float(r) for a,r in zip(anat.shape, wm.shape)]
        # match over + underlay dimensions
        wm_to_anat = nd.interpolation.zoom(wm, zoom=dsfactor)
        gm_to_anat = nd.interpolation.zoom(gm, zoom=dsfactor)
        dv_to_anat = nd.interpolation.zoom(dv, zoom=dsfactor)
        vent_to_anat = nd.interpolation.zoom(vent, zoom=dsfactor)
        
        # set small values in overlays to be transparent
        wm_to_anat = np.ma.masked_where(wm_to_anat < 1, wm_to_anat)
        gm_to_anat = np.ma.masked_where(gm_to_anat < 1, gm_to_anat)
        dv_to_anat = np.ma.masked_where(dv_to_anat < 1, dv_to_anat)
        vent_to_anat = np.ma.masked_where(vent_to_anat < 1, vent_to_anat)

        # T1
        plt.subplot(1,3,1)
        mid = np.round(anat.shape[0] / 2)
        plt.imshow(anat[mid, :, :], cmap=plt.cm.gray,
                                    interpolation='nearest')

        # white matter
        cmap = plt.cm.BrBG
        cmap.set_bad('g', 0)
        plt.imshow(wm_to_anat[mid, :, :], cmap=cmap,
                                           interpolation='nearest',
                                           alpha=0.5)

        # gray matter
        cmap = plt.cm.winter
        cmap.set_bad('g', 0)
        plt.imshow(gm_to_anat[mid, :, :], cmap=cmap,
                                           interpolation='nearest',
                                           alpha=0.5)

        # draining vessels matter
        cmap = plt.cm.cool
        cmap.set_bad('g', 0)
        plt.imshow(dv_to_anat[mid, :, :], cmap=cmap,
                                           interpolation='nearest',
                                           alpha=0.5)

        # ventricles
        cmap = plt.cm.RdYlGn
        cmap.set_bad('g', 0)
        plt.imshow(vent_to_anat[mid, :, :], cmap=cmap,
                                           interpolation='nearest',
                                           alpha=0.5)

        plt.axis('off')

        # T1
        plt.subplot(1,3,2)
        mid = np.round(anat.shape[1] / 2)
        plt.imshow(anat[:, mid, :], cmap=plt.cm.gray,
                                    interpolation='nearest')
        
        # white matter
        cmap = plt.cm.BrBG
        cmap.set_bad('g', 0)
        plt.imshow(wm_to_anat[:, mid, :], cmap=cmap,
                                           interpolation='nearest',
                                           alpha=0.5)

        # gray matter
        cmap = plt.cm.winter
        cmap.set_bad('g', 0)
        plt.imshow(gm_to_anat[:, mid, :], cmap=cmap,
                                           interpolation='nearest',
                                           alpha=0.5)

        # draining vessels matter
        cmap = plt.cm.cool
        cmap.set_bad('g', 0)
        plt.imshow(dv_to_anat[:, mid, :], cmap=cmap,
                                           interpolation='nearest',
                                           alpha=0.5)

        # ventricles
        cmap = plt.cm.RdYlGn
        cmap.set_bad('g', 0)
        plt.imshow(vent_to_anat[:, mid, :], cmap=cmap,
                                           interpolation='nearest',
                                           alpha=0.5)
        plt.axis('off')

        plt.subplot(1,3,3)
        mid = np.round(anat.shape[2] / 2)
        plt.imshow(anat[:, :, mid], cmap=plt.cm.gray,
                                    interpolation='nearest')

        # white matter
        cmap = plt.cm.BrBG
        cmap.set_bad('g', 0)
        plt.imshow(wm_to_anat[:, :, mid], cmap=cmap,
                                           interpolation='nearest',
                                           alpha=0.5)

        # gray matter
        cmap = plt.cm.winter
        cmap.set_bad('g', 0)
        plt.imshow(gm_to_anat[:, :, mid], cmap=cmap,
                                           interpolation='nearest',
                                           alpha=0.5)

        # draining vessels matter
        cmap = plt.cm.cool
        cmap.set_bad('g', 0)
        plt.imshow(dv_to_anat[:, :, mid], cmap=cmap,
                                           interpolation='nearest',
                                           alpha=0.5)

        # ventricles
        cmap = plt.cm.RdYlGn
        cmap.set_bad('g', 0)
        plt.imshow(vent_to_anat[:, :, mid], cmap=cmap,
                                           interpolation='nearest',
                                           alpha=0.5)
        plt.axis('off')

        plt.suptitle(str(expt) + ' ' + str(mode) + ': ' + str(subj))
        plt.tight_layout()
        plt.savefig(pdf, format='pdf')
        plt.close()

    # Add some metadata and close the PDF object
    d = pdf.infodict()
    d['Title'] = 'Quality Control: Correctness of the Tissue Masks'
    d['Author'] = u'Joseph D Viviano\xe4nen'
    d['Subject'] = 'Quality Control'
    d['Keywords'] = 'QC EPI Tissue Masks'
    d['CreationDate'] = datetime.datetime.today()
    d['ModDate'] = datetime.datetime.today()
    pdf.close()

## JDV Feb 24 2014