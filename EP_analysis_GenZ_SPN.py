# -*- coding: utf-8 -*-
"""
GenZ analysis script for SPN analysis.
"""

import mnefun
import numpy as np
from score import (score, vis_names, vis_numbers,
                   pick_aud_cov_events, pick_vis_cov_events)

params = mnefun.Params(tmin=-2.2, tmax=0.1, t_adjust=0, decim=4, lp_cut=80,
                       bmin=-2.2, bmax=-2.0)
params.work_dir = '/brainstudio/MEG/genz/genz_proc/active'
params.subjects = ['genz324_13a', 'genz428_15a']
params.subject_indices = np.arange(len(params.subjects))
#params.subject_indices = np.setdiff1d(np.arange(len(params.subjects)), [4,6,7]) 
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
params.epochs_tag = '-SPN-epo'
# The ones we actually want
params.analyses = [
    'SPN',
    'SPN-Split',
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
#epo = mne.read_epochs('genz425_15a/epochs/All_80-sss_genz425_15a-SPN-epo.fif')
#epo.average().plot()
