# -*- coding: utf-8 -*-

"""This script is a template for processing data using mnefun."""

# imports

import mne
import mnefun

# paths to important places

raw_dir =

# subjects

subjects = []

# parameters needed by mnefun functions

study_params = mnefun.Params()

# multiple functions need the following parameters

study_params.
study_params.
study_params.
study_params.
study_params.
study_params.
study_params.
study_params.

# for fetch_raw
study_params.
study_params.
study_params.

# for do_score
study_params.
study_params.
study_params.

# for push_raw
study_params.
study_params.
study_params.

# for do_sss
# SSS denoising params
self.sss_type = 'maxfilter'
self.mf_args = ''
self.tsss_dur = 60.
self.trans_to = 'median'  # where to transform head positions to
self.sss_format = 'float'  # output type for MaxFilter
self.movecomp = 'inter'
self.int_order = 8
self.ext_order = 3
self.st_correlation = .98
self.sss_origin = 'auto'
self.sss_regularize = 'in'
self.filter_chpi = True
study_params.
study_params.
study_params.

# for fetch_sss
study_params.
study_params.
study_params.

# for channel fixing
study_params.
study_params.
study_params.

# for do_ssp
study_params.
study_params.
study_params.

# for apply_ssp
study_params.
study_params.
study_params.

# for write_epochs
study_params.
study_params.
study_params.

# timing parameters

self.tmin = tmin  # minimum time for events
self.tmax = tmax  # maximum time for events

self.reject_tmin = reject_tmin
self.reject_tmax = reject_tmax

self.t_adjust = t_adjust # set this if you need to compensate for trigger delays


# parameters for setting a baseline
# baseline compensation is for making a noise covariance matrix
# when you have spontaneous activity going on (as opposed to evoked activity that you will turn into epochs)

self.baseline = baseline
self.bmin = bmin  # lower limit for baseline compensation
self.bmax = bmax  # upper limit for baseline compensation

# general parameters
self.subjects = []
self.run_names = None  # this parameter allows you to have multiple files per subject; generally condition name is the variable
self.inv_names = None  # this parameter lets you separate inverse solutions (i.e. between conditions)
self.inv_runs = None # how many files per inverse solution
self.work_dir = os.getcwd()



# tell mnefun where to find ecg and eog channels

self.ecg_channel = ecg_channel
self.eog_channel = eog_channel

# set how many cores you want to use to do processing

self.n_jobs = n_jobs # a general number of cores to use
self.n_jobs_mkl = n_jobs_mkl # Jobs for MKL threading (prob 1 or 2)
self.n_jobs_fir = n_jobs_fir  # Jobs when doing FIR filtering
self.n_jobs_resample = n_jobs_resample

# parameters for filtering
self.filter_length = filter_length
self.cont_lp = 5
self.lp_cut = lp_cut # cutoff for lowpass filtering (eliminates high frequency noise)
self.hp_cut = hp_cut # cutoff for highpass filtering (eliminates low frequency noise)
self.lp_trans = lp_trans # transition band for lowpass
self.hp_trans = hp_trans
self.phase = 'zero-double'
self.fir_window = 'hann'
self.fir_design = 'firwin2'
self.disp_files = True
self.plot_drop_logs = False  # plot drop logs after do_preprocessing_
self.proj_sfreq = proj_sfreq # projector sample frequency
self.decim = decim # how much to decimate data while epoching

# parameters for epoching

self.drop_thresh = drop_thresh # percentage threshold (for plotting Epochs drop_log)


self.match_fun = match_fun # a function to equalize event counts
self.epochs_type = epochs_type


self.bem_type = bem_type # can be 5120 or 5120-5120-5120

self.fwd_mindist = fwd_mindist

self.auto_bad = auto_bad  # max number of events disqualified by channel before channel itself becomes excluded automatically
self.auto_bad_reject = None
self.auto_bad_flat = None
self.auto_bad_meg_thresh = 10
self.auto_bad_eeg_thresh = 10


self.plot_raw = plot_raw


# names of sub-directories under the subject directory; these directories are created during processing
self.epochs_dir = 'epochs'
self.cov_dir = 'covariance'
self.inverse_dir = 'inverse'
self.forward_dir = 'forward'
self.list_dir = 'lists'
self.trans_dir = 'trans'
self.bad_dir = 'bads'
self.raw_dir = 'raw_fif'
self.sss_dir = 'sss_fif'
self.pca_dir = 'sss_pca_fif'


# extensions that get added to file names when files are being created by processing
self.epochs_tag = '-epo'
self.inv_tag = '-sss'
self.inv_fixed_tag = '-fixed'
self.inv_loose_tag = ''
self.inv_free_tag = '-free'
self.inv_erm_tag = '-erm'
self.eq_tag = 'eq'
self.sss_fif_tag = '_raw_sss.fif'
self.bad_tag = '_post-sss.txt'
self.keep_orig = False # This is used by fix_eeg_channels to fix original files
self.raw_fif_tag = '_raw.fif'
self.cal_file = None
self.ct_file = None

