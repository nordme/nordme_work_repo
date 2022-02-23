# -*- coding: utf-8 -*-

import os
import os.path as op
import mne
import time
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

# set paths

data_dir = '/media/erica/Rocstor/spi/discard'
save_dir = '/media/erica/Rocstor/spi/discard/raw_plots'

# data_dir = '/data/spi/'
# save_dir = '/data/spi/raw_plots/raw'

# choose options
matplotlib.use('Agg')
# file_name = '%s_otp_raw_sss.fif'
file_name = '%s_raw.fif'
sub_dir = 'raw_fif'
# file_name = '%s_raw_sss.fif'
# sub_dir = 'sss_fif'
lp_cut = 80.0

subjects = [s for s in os.listdir(data_dir) if op.isdir(op.join(data_dir, s)) and 'spi' in s]
# subjects = ['spi_7m_106', 'spi_7m_110', 'spi_7m_143', 'spi_7m_156', 'spi_7m_161', 'spi_11m_128', 'spi_11m_155', 'spi_11m_180']
# subjects = ['spi_11m_128']
subjects.sort()

for subject in subjects:
    fpath = op.join(data_dir, subject, sub_dir, file_name % subject)
    save_path = op.join(save_dir, '%s_raw_plot.png' % subject)
    raw = mne.io.read_raw_fif(fpath, allow_maxshield=True)
    print('plotting sss segs for subject %s' % subject)

    # Use Eric's report code
    t0 = time.time()
    times = np.linspace(raw.times[0], raw.times[-1], 12)[1:-1]
    raw_plot = list()
    for t in times:
        this_raw = raw.copy().crop(
            max(t - 0.5, 0), min(t + 0.5, raw.times[-1]))
        this_raw.load_data()
        this_raw._data[:] -= np.mean(this_raw._data, axis=-1,
                                     keepdims=True)
        raw_plot.append(this_raw)
    raw_plot = mne.concatenate_raws(raw_plot)
    for key in ('BAD boundary', 'EDGE boundary'):
        raw_plot.annotations.delete(
            np.where(raw_plot.annotations.description == key)[0])
    new_events = np.linspace(
        0, int(round(10 * raw.info['sfreq'])) - 1, 11).astype(int)
    new_events += raw_plot.first_samp
    new_events = np.array([new_events,
                           np.zeros_like(new_events),
                           np.ones_like(new_events)]).T
    fig = raw_plot.plot(group_by='selection', butterfly=True,
                        events=new_events, lowpass=lp_cut)
    fig.axes[0].lines[-1].set_zorder(10)  # events
    fig.axes[0].set(xticks=np.arange(0, len(times)) + 0.5)
    xticklabels = ['%0.1f' % t for t in times]
    fig.axes[0].set(xticklabels=xticklabels)
    fig.axes[0].set(xlabel='Center of 1-second segments')
    fig.axes[0].grid(False)
    for _ in range(len(fig.axes) - 1):
        fig.delaxes(fig.axes[-1])
    fig.set(figheight=(fig.axes[0].get_yticks() != 0).sum(),
            figwidth=12)
    fig.subplots_adjust(0.025, 0.0, 1, 1, 0, 0)
    fig.savefig(save_path)
    plt.close()
    print('%5.1f sec' % ((time.time() - t0),))
