import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt
import scipy.fftpack as fft
import scipy.signal as sig
import scipy as sp
import os

def load_periodogram(path, n):
    power = np.genfromtxt(path)
    power = sig.detrend(power)
    power = fft.fft(power)[0:n]
    power = np.abs(power)
    power = power / sum(power)
    return power

def load_welch_PSD(path):
    tmp = np.genfromtxt(path)
    tmp = sig.welch(tmp, fs=fs, 
                         window='hann', 
                         nperseg=20, 
                         noverlap=None, 
                         return_onesided=True)

    freqs = tmp[0]
    power = tmp[1] / np.sum(tmp[1])
    return freqs, power

# some frequency stuff
# fslhd func_MNI.01.nii.gz | sed -n 22p
TR = 2.5

if TR >= 1000:
    TR = TR / 1000

fs = 1.0 / TR
ny = fs / 2.0

# number and list of frequency bins
#n = len(np.genfromtxt('PARAMS/global_mean.02.1D'))/2
#freq = np.linspace(0, ny, n)

freq = load_welch_PSD('PARAMS/global_mean.02.1D')[0]
n = len(freq) 

# load normalized periodograms
files = os.listdir('PARAMS')
dv = np.zeros(n)
vent = np.zeros(n)
gm = np.zeros(n)

for i, f in enumerate(files):
    if files[i][:-6] == 'global_mean':
        #power = load_periodogram(os.path.join('PARAMS', f), n)
        freqs, power = load_welch_PSD(os.path.join('PARAMS', f))
        dv = np.vstack((dv, power))

    elif files[i][:-6] == 'dv':
        #power = load_periodogram(os.path.join('PARAMS', f), n)
        freqs, power = load_welch_PSD(os.path.join('PARAMS', f))
        vent = np.vstack((vent, power))

    elif files[i][:-6] == 'vent':
        #power = load_periodogram(os.path.join('PARAMS', f), n)
        freqs, power = load_welch_PSD(os.path.join('PARAMS', f))
        gm = np.vstack((gm, power))

dv = dv[1:, :]
vent = vent[1:, :]
gm = gm[1:, :]

# load in full noise model
ts = nib.load('func_noise.01.nii.gz').get_data()
ma = nib.load('anat_gm.nii.gz').get_data()
dim = ts.shape
ts = ts.reshape(dim[0]*dim[1]*dim[2], dim[3])
ma = ma.reshape(dim[0]*dim[1]*dim[2])
idx = np.where(ma > 0)[0]
ts = ts[idx, :]
noise = np.zeros((len(idx), len(freq)))

for i, t in enumerate(ts):
    power = sig.welch(t, fs=fs, 
                       window='hann', 
                       nperseg=20, 
                       noverlap=None, 
                       return_onesided=True)

    power = power[1] / np.sum(power[1])
    noise[i, :] = power

# load in retained signal
ts = nib.load('func_filtered.01.nii.gz').get_data()
ma = nib.load('anat_gm.nii.gz').get_data()
dim = ts.shape
ts = ts.reshape(dim[0]*dim[1]*dim[2], dim[3])
ma = ma.reshape(dim[0]*dim[1]*dim[2])
idx = np.where(ma > 0)[0]
ts = ts[idx, :]

signal = np.zeros((len(idx), len(freq)))
for i, t in enumerate(ts):
    power = sig.welch(t, fs=fs, 
                       window='hann', 
                       nperseg=20, 
                       noverlap=None, 
                       return_onesided=True)

    power = power[1] / np.sum(power[1])
    signal[i, :] = power

noise_sem  = np.std(noise, axis=0) / np.repeat(np.sqrt(noise.shape[0]), noise.shape[1])
noise_mean = np.mean(noise, axis=0)

signal_sem  = np.std(signal, axis=0) / np.repeat(np.sqrt(signal.shape[0]), signal.shape[1])
signal_mean = np.mean(signal, axis=0)

dv_sem = np.std(dv, axis=0) / np.repeat(np.sqrt(dv.shape[0]), n)
dv_mean = np.mean(dv, axis=0)

vent_sem = np.std(vent, axis=0) / np.repeat(np.sqrt(vent.shape[0]), n)
vent_mean = np.mean(vent, axis=0)

gm_sem = np.std(gm, axis=0) / np.repeat(np.sqrt(gm.shape[0]), n)
gm_mean = np.mean(gm, axis=0)

# # normalized peridograms of timeseries
# plt.subplot(2,1,1)

# # draining vessles
# markerline, stemlines, baseline = plt.stem(freqs, dv_mean)
# plt.setp(markerline, 'markerfacecolor', 'red')
# plt.setp(stemlines, 'color','red', 'linewidth', 2)

# # ventricles
# markerline, stemlines, baseline = plt.stem(freqs, vent_mean)
# plt.setp(markerline, 'markerfacecolor', 'blue')
# plt.setp(stemlines, 'color','blue', 'linewidth', 2)

# # global signal oh my
# markerline, stemlines, baseline = plt.stem(freqs, gm_mean)
# plt.setp(markerline, 'markerfacecolor', 'green')
# plt.setp(stemlines, 'color','green', 'linewidth', 2)

# labels = []
# bins = plt.xticks()[0]
# for ind in bins:
#     ind = int(ind)
#     if ind > 0:
#         ind = ind - 1
#     label = str(freq[int(ind)])
#     labels.append(label[:4])
# plt.xticks(bins, labels)
# plt.xticks(bins, labels)

# # set bottom to be black as the night
# plt.setp(baseline, 'color','black', 'linewidth', 1)

# loglog plot
y_min = np.min(np.concatenate((dv_mean[1:], vent_mean[1:], gm_mean[1:], pxx_mean[1:])))
y_max = np.max(np.concatenate((dv_mean, vent_mean, gm_mean, pxx_mean[1:])))


# compare noise and signal models
plt.subplot(2,1,1)

# full noise model
plt.loglog(freq, noise_mean, color='black')
plt.loglog(freq, noise_mean + noise_sem, color='black', alpha=0.5)
plt.loglog(freq, noise_mean - noise_sem, color='black', alpha=0.5)

# full signal model
plt.loglog(freq, signal_mean, color='grey')
plt.loglog(freq, signal_mean + signal_sem, color='grey', alpha=0.5)
plt.loglog(freq, signal_mean - signal_sem, color='grey', alpha=0.5)

plt.ylim((y_min, y_max))
plt.xlim((freq[1], freq[-1]))

# compare individual regressors
plt.subplot(2,1,2)

# draining vessels
plt.loglog(freq, dv_mean, color='green')
plt.loglog(freq, dv_mean + dv_sem, color='green', alpha=0.5)
plt.loglog(freq, dv_mean + dv_sem, color='green', alpha=0.5)

# ventricles
plt.loglog(freq, vent_mean, color='blue')
plt.loglog(freq, vent_mean + vent_sem, color='blue', alpha=0.5)
plt.loglog(freq, vent_mean - vent_sem, color='blue', alpha=0.5)

# global mean
plt.loglog(freq, gm_mean, color='red')
plt.loglog(freq, gm_mean + gm_sem, color='red', alpha=0.5)
plt.loglog(freq, gm_mean - gm_sem, color='red', alpha=0.5)

plt.ylim((y_min, y_max))
plt.xlim((freq[1], freq[-1]))