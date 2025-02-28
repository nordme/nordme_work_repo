from pathlib import Path
from datetime import datetime
import csv
import numpy as np
import mne
from mne.minimum_norm import source_induced_power
import h5io

work_dir = Path('/data/erica/rs/')
anat_dir = Path('/data/anat_subjects')

subjects = ['erp_1', 'erp_2', 'erp_3']
atlas = 'aparc'
a_len = 68
bands = [np.arange((i*4)+4, ((i+1)*4)+4, 1) for i in range(13)]
lam = 1./9.
reject = dict(grad=2000e-13, mag=6000e-15)
flat = dict(grad=1e-13, mag=1e-15)
n_jobs = 8
baseline = None
baseline_mode = 'mean'
b_tag = str(baseline_mode) if baseline else 'nobaseline'
method = 'eLORETA'
m_tag = str(method[0:4])

for si, subject in enumerate(subjects):
    s_csv = work_dir / subject / f'{subject}_{atlas}_{b_tag}_{m_tag}_rs_spower.csv'
    stime = datetime.now().strftime('%H:%M')
    if not s_csv.exists():
        print(f'Calculating rs power for subject {subject}')
        s_data = np.zeros((58, a_len))
        # read in files
        sub_path = work_dir / subject
        r_path = sub_path / 'sss_pca_fif' / f'{subject}_rest_allclean_fil80_raw_sss.fif'
        inv_path = sub_path / 'inverse' / f'{subject}-meg-erm-inv.fif'
        cov_path = sub_path / 'covariance' / f'{subject}_erm_allclean_fil80-sss-cov.fif'
        inv = mne.minimum_norm.read_inverse_operator(inv_path)
        cov = mne.read_cov(cov_path)
        src = inv['src']
        labels = mne.read_labels_from_annot(subject=subject, parc=atlas,
                                            subjects_dir=anat_dir)
        labels = [l for l in labels if not '???' in l.name
                  and not l.name.startswith('unknown')]
        l_len = len(labels)
        raw = mne.io.read_raw_fif(r_path).load_data()
        events = mne.make_fixed_length_events(raw, duration=5.0)
        epochs = mne.Epochs(raw, events, tmin=0.0, tmax=5.0, reject=reject,
                            flat=flat, baseline=None, preload=True)
        for bi, band in enumerate(bands):
            low, high = bands[bi][0], bands[bi][-1]
            y_span = np.arange(low, high + 1, 1)
            filt_start = datetime.now().strftime('%H:%M:%S.%f')[:-3]
            print(f'Begin filtering {band} at {filt_start}')
            l_power = source_induced_power(epochs, inv, freqs=bands[bi],
                                           label=labels, lambda2=lam,
                                           method=method,
                                           baseline=baseline,
                                           baseline_mode=baseline_mode,
                                           return_plv=False,
                                           n_jobs=n_jobs)
            lp_path = sub_path / f'{subject}_{low}-{high}_rs_lp_{b_tag}_{m_tag}.h5'
            h5io.write_hdf5(lp_path, data=l_power)
            # convert to meaningful numbers, if eLOR
            if method == 'eLORETA':
                l_power *= 1e19
            # mean over time
            s_ave = np.mean(l_power, axis=-1)
            # mean over frequencies
            s_ave = (np.round(s_ave, 5)).T
            assert s_ave.shape == (4, a_len)
            s_data[low - 1:high, :] = s_ave
            del l_power
        with open(s_csv, 'w') as sf:
            wtr = csv.writer(sf)
            for sr in s_data:
                wtr.writerow(sr)
        etime = datetime.now().strftime('%H:%M')
        print(f'Subject {subject} started at {stime}; finished at {etime}')
