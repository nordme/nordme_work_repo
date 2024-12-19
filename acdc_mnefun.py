#!/usr/bin/env python2
# -*- coding: utf-8 -*-


import mnefun
import numpy as np
from acdc_score import (score_acdc, score_acdc_eeg)

# raw_dir = '/data/acdc/'
raw_dir = '/media/erica/Rocstor/infslow'
subjects = ['acdc']

# INITIALIZE

acdc_params = mnefun.Params(tmin=-0.05, tmax=1.0, n_jobs=8,
                            decim=1, n_jobs_mkl=8, proj_sfreq=250,
                            n_jobs_fir=8, n_jobs_resample=8,
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
acdc_params.trans_to = (0.0, 0.0, 0.04)  # where to transform head positions to
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
acdc_params.on_missing = 'warn'  # for epochs

# epoch rejection

acdc_params.auto_bad = None  # max number of events disqualified by channel before channel becomes excluded automatically
acdc_params.auto_bad_reject = None
acdc_params.auto_bad_flat = None
acdc_params.autoreject_thresholds = False
acdc_params.reject = dict(grad=2000e-13, mag=6000e-15)
acdc_params.flat = dict(grad=1e-13, mag=1e-15)


# COVARIANCE

# covariance
# pacc_params.pick_events_cov = pick_cov_events_pacc # Function to pick a subset of events to use to make a covariance
acdc_params.cov_method = 'shrunk'
acdc_params.compute_rank = True
acdc_params.cov_rank = None
acdc_params.cov_rank_method = 'compute_rank'
acdc_params.cov_rank_tol = 5e-2
acdc_params.cov_method = 'shrunk'

# FORWARDS

# boolean for whether data set(s) have an individual mri
acdc_params.on_process = None
acdc_params.structurals = acdc_params.subjects
acdc_params.bem_type = '5120'


# INVERSES

acdc_params.inv_names = ['%s']  # this parameter lets you separate inverse solutions (i.e. between conditions)
acdc_params.inv_runs = [0]  # how many files per inverse solution


# REPORTS
inv = '%s-80-sss-meg-inv.fif'
show = [{"analysis":'All', "name":'%s' % kind, 'inv': inv}
        for kind in ('standard', 'oddball1', 'oddball2')
        ]
cov = '%s-80-sss-cov.fif'
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
    source=show,
    covariance=cov,
    drop_log=False,
    whitening=show,
    snr=False
    )

# JOBS

mnefun.do_processing(
    acdc_params,
    do_score = False,
    do_sss = True,
    gen_ssp = True,
    apply_ssp = True,
    write_epochs = True,
    gen_covs = True,  # Generate covariances
    gen_fwd = False,  # Generate forward solutions (and source space if needed)
    gen_inv = True,  # Generate inverses
    gen_report = False,
    print_status = False
)

