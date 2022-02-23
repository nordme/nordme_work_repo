# -*- coding: utf-8 -*-
"""
Genz eog projectors.

"""
# for genz 232: use 'EOG062' as the ECG channel; use ['ECG063', 'EOG061'] as the EOG channels

import os
import os.path as op
import mnefun
import numpy as np


lp_cut = 80
njobs = 8

fixed_or_twa = 'twa'
if fixed_or_twa == 'twa':
    trans_to = 'twa'
else:
    trans_to = (0.0, 0.0, 0.04)

# raw_dir = '/storage/genz_active/t1/%s_hp/' % fixed_or_twa
raw_dir = '/media/erica/Rocstor/genz/eog_fix/'
anat_dir = '/media/erica/Rocstor/anat'

skip = []
# subjs = [x for x in os.listdir(raw_dir) if op.isdir('%s%s' % (raw_dir, x)) and 'genz' in x
#         and not np.in1d(x, skip)]
subjs = ['genz113_9a']
# subjs = ['genz106_9a', 'genz115_9a', 'genz120_9a', 'genz208_11a', 'genz210_11a', 'genz225_11a', 'genz230_11a',
#         'genz328_13a', 'genz415_15a', 'genz424_15a', 'genz507_17a', 'genz517_17a', 'genz518_17a', 'genz520_17a']
subjs.sort()
print(subjs)
params = mnefun.Params(tmin=-0.1, tmax=0.75, t_adjust=0, n_jobs=njobs,
                       decim=4, n_jobs_mkl=njobs, proj_sfreq=200,
                       n_jobs_fir=njobs, n_jobs_resample=njobs,
                       filter_length='auto', lp_cut=lp_cut, bmin=-0.1,
                       lp_trans='auto', bem_type='inner_skull')

params.subjects = subjs
params.structurals = subjs
params.bem_type = '5120'
params.work_dir = raw_dir
params.subjects_dir = anat_dir
params.subject_indices = np.arange(len(params.subjects))
params.run_names = [
    '%s_emojis_learn_01',
    '%s_thumbs_learn_01',
    '%s_faces_learn_01',
    '%s_emojis_test_01',
    '%s_faces_test_01',
    '%s_thumbs_test_01',
]
params.subject_run_indices = None
params.get_projs_from = np.arange(6)
# params.get_projs_from = [0, 1, 2, 4]
# params.get_projs_from = [0, 2]
params.reject = dict(grad=2000e-13, mag=6000e-15)
params.flat = dict(grad=1e-13, mag=1e-15)
params.ssp_ecg_reject = dict(grad=600e-13, mag=1800e-15)
params.ecg_t_lims = (-0.05, 0.05)

params.eog_channel = 'EOG061'
params.ssp_eog_reject = dict(grad=500e-13, mag=1500e-15)
params.eog_t_lims = (-0.25, 0.25)
params.eog_f_lims = (0.5, 2)
params.eog_thresh = 0.0003
# params.pca_dir = 'h_eog'
params.proj_nums = [[1, 1, 0],
                    [1, 0, 0],
                    [0, 0, 0]]
params.report_params.update(  # add a couple of nice diagnostic plots
    good_hpi_count=False,
    chpi_snr=False,
    head_movement=False,
    raw_segments=False,
    ssp_topomaps=True,
    drop_log=True,
    bem=False,  # Using a surrogate
    covariance=False,
    whitening=False,
    snr=False,
    source=False,
    source_alignment=True,
    psd=False  # often slow
)

mnefun.do_processing(
    params,
    gen_ssp=False,  # Generate SSP vectors
    apply_ssp=False,
    gen_report=True,
    print_status=False
)
