import mne
import numpy as np
import os.path as op

def score_acdc(p):
    raw_dir = p.work_dir
    f_name = p.run_names[0]
    subject = p.subjects[0]
    standard = []
    oddball1 = []
    oddball2 = []
    raw_path = op.join(raw_dir, subject, 'raw_fif', f_name % subject + '_raw.fif')
    event_fname=op.join(raw_dir, subject, 'lists', 'ALL_acdc_eeg_meg_adult_actual-eve.lst')
    raw = mne.io.read_raw_fif(raw_path, allow_maxshield=True)
    ones = mne.find_events(raw, mask=1)
    events = mne.find_events(raw)
    for one in ones:
        category=0
        event = [e for e in events if e[0]==one[0]]
        event_idx = int(np.where(events[:, 0] == event[0][0])[0])
        one_back = events[event_idx-1]
        try:
            two_back = events[event_idx-2]
        except Error:
            two_back = [0, 0, 1]
        add_ob = 3 if one_back[2]==8 else 1
        add_tb = 1 if two_back[2]==4 else 0
        category += add_ob
        category += add_tb
        one[2]=category
    assert (np.diff(ones[:, 0]) > 0).all()
    mne.write_events(event_fname, ones)

def score_acdc_eeg(p):
    raw_dir = p.work_dir
    f_name = p.run_names[0]
    subject = p.subjects[0]
    raw_path = op.join(raw_dir, subject, 'raw_fif', f_name % subject + '_raw.fif')
    event_fname=op.join(raw_dir, subject, 'lists', 'ALL_acdc_eeg_meg_adult_actual-eve.lst')
    raw = mne.io.read_raw_fif(raw_path, allow_maxshield=True)
    events = mne.find_events(raw, stim_channel='STI 014')
    events[:, 2] = events[:, 2]*10
    onsets = [e for e in events if e[2]==20]
    for onset in onsets:
        category=0
        event = [e for e in events if e[0]==onset[0]]
        event_idx = int(np.where(events[:, 0] == event[0][0])[0])
        one_back = events[event_idx-1]
        try:
            two_back = events[event_idx-2]
        except Error:
            two_back = [0, 0, 2]
        add_ob = 3 if one_back[2]==30 else 1
        add_tb = 1 if two_back[2]==10 else 0
        category += add_ob
        category += add_tb
        onset[2]=category
    assert (np.diff(onsets[:, 0]) > 0).all()
    mne.write_events(event_fname, onsets)