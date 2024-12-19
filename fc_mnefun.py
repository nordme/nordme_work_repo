#!/usr/bin/env python2
# -*- coding: utf-8 -*-


import mnefun
import numpy as np


raw_dir = '/data/fc/'
subjects = ['fc_6mo_305']

# INITIALIZE

acdc_params = mnefun.Params(tmin=-0.05, tmax=1.0, n_jobs=8,
                            decim=1, n_jobs_mkl=8, proj_sfreq=250,
                            n_jobs_fir=8, n_jobs_resample=8,
                            filter_length='auto', epochs_type='fif',
                            lp_cut=80., hp_cut=1.0,
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
acdc_params.sss_type = 'python'
acdc_params.tsss_dur = 4.0
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


# JOBS

mnefun.do_processing(
    acdc_params,
    do_sss = True,
)

