# -*- coding: utf-8 -*-
"""
GenZ analysis script for feedback related-negtivity FRN analysis.
"""
#'genz115_9a'
#  max(self.selection) + 1))]
#ValueError: max() arg is an empty sequence

import mnefun
import numpy as np
from score import (vis_names, vis_numbers)

params = mnefun.Params(tmin=-0.2, tmax=0.8, t_adjust=0, decim=4, lp_cut=80,
                       bmin=-0.2, bmax=0.0)
params.work_dir = '/brainstudio/MEG/genz/genz_proc/active'
params.subjects = ['genz332_13a']
params.subject_indices = np.arange(len(params.subjects))
# params.subject_indices = np.setdiff1d(np.arange(len(params.subjects)), [4,6,7])
params.run_names = [
    '%s_emojis_learn_01',
    '%s_faces_learn_01',
    '%s_thumbs_learn_01',
]
# Trial rejection
params.reject = dict()
params.auto_bad_reject = None
params.ssp_ecg_reject = None
params.flat = dict(grad=1e-13, mag=1e-15)
# Which runs and trials to use
params.on_missing = 'ignore'  # some subjects will not complete the paradigm
params.in_names = vis_names
params.in_numbers = vis_numbers
params.epochs_tag = '-FRN-epo'
# The ones we actually want
params.analyses = [
    'FRN',
    'FRN-Split',
    ]
params.out_names = [
    ['vis'],
    params.in_names,
    ]
params.out_numbers = [  # these don't matter as long as they don't overlap...
    [1] * len(params.in_names),
    100000 * np.arange(1, len(params.in_names) + 1),
    ]
params.must_match = [[]] * len(params.analyses)
mnefun.do_processing(
    params,
    write_epochs=True,
    print_status=False,
)

#import mne
#epo = mne.read_epochs('genz425_15a/epochs/All_80-sss_genz425_15a-FRN-epo.fif')
#epo.average().plot()
