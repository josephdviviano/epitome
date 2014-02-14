import nibabel as nib
import numpy as np
from scipy import ndimage as nd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import ypp_inputs
import os

orientation = 's'
subj = '101'

def get_subj(dir):
    """
    Gets all folder names in a directory.
    """
    subjects = []
    for subj in os.walk(dir).next()[1]:
        if os.path.isdir(os.path.join(dir, subj)) == True:
            subjects.append(subj)
    return subjects

def main():
    """
    Prints the central slice of the T1 and co-registered + deskulled EPI.
    """

    # declare all variables
    path, expt, subjects, mode, core = ypp_inputs.init()

    # get subject numbers
    #subjects = get_subj(os.path.join(path, expt))

    # loop through all subjects
    pdf = PdfPages(os.path.join(path, expt, 'qc_reg_EPI_to_T1.pdf'))
    for subj in subjects:

        # load in data
        anat = nib.load(os.path.join(path, expt, subj, 'T1/SESS01/anat_T1_brain.nii.gz')).get_data()
        reg = nib.load(os.path.join(path, expt, subj,'T1/SESS01/reg_EPI_to_T1.nii.gz')).get_data()

        # get size ratio between over + underlay
        dsfactor = [a/float(r) for a,r in zip(anat.shape, reg.shape)]
        # match over + underlay dimensions
        reg_to_anat = nd.interpolation.zoom(reg, zoom=dsfactor)
        # set small values in overlay to be transparent
        reg_to_anat = np.ma.masked_where(reg_to_anat < 100, reg_to_anat)
        cmap = plt.cm.Reds
        cmap.set_bad('g', 0)

        # generate the image

        plt.subplot(2,2,1)
        mid = np.round(anat.shape[0] / 2)
        plt.imshow(anat[mid, :, :], cmap=plt.cm.gray,
                                    interpolation='nearest')
        plt.imshow(reg_to_anat[mid, :, :], cmap=cmap,
                                           interpolation='nearest',
                                           alpha=0.5)

        plt.subplot(2,2,2)
        mid = np.round(anat.shape[1] / 2)
        plt.imshow(anat[:, mid, :], cmap=plt.cm.gray,
                                    interpolation='nearest')
        plt.imshow(reg_to_anat[:, mid, :], cmap=cmap,
                                           interpolation='nearest',
                                           alpha=0.5)

        plt.subplot(2,2,3)
        mid = np.round(anat.shape[2] / 2)
        plt.imshow(anat[:, :, mid], cmap=plt.cm.gray,
                                    interpolation='nearest')
        plt.imshow(reg_to_anat[:, :, mid], cmap=cmap,
                                           interpolation='nearest',
                                           alpha=0.5)

        plt.suptitle(str(expt) + ' ' + str(mode) + ': ' + str(subj))
        pdf.savefig()
        plt.close()

        # # We can also set the file's metadata via the PdfPages object:
        # d = pdf.infodict()
        # d['Title'] = 'Multipage PDF Example'
        # d['Author'] = u'Jouni K. Sepp\xe4nen'
        # d['Subject'] = 'How to create a multipage pdf file and set its metadata'
        # d['Keywords'] = 'PdfPages multipage keywords author title subject'
        # d['CreationDate'] = datetime.datetime(2009, 11, 13)
        # d['ModDate'] = datetime.datetime.today()