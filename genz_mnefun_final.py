# -*- coding: utf-8 -*-
"""
GenZ pilot analysis script.

"""
# for genz 232: use 'EOG062' as the ECG channel; use ['ECG063', 'EOG061'] as the EOG channels

import os
import os.path as op
import mnefun
import numpy as np
import yaml
from genz_score import (score, aud_in_names, aud_in_numbers,
                   pick_aud_cov_events, pick_vis_cov_events)

lp_cut = 80

fixed_or_twa = 'twa'
if fixed_or_twa == 'twa':
    trans_to = 'twa'
else:
    trans_to = (0.0, 0.0, 0.04)

raw_dir = '/storage/genz_active/t1/%s_hp/' % fixed_or_twa
yml_path = '/home/nordme/github/GenZ/'

skip = []
subjs = [x for x in os.listdir(raw_dir) if op.isdir('%s%s' % (raw_dir, x)) and 'genz' in x
         and not np.in1d(x, skip)]
# subjs = ['genz105_9a']
subjs.sort()

params = mnefun.Params(tmin=-0.1, tmax=0.75, t_adjust=0, n_jobs=18,
                       decim=4, n_jobs_mkl=1, proj_sfreq=200,
                       n_jobs_fir=18, n_jobs_resample=18,
                       filter_length='auto', lp_cut=lp_cut, bmin=-0.1,
                       lp_trans='auto', bem_type='inner_skull')

params.subjects = subjs
params.work_dir = raw_dir
params.subject_indices = np.arange(len(params.subjects))
params.subject_indices = np.setdiff1d(np.arange(len(params.subjects)), [np.arange(37)])
params.dates = [(2014, 10, 14)] * len(params.subjects)
params.structurals = params.subjects
params.subject_run_indices = None
params.subjects_dir = op.join('/storage', 'anat', 'subjects')
params.score = score
params.run_names = [
    '%s_emojis_learn_01',
    '%s_thumbs_learn_01',
    '%s_faces_learn_01',
    '%s_emojis_test_01',
    '%s_faces_test_01',
    '%s_thumbs_test_01',
]
# params.acq_ssh = 'maggie@minea.ilabs.uw.edu'
params.acq_dir = ['/brainstudio/MEG/genz']
params.sws_ssh = 'nordme@kasga.ilabs.uw.edu'  # kasga
params.sws_dir = '/data07/nordme/genz'
# tSSS params
params.sss_type = 'python'
params.sss_regularize = 'in'
params.st_correlation = 0.98
params.trans_to = trans_to
params.tsss_dur = 20.
params.movecomp = 'inter'
params.coil_t_window = 'auto'
params.mf_autobad = True
params.mf_autobad_type = 'python'
params.hp_type = 'python'
# SSP params
with open(op.join(yml_path, 'gp_ssp_ecg_reject.yml')) as f:
    params.ssp_ecg_reject = yaml.load(f, Loader=yaml.FullLoader)
# params.ssp_ecg_reject = dict(grad=1000e-13, mag=3000e-15)
with open(op.join(yml_path, 'gp_ecg_channel.yml')) as f:
    params.ecg_channel = yaml.load(f, Loader=yaml.FullLoader)
with open(op.join(yml_path, 'gp_ssp_eog_reject.yml')) as f:
    params.ssp_eog_reject = yaml.load(f, Loader=yaml.FullLoader)
with open(op.join(yml_path, 'gp_eog_channel.yml')) as f:
    params.eog_channel = yaml.load(f, Loader=yaml.FullLoader)
with open(op.join(yml_path, 'gp_eog_t_lims.yml')) as f:
    params.eog_t_lims = yaml.load(f, Loader=yaml.FullLoader)
with open(op.join(yml_path, 'gp_eog_f_lims.yml')) as f:
    params.eog_f_lims = yaml.load(f, Loader=yaml.FullLoader)
