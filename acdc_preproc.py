# -*- coding: utf-8 -*-

"""This script is a template for processing data using mnefun."""

# imports

import mne
import mnefun
import os
import os.path as op

# paths to important places

raw_dir = '/home/nordme/data/eeg_data/'

# subjects


# parameters needed by mnefun functions

acdc_params = mnefun.Params(tmin=-0.1, tmax=0.75, t_adjust=0,
                       decim=4, n_jobs_mkl=1, proj_sfreq=200,
                       filter_length='auto', lp_cut=80., bmin=-0.1,
                       lp_trans='auto', bem_type='inner_skull')

# SSS denoising params
acdc_params.sss_type = 'python'
acdc_params.tsss_dur = 20.
acdc_params.trans_to = 'twa'  # where to transform head positions to
acdc_params.movecomp = 'inter'
acdc_params.st_correlation = .98
acdc_params.sss_regularize = 'in'
acdc_params.filter_chpi = True
acdc_params.mf_autobad_type='python'
acdc_params.mf_autobad=True

# general parameters
acdc_params.subjects = ['acdc_eeg_meg_adult']
acdc_params.run_names = ['%s']   # this parameter allows you to have multiple files per subject; generally condition name is the variable
acdc_params.inv_names = None  # this parameter lets you separate inverse solutions (i.e. between conditions)
acdc_params.inv_runs = None # how many files per inverse solution
acdc_params.work_dir = raw_dir
acdc_params.get_projs_from = range(len(acdc_params.run_names))
acdc_params.proj_nums = [[1, 1, 0],  # ECG: grad/mag/eeg
                         [0, 0, 0],  # EOG
                         [0, 0, 0]]

# set how many cores you want to use to do processing

acdc_params.n_jobs = 6 # a general number of cores to use
acdc_params.n_jobs_mkl = 6 # Jobs for MKL threading (prob 1 or 2)
acdc_params.n_jobs_fir = 6 # Jobs when doing FIR filtering
acdc_params.n_jobs_resample = 6


# parameters for epoching


acdc_params.bem_type = 5120 # can be 5120 or 5120-5120-5120
acdc_params.auto_bad = None  # max number of events disqualified by channel before channel becomes excluded automatically
acdc_params.auto_bad_reject = None

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

# names of sub-directories under the subject directory; these directories are created during processing
acdc_params.epochs_dir = 'epochs'
acdc_params.cov_dir = 'covariance'
acdc_params.inverse_dir = 'inverse'
acdc_params.forward_dir = 'forward'
acdc_params.list_dir = 'lists'
acdc_params.trans_dir = 'trans'
acdc_params.bad_dir = 'bads'
acdc_params.raw_dir = 'raw_fif'
acdc_params.sss_dir = 'sss_fif'
acdc_params.pca_dir = 'sss_pca_fif'


# extensions that get added to file names when files are being created by processing
acdc_params.epochs_tag = '-epo'
acdc_params.inv_tag = '-sss'
acdc_params.inv_fixed_tag = '-fixed'
acdc_params.inv_loose_tag = ''
acdc_params.inv_free_tag = '-free'
acdc_params.inv_erm_tag = '-erm'
acdc_params.eq_tag = 'eq'
acdc_params.sss_fif_tag = '_raw_sss.fif'
acdc_params.bad_tag = '_post-sss.txt'
acdc_params.keep_orig = False # This is used by fix_eeg_channels to fix original files
acdc_params.raw_fif_tag = '_raw.fif'
acdc_params.cal_file = None
acdc_params.ct_file = None

# boolean for whether data set(s) have an individual mri
acdc_params.on_process = None

# covariance parameters

acdc_params.cov_method = 'empirical'

# These should be overridden by the user unless they are only doing
# a small subset, e.g. epoching

acdc_params.structurals = None
acdc_params.dates = None
acdc_params.score = None  # defaults to passing events through
acdc_params.sws_ssh = 'nordme@kasga.ilabs.uw.edu'  # kasga
acdc_params.sws_dir = '/data07/nordme/genz'
acdc_params.sws_port = 22
acdc_params.subject_indices = [0]
acdc_params.in_names = []
acdc_params.in_numbers = []
acdc_params.analyses = ['All']
acdc_params.out_names = []
acdc_params.out_numbers = []
acdc_params.must_match = [[]] * len(acdc_params.analyses)
acdc_params.on_missing = 'ignore'  # for epochs
acdc_params.subject_run_indices = None
acdc_params.autoreject_thresholds = False
acdc_params.autoreject_types = ('mag', 'grad')
acdc_params.subjects_dir = None
acdc_params.report_params = dict(
    good_hpi_count=True,
    head_movement=True,
    psd=True,
    ssp_topomaps=True,
    source_alignment=True,
    bem=True,
    source=None,
    )
acdc_params.coil_dist_limit = 0.005
acdc_params.coil_t_window = 0.2  # default is same as MF
acdc_params.coil_t_step_min = 0.01
acdc_params.proj_ave = False
acdc_params.compute_rank = False
acdc_params.cov_rank = True
acdc_params.force_erm_cov_rank_full = True  # force empty-room inv rank

# specify what jobs to do

mnefun.do_processing(
    acdc_params,
    fetch_raw = False,
    do_score = False,
    push_raw = False,
    do_sss = False,
    fetch_sss = False,
    do_ch_fix = False,
    gen_ssp = False,
    apply_ssp = False,
    write_epochs = True
)

