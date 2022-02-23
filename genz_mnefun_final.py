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

eog_or_vh = 'eog'  # Choose between regular eog and separated vertical, horizontal eog

# raw_dir = '/storage/genz_active/t1/%s_hp/' % fixed_or_twa
# raw_dir = '/storage/genz_active/t1/twa_hp/'
# yml_path = '/home/erica/repos/GenZ-1/params/'
raw_dir = '/media/erica/Rocstor/genz/'
yml_path = '/media/erica/Rocstor/genz/params/'

skip = []
# subjs = [x for x in os.listdir(raw_dir) if op.isdir('%s%s' % (raw_dir, x)) and 'genz' in x
#         and not np.in1d(x, skip)]
subjs = ['genz113_9a']
subjs.sort()

params = mnefun.Params(tmin=-0.1, tmax=0.75, t_adjust=0, n_jobs=18,
                       decim=4, n_jobs_mkl=1, proj_sfreq=200,
                       n_jobs_fir=18, n_jobs_resample=18,
                       filter_length='auto', lp_cut=lp_cut, bmin=-0.1,
                       lp_trans='auto', bem_type='inner_skull')

params.subjects = subjs
params.work_dir = raw_dir
params.subject_indices = np.arange(len(params.subjects))
params.dates = [(2014, 10, 14)] * len(params.subjects)
params.structurals = params.subjects
params.subject_run_indices = None
params.subjects_dir = '/media/erica/Rocstor/anat/'
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
with open(op.join(yml_path, 'ecg_proj_params_%s.yml' % fixed_or_twa)) as f:
    params.ssp_ecg_reject, params.ecg_channel = yaml.load(f, Loader=yaml.FullLoader)

if eog_or_vh == 'eog':
    with open(op.join(yml_path, 'proj_params_%s.yml' % fixed_or_twa)) as f:
         params.proj_nums, params.get_projs_from, params.ssp_eog_reject = yaml.load(f, Loader=yaml.FullLoader)
    with open(op.join(yml_path, 'eog_proj_params_%s.yml' % fixed_or_twa)) as f:
        params.eog_channel, params.eog_f_lims, params.eog_t_lims, params.eog_thresh = yaml.load(f, Loader=yaml.FullLoader)
else:
    with open(op.join(yml_path, 'vh_proj_params_%s.yml' % fixed_or_twa)) as f:
         params.proj_nums, params.get_projs_from, params.ssp_eog_reject = yaml.load(f, Loader=yaml.FullLoader)
    with open(op.join(yml_path, 'veog_proj_params_%s.yml' % fixed_or_twa)) as f:
         params.veog_channel, params.veog_f_lims, params.veog_t_lims, params.veog_thresh = yaml.load(f, Loader=yaml.FullLoader)
    with open(op.join(yml_path, 'heog_proj_params_%s.yml' % fixed_or_twa)) as f:
         params.heog_channel, params.heog_f_lims, params.heog_t_lims, params.heog_thresh = yaml.load(f, Loader=yaml.FullLoader)

params.plot_drop_logs=True
# epoch rejection params
# params.epochs_proj = 'delayed'
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
params.force_erm_cov_rank_full = False
params.runs_empty = ['%s_erm_01'] # add in the empty room covariance
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

cov = '%s_aud-' + str(lp_cut) + '-sss-cov.fif'
inv = '%s_aud-' + str(lp_cut) + '-sss-meg-inv.fif'

show = [{"proj": True, "analysis":'Split', "name":'aud/%s/learn/s%02d' % (kind, syl), "times":times, "cov":cov, "inv":inv}
        for kind in ('emojis', 'faces', 'thumbs')
        for syl in (1,2,3)]

params.report_params.update(  # add a couple of nice diagnostic plots
#    good_hpi_count=True,
    good_hpi_count=False,
    raw_segments=True,
    chpi_snr=False,
    head_movement=False,
    ssp_topomaps=True,
    drop_log=True,
    bem=False,  # Using a surrogate
    covariance=cov,
    whitening=show,
    sensor=show,
    snr=show,
    source=show,
    source_alignment=True,
    psd=False  # often slow
)
default = True

mnefun.do_processing(
    params,
    do_score=False,  # do scoring
    do_sss=False, # Run SSS remotely
    gen_ssp=False,  # Generate SSP vectors
    apply_ssp=False,  # Apply SSP vectors and filtering
    write_epochs=False,  # Write epochs to disk
    gen_covs=False,  # Generate covariances
    gen_fwd=False,  # Generate forward solutions (and source space if needed)
    gen_inv=False,  # Generate inverses
    gen_report=True,
    print_status=False,
)