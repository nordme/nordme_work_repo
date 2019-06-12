#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import os
import os.path as op
import mne
import mnefun
import numpy as np
from mnefun._paths import (get_raw_fnames, get_event_fnames)


# words = 1
# faces = 2
# cars = 3 (channels 1 and 2)
# alien = 4


prek_in_names = ['words', 'faces', 'cars', 'alien', 'presses']

prek_in_numbers = [1, 2, 3, 4, 5]

prek_out_names = [prek_in_names]

prek_out_numbers = [prek_in_numbers]


def prek_score(p, subjects):
    for si, subject in enumerate(subjects):
        fnames = get_raw_fnames(p, subject, which='raw', erm=False, add_splits=False, run_indices=None)
        event_fnames = get_event_fnames(p, subject, run_indices=None)
        for fi, fname in enumerate(fnames):
            raw = mne.io.read_raw_fif(fname, allow_maxshield=True)

            # find four categories of visual events
            words = mne.find_events(raw, shortest_event=2, mask=1)
            faces = mne.find_events(raw, shortest_event=2, mask=2)
            cars = mne.find_events(raw, shortest_event=2, mask=3)
            alien = mne.find_events(raw, shortest_event=2, mask=4)

            cars = [x for x in cars if x[2] == 3]
            words = [x for x in words if not np.in1d(x[0], cars)]
            faces = [x for x in faces if not np.in1d(x[0], cars)]

            words = np.array(words)
            faces = np.array(faces)
            cars = np.array(cars)
            alien = np.array(alien)

            # check that these events have distinct timestamps
            assert not np.in1d(words[:, 0], cars[:, 0]).any()
            assert not np.in1d(words[:, 0], faces[:, 0]).any()
            assert not np.in1d(cars[:, 0], faces[:, 0]).any()
            assert not np.in1d(alien[:, 0], cars[:, 0]).any()
            assert not np.in1d(alien[:, 0], faces[:, 0]).any()
            assert not np.in1d(alien[:, 0], words[:, 0]).any()

            # find button presses and turn them all into events with a value of 5
            presses = mne.find_events(raw, shortest_event=2, mask=240)
            presses[:, 2] = 5

            # return all events
            events = np.concatenate((words, cars, faces, alien, presses))
            mne.write_events(event_fnames[fi], events)


def pick_cov_events_prek(events):
    events = [x for x in events if x[2] != 5] # we only want visual events, not button presses
    return events



