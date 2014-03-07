import numpy as np
import matplotlib.pyplot as plt
import scipy.fftpack as fft
import scipy.signal as sig
import os

def load_periodogram(path, n):
    tmp = np.genfromtxt(path)
    tmp = sig.detrend(tmp)
    tmp = fft.fft(tmp)[0:n]
    tmp = np.abs(tmp)
    tmp = tmp / sum(tmp)
    return tmp

# some frequency stuff
# fslhd func_MNI.01.nii.gz | sed -n 22p
TR = 2.5

if TR >= 1000:
    TR = TR / 1000

nyquist = 1 / TR / 2.0

# number and list of frequency bins
n = len(np.genfromtxt('PARAMS/global_mean.02.1D'))/2
freq = np.linspace(0, nyquist, n)

# load normalized periodograms
files = os.listdir('PARAMS')
dv = np.zeros(n)
vent = np.zeros(n)
gm = np.zeros(n)

for i, f in enumerate(files):
    if files[i][:-6] == 'global_mean':
        tmp = load_periodogram(os.path.join('PARAMS', f), n)
        dv = np.vstack((dv, tmp))

    elif files[i][:-6] == 'dv':
        tmp = load_periodogram(os.path.join('PARAMS', f), n)
        vent = np.vstack((vent, tmp))

    elif files[i][:-6] == 'vent':
        tmp = load_periodogram(os.path.join('PARAMS', f), n)
        gm = np.vstack((gm, tmp))

dv = dv[1:, :]
vent = vent[1:, :]
gm = gm[1:, :]

dv_sem = np.std(dv, axis=0) / np.repeat(np.sqrt(dv.shape[0]), n)
dv_mean = np.mean(dv, axis=0)

vent_sem = np.std(vent, axis=0) / np.repeat(np.sqrt(vent.shape[0]), n)
vent_mean = np.mean(vent, axis=0)

gm_sem = np.std(gm, axis=0) / np.repeat(np.sqrt(gm.shape[0]), n)
gm_mean = np.mean(gm, axis=0)

# normalized peridograms of timeseries
plt.subplot(2,1,1)

# draining vessles
markerline, stemlines, baseline = plt.stem(np.arange(n), dv_mean)
plt.setp(markerline, 'markerfacecolor', 'red')
plt.setp(stemlines, 'color','red', 'linewidth', 2)

# ventricles
markerline, stemlines, baseline = plt.stem(np.arange(n), vent_mean)
plt.setp(markerline, 'markerfacecolor', 'blue')
plt.setp(stemlines, 'color','blue', 'linewidth', 2)

# global signal oh my
markerline, stemlines, baseline = plt.stem(np.arange(n), gm_mean)
plt.setp(markerline, 'markerfacecolor', 'green')
plt.setp(stemlines, 'color','green', 'linewidth', 2)

labels = []
bins = plt.xticks()[0]
for ind in bins:
    ind = int(ind)
    if ind > 0:
        ind = ind - 1
    label = str(freq[int(ind)])
    labels.append(label[:4])
plt.xticks(bins, labels)

# set bottom to be black as the night
plt.setp(baseline, 'color','black', 'linewidth', 1)

# loglog plot
plt.subplot(2,1,2)
y_min = np.min(np.concatenate((dv_mean[1:], vent_mean[1:], gm_mean[1:])))
y_max = np.max(np.concatenate((dv_mean, vent_mean, gm_mean)))

plt.loglog(freq, dv_mean, color='red')
plt.loglog(freq, dv_mean + dv_sem, color='red', alpha=0.25)
plt.loglog(freq, dv_mean + dv_sem, color='red', alpha=0.25)

plt.loglog(freq, vent_mean, color='blue')
plt.loglog(freq, vent_mean + vent_sem, color='blue', alpha=0.25)
plt.loglog(freq, vent_mean - vent_sem, color='blue', alpha=0.25)

plt.loglog(freq, gm_mean, color='green')
plt.loglog(freq, gm_mean + gm_sem, color='green', alpha=0.25)
plt.loglog(freq, gm_mean - gm_sem, color='green', alpha=0.25)

plt.ylim((y_min, y_max))
plt.xlim((freq[1], freq[-1]))
