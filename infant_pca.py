import os.path as op
import numpy as np
import matplotlib.pyplot as plt
import mne
from mne.preprocessing import (create_ecg_epochs, create_eog_epochs,
                               compute_proj_ecg, compute_proj_eog, ICA)

path = '/data/fc/fc_6mo_305/sss_fif/fc_6mo_305_raw_sss.fif'
raw = mne.io.read_raw_fif(path)
raw_ica = raw.copy().load_data().filter(l_freq=1, h_freq=None)
# raw.plot()

reject = dict(grad=900e-13, mag=2000e-15)

long_ecg_ep = create_ecg_epochs(raw, ch_name='MEG1533', l_freq=12,
                                             h_freq=25, tmin=-0.5, tmax=0.5)

short_ecg_ep = create_ecg_epochs(raw, ch_name='MEG1533', l_freq=12, h_freq=25,
                                 tmin=-0.1, tmax=0.05)

long_ave = long_ecg_ep.average()
long_ave.apply_baseline(baseline=(-0.5, -0.4))

short_ave = short_ecg_ep.average()
short_ave.apply_baseline(baseline=(-0.1, -0.05))
s_plot = short_ave.plot()
s_plot.suptitle('Average QRS Complex from Infant ECG')
s_plot.tight_layout()
s_plot.savefig('/home/erica/Documents/MEG_Center/infant_ecg_evk.png')
plt.close()


l_proj, l_ev = compute_proj_ecg(raw)

s_proj, s_ev = compute_proj_ecg(raw, tmin=-0.1, tmax=0.05, l_freq=12,
                                h_freq=25, reject=reject, qrs_threshold=0.2)
t_plot = mne.viz.plot_projs_topomap(s_proj, raw.info)
t_plot.suptitle('Infant ECG Projectors')
t_plot.tight_layout()
t_plot.savefig('/home/erica/Documents/MEG_Center/ecg_proj.png')
plt.close()

raw.add_proj(s_proj)
raw.plot()

ica = ICA(n_components=10, max_iter='auto', random_state=1)
