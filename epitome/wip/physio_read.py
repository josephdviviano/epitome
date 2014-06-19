#!/usr/bin/env python

import numpy as np
import scipy.signal as sig
import bioread as bio
import matplotlib.pyplot as plt

data = bio.read_file("22005.acq")
data.channels

# [Channel resp: 2462018 samples, 500.0 samples/sec,
#  Channel CO2: 2462018 samples, 500.0 samples/sec,
#  Channel SPO2: 2462016 samples, 500.0 samples/sec,
#  Channel pulse waveform: 2462016 samples, 500.0 samples/sec,
#  Channel TTL pulse: 2462014 samples, 500.0 samples/sec, << - onsets and offsets
#  Channel SPO2 filtered: 2462014 samples, 500.0 samples/sec,
#  Channel Pulse Rate: 1231003 samples, 250.0 samples/sec]

ttl_dat = data.channels[4].data

def find_transitions(ttl_dat):
	"""
	Takes TTL data, returns an equal-length vector with 1s @ onsets & offsets.
	"""
	# normalize TTL data & set small values to == 0
	ttl_dat_max = np.max(ttl_dat)
	ttl_dat = ttl_dat / ttl_dat_max

	ttl_dat_negatives = np.where(ttl_dat < 0.1)[0]
	ttl_dat[ttl_dat_negatives] = 0

	## find peaks (values > 0)
	ttl_idx = np.where(ttl_dat > 0)[0]
	ttl_dif = np.diff(ttl_idx)

	## find all of the transition points
	trans = np.array([])
	for x in np.unique(ttl_dif):
		if len(np.where(ttl_dif == x)[0]) == 1:
			trans = np.append(trans, np.where(ttl_dif == x)[0]) # offsets

	trans = np.union1d(trans, trans+1) # add onset
	trans = ttl_idx[trans.tolist()] # find most transition indicies
	trans = np.append(ttl_idx[0], trans) # add in the 1st transition
	trans = trans[:-1] # remove the stop signal

	# generate a vector of onsets & offsets
	ttl_out = np.zeros(len(ttl_dat))
	ttl_out[trans.tolist()] = 1

	return ttl_out

# plot normalized data
ttl_dat_max = np.max(ttl_dat)
plt.plot(ttl_dat / float(ttl_dat_max))
plt.plot(ttl_out)

#ttl_idx_max = np.max(ttl_idx)
#plt.plot(ttl_idx / float(ttl_idx_max))

#ttl_dif_max = np.max(ttl_dif)
#plt.plot(ttl_dif / float(ttl_dif_max))
