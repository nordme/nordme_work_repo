# -*- coding: utf-8 -*-
import mne
import numpy as np

subject = 'erica_peterson'

raw = mne.io.read_raw_fif(f'/media/erica/Rocstor/infslow/{subject}/raw_fif/{subject}_erp_pre_raw.fif', allow_maxshield=True)
sim =mne.io.read_raw_fif(f'/media/erica/Rocstor/infslow/{subject}/raw_fif/infraslow_6s_high_pos_raw.fif', allow_maxshield=True)
sum_save = f'/media/erica/Rocstor/infslow/{subject}/raw_fif/raw_sum_6s_high_pos_raw.fif'

rd = raw.copy().load_data().pick('meg')         # 306 x n_samples
sd = sim.copy().load_data().pick('meg')          # 306 x k_samples; k=speed*sfreq, k<n
rd = rd._data
sd = sd._data

rd[156] = (rd[153] + rd[159])/2

dsum = sd.copy() if len(sd[0]) < len(rd[0]) else rd.copy()
length = min(len(sd[0]), len(rd[0]))
for i in np.arange(length):
    dsum[:, i] += rd[:, i]          # add values from inf wave to raw data

dsum = dsum[:, :length]

d_extra = raw.get_data()[306:, :length]
dsum = np.vstack((dsum, d_extra))   # put back stim channel, etc

raw_sum = sim.copy().load_data() if len(sd[0]) < len(rd[0]) else raw.copy().load_data()
raw_sum._data = dsum
raw_sum.save(sum_save, overwrite=True)




