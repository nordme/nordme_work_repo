#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import os
import os.path as op
import mne
import mnefun
import numpy as np
from prek_score_ep import (prek_score, prek_in_names, prek_in_numbers, prek_out_names, prek_out_numbers, pick_cov_events_prek)

raw_dir = '/storage/mmf/'

# subjects
skip = []
subjects = [x for x in os.listdir(raw_dir) if op.isdir(raw_dir + x) and 'mmf' in x and not np.in1d(x, skip)]


# INITIALIZE

mmf_params = mnefun.Params(tmin=-0.05, tmax=1.0, n_jobs=18,
                           decim=2, n_jobs_mkl=18, proj_sfreq=250,
                           n_jobs_fir=18, n_jobs_resample=18,
                           filter_length='5s', epochs_type='fif', lp_cut=80.,
                           bmin=-0.1, plot_raw=False, bem_type='5120')

# GENERAL
mmf_params.work_dir = raw_dir
mmf_params.subjects = subjects
mmf_params.run_names = ['%s'] # this parameter allows you to have multiple files per subject; generally condition name is the variable
mmf_params.subject_indices = np.arange(len(subjects))
mmf_params.subject_run_indices = None
mmf_params.subjects_dir = None
mmf_params.disp_files = True # display files --- this parameter has your script say the files its working on

# SSS
mmf_params.sws_ssh = 'nordme@kasga.ilabs.uw.edu'  # kasga
mmf_params.sws_dir = '/data07/nordme/mmf/'
mmf_params.sss_type = 'python'
mmf_params.tsss_dur = 4.
mmf_params.trans_to = 'twa'  # where to transform head positions to
mmf_params.sss_format = 'float'  # output type for MaxFilter
mmf_params.movecomp = 'inter'
mmf_params.int_order = 8
mmf_params.ext_order = 3
mmf_params.st_correlation = .98
mmf_params.sss_origin = 'auto'
mmf_params.sss_regularize = 'in'
mmf_params.filter_chpi = True

# parameters for filtering
mmf_params.cont_lp = 5
mmf_params.phase = 'zero-double'
mmf_params.fir_window = 'hann'
mmf_params.fir_design = 'firwin2'

# params for movement comp
mmf_params.rotation_limit = np.inf
mmf_params.translation_limit = np.inf
mmf_params.coil_bad_count_duration_limit = np.inf  # for annotations
mmf_params.coil_dist_limit = 0.005
mmf_params.coil_t_window = 0.2  # default is same as maxfilter
mmf_params.coil_t_step_min = 0.01

# SSP
mmf_params.get_projs_from = range(len(mmf_params.run_names))
mmf_params.proj_nums = [[1, 1, 0],  # ECG: grad/mag/eeg
                        [1, 1, 0],  # EOG
                        [0, 0, 0]]
mmf_params.proj_ave = False

# EPOCHS

mmf_params.must_match = []
mmf_params.on_missing = 'warning'  # for epochs

# epoch rejection

mmf_params.auto_bad = None  # max number of events disqualified by channel before channel becomes excluded automatically
mmf_params.auto_bad_reject = None
mmf_params.auto_bad_flat = None
mmf_params.autoreject_thresholds = False
mmf_params.reject = dict()
mmf_params.flat = dict(grad=1e-13, mag=1e-15)

# COVARIANCE

# covariance
mmf_params.cov_method = 'empirical'
mmf_params.compute_rank = True  # compute rank of the noise covariance matrix
mmf_params.cov_rank = None  # preserve cov rank when using advanced estimators
mmf_params.force_erm_cov_rank_full = False  # compute and use the empty-room rank

# FORWARDS

# boolean for whether data set(s) have an individual mri
mmf_params.on_process = None
mmf_params.structurals = ['fsaverage' * len(mmf_params.subjects)]

# INVERSES

mmf_params.inv_names = []  # this parameter lets you separate inverse solutions (i.e. between conditions)
mmf_params.inv_runs = []  # how many files per inverse solution

# REPORTS

mmf_params.plot_drop_logs = False  # plot drop logs after do_preprocessing_
mmf_params.report_params = dict(
    good_hpi_count=True,
    head_movement=True,
    psd=True,
    ssp_topomaps=True,
    source_alignment=True,
    bem=True,
    source=None,
    )

# JOBS

mnefun.do_processing(
    mmf_params,
    do_score = True,
    do_sss = False,
    gen_ssp = False,
    apply_ssp = False,
    write_epochs = False,
    gen_covs = False,  # Generate covariances
    gen_fwd = False,  # Generate forward solutions (and source space if needed)
    gen_inv = False,  # Generate inverses
    gen_report = False,
    print_status = True
)