with open(op.join(yml_path, 'gp_eog_thresh.yml')) as f:
    params.eog_thresh = yaml.load(f, Loader=yaml.FullLoader)
with open(op.join(yml_path, 'gp_proj_nums.yml')) as f:
    params.proj_nums = yaml.load(f, Loader=yaml.FullLoader)
params.get_projs_from = np.arange(6)
params.plot_drop_logs=True
# epoch rejection params
#params.epochs_proj = 'delayed'
params.reject = dict(grad=2000e-13, mag=6000e-15)
params.flat = dict(grad=1e-13, mag=1e-15)
# cov and inv params
params.inv_names = ['%s_aud']     # ['%s_aud', '%s_vis']
params.inv_runs = [np.arange(6)]     # [np.arange(3, 6), np.arange(0, 3)]
params.pick_events_cov = pick_aud_cov_events
params.on_missing = 'ignore'  # some subjects will not complete the paradigm
params.every_other = True
params.in_names = aud_in_names
params.in_numbers = aud_in_numbers
params.compute_rank = True
params.cov_rank = None
params.cov_rank_method = 'compute_rank'
params.cov_rank_tol = 5e-2
params.cov_method = 'shrunk'
# params.force_erm_cov_rank_full = False
# params.runs_empty = ['%s_erm_01'] # add in the empty room covariance
params.bmax = 0.0
params.bmin = -0.1
params.bem_type = '5120'
# The ones we actually want
params.analyses = [
    'All',
    'Split',
    ]
params.out_names = [
    ['aud', 'vis_onset'],
    params.in_names,
    ]
params.out_numbers = [  # these don't matter as long as they don't overlap...
    [1] * (3 * 12 + 3 * 3) + [2],
    100000 * np.arange(1, len(params.in_names) + 1),
    ]
# do not trial count match for now
params.must_match = [None] * len(params.analyses)
times = [0.05, .105, .22, .55]
# cov = '%s_erm_01_allclean_fil80-sss-cov.fif'
# inv = '%s-meg-erm-inv.fif'
cov = '%s_aud-' + str(lp_cut) + '-sss-cov.fif'
inv = '%s_aud-' + str(lp_cut) + '-sss-meg-inv.fif'
#show = [{"proj": p, "analysis":'Split', "name":'aud/%s/learn/s%02d' % (kind, syl), "times":times, "cov":cov, "inv":inv}
#        for p in [True, False]
#        for kind in ('emojis', 'faces', 'thumbs')
#        for syl in (1,2,3)]

show = [{"analysis":'Split', "name":'aud/%s/learn/s%02d' % (kind, syl), "times":times, "cov":cov, "inv":inv}
        for kind in ('emojis', 'faces', 'thumbs')
        for syl in (1,2,3)]

params.report_params.update(  # add a couple of nice diagnostic plots
    good_hpi_count=True,
#    chpi_snr=False,
#    head_movement=True,
    raw_segments=True,
#    good_hpi_count=False,
    chpi_snr=False,
    head_movement=False,
#    raw_segments=False,
    ssp_topomaps=True,
    drop_log=True,
#    bem=False,  # Using a surrogate
    covariance=cov,
#    covariance=False,
    whitening=show,
#    whitening=False,
    sensor=show,
#    sensor_topo=show,
    snr=False,
#    source=True,
#    snr=show,
    source=show,
    source_alignment=True,
    psd=True  # often slow
)
default = True

mnefun.do_processing(
    params,
    do_score=False,  # do scoring
    do_sss=False, # Run SSS remotely
    gen_ssp=False,  # Generate SSP vectors
    apply_ssp=False,  # Apply SSP vectors and filtering
    write_epochs=True,  # Write epochs to disk
    gen_covs=True,  # Generate covariances
    gen_fwd=False,  # Generate forward solutions (and source space if needed)
    gen_inv=True,  # Generate inverses
    gen_report=True,
    print_status=False,
)