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
4 = aliens (N=10) + 10 button responses (64)

"""
import numpy as np
import mnefun
from prek_score import prek_score
import os
import os.path as op
# from analysis.aux_functions import load_paths, load_params

lp_cut = 30
pre_or_post = 'post'  # str: 'pre' or 'post' convenience variable for rerunning
ecg_reject = dict(grad=1500e-13, mag=4500e-15)
eog_reject = dict(grad=2000e-13, mag=6000e-15)

# load subjects
# *_, subjects, cohort = load_params()

# if cohort == 'replication':
#    target_dir = '/mnt/scratch/prek/r_cohort/%s_camp/twa_hp/erp/' % pre_or_post
#else:
#    target_dir = '/mnt/scratch/prek/%s_camp/twa_hp/erp/' % pre_or_post


pre_subs = ['prek_1103', 'prek_1262', 'prek_1401', 'prek_1490', 'prek_1751',
            'prek_1869', 'prek_1916', 'prek_2106', 'prek_2135', 'prek_2186',
            'prek_1184', 'prek_1208', 'prek_1113', 'prek_1293', 'prek_1210',
            'prek_1241', 'prek_1443', 'prek_1505', 'prek_1673', 'prek_1676',
            'prek_1798', 'prek_1812', 'prek_1921', 'prek_1951', 'prek_2116',
            'prek_2118', 'prek_2136', 'prek_2244']

post_subs = ['prek_1110', 'prek_1293', 'prek_1382', 'prek_1490', 'prek_1691',
            'prek_1762', 'prek_1818', 'prek_1936', 'prek_2110', 'prek_2135',
            'prek_2136', 'prek_2173', 'prek_2186', 'prek_2213', 'prek_1103',
            'prek_1208', 'prek_1210', 'prek_1460', 'prek_1673', 'prek_1798',
            'prek_1964', 'prek_2085', 'prek_2174', 'prek_1113',
            'prek_1443', 'prek_1401', 'prek_1756', 'prek_1869', 'prek_1812',
            'prek_1916', 'prek_2091', 'prek_2172', 'prek_2118', 'prek_2212',
            'prek_2244', 'prek_1939']

post_rerun = ["prek_1103",
              'prek_1113',
              'prek_1208',
              'prek_1210',
              'prek_1241',
              'prek_1262',
              'prek_1293',
              'prek_1401',
              'prek_1443',
              'prek_1460',
              'prek_1490',
              'prek_1673',
              'prek_1751',
              'prek_1762',
              'prek_1798',
              'prek_1818',
              'prek_1916',
              'prek_1936',
              'prek_1951',
              'prek_1964',
              'prek_1966',
              'prek_2085',
              'prek_2090',
              'prek_2106',
              'prek_2118',
              'prek_2135',
              'prek_2136',
              'prek_2172',
              'prek_2174',
              'prek_2186',
              'prek_2212']



params = mnefun.Params(tmin=-0.1, tmax=1, t_adjust=-0.067, n_jobs=8,
                       proj_sfreq=200, n_jobs_fir='cuda',
                       filter_length='5s', lp_cut=lp_cut,
                       n_jobs_resample='cuda',
                       bmin=-0.1, bem_type='5120')
# load paths
# _, subjects_dir, _ = load_paths()
target_dir = '/media/erica/Rocstor/prek/post_camp'
subjects_dir = '/media/erica/Rocstor/anat'
skip = ['prek_2171', 'prek_2259']
subjects = [s for s in os.listdir(target_dir) if op.isdir(op.join(target_dir, s)) and 'prek' in s and not np.in1d(s, skip)]
subjects.sort()
print(subjects)

structurals = [x.upper() for x in subjects]
params.subjects = subjects
params.work_dir = target_dir
params.subjects_dir = subjects_dir
params.score = prek_score
params.structurals = structurals
params.dates = [(2013, 0, 00)] * len(params.subjects)
# define which subjects to run
params.subject_indices = np.arange(len(params.subjects))
# Aquistion params
params.acq_ssh = 'nordme@kasga.ilabs.uw.edu'
params.acq_dir = '/brainstudio/prek/'
params.sws_ssh = 'nordme@kasga.ilabs.uw.edu'
params.sws_dir = '/data07/nordme/prek/'
# SSS options
params.sss_type = 'python'
params.sss_regularize = 'in'
params.tsss_dur = 4.  # tSSS duration
params.int_order = 8
params.st_correlation = 0.98
params.trans_to = 'twa'  # "twa" (time-weighted avg) or "fixed" head pos; use "fixed" for within-subj sensor-level analyses
params.coil_t_window = 'auto'
params.movecomp = 'inter'
params.hp_type = 'python'
params.mf_autobad = True
params.mf_autobad_type = 'python'
# remove segments with < 3 good coils for at least 100 ms
params.coil_bad_count_duration_limit = 0.1
# SSP and rejection params
params.reject = dict()
params.auto_bad_reject = None
params.flat = dict(grad=1e-13, mag=1e-15)
params.auto_bad_flat = None
params.auto_bad_meg_thresh = 10
# SSP
params.ssp_ecg_reject = ecg_reject
params.ecg_channel = 'ECG063'
params.ssp_eog_reject = eog_reject
params.veog_channel = 'EOG062'
params.veog_f_lims = (0.5, 2)
params.veog_t_lims = (-0.22, 0.22)
#params.veog_thresh = 0.0002
#with open(erp_ecg_path) as f:
#    params.ssp_ecg_reject, params.ecg_channel = yaml.load(f, Loader=yaml.FullLoader)
#with open(erp_veog_path) as f:
#    params.ssp_eog_reject,\
#    params.veog_channel,\
#    params.veog_f_lims,\
#    params.veog_t_lims,\
#    params.veog_thresh = yaml.load(f, Loader=yaml.FullLoader)
# naming
params.run_names = ['%s_erp_' + pre_or_post]
params.subject_run_indices = None
params.get_projs_from = np.arange(1)
params.inv_names = ['%s']
params.inv_runs = np.arange(1)
params.runs_empty = ['%s_erm']
# proj
params.proj_nums = [[1, 1, 0],  # ECG: grad/mag/eeg
                    [0, 0, 0],  # EOG
                    [0, 0, 0],  # Continuous (from ERM)
                    [0, 0, 0],  # HEOG
                    [1, 1, 0]]  # VEOG
params.cov_method = 'shrunk'
params.bem_type = '5120'
params.compute_rank = True
params.cov_rank = None
params.force_erm_cov_rank_full = False
# Epoching
params.reject_epochs_by_annot = False   # new param due to EOG annots
params.in_names = ['words', 'faces', 'cars', 'aliens']
params.in_numbers = [10, 20, 30, 40]
params.analyses = ['All',
                   'Conditions']
params.out_names = [['All'],
                    ['words', 'faces', 'cars', 'aliens']]
params.out_numbers = [[10, 10, 10, 10],  # Combine all trials
                      [10, 20, 30, 40],  # Separate trials
                      ]
params.must_match = [[],  # trials to match
                     [],
                     ]

params.report_params.update(  # add plots
    bem=True,
    sensor=[
        dict(analysis='Conditions', name='words', times='peaks'),
        dict(analysis='Conditions', name='faces', times='peaks'),
        dict(analysis='Conditions', name='cars', times='peaks'),
        dict(analysis='Conditions', name='aliens', times='peaks'),
    ],
    source=[
        dict(analysis='Conditions', name='words',
             inv='%s-' + str(lp_cut) + '-sss-meg-free-inv.fif',
             views=['lat', 'caudal'], size=(800, 800)),
        dict(analysis='Conditions', name='faces',
             inv='%s-' + str(lp_cut) + '-sss-meg-free-inv.fif',
             views=['lat', 'caudal'], size=(800, 800)),
        dict(analysis='Conditions', name='cars',
             inv='%s-' + str(lp_cut) + '-sss-meg-free-inv.fif',
             views=['lat', 'caudal'], size=(800, 800)),
        dict(analysis='Conditions', name='aliens',
             inv='%s-' + str(lp_cut) + '-sss-meg-free-inv.fif',
             views=['lat', 'caudal'], size=(800, 800)),
    ],
    snr=[
        dict(analysis='Conditions', name='words',
             inv='%s-' + str(lp_cut) + '-sss-meg-free-inv.fif'),
        dict(analysis='Conditions', name='faces',
             inv='%s-' + str(lp_cut) + '-sss-meg-free-inv.fif'),
        dict(analysis='Conditions', name='cars',
             inv='%s-' + str(lp_cut) + '-sss-meg-free-inv.fif'),
        dict(analysis='Conditions', name='aliens',
             inv='%s-' + str(lp_cut) + '-sss-meg-free-inv.fif')
    ],
    whitening=[
        dict(analysis='Conditions', name='words',
             cov='%s-' + str(lp_cut) + '-sss-cov.fif'),
        dict(analysis='Conditions', name='faces',
             cov='%s-' + str(lp_cut) + '-sss-cov.fif'),
        dict(analysis='Conditions', name='cars',
             cov='%s-' + str(lp_cut) + '-sss-cov.fif'),
        dict(analysis='Conditions', name='aliens',
             cov='%s-' + str(lp_cut) + '-sss-cov.fif')
    ],
    psd=False,
)

mnefun.do_processing(
    params,
    fetch_raw=False,
    do_sss=False,        # do tSSS
    do_score=False,      # do scoring
    gen_ssp=True,        # generate ssps
    apply_ssp=True,      # apply ssps
    write_epochs=False,   # epoching & filtering
    gen_covs=False,       # make covariance
    gen_fwd=False,        # generate fwd model
    gen_inv=False,        # general inverse
    gen_report=True,     # print report
    print_status=True    # show status
)
