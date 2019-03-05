# -*- coding: utf-8 -*-

"""This is a script written to allow researchers to read in data line by line and explore it as it transforms."""

import os
import os.path as op
import mne
import mnefun

raw_dir = '/home/nordme/data/speak_imagine/'
save_dir = '/home/nordme/data/speak_imagine/'

f_name = 'erica_task_speak_imagine_01_raw.fif'
f_name1 = 'erica'
f_path = op.join(raw_dir, f_name)

# populate the directory with all of the sub-directories we'll need for our products along the way

raw
sss
tsss
gen ssp
apply ssp
epochs
averages
covariances
forwards
inverses


# read in the raw data

raw = mne.io.read_raw_fif(f_path, allow_maxshield=True)

raw.copy()

print(raw)

raw.crop(tmin=5., tmax=25.)

data, times = raw[:, :]

print(data.shape)

print(data)


# clean the data

# our very first step is SSS, starting with head position estimation

sss_out = '_pos'

sss = run_sss_command(raw, fname_out=sss_out)

from mnefun import run_sss

# epochs and averages






#