# boolean for whether data set(s) have an individual mri
self.on_process = None

# Use more than EXTRA points to fit headshape
self.dig_with_eeg = False


# covariance parameters
self.pick_events_cov = None # Function to pick a subset of events to use to make a covariance
self.cov_method = cov_method


self.proj_extra = None

# These should be overridden by the user unless they are only doing
# a small subset, e.g. epoching

self.structurals = None
self.dates = None
self.score = None  # defaults to passing events through
self.acq_ssh = self.acq_dir = None
self.acq_port = 22
self.sws_ssh = self.sws_dir = None
self.sws_port = 22
self.subject_indices = []
self.get_projs_from = []
self.runs_empty = []
self.proj_nums = [[0] * 3] * 3
self.in_names = []
self.in_numbers = []
self.analyses = []
self.out_names = []
self.out_numbers = []
self.must_match = []
self.on_missing = 'error'  # for epochs
self.subject_run_indices = None
self.autoreject_thresholds = False
self.autoreject_types = ('mag', 'grad', 'eeg')
self.subjects_dir = None
self.src_pos = 7.
self.report_params = dict(
    good_hpi_count=True,
    head_movement=True,
    psd=True,
    ssp_topomaps=True,
    source_alignment=True,
    bem=True,
    source=None,
    )
self.rotation_limit = np.inf
self.translation_limit = np.inf
self.coil_bad_count_duration_limit = np.inf  # for annotations
self.coil_dist_limit = 0.005
self.coil_t_window = 0.2  # default is same as MF
self.coil_t_step_min = 0.01
self.proj_ave = False
self.compute_rank = False
self.cov_rank = 'full'
self.force_erm_cov_rank_full = True  # force empty-room inv rank

# specify what jobs to do

mnefun.do_processing(
    study_params,
    fetch_raw = False,
    do_score = False,
    push_raw = False,
    do_sss = False,
    fetch_sss = False,
    do_ch_fix = False,
    do_ssp = False,
    apply_ssp = False,
    write_epochs = False
)


import os
import os.path as op
import mne
import mnefun
import numpy as np
from prek_score import (prek_score, prek_in_names, prek_in_numbers, prek_out_names, prek_out_numbers)

raw_dir = '/home/nordme/data/prek/'

# subjects

subjects = [x for x in os.listdir(raw_dir) if op.isdir(op.join(raw_dir, x)) and 'prek' in x]

mne.preprocessing.maxwell_filter()

# INITIALIZE

prek_params = mnefun.Params(tmin=-0.05, tmax=1.0, n_jobs=6,
                       decim=2, n_jobs_mkl=1, proj_sfreq=250,
                       n_jobs_fir=6, n_jobs_resample=6,
                       filter_length='auto', epochs_type='fif', lp_cut=40.,
                       bmin=-0.05, plot_raw=False)

# GENERAL
prek_params.work_dir = '/home/nordme/data/prek/'
prek_params.subjects = subjects
prek_params.run_names = None  # this parameter allows you to have multiple files per subject; generally condition name is the variable
prek_params.subject_indices = []
prek_params.subject_run_indices = None
prek_params.subjects_dir = None
prek_params.disp_files = True # display files --- this parameter has your script say the files its working on

# set how many cores you want to use to do processing
prek_params.n_jobs = n_jobs # a general number of cores to use
prek_params.n_jobs_mkl = n_jobs_mkl # Jobs for MKL threading (prob 1 or 2)
prek_params.n_jobs_fir = n_jobs_fir  # Jobs when doing FIR filtering
prek_params.n_jobs_resample = n_jobs_resample

# SSS
prek_params.sss_type = 'python'
prek_params.mf_args = '' # maxfilter arguments. Only used with sss_type = 'maxfilter' (remote maxfiltering, not python)
prek_params.tsss_dur = 4.
prek_params.trans_to = (.0, .0, 0.04)  # where to transform head positions to
prek_params.sss_format = 'float'  # output type for MaxFilter
prek_params.movecomp = 'inter'
prek_params.int_order = 8
prek_params.ext_order = 3
prek_params.st_correlation = .98
prek_params.sss_origin = 'auto'
prek_params.sss_regularize = 'in'
prek_params.filter_chpi = True

    # parameters for filtering
prek_params.filter_length = filter_length
prek_params.cont_lp = 5
prek_params.lp_cut = lp_cut # cutoff for lowpass filtering (eliminates high frequency noise)
prek_params.hp_cut = hp_cut # cutoff for highpass filtering (eliminates low frequency noise)
prek_params.lp_trans = lp_trans # transition band for lowpass
prek_params.hp_trans = hp_trans
prek_params.phase = 'zero-double'
prek_params.fir_window = 'hann'
prek_params.fir_design = 'firwin2'

    # params for movement comp
