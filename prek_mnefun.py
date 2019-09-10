# -*- coding: utf-8 -*-

"""
Created on Fri May 17 7:11:32 2019

@author: mdclarke

mnefun processing script for PreK Project

Notes:
1) run preprocessing (up to gen_covs)
2) run prek_setup_source.py
3) coregistration (mne coreg)
4) run fwd + inv (this script)

1 = words (N=30)
2 = faces (N=30)
3 = cars (N=30)
4 = aliens (N=10) + 10 button responses

"""
import mnefun
import numpy as np
import os
import os.path as op
from prek_score import prek_score

dir = '/home/nordme/data/prek/post_camp/twa_hp/'

params = mnefun.Params(tmin=-0.1, tmax=1, t_adjust=-0.067, n_jobs=18,
                       proj_sfreq=200, n_jobs_fir=18,
                       filter_length='5s', lp_cut=80., 
                       n_jobs_resample=18,
                       bmin=-0.1, bem_type='5120')
#1451 rename
skip = ['prek_1259', 'prek_1451']
subjects = [x for x in os.listdir(dir) if op.isdir(op.join(dir, x)) and 'prek' in x and not np.in1d(x, skip)]
# subjects = ['prek_1110']
subjects.sort()

structurals = ['PREK_%s' % x[5:9] for x in subjects]

params.score = prek_score
params.work_dir = dir
params.subjects = subjects
params.structurals = structurals
params.dates = [(2013, 0, 00)] * len(params.subjects)
# define which subjects to run
params.subject_indices = np.arange(len(params.subjects))
# params.subject_indices = np.setdiff1d(np.arange(len(params.subjects)), np.arange(41))
# Aquistion params 
params.acq_ssh = 'nordme@kasga.ilabs.uw.edu'
params.acq_dir = '/brainstudio/prek/'
params.sws_ssh = 'nordme@kasga.ilabs.uw.edu'
params.sws_dir = '/data07/nordme/prek/'
# SSS options
params.sss_type = 'python'
params.sss_regularize = 'in'
params.tsss_dur = 4. # tSSS duration
params.int_order = 8
params.st_correlation = .98
params.trans_to='twa' # time weighted average head position (change this to fixed pos for group analysis)
params.coil_t_window = 'auto'
params.movecomp='inter'
# remove segments with < 3 good coils for at least 100 ms
params.coil_bad_count_duration_limit = 0.1
# Trial rejection criteria
params.reject = dict()
params.auto_bad_reject = None
params.ssp_ecg_reject = None
params.flat = dict(grad=1e-13, mag=1e-15)
params.auto_bad_flat = None
params.auto_bad_meg_thresh = 10
# naming
# params.run_names = ['%s_erp_pre']
params.run_names = ['%s_erp_post']
params.get_projs_from = np.arange(1)
params.inv_names = ['%s']
params.inv_runs = [np.arange(1)]
params.runs_empty = []
# proj
params.proj_nums = [[1, 1, 0],  # ECG: grad/mag/eeg
                    [1, 1, 0],  # EOG
                    [0, 0, 0]]  # Continuous (from ERM)
params.cov_method = 'empirical'
params.bem_type = '5120'
params.compute_rank = True

# Epoching
params.score = prek_score
params.in_names = ['words', 'faces', 'cars', 'aliens']
params.in_numbers = [10, 20, 30, 40]
params.analyses = ['All',
                   'Conditions']
params.out_names = [['All'],
                    ['words', 'faces', 'cars', 'aliens']]
params.out_numbers = [[10, 10, 10, 10],  # Combine all trials
                      [10, 20, 30, 40],  # Separate trials
    ]
params.must_match = [
    [], # trials to match
    [],
    ]

params.report_params.update(  # add plots
    bem=True, 
    good_hpi_count=True,
    sensor=[
        dict(analysis='Conditions', name='words', times='peaks'),
        dict(analysis='Conditions', name='faces', times='peaks'),
        dict(analysis='Conditions', name='cars', times='peaks'),
        dict(analysis='Conditions', name='aliens', times='peaks'),
    ],
    source=[
        dict(analysis='Conditions', name='words',
             inv='%s-80-sss-meg-free-inv.fif',
             views=['lat', 'caudal'], size=(800, 800)), 
        dict(analysis='Conditions', name='faces',
             inv='%s-80-sss-meg-free-inv.fif', 
             views=['lat', 'caudal'], size=(800, 800)),
        dict(analysis='Conditions', name='cars',
             inv='%s-80-sss-meg-free-inv.fif',
             views=['lat', 'caudal'], size=(800, 800)),
        dict(analysis='Conditions', name='aliens',
             inv='%s-80-sss-meg-free-inv.fif',
             views=['lat', 'caudal'], size=(800, 800)),
    ],
    snr=[
        dict(analysis='Conditions', name='words',
             inv='%s-80-sss-meg-free-inv.fif'),
        dict(analysis='Conditions', name='faces',
             inv='%s-80-sss-meg-free-inv.fif'),
        dict(analysis='Conditions', name='cars',
             inv='%s-80-sss-meg-free-inv.fif'),
        dict(analysis='Conditions', name='aliens',
             inv='%s-80-sss-meg-free-inv.fif')
    ],
    psd=False,
)

mnefun.do_processing(
    params,
    fetch_raw=False,
    do_sss=False, # do tSSS
    do_score=False,  # do scoring
    gen_ssp=False, # generate ssps
    apply_ssp=False, # apply ssps
    write_epochs=False, # epoching & filtering
    gen_covs=False, # make covariance
    gen_fwd=False, # generate fwd model
    gen_inv=False, # general inverse
    gen_report=False, #print report
    print_status=True # show status
)
