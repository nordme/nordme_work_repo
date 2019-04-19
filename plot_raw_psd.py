# -*- coding: utf-8 -*-

import mne
import os
import os.path as op
import matplotlib.pyplot as plt

files = ['one_back_d0_1000_330_raw.fif',
         'two_back_d0_1000_330_raw.fif',
         'three_back_d0_1000_330_raw.fif',
         'four_back_d0_1000_330_raw.fif',
         'five_back_d0_1000_330_raw.fif' ]

raw_dir = '/home/nordme/data/cHPI_test/raw'
save_dir = '/home/nordme/data/cHPI_test/images'

channel_picks = [[2631, 2632, 2633],
                 [1411, 1412, 1413],
                 [811, 812, 813],
                 [1111, 1112, 1113],
                 [1531, 1532, 1533]]
files = ['erm_01_raw.fif']

for f in files:
    f_path = (op.join(raw_dir, f))
    raw = mne.io.read_raw_fif(f_path, allow_maxshield=True)
    raw.info['bads'] += ['MEG1743', 'MEG1842']
    settings = mne.pick_types(raw.info, exclude='bads', chpi=True)
    fig = raw.plot_psd(picks=settings)
    plt.show()
    fig.savefig(op.join(save_dir, '%s_psd.png' % f[:-4]))
