# -*- coding: utf-8 -*-

import mne

import os.path as op

raw_dir = '/brainstudio/MEG/metwo/metwo_101/181206/'

raw_files = ['metwo_101_7m_01_raw.fif',
             'metwo_101_7m_02_raw.fif',
             'metwo_101_04_raw.fif',
             'metwo_101_03_raw.fif']

for file in raw_files:
    file_path = op.join(raw_dir + file)
    raw_info = mne.io.read_raw_fif(file_path, allow_maxshield=True)
    events = mne.find_events(raw_info, mask=1)
    print('Events for file %s:' % file)
    print('This file had %d events.' % len(events))

