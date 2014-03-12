import os
import datetime

import numpy as np
import scipy as sp
import scipy.signal as sig

import nibabel as nib

import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

import ypp_inputs

def get_subj(dir):
    """
    Gets all folder names in a directory.
    """
    subjects = []
    for subj in os.walk(dir).next()[1]:
        if os.path.isdir(os.path.join(dir, subj)) == True:
            subjects.append(subj)
    return subjects

def load_PSD(path, fs):
    tmp = np.genfromtxt(path)
    tmp = sig.welch(tmp, fs=fs, 
                         window='hann', 
                         nperseg=20, 
                         noverlap=None, 
                         return_onesided=True)

    freqs = tmp[0]
    power = tmp[1] / np.sum(tmp[1])
    return freqs, power

def main():
    # declare all variables
    path, expt, subjects, mode, core = ypp_inputs.init()

    # get subject numbers
    subjects = get_subj(os.path.join(path, expt))

    # loop through all subjects
    pdf = PdfPages(os.path.join(path, expt, 'qc_regressor_spectra.pdf'))
    for subj in subjects:

        subjpath = os.path.join(path, expt, subj)
        modepath = os.path.join(path, expt, subj, mode)
        # some frequency stuff
        # fslhd func_MNI.01.nii.gz | sed -n 22p
        TR = 2.5
        if TR >= 1000:
            TR = TR / 1000
        fs = 1.0 / TR
        ny = fs / 2.0

        # get the number of sessions
        sessions = len([f for f in os.listdir(modepath) 
                           if os.path.isdir(os.path.join(modepath, f)) 
                          and f[0:4] == 'SESS'])

        # number and list of frequency bins
        #n = len(np.genfromtxt('PARAMS/global_mean.02.1D'))/2
        #freq = np.linspace(0, ny, n)

        for sess in range(sessions):

            freq = load_PSD(os.path.join(modepath, 'SESS' + '%02d'%(sess+1), 
                                              'PARAMS/global_mean.01.1D'), fs)[0]
            n = len(freq) 

            # get the number of runs
            runs = len([f for f in os.listdir(os.path.join(modepath, 'SESS' + '%02d'%(sess+1))) 
                                if os.path.isdir(os.path.join(modepath, 'SESS' + '%02d'%(sess+1), f)) 
                                and f[0:3] == 'RUN'])

            # load in the subject brain mask
            ma = nib.load(os.path.join(modepath, 'SESS' + '%02d'%(sess+1), 'anat_gm.nii.gz')).get_data()
            ma = ma.reshape(ma.shape[0]*ma.shape[1]*ma.shape[2])
            idx = np.where(ma > 0)[0]

            # init the data arrays
            dv = np.zeros(n)
            vent = np.zeros(n)
            gm = np.zeros(n)
            raw = np.zeros((len(idx) * runs, len(freq)))
            noise = np.zeros((len(idx) * runs, len(freq)))
            signal = np.zeros((len(idx) * runs, len(freq)))

            ind = 0

            for run in range(runs):
                # load normalized periodograms
                files = os.listdir(os.path.join(modepath, 'SESS' + '%02d'%(sess+1), 'PARAMS'))
                for i, f in enumerate(files):
                    if files[i][:-6] == 'global_mean':
                        #power = load_periodogram(os.path.join('PARAMS', f), n)
                        freqs, power = load_PSD(os.path.join(modepath, 
                            'SESS' + '%02d'%(sess+1),'PARAMS', f), fs)
                        dv = np.vstack((dv, power))

                    elif files[i][:-6] == 'dv':
                        #power = load_periodogram(os.path.join('PARAMS', f), n)
                        freqs, power = load_PSD(os.path.join(modepath, 
                            'SESS' + '%02d'%(sess+1),'PARAMS', f), fs)
                        vent = np.vstack((vent, power))

                    elif files[i][:-6] == 'vent':
                        #power = load_periodogram(os.path.join('PARAMS', f), n)
                        freqs, power = load_PSD(os.path.join(modepath, 
                            'SESS' + '%02d'%(sess+1),'PARAMS', f), fs)
                        gm = np.vstack((gm, power))

                # load in unfiltered data
                ts = nib.load(os.path.join(path, expt, subj, mode,
                                          'SESS' + '%02d'%(sess+1),
                                          'func_scaled.' + '%02d'%(run+1) + '.nii.gz')).get_data()
                ts = ts.reshape(ts.shape[0]*ts.shape[1]*ts.shape[2], ts.shape[3])
                ts = ts[idx, :]
                
                for i, t in enumerate(ts):
                    power = sig.welch(t, fs=fs, 
                                         window='hann', 
                                         nperseg=20, 
                                         noverlap=None, 
                                         return_onesided=True)
                    
                    if np.sum(power[1] > 0):
                        power = power[1] / np.sum(power[1])
                        raw[i + ind, :] = power
                    else:
                        print 'hello doctor! ind = ' + str(i)
                        raw[i+ind, :] = raw[i+ind-1, :]

                # load in full noise model
                ts = nib.load(os.path.join(path, expt, subj, mode,
                                          'SESS' + '%02d'%(sess+1),
                                          'func_noise.' + '%02d'%(run+1) + '.nii.gz')).get_data()
                ts = ts.reshape(ts.shape[0]*ts.shape[1]*ts.shape[2], ts.shape[3])
                ts = ts[idx, :]
                
                for i, t in enumerate(ts):
                    power = sig.welch(t, fs=fs, 
                                         window='hann', 
                                         nperseg=20, 
                                         noverlap=None, 
                                         return_onesided=True)
                    if np.sum(power[1] > 0):
                        power = power[1] / np.sum(power[1])
                        noise[i + ind, :] = power
                    else:
                        print 'hello nurse! ind = ' + str(i)
                        noise[i+ind, :] = noise[i+ind-1, :]

                # load in residual signal
                filename = 'func_filtered.' + '%02d'%(run+1) + '.nii.gz'
                ts = nib.load(os.path.join(path, expt, subj, mode,
                                          'SESS' + '%02d'%(sess+1),
                                          filename)).get_data()
                ts = ts.reshape(ts.shape[0]*ts.shape[1]*ts.shape[2], ts.shape[3])
                ts = ts[idx, :]

                for i, t in enumerate(ts):
                    power = sig.welch(t, fs=fs, 
                                         window='hann', 
                                         nperseg=20, 
                                         noverlap=None, 
                                         return_onesided=True)

                    if np.sum(power[1] > 0):
                        power = power[1] / np.sum(power[1])
                        signal[i + ind, :] = power
                    else:
                        print 'hello judge! ind = ' + str(i)
                        signal[i + ind, :] = signal[i+ind-1, :]

                ind = ind + len(idx)

            # strip off empty vector
            dv = dv[1:, :]
            vent = vent[1:, :]
            gm = gm[1:, :]

            # calculate mean, sd, sem from data
            sd_raw = np.std(raw, axis=0)
            sd_fit = np.std(noise, axis=0)
            sd_sig = np.std(signal, axis=0)
            sd_drv = np.std(dv, axis=0)
            sd_vnt = np.std(vent, axis=0)
            sd_grm = np.std(gm, axis=0)

            se_raw = sd_raw / np.repeat(np.sqrt(raw.shape[0]), raw.shape[1])
            se_fit = sd_fit / np.repeat(np.sqrt(noise.shape[0]), noise.shape[1])
            se_sig = sd_sig / np.repeat(np.sqrt(signal.shape[0]), signal.shape[1])
            se_drv = sd_drv / np.repeat(np.sqrt(dv.shape[0]), n)
            se_vnt = sd_vnt / np.repeat(np.sqrt(vent.shape[0]), n)
            se_grm = sd_grm / np.repeat(np.sqrt(gm.shape[0]), n)

            mu_raw = np.mean(raw, axis=0)
            mu_fit = np.mean(noise, axis=0)
            mu_sig = np.mean(signal, axis=0)
            mu_drv = np.mean(dv, axis=0) 
            mu_vnt = np.mean(vent, axis=0)
            mu_grm = np.mean(gm, axis=0)

            ## loglog spectra plot : brain noise as scale free?
            y_min = np.min(np.concatenate((mu_drv[1:],
                                           mu_vnt[1:],
                                           mu_grm[1:],
                                           mu_fit[1:],
                                           mu_sig[1:])))
            y_max = np.max(np.concatenate((mu_drv,
                                           mu_vnt,
                                           mu_grm,
                                           mu_fit,
                                           mu_sig)))


            # compare noise and signal models
            fig, ax = plt.subplots(nrows=3, 
                                   ncols=1,
                                   figsize=(4, 12),
                                   dpi=72,
                                   facecolor='white')

            # compare overall models
            ax[0].loglog(freq, mu_raw, color='black', linewidth=2, label='Raw Data')
            ax[0].fill_between(freq, mu_raw + sd_raw, mu_raw, color='black', 
                                                            alpha=0.5)
            ax[0].fill_between(freq, mu_raw - sd_raw, mu_raw, color='black', 
                                                            alpha=0.5)
            ax[0].loglog(freq, mu_raw + se_raw, color='black', linestyle='-.', 
                                                             linewidth=0.5)
            ax[0].loglog(freq, mu_raw - se_raw, color='black', linestyle='-.', 
                                                             linewidth=0.5)

            ax[0].loglog(freq, mu_fit, color='blue', linewidth=2, label='Noise Model')
            ax[0].fill_between(freq, mu_fit + sd_fit, mu_fit, color='blue', 
                                                            alpha=0.5)
            ax[0].fill_between(freq, mu_fit - sd_fit, mu_fit, color='blue', 
                                                            alpha=0.5)
            ax[0].loglog(freq, mu_fit + se_fit, color='blue', linestyle='-.', 
                                                            linewidth=0.5)
            ax[0].loglog(freq, mu_fit - se_fit, color='blue', linestyle='-.', 
                                                            linewidth=0.5)

            ax[0].loglog(freq, mu_sig, color='red', linewidth=2, label='Residuals')
            ax[0].fill_between(freq, mu_sig + sd_sig, mu_sig, color='red', 
                                                            alpha=0.5)
            ax[0].fill_between(freq, mu_sig - sd_sig, mu_sig, color='red', 
                                                            alpha=0.5)
            ax[0].loglog(freq, mu_sig + se_sig, color='red', linestyle='-.', 
                                                           linewidth=0.5)
            ax[0].loglog(freq, mu_sig - se_sig, color='red', linestyle='-.', 
                                                           linewidth=0.5)

            ax[0].set_ylim((y_min, y_max))
            ax[0].set_xlim((freq[1], freq[-1]))

            ax[0].legend(loc=3, fontsize=10, frameon=False)

            # compare individual regressors
            ax[1].loglog(freq, mu_drv, color='black', linewidth=2, label='Draining Veins')
            ax[1].fill_between(freq, mu_drv + sd_drv, mu_drv, color='black', 
                                                            alpha=0.5)
            ax[1].fill_between(freq, mu_drv - sd_drv, mu_drv, color='black', 
                                                            alpha=0.5)
            ax[1].loglog(freq, mu_drv + se_drv,  color='black', linestyle='-.', 
                                                              linewidth=0.5)
            ax[1].loglog(freq, mu_drv + se_drv,  color='black', linestyle='-.', 
                                                              linewidth=0.5)

            ax[1].loglog(freq, mu_vnt, color='blue', linewidth=2, label='Ventricles')
            ax[1].fill_between(freq, mu_vnt + sd_vnt, mu_vnt, color='blue', 
                                                            alpha=0.5)
            ax[1].fill_between(freq, mu_vnt - sd_vnt, mu_vnt, color='blue', 
                                                            alpha=0.5)
            ax[1].loglog(freq, mu_vnt + se_vnt, color='blue', linestyle='-.', 
                                                            linewidth=0.5)
            ax[1].loglog(freq, mu_vnt - se_vnt, color='blue', linestyle='-.', 
                                                            linewidth=0.5)

            ax[1].loglog(freq, mu_grm, color='red', linewidth=2, label='Global Mean')
            ax[1].fill_between(freq, mu_grm + sd_grm, mu_grm, color='red', 
                                                            alpha=0.5)
            ax[1].fill_between(freq, mu_grm - sd_grm, mu_grm, color='red', 
                                                            alpha=0.5)
            ax[1].loglog(freq, mu_grm + se_grm, color='red', linewidth=0.5, 
                                                           linestyle='-.')
            ax[1].loglog(freq, mu_grm - se_grm, color='red', linewidth=0.5, 
                                                           linestyle='-.')

            ax[1].set_ylim((y_min, y_max))
            ax[1].set_xlim((freq[1], freq[-1]))

            ax[1].legend(loc=3, fontsize=10, frameon=False)

            # compare global mean with mean spectra
            ax[2].loglog(freq, mu_raw, color='black', linewidth=2, label='Raw Data')
            ax[2].fill_between(freq, mu_raw + sd_raw, mu_raw, color='black', 
                                                            alpha=0.5)
            ax[2].fill_between(freq, mu_raw - sd_raw, mu_raw, color='black', 
                                                            alpha=0.5)
            ax[2].loglog(freq, mu_raw + se_raw, color='black', linestyle='-.', 
                                                             linewidth=0.5)
            ax[2].loglog(freq, mu_raw - se_raw, color='black', linestyle='-.', 
                                                             linewidth=0.5)

            ax[2].loglog(freq, mu_grm, color='red', linewidth=2, label='Global Mean')
            ax[2].fill_between(freq, mu_grm + sd_grm, mu_grm, color='red', 
                                                            alpha=0.5)
            ax[2].fill_between(freq, mu_grm - sd_grm, mu_grm, color='red', 
                                                            alpha=0.5)
            ax[2].loglog(freq, mu_grm + se_grm, color='red', linestyle='-.', 
                                                           linewidth=0.5)
            ax[2].loglog(freq, mu_grm - se_grm, color='red', linestyle='-.', 
                                                           linewidth=0.5)

            ax[2].set_ylim((y_min, y_max))
            ax[2].set_xlim((freq[1], freq[-1]))

            ax[2].legend(loc=3, fontsize=10, frameon=False)

            fig.subplots_adjust(hspace=0.15)

            plt.suptitle(str(expt) + ' ' + str(mode) + ': ' + str(subj))
            plt.savefig(pdf, format='pdf')
            plt.close()

    # Add some metadata and close the PDF object
    d = pdf.infodict()
    d['Title'] = 'Quality Control: Spectra of data, modelled noise, residuals'
    d['Author'] = u'Joseph D Viviano\xe4nen'
    d['Subject'] = 'Quality Control'
    d['Keywords'] = 'QC modelled noise spectra'
    d['CreationDate'] = datetime.datetime.today()
    d['ModDate'] = datetime.datetime.today()
    pdf.close()

    # JDV