# -*- coding: utf-8 -*-

# imports, paths, subjects

import mne
import mnefun
import os
import os.path as op
import numpy as np
import matplotlib.pyplot as plt

fetch_dir = '/home/nordme/data/genz/genz_active/'
save_dir = '/home/nordme/data/genz/genz_active/'

subjects = ['genz334_13a']

use_mnefun = False

# set mnefun parameters

# general params
genz_params = mnefun.Params()
genz_params.subjects = subjects
genz_params.work_dir = save_dir   # top level directory where you're putting processed data
genz_params.raw_dir = 'raw_fif'   # sub-directory under the subject folder where raw files are stored
genz_params.subject_indices = np.setdiff1d(np.arange(len(genz_params.subjects)), [])
genz_params.subject_run_indices = np.arange(0,1,1)
genz_params.run_names = ['%s_emojis_learn_01']

# SSP parameters



# do SSP with mnefun




# do SSP from mne-python straight up

