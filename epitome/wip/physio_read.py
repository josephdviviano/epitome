#!/usr/bin/env python

import numpy as np

import bioread as bio

data = bio.read_file("22005.acq")
data.channels

# [Channel resp: 2462018 samples, 500.0 samples/sec,
#  Channel CO2: 2462018 samples, 500.0 samples/sec,
#  Channel SPO2: 2462016 samples, 500.0 samples/sec,
#  Channel pulse waveform: 2462016 samples, 500.0 samples/sec,
#  Channel TTL pulse: 2462014 samples, 500.0 samples/sec, << - onsets and offsets
#  Channel SPO2 filtered: 2462014 samples, 500.0 samples/sec,
#  Channel Pulse Rate: 1231003 samples, 250.0 samples/sec]

#  