
import mnefun
from mnefun import Params
import numpy as np

raw_dir = '/data/delta'
anat_dir = '/data/anat_subjects'
subjects = ['erica_peterson']
lp_cut = 80
trans_to = 'twa'
reject = dict(grad=2000e-13, mag=6000e-15)

params = Params(tmin=-0.1, tmax=0.75, t_adjust=0, n_jobs=12,
                       decim=4, n_jobs_mkl=12, proj_sfreq=200,
                       n_jobs_fir=12, n_jobs_resample=12,
                       filter_length='auto', lp_cut=lp_cut, bmin=-0.1,
                       lp_trans='auto', bem_type='inner_skull')

params.subjects = subjects
params.work_dir = raw_dir
params.subject_indices = np.arange(0, len(params.subjects))
params.subjects_dir = anat_dir
params.run_names = [
    '%s_speak_imagine',
    '%s_test'
]
#params.runs_empty = ['%s_erm']
params.subject_run_indices = [[0, 1]]*len(subjects)
# scoring
#params.score = control_score
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
params.coil_dist_limit = 0.007
# SSP params
params.proj_meg = 'combined'
params.ecg_channel = 'ECG061'
params.ssp_ecg_reject = dict(grad=2000e-13, mag=6000e-15)
params.eog_channel = None
params.ssp_eog_reject = dict(grad=2000e-13, mag=6000e-15)
params.get_projs_from = [0]
params.proj_nums = [[1, 1, 0],
                    [1, 1, 0],
                    [0, 0, 0]]
params.plot_drop_logs=False
# epoch params
params.reject = reject
params.flat = dict(grad=1e-13, mag=1e-15)
params.bmax = 0.0
params.bmin = -0.1
params.must_match = [[]]
# fwd params
params.structurals = params.subjects
params.bem_type = '5120'
# cov params
params.compute_rank = True
params.cov_rank = None
params.cov_rank_method = 'compute_rank'
params.cov_rank_tol = 8e-2
params.cov_method = 'shrunk'
params.force_erm_cov_rank_full = False
# inv params
params.inv_names = ['%s']
params.inv_runs = [[0, 1]]
params.on_missing = 'ignore'  # some subjects will not complete the paradigm
params.every_other = False
# reports parameters
times = [0.05, .105, .22, .55]
cov = '%s-' + str(lp_cut) + '-sss-cov.fif'
inv = '%s-' + str(lp_cut) + '-sss-meg-inv.fif'

params.report_params.update(  # add a couple of nice diagnostic plots
    good_hpi_count=True,
    raw_segments=True,
    chpi_snr=True,
    head_movement=True,
    ssp_topomaps=True,
    drop_log=True,
    bem=True,
    covariance=cov,
    whitening=False,
    sensor=False,
    snr=False,
    source=False,
    source_alignment=True,
    psd=True,
)
default = True

mnefun.do_processing(
    params,
    fetch_raw=False,  # fetch raw files
    do_score=False,  # do scoring
    do_sss=False,  # Run SSS locally
    gen_ssp=True,  # Generate SSP vectors
    apply_ssp=True,  # Apply SSP vectors and filtering
    write_epochs=False,  # Write epochs to disk
    gen_covs=False,  # Generate covariances
    gen_fwd=False,  # Generate forward solutions (and source space if needed)
    gen_inv=False,  # Generate inverses
    gen_report=False,
    print_status=default,
)