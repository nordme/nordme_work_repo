# -*- coding: utf-8 -*-
"""
GenZ pilot analysis script.
@author: Kambiz Tavabi
@contact: ktavabi@gmail.com
@license: MIT
@date: 04/21/2018
"""

import os.path as op
import mnefun
import numpy as np
# from picks import names, bad_channels

params = mnefun.Params(n_jobs=6, tmin=-1., tmax=1.,
                       decim=5, proj_sfreq=200,
                       n_jobs_fir=4, n_jobs_resample=4,
                       filter_length='auto', lp_cut=80.,
                       lp_trans='auto', bem_type='5120')


params.subjects = ['genz126_9a',
                   'genz125_9ab',
                   'genz128_9ab',
                   'genz529_17ab',
                   'genz530_17a',
                   'genz530_17ab',
                   'genz530_17ac']

params.work_dir = '/brainstudio/MEG/genz/genz_proc/resting'
params.subject_indices = [0]
params.subjects_dir = '/brainstudio/MEG/genz/anatomy'
# write prebads

params.force_erm_cov_rank_full = False
params.dates = [None] * len(params.subjects)
params.structurals = params.subjects
params.subject_run_indices = None
#  params.subjects_dir = '/brainstudio/data/genz/freesurf_subjs'
params.score = None
params.run_names = ['%s_rest_01']
params.runs_empty = ['%s_erm_01']  # Define empty room runs
# params.acq_ssh = 'kambiz@minea.ilabs.uw.edu'
# params.acq_dir = ['/sinuhe/data01/genz', '/sinuhe/data03/genz']
params.sws_ssh = 'nordme@kasga.ilabs.uw.edu'  # kasga
params.sws_dir = '/data07/nordme/genz'
params.sss_type = 'python'
params.sss_regularize = 'in'
params.st_correlation = 0.98
params.trans_to = 'twa'
params.tsss_dur = 300.
# Set the parameters for head position estimation:
params.coil_dist_limit = 0.01
params.coil_t_window = 'auto'  # use the smallest reasonable window size
# remove segments with < 3 good coils for at least 1 sec
params.coil_bad_count_duration_limit = 1.  # sec
# Annotation params
params.rotation_limit = 20.  # deg/s
params.translation_limit = 0.01  # m/s
# Trial rejection
params.reject = dict()
params.proj_ave = True
params.flat = dict(grad=1e-13, mag=1e-15)
# Which runs and trials to use
params.get_projs_from = np.arange(1)
params.inv_names = ['%s']
params.inv_runs = [np.arange(1)]
params.proj_nums = [[2, 2, 0],  # ECG: grad/mag/eeg
                    [2, 2, 0],  # EOG
                    [0, 0, 0]]  # Continuous (from ERM)
params.on_missing = 'ignore'  # some subjects will not complete the paradigm
params.report_params.update(
    bem=True,
    psd=True,  # often slow
    ssp=True,
    source_alignment=True

)

mnefun.do_processing(
    params,
    fetch_raw=False,
    do_score=False,
    push_raw=False,
    do_sss=False,
    fetch_sss=False,
    do_ch_fix=False,
    gen_ssp=False,
    apply_ssp=False,
    write_epochs=False,
    gen_covs=False,
    gen_fwd=False,
    gen_inv=False,
    gen_report=True,
    print_status=True,
)
