import mne
import numpy as np
import os.path as op
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


amps = [1e-07, 1e-10, 1e-13]
amp_names = ['high', 'med', 'low']
speeds = [6, 60, 240]
path = '/media/erica/Rocstor/infslow/spi_11m_127/'
tmin = 0.0
baseline=None

for si, speed in enumerate(speeds):
    for ai, (amp, a_name) in enumerate(zip(amps, amp_names)):
        fig, axes = plt.subplots(ncols=2)
        r_path = op.join(path, 'raw_fif', f'infraslow_{speed}s_{a_name}_raw.fif')
        s_path = op.join(path, 'sss_pca_fif', f'infraslow_{speed}s_{a_name}_allclean_fil80_raw_sss.fif')
        raw = mne.io.read_raw_fif(r_path, allow_maxshield=True)
        ssp = mne.io.read_raw_fif(s_path)
        events = mne.find_events(raw, mask=1)
        print('len of events:', len(events))
        r_eps = mne.Epochs(raw, events, tmin=tmin, tmax=speed, baseline=baseline)
        s_eps = mne.Epochs(ssp, events, tmin=tmin, tmax=speed, baseline=baseline)
        r_ave = r_eps.average()
        s_ave = s_eps.average()
        print('plotting raw figs')
        r_figm, r_figg = r_ave.plot_joint()
        r_figm.savefig(op.join(path, 'images', f'{speed}s_{a_name}_plot_joint_mag_raw.png'))
        r_figg.savefig(op.join(path, 'images', f'{speed}s_{a_name}_plot_joint_grad_raw.png'))
        plt.close()
        print('plotting ssp figs')
        s_figm, s_figg = s_ave.plot_joint()
        s_figm.savefig(
            op.join(path, 'images', f'{speed}s_{a_name}_plot_joint_mag_ssp.png'))
        s_figg.savefig(
            op.join(path, 'images', f'{speed}s_{a_name}_plot_joint_grad_ssp.png'))
        plt.close()




