#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 10 12:46:57 2019

@author: nordme
"""

##### Examine prek psds ######

import os
import os.path as op
import mne
import numpy as np
import matplotlib.pyplot as plt

sub_dir = '/storage/prek/'

skip = ['prek_1259', 'prek_1451', 'prek_1319', 'prek_1505', 'prek_1714']
subjects = [x for x in os.listdir('/storage/prek/') if op.isdir(x) and 'prek' in x and not np.in1d(x, skip)]
subjects.sort()
subjects = subjects[20:39]

save_dir = '/home/nordme/data/prek/psd/'

for subject in subjects: 
    erp_path = op.join(sub_dir, subject, 'sss_pca_fif',
                       '%s_erp_pre_allclean_fil80_raw_sss.fif' % subject)
    ssvep_path = op.join(sub_dir, subject, 'sss_pca_fif',
                       '%s_pskt_01_pre_allclean_fil80_raw_sss.fif' % subject)
    erp = mne.io.read_raw_fif(erp_path)
    ssvep = mne.io.read_raw_fif(ssvep_path)
    
    erp_plot = erp.plot_psd(fmin=0.5, fmax=20.0, show=False)
    erp_plot.savefig(op.join(save_dir,'%s_erp_psd.png' % subject))
    plt.close()
    
    ssvep_plot = ssvep.plot_psd(fmin=0.5, fmax=20.0, show=False)   
    ssvep_plot.savefig(op.join(save_dir, '%s_ssvep_psd.png' % subject))
    plt.close()