#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 18:00:23 2019

@author: nordme
"""

import os
import os.path as op
import mne
from mne.minimum_norm import (apply_inverse, read_inverse_operator)
import numpy as np

# set important variables

#raw_dir = '/home/nordme/data/genz/genz_active/'

stc_dir = '/brainstudio/MEG/genz/genz_proc/active/twa_hp/dSPM_ave/auditory'

stcs = [s[0:-7] for s in os.listdir(stc_dir) if '-lh' in s and 'both' in s]
stcs.sort()


peak_amplitudes= []
percentiles = []

for stc in stcs:
    print('Working on stc %s' % stc)
    stc_path = op.join(stc_dir, stc )
    stc_actual = mne.read_source_estimate(stc_path)
    peak_vertex, peak_time = stc_actual.get_peak(vert_as_index=True, time_as_index=True)
    peak_ampl = stc_actual.data[peak_vertex, peak_time]
    percentiles.append([stc, np.percentile(stc_actual.data, 0), np.percentile(stc_actual.data, 25), 
                        np.percentile(stc_actual.data, 75), np.percentile(stc_actual.data, 100),
                        ])
    peak_amplitudes.append([stc, peak_vertex, peak_time, peak_ampl])
    print('Saved percentiles and peak amplitudes for stc %s' % stc)
    
    
print('percentiles: \n %s' % percentiles)
print('peak amplitudes: \n %s' % peak_amplitudes)
# print('peak times: \n %s' % peak_amplitudes[:, 2])

# create a nice graph of the peak amplitudes by age

# nines = 

# elevens = 

# thirteens = 

# fifteens = 

# seventeens = 
