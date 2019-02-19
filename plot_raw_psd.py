# -*- coding: utf-8 -*-

import mne
import os
import os.path as op
import matplotlib.pyplot as plt

files = ['one_back_control_1000_330_raw.fif',
         # 'one_back_down_1000_330_raw.fif',
         'one_back_fardown_1000_330_raw.fif',
         'five_back_control_1000_330_raw.fif',
         # 'five_back_down_1000_330_raw.fif',
         'five_back_fardown_1000_330_raw.fif',
         # 'five_back_down_2000_660_raw.fif',
         # 'five_back_fardown_2000_660_raw.fif'
         'one_front_control_1000_330_raw.fif',
         'one_front_forward_1000_330_raw.fif',
         'five_front_control_1000_330_raw.fif',
         'five_front_forward_1000_330_raw.fif'
         ]

raw_dir = '/home/nordme/data/cHPI_test'
save_dir = '/home/nordme/data/cHPI_test'

channel_picks = [[2631, 2632, 2633],
                 [1411, 1412, 1413],
                 [811, 812, 813],
                 [1111, 1112, 1113],
                 [1531, 1532, 1533]]



for f in files:
    f_path = (op.join(raw_dir, f))
    raw = mne.io.read_raw_fif(f_path, allow_maxshield=True)
    raw.info['bads'] += ['MEG1743', 'MEG1842']
    settings = mne.pick_types(raw.info, exclude='bads', chpi=True)
    plt.figure()
    ax = plt.axes()
    ax.set_title('%s' % f)
    fig = raw.plot_psd(picks=settings)
    plt.show()
