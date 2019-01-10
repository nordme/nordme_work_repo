# -*- coding: utf-8 -*-

import mne
import os
import os.path as op
import matplotlib.pyplot as plt

subjects = ['baby_doll']

raw_dir = '/home/nordme/data/cHPI_test'
save_dir = '/home/nordme/data/cHPI_test'

channel_picks = [[2631, 2632, 2633],
                 [1411, 1412, 1413],
                 [811, 812, 813],
                 [1111, 1112, 1113],
                 [1531, 1532, 1533]]



for s, c in zip(subjects, channel_picks):
    print(c[0])
    s_path = (op.join(raw_dir, s, 'initial_run_01_raw.fif'))
    raw = mne.io.read_raw_fif(s_path, allow_maxshield=True)
    raw.info['bads'] += ['MEG1743', 'MEG1842']
    settings = mne.pick_types(raw.info, exclude='bads', chpi=True)
    fig = mne.viz.plot_raw_psd(raw, picks=settings)
    plt.show()
