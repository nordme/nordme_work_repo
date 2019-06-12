# -*- coding: utf-8 -*-

import mne
import os
import os.path as op
import matplotlib.pyplot as plt
from itertools import product

# bands = [[0.1, 22], [20, 42], [38, 55], [62, 80], [85, 105]]

# bands = [[14, 18], [26, 33], [37, 44], [69, 74], [97, 102]]

bands = [[0.1, 105]]

raw_dir = '/home/nordme/data/cHPI_test/raw'
save_dir = '/home/nordme/data/cHPI_test/psd'

files = ['/home/nordme/data/cHPI_test/raw/erm_01_raw.fif',
         '/home/nordme/data/cHPI_test/raw/line_d0_1000_330_raw.fif',
         '/home/nordme/data/cHPI_test/raw/square_d0_1000_330_raw.fif',
         #'/home/nordme/data/cHPI_test/raw/square_but_mmdirect_1000_330_raw.fif',
         '/home/nordme/data/cHPI_test/raw/square_but_mmdirect_1000_330_MXSOFF_raw.fif',
         '/home/nordme/data/cHPI_test/raw/one_back_d0_1000_330_raw.fif',
         '/home/nordme/data/cHPI_test/raw/two_back_d0_1000_330_raw.fif',
         '/home/nordme/data/cHPI_test/raw/three_back_d0_1000_330_raw.fif',
         '/home/nordme/data/cHPI_test/raw/four_back_d0_1000_330_raw.fif',
         '/home/nordme/data/cHPI_test/raw/five_back_d0_1000_330_raw.fif',
         '/home/nordme/data/cHPI_test/raw/low_int_1_d0_1000_330_raw.fif',
         '/home/nordme/data/cHPI_test/raw/low_int_2_d0_1000_330_raw.fif',
         '/home/nordme/data/cHPI_test/raw/low_int_3_d0_1000_330_raw.fif']



for (f, [fmin, fmax]) in product(files, bands):
    if 'low_int' in f:
        f_path = f
        raw = mne.io.read_raw_fif(f_path, allow_maxshield=True)
        raw.info['bads'] += ['MEG1743', 'MEG1842', 'MEG1811', 'MEG1433']
        settings = mne.pick_types(raw.info, exclude='bads', chpi=True)
        fig = raw.plot_psd(picks=settings, fmin=fmin, fmax=fmax, average=True, area_mode='std')
        fig.suptitle(t='%s' % f[32:-16], x=0.5, y=0.01, va='top')
        plt.show()
        fig.savefig(op.join(save_dir, '%s%s_%s_std_psd.png' % (f[32:-16], fmin, fmax)))
        plt.close()
