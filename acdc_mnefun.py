#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import os
import os.path as op
import mne
import mnefun
import numpy as np

#def pacc_score(p, subjects):

#    events = mne.find


raw_dir = '/home/nordme/data/for_499/'

subjects = ['littrell_ryan']

# subjects = [x for x in os.listdir(raw_dir) if op.isdir(op.join(raw_dir, x)) and 'pitchacc' in x]

# INITIALIZE

acdc_params = mnefun.Params(tmin=-0.05, tmax=1.0, n_jobs=18,
                            decim=1, n_jobs_mkl=18, proj_sfreq=250,
                            n_jobs_fir=18, n_jobs_resample=18,
                            filter_length='auto', epochs_type='fif', lp_cut=100.,
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
acdc_params.tsss_dur = 4.
acdc_params.trans_to = (0., 0., 0.04)  # where to transform head positions to
acdc_params.sss_format = 'float'  # output type for MaxFilter
acdc_params.movecomp = 'inter'
acdc_params.int_order = 8
acdc_params.ext_order = 3
acdc_params.st_correlation = .98
acdc_params.sss_origin = 'auto'
acdc_params.sss_regularize = 'in'
acdc_params.filter_chpi = True

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

acdc_params.score = None
acdc_params.analyses = ['All', 'Split']

acdc_params.in_names = ['pitches', 'speech']
acdc_params.in_numbers = [4, 8]

acdc_params.out_names = [['All'], ['Split']]
acdc_params.out_numbers = [[1, 1], [1, 2]]

#out_numbers: Event numbers to convert to (e.g., [[1, 1, 2, 3, 3], ...] would create
# three event types, where the first two and last two event types from
# the original list get collapsed over).

# epoching settings

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
# pacc_params.ssp_eog_reject = dict(grad=3500e-13, mag=4.0e-12)
# pacc_params.ssp_ecg_reject = dict(grad=3500e-13, mag=4.0e-12)

# pacc_params.auto_bad_reject = dict(grad=3500e-13, mag=4.0e-12)
# pacc_params.auto_bad_flat = dict(grad=1e-13, mag=1e-15)


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

acdc_params.plot_drop_logs = False  # plot drop logs after do_preprocessing_
acdc_params.report_params = dict(
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
    acdc_params,
    do_score = False,
    do_sss = True,
    gen_ssp = False,
    apply_ssp = False,
    write_epochs = False,
    gen_covs = False,  # Generate covariances
    gen_fwd = False,  # Generate forward solutions (and source space if needed)
    gen_inv = False,  # Generate inverses
    gen_report = False,
    print_status = True
)

