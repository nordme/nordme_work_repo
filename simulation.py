# -*- coding: utf-8 -*-
import mne
import numpy as np
import os.path as op
from mne.simulation import SourceSimulator as ss
from mne.simulation import (simulate_raw, add_noise, add_ecg, add_eog, simulate_stc, simulate_sparse_stc)
from mne.minimum_norm import (make_inverse_operator, apply_inverse)

# simulate raw data with infraslow sinusoid signal
main_path = '/media/erica/Rocstor/infslow/spi_11m_127/'
anat_dir = '/media/erica/Rocstor/infslow/anat/'
raw = mne.io.read_raw_fif('/media/erica/Rocstor/infslow/spi_11m_127/raw_fif/spi_11m_127_raw.fif', allow_maxshield=True)
sss = mne.io.read_raw_fif('/media/erica/Rocstor/infslow/spi_11m_127/sss_fif/spi_11m_127_raw_sss.fif')
info = sss.info
sfreq = info['sfreq']
dur = raw.times[-1] - raw.times[0]
subject_fwd = '/media/erica/Rocstor/infslow/spi_11m_127/forward/spi_11m_127-sss-fwd.fif'
subject_cov = '/media/erica/Rocstor/infslow/spi_11m_127/covariance/spi_11m_127-80-sss-cov.fif'
tmin = 0
#tmax =
#baseline =
tstep = 1/2000 # 1 / sfreq
lamb = 1/9.
method = 'dSPM'
labels = mne.read_labels_from_annot(subject='spi_11m_127', subjects_dir='/media/erica/Rocstor/infslow/anat/')
label = labels[-9]
#amps = [1e-07, 1e-10, 1e-13]
#amp_names = ['high', 'med', 'low']
# speeds = [6, 60, 240]
#speeds = [60, 240]
amps = [1e-10]
amp_names = ['med']
speeds = [6]
fwd = mne.read_forward_solution(subject_fwd)
src = fwd['src']
cov = mne.read_cov(subject_cov)
f = raw.info['sfreq']

def make_wave(times, secs_per_cycle=6, amp=1e-10):   # describe the activity on the label vertices
    coef = (2*np.pi)/secs_per_cycle  # np.sin wants input in radians
    x = times * coef
    y = np.sin(x) * amp
    return y

for speed in speeds:
    events = []
    e_num = round(len(raw.times)/(f*speed))
    for n in np.arange(e_num):
        start = int(raw.first_samp + 5 + (speed*f)*n)
        events.append([start, 0, 1])
    events = np.array(events)
    for amp, amp_name in zip(amps, amp_names):
        print(f'creating raw file for {speed} s dur and {amp_name} amplitude')
        stc_path = op.join(main_path, 'sim_stc', f'stc_{speed}s_{amp}_sim')
        save_name = op.join(main_path, 'raw_fif', f'infraslow_{speed}s_{amp_name}_raw.fif')
        ep_stop = int(raw.info['sfreq'] * speed)
        times = raw.times[:ep_stop]
        wave = make_wave(times, speed, amp)

#        sim = ss(src, tstep)
#        sim.add_data(label=label, waveform=wave, events=events)
#        stc = sim.get_stc()
#        stc.save(stc_path)
#        stc_data = np.zeros(raw.n_times)
#        for event in events:
#            start_idx = int(event[
#                                0] - raw.first_samp)  # np.zeros indexing starts with zero
#            end_idx = int(start_idx + sfreq * speed)
#            if end_idx > (raw.last_samp - raw.first_samp):
#                print('Reached end of recording')
#            else:
#                wav = make_wave(times, speed, amp)
#                stc_data[start_idx:end_idx] += wav
#        sim_stc = simulate_stc(src, labels=[label], stc_data=[stc_data], tmin=0.0, tstep=tstep, value_fun=None,
#                 allow_overlap=False)
        sim_stc = simulate_sparse_stc(src, n_dipoles=1, times=times,
                                      data_fun=make_wave, labels=[label],
                                      location='center', subjects_dir=anat_dir)
        print(f'saved stc for {speed} s dur and {amp_name} amplitude')
        # create raw file
        sim_raw = simulate_raw(info=info, stc=[sim_stc] * e_num, forward=fwd)
#        raw_sim = simulate_raw(info=info, stc=sim_stc, forward=fwd)
        add_noise(sim_raw, cov, random_state=0)
        add_eog(sim_raw, random_state=0)
        add_ecg(sim_raw, random_state=0)
        raw.save(save_name, overwrite=True)
        del sim_raw

#        epochs = mne.Epochs(raw_sim, events, event_id, tmin, tmax, baseline)
#        evk = epochs.average()
#        inv = make_inverse_operator(epochs.info, fwd, cov)
#        re_stc = apply_inverse(evk, inv, lamb, method)

#        brain = re_stc.plot(hemi='split', views=['lat', 'med'])
#        fig = evk.plot()

