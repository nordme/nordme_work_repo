#!/usr/bin/env python2
# -*- coding: utf-8 -*-


import mnefun
import numpy as np
from acdc_score import (score_acdc, score_acdc_eeg)

raw_dir = '/home/nordme/data/eeg_data/'

subjects = ['acdc_eeg_meg_adult']


# INITIALIZE

acdc_params = mnefun.Params(tmin=-0.05, tmax=1.0, n_jobs=18,
                            decim=1, n_jobs_mkl=18, proj_sfreq=250,
                            n_jobs_fir=18, n_jobs_resample=18,
                            filter_length='auto', epochs_type='fif', lp_cut=80.,
                            bmin=-0.05, plot_raw=False)

# GENERAL
acdc_params.work_dir = raw_dir
acdc_params.subjects = subjects
acdc_params.run_names = ['%s'] # this parameter allows you to have multiple files per subject; generally condition name is the variable
acdc_params.subject_indices = np.arange(len(subjects))
acdc_params.subject_run_indices = None
acdc_params.subjects_dir = None
acdc_params.disp_files = True # display files --- this parameter has your script say the files its working on

# SSS
acdc_params.sws_ssh = 'nordme@kasga.ilabs.uw.edu'  # kasga
acdc_params.sws_dir = '/data07/nordme/genz'
acdc_params.sss_type = 'python'
acdc_params.tsss_dur = 20.
acdc_params.trans_to = 'twa'  # where to transform head positions to
acdc_params.movecomp = 'inter'
acdc_params.st_correlation = .98
acdc_params.sss_regularize = 'in'
acdc_params.hp_type='python'
acdc_params.filter_chpi = True
acdc_params.mf_autobad_type='python'
acdc_params.mf_autobad=True

# parameters for filtering
acdc_params.cont_lp = 5
acdc_params.phase = 'zero-double'
acdc_params.fir_window = 'hann'
acdc_params.fir_design = 'firwin2'

# params for movement comp
acdc_params.rotation_limit = np.inf
acdc_params.translation_limit = np.inf
acdc_params.coil_bad_count_duration_limit = np.inf  # for annotations
acdc_params.coil_dist_limit = 0.005
acdc_params.coil_t_window = 0.2  # default is same as maxfilter
acdc_params.coil_t_step_min = 0.01

# SSP
acdc_params.get_projs_from = range(len(acdc_params.run_names))
acdc_params.proj_nums = [[1, 1, 0],  # ECG: grad/mag/eeg
                         [0, 0, 0],  # EOG
                         [0, 0, 0]]
acdc_params.proj_ave = False

# EPOCHS

acdc_params.score = score_acdc(acdc_params)
acdc_params.reject_epochs_by_annot=True
acdc_params.analyses = ['All']
acdc_params.in_names = ['standard', 'oddball1', 'oddball2']
acdc_params.in_numbers = [1, 3, 4]
acdc_params.out_names = [acdc_params.in_names]
acdc_params.out_numbers = [acdc_params.in_numbers]
acdc_params.must_match=[[]*(len(acdc_params.analyses))]
# must_match: Indices from the original in_names that must match in event counts
#        before collapsing. List of lists
acdc_params.on_missing = 'warning'  # for epochs

# epoch rejection

acdc_params.auto_bad = None  # max number of events disqualified by channel before channel becomes excluded automatically
acdc_params.auto_bad_reject = None
acdc_params.auto_bad_flat = None
acdc_params.autoreject_thresholds = False
acdc_params.reject = dict()
acdc_params.flat = dict(grad=1e-13, mag=1e-15)


# COVARIANCE

# covariance
# pacc_params.pick_events_cov = pick_cov_events_pacc # Function to pick a subset of events to use to make a covariance
acdc_params.cov_method = 'empirical'
acdc_params.cov_rank = 'full'

# FORWARDS

# boolean for whether data set(s) have an individual mri
acdc_params.on_process = None
acdc_params.structurals = acdc_params.subjects


# INVERSES

acdc_params.inv_names = None  # this parameter lets you separate inverse solutions (i.e. between conditions)
acdc_params.inv_runs = None  # how many files per inverse solution


# REPORTS
show = [{"analysis":'All', "name":'%s' % kind}
        for kind in ('standard', 'oddball1', 'oddball2')
        ]

acdc_params.plot_drop_logs = False  # plot drop logs after do_preprocessing_
acdc_params.report_params = dict(
    good_hpi_count=True,
    head_movement=True,
    psd=True,
    ssp_topomaps=True,
    raw_segments=True,
    sensor=show,
    source_alignment=False,
    bem=False,
    source=False,
    covariance=False,
    drop_log=False,
    whitening=False,
    snr=False
    )

# JOBS

mnefun.do_processing(
    acdc_params,
    do_score = False,
    do_sss = False,
    gen_ssp = False,
    apply_ssp = False,
    write_epochs = False,
    gen_covs = False,  # Generate covariances
    gen_fwd = False,  # Generate forward solutions (and source space if needed)
    gen_inv = False,  # Generate inverses
    gen_report = True,
    print_status = False
)

