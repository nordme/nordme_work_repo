# -*- coding: utf-8 -*-

import mne
import os.path as op
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator)

subjects = ['genz_c126']
raw_files = ['%s_rest_raw.fif']
#data_dir = '/data/genz/ep_t2/'
data_dir = '/media/erica/data1/genz_control'
ecg_ch = 'ECG001'
#ecg_ch = 'ECG063'

for subject in subjects:
    for file in raw_files:
        save_path = op.join(data_dir, subject, '%s_ecg_plot.png' % subject)
        raw_path = op.join(data_dir, subject, 'raw_fif', file % subject)
        raw = mne.io.read_raw_fif(raw_path, allow_maxshield=True)
        time_sample = raw.times[-1]/5
        data = []
        for x in range(4):
            tmin = (time_sample*x) + 1
            tmax = tmin + 4
            print('tmin: %s' % tmin)
            print('tmax: %s' % tmax)
            crop = raw.copy().crop(tmin, tmax)
#            crop.pick_types(ecg=True)
            data.append(crop.get_data(picks=[ecg_ch]))

        fig, axes = plt.subplots(nrows=4, ncols=1, figsize=(22,16))

        for i, ax in enumerate(axes):

            y = data[i][0]
            y *= 1000000
            y_mean = y.mean()
            y = y - y_mean
            x = np.arange(0, 4001)
            ax.plot(x, y)

            ax.set_xlim([0, 4005])
            ax.set_xticks(ticks=(0, 1000, 2000, 3000, 4000))
            ax.set_xticklabels((0, 1, 2, 3, 4))
            ax.set_xlabel('Seconds')
            ax.set_ylim([-800, 800])
            ax.set_ylabel('microvolts')

            ax.xaxis.set_major_locator(MultipleLocator(1000))
            ax.xaxis.set_minor_locator(MultipleLocator(40))
            ax.yaxis.set_major_locator(MultipleLocator(500))
            ax.yaxis.set_minor_locator(MultipleLocator(100))

            ax.grid(visible=True, color='0.7', which='both')

        fig.suptitle('%s ECG for %s' % (subject, file.split('_')[1]))
        fig.savefig(save_path)
