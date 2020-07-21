# -*- coding: utf-8 -*-
"""
GenZ analysis script for feedback related-negtivity FRN  and SPN analysis.
"""

import mnefun
import numpy as np
import os
import os.path as op
from score import (vis_names, vis_numbers, pick_vis_cov_events)

lp_cut = 80
raw_dir = '/storage/genz_active/t1/fixed_hp/'
subjects = [x for x in os.listdir(raw_dir) if 'genz' in x and op.isdir(op.join(raw_dir, x))]
# subjects = ['genz105_9a']
subjects.sort()

params = mnefun.Params(tmin=-2.1, tmax=0.8, t_adjust=0, decim=4, lp_cut=lp_cut,
                       bmin=-2.1, bmax=-2.0)

params.subjects = subjects
params.work_dir = raw_dir
params.subject_indices = np.setdiff1d(np.arange(len(params.subjects)), [])
params.run_names = [
    '%s_emojis_learn_01',
    '%s_faces_learn_01',
    '%s_thumbs_learn_01',
]
# Trial rejection
params.reject = dict(grad=2000e-13, mag=6000e-15)
params.flat = dict(grad=1e-13, mag=1e-15)
# Which runs and trials to use
params.on_missing = 'ignore'  # some subjects will not complete the paradigm
params.in_names = vis_names
params.in_numbers = vis_numbers
params.epochs_tag = '-vis-epo'
# params.inv_tag = 'all-sss'
# covariance params
params.inv_names = ['%s_vis']     # ['%s_aud', '%s_vis']
params.inv_runs = [np.arange(0,3)]
params.pick_events_cov = pick_vis_cov_events
params.compute_rank = True
params.cov_rank = None
params.cov_rank_method = 'compute_rank'
params.cov_rank_tol = 5e-2
params.cov_method = 'shrunk'
cov = '%s_vis-' + str(lp_cut) + '-sss-cov.fif'
# params.force_erm_cov_rank_full = False
# params.runs_empty = ['%s_erm_01']
# The ones we actually want
params.analyses = [
    'vis',
    'vis-Split',
    ]
params.out_names = [
    ['vis'],
    params.in_names,
    ]
params.out_numbers = [  # these don't matter as long as they don't overlap...
    [1] * len(params.in_names),
    100000 * np.arange(1, len(params.in_names) + 1),
    ]
params.must_match = [[]] * len(params.analyses)  # not matching for twa_hp run (for Eric)
# params.must_match = [None] * len(params.analyses)  # do matching for sensor space run

mnefun.do_processing(
    params,
    write_epochs=True,
    gen_covs=False,
    gen_inv=False,
    print_status=False,
)

