import mne
import mnefun
import numpy as np


amps = [1e-07, 1e-10, 1e-13]
amp_names = ['high', 'med', 'low']
speeds = [6, 60, 240]

run_names = ['infraslow_6s_high',
             'infraslow_6s_med',
#             'infraslow_6s_low',
             'infraslow_60s_high',
             'infraslow_60s_med',
#             'infraslow_60s_low',
             'infraslow_240s_high',
             'infraslow_240s_med',
#             'infraslow_240s_low',
             ]
lp_cut = 80.0
work_dir = '/media/erica/Rocstor/infslow/'

params = mnefun.Params(tmin=-0.1, tmax=60, n_jobs=12,
                       decim=2, proj_sfreq=200, n_jobs_fir='cuda',
                       filter_length='auto', lp_cut=lp_cut, lp_trans='auto',
                       hp_cut=None, n_jobs_resample='cuda',
                       bmin=-0.5, bmax=0.0, baseline=None, bem_type='5120')


params.subjects = ['spi_11m_127']
params.structurals = params.subjects
params.work_dir = work_dir
params.subjects_dir = '/media/erica/Rocstor/anat'
params.dates = [(2013, 1, 1)] * len(params.subjects)
params.subject_indices = np.arange(len(params.subjects))
# SSS options
params.hp_type = 'python'
params.sss_type = 'python'
params.sss_regularize = 'in'
params.tsss_dur = 4.
params.int_order = 8
params.st_correlation = .98
params.trans_to = 'twa'
params.coil_t_window = 'auto'
params.movecomp = 'inter'
# remove segments with < 3 good coils for at least 100 ms
params.coil_bad_count_duration_limit = 0.1
# Trial rejection criteria
params.reject = dict()
params.auto_bad_reject = None
params.ssp_ecg_reject = None
params.flat = dict(grad=1e-13, mag=1e-15)
params.auto_bad_flat = None
params.auto_bad_meg_thresh = 10
params.run_names = run_names
params.get_projs_from = np.arange(1)
params.inv_names = ['%s']
params.inv_runs = [np.arange(1)]
params.runs_empty = []
params.proj_nums = [[1, 1, 0],  # ECG: grad/mag/eeg  # used to be 1, 1, 0
                    [0, 0, 0],  # EOG
                    [0, 0, 0]]  # Continuous (from ERM)
params.pick_events_cov = lambda x: x[x[:, 2] == 100] # use sentence onset for noise cov
params.cov_method = 'empirical'
params.bem_type = '5120'
params.compute_rank = True
# Epoching
params.in_names = ['event']
params.on_missing = 'warning'
params.compute_rank = True
params.in_numbers = [1]
params.out_numbers = [params.in_numbers]
params.out_names = [params.in_names]
params.must_match = [[]]

default = False
mnefun.do_processing(
    params,
    fetch_raw=False,
    do_score=True,
    do_sss=True,
    gen_ssp=True,
    apply_ssp=True,
    write_epochs=default,
    gen_covs=default,
    gen_fwd=default,
    gen_inv=default,
    gen_report=False,
    print_status=default,
)