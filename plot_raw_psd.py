# -*- coding: utf-8 -*-

import mne
import os
import os.path as op
import matplotlib.pyplot as plt
from itertools import product

# bands = [[0.1, 22], [20, 42], [38, 55], [62, 80], [85, 105]]

# bands = [[14, 18], [26, 33], [37, 44], [69, 74], [97, 102]]

bands = [[0.1, 105]]

raw_dir = '/home/nordme/data/cHPI_test/June_6/'
save_dir = '/home/nordme/data/cHPI_test/psd/June_6/'

files = [raw_dir + x for x in os.listdir(raw_dir)]


for (f, [fmin, fmax]) in product(files, bands):
#    if 'low_int' in f:
    f_path = f
    raw = mne.io.read_raw_fif(f_path, allow_maxshield=True)
    raw.info['bads'] += ['MEG1433']
    settings = mne.pick_types(raw.info, exclude='bads', chpi=True)
    fig = raw.plot_psd(picks=settings, fmin=fmin, fmax=fmax, average=False, area_mode='std')
    fig.suptitle(t='%s' % f[35:-8], x=0.5, y=0.01, va='top')
    plt.show()
    fig.savefig(op.join(save_dir, '%s_%s_%s_psd.png' % (f[35:-8], fmin, fmax)))
    plt.close()