prek_params.rotation_limit = np.inf
prek_params.translation_limit = np.inf
prek_params.coil_bad_count_duration_limit = np.inf  # for annotations
prek_params.coil_dist_limit = 0.005
prek_params.coil_t_window = 0.2  # default is same as MF
prek_params.coil_t_step_min = 0.01

# SSP

prek_params.proj_extra = None # set this if you've got extra projectors to use
prek_params.proj_sfreq = proj_sfreq # projector sample frequency
prek_params.ecg_channel = ecg_channel
prek_params.eog_channel = eog_channel
prek_params.get_projs_from = range(len(params.run_names))
prek_params.proj_nums = [[1, 1, 0],  # ECG: grad/mag/eeg
                            [1, 1, 0],  # EOG
                            [0, 0, 0]]
prek_params.proj_ave = False


# EPOCHS

prek_params.score = prek_score  # defaults to passing events through

prek_params.in_names = prek_in_names   # Names of input events.
prek_params.in_numbers = prek_in_numbers # Event numbers (in scored event files) associated with each name.

prek_params.analyses = []

prek_params.out_names = prek_out_names # Event types to make out of old ones.
# Event numbers to convert to (e.g., [[1, 1, 2, 3, 3], ...] would create
# three event types, where the first two and last two event types from
# the original list get collapsed over).
prek_params.out_numbers = prek_out_numbers


# epoching settings

# must_match: Indices from the original in_names that must match in event counts
#        before collapsing. Should eventually be expanded to allow for
#        ratio-based collapsing.

prek_params.must_match = []
prek_params.match_fun = None # Set this if you wrote your own function to equalize event counts

prek_params.tmin = tmin  # minimum time for events
prek_params.tmax = tmax  # maximum time for events

prek_params.reject_tmin = reject_tmin  # defaults to tmin
prek_params.reject_tmax = reject_tmax  # defaults to tmax

prek_params.t_adjust = t_adjust # set this if you need to compensate for trigger delays

prek_params.decim = decim # how much to decimate data while epoching

prek_params.on_missing = 'error'  # for epochs

# epoch rejection

prek_params.drop_thresh = drop_thresh # percentage threshold (for plotting Epochs drop_log)

prek_params.epochs_type = epochs_type
prek_params.auto_bad = None  # max number of events disqualified by channel before channel becomes excluded automatically
prek_params.auto_bad_reject = None
prek_params.auto_bad_flat = None
prek_params.autoreject_thresholds = False
prek_params.reject = dict(grad=3500e-13, mag=4.0e-12, eog=150e-6)
prek_params.ssp_eog_reject = dict(grad=3500e-13, mag=4.0e-12)
prek_params.ssp_ecg_reject = dict(grad=3500e-13, mag=4.0e-12)
# prek_params.auto_bad_reject = dict(grad=3500e-13, mag=4.0e-12)
# prek_params.auto_bad_flat = dict(grad=1e-13, mag=1e-15)


# COVARIANCE


    # parameters for setting a baseline
    # baseline compensation is for making a noise covariance matrix
    # when you have spontaneous activity going on (as opposed to evoked activity that you will turn into epochs)

prek_params.baseline = baseline
prek_params.bmin = bmin  # lower limit for baseline compensation
prek_params.bmax = bmax  # upper limit for baseline compensation

    # covariance parameters
prek_params.pick_events_cov = None # Function to pick a subset of events to use to make a covariance
prek_params.cov_method = 'empirical'
prek_params.compute_rank = False
prek_params.cov_rank = 'full'
prek_params.force_erm_cov_rank_full = True  # force empty-room inv rank

# FORWARDS

    # boolean for whether data set(s) have an individual mri
prek_params.on_process = None
prek_params.bem_type = bem_type # can be 5120 or 5120-5120-5120
prek_params.fwd_mindist = fwd_mindist
prek_params.structurals = None
prek_params.src_pos = 7.


# INVERSES

prek_params.inv_names = None  # this parameter lets you separate inverse solutions (i.e. between conditions)
prek_params.inv_runs = None # how many files per inverse solution


# REPORTS

prek_params.plot_drop_logs = False  # plot drop logs after do_preprocessing_
prek_params.report_params = dict(
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
    prek_params,
    do_score = True,
    do_sss = True,
    gen_ssp = True,
    apply_ssp = True,
    write_epochs = True,
    gen_covs = False,  # Generate covariances
    gen_fwd = False,  # Generate forward solutions (and source space if needed)
    gen_inv = False,  # Generate inverses
    gen_report = False,
    print_status = True
)

