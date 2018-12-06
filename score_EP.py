#!/usr/bin/env mne
# -*- coding: utf-8 -*-

"""Erica's scoring function:

Takes auditory triggers from learn and epochs each of those in order to calculate power spectral
density as well as spectral coherence for subjects doing implicit language learning.

The other analysis scores from the feedback response until the button press onset.

"""



"""
Scoring function for GenZ pilot data.

- ten-thousands: (10000-30000):  type (emojis/faces/thumbs)
- hundreds digit (100-200):      learn or test

I'll be using 101k, 201k, 301k

Auditory triggers:

- ones+tens digit (1-12):        auditory syllable onset

"""

from __future__ import print_function

import glob  # noqa, analysis:ignore
import os.path as op

import numpy as np

import mne
from mnefun._paths import get_raw_fnames, get_event_fnames
from expyfun.io import read_tab, read_tab_raw  # noqa, analysis:ignore

subjects = ['genz530_17a']

# distinguish between learn blocks and test blocks
block_codes = {'learn': 100, 'test': 200}
# visual condition (also hard-coded correct=1000 / incorrect=2000 below)
vis_codes = {'emojis': 10000, 'faces': 20000, 'thumbs': 30000}






# aud_names = ['aud/%s/%s/s%02d' % (vis, block, ii)
#             for vis in ('emojis', 'faces', 'thumbs')
#             for block in ('learn', 'test')
#             for ii in range(1, 13 if block == 'test' else 4)]
#
#aud_numbers = [vis_codes[name.split('/')[1]] +
#               kind_codes[name.split('/')[2]] +
##              int(name.split('/')[3][1:])
#             for name in aud_names]
# manual list
# aud_numbers_manual = [
#   10101, 10102, 10103,
#   10201, 10202, 10203, 10204, 10205, 10206, 10207, 10208, 10209, 10210, 10211, 10212,  # noqa
#   20101, 20102, 20103,
#   20201, 20202, 20203, 20204, 20205, 20206, 20207, 20208, 20209, 20210, 20211, 20212,  # noqa
#   30101, 30102, 30103,
#   30201, 30202, 30203, 30204, 30205, 30206, 30207, 30208, 30209, 30210, 30211, 30212,  # noqa
#    ]
# assert aud_numbers == aud_numbers_manual

#
# Visual coding
#
# vis_names = ['vis/%s/%s/%s' % (vis, block, correct)
#             for vis in ('emojis', 'faces', 'thumbs')
#            for block in ('learn', 'test')
#             for correct in ('correct', 'incorrect')]
# vis_numbers = [vis_codes[name.split('/')[1]] +
#               kind_codes[name.split('/')[2]] +
#               vis_correct_codes[name.split('/')[3]]
#               for name in vis_names]
# vis_numbers_manual = [
#    11100, 12100, 11200, 12200,
#    21100, 22100, 21200, 22200,
#    31100, 32100, 31200, 32200,
#    ]
# assert vis_numbers == vis_numbers_manual

#
# Visual trial onset coding
#
vis_onset_number = 99999

#
# Auditory coding


aud_names = ['%s' % block for block in vis_codes]

aud_numbers = [10100, 20100, 30100]


# Combine the lists
aud_in_names = aud_names + ['vis_onset']
aud_in_numbers = aud_numbers + [vis_onset_number]
assert len(set(aud_in_numbers)) == len(aud_in_numbers)  # this assures us that all our numbers are unique
assert len(aud_in_numbers) == len(aud_in_names)

# There are 4 pseudowords for each block:
pseudowords = [['sae-aa-ku', 'oeoe-ke-yy', 'ie-ky-soe', 'ko-ei-ae'],
               ['sa-ia-ui', 'ue-kae-si', 'koe-ai-ee', 'ka-ke-so'],
               ['ua-se-au', 'eu-sy-ii', 'iu-ea-ki', 'oo-su-aeae']]

# fixed for now, could make flexible eventually
block_order = ['emojis_learn', 'emojis_test',
               'faces_learn', 'faces_test',
               'thumbs_learn', 'thumbs_test']
n_resp = 23
blocks = [1, 4, 2, 5, 3, 6]
verbose = False  # warn about timing deviations; probably not necessary


def score(p, subjects, run_indices):
    # load experimental files that determined order
    test_trigs = []
    want_resp = []
    for ii in range(3):
        fname_check = op.join('lists',
                              'block%d_short_test_triggers.txt' % (ii + 1,))
        fname_run = op.join('lists',
                            'block%d_short_test.txt' % (ii + 1,))
        run_names = np.loadtxt(fname_run, np.unicode)
        run_names = [r.split('_')[0] for r in run_names]
        run_trigs = np.loadtxt(fname_check, int, skiprows=1)
        assert len(run_names) == len(run_trigs) == n_resp * 3
        test_trigs.append(run_trigs)
        # 1-2-3: exact syllable sequence presented during learning block.
        # Each 1-2-3 trigger is a 'pseudoword' that should have been learned
        # during learning block. Let's verify this:
        mask = ((run_trigs[:-2] == 1) &
                (run_trigs[1:-1] == 2) &
                (run_trigs[2:] == 3))
        word_offsets = np.where(mask)[0]
        assert len(word_offsets) == 4
        want_resp.append(~mask[::3] + 1)
        assert len(want_resp[-1]) == n_resp, len(want_resp[-1])
        words = ['-'.join(run_names[oi:oi+3]) for oi in word_offsets]
        for word in words:
            assert word in pseudowords[ii], (word, ii + 1)
    del words

    for si, subj in enumerate(subjects):
        print(('  Scoring subject %s:' % subj).ljust(32),
              end='\n' if verbose else '')

        raw_fnames = get_raw_fnames(p, subj, 'raw', False, False,
                                    run_indices[si])
        eve_fnames = get_event_fnames(p, subj, run_indices[si])

        csv = []
        beh_print = []
        blocks_used = np.zeros(6, bool)

        for ri, raw_fname in enumerate(raw_fnames):
            raw = mne.io.read_raw_fif(raw_fname, allow_maxshield='yes')

            # encode learn/test type
            keys = sorted(block_codes.keys())
            which = np.where(['_%s_' % key in raw_fname for key in keys])[0]
            assert len(which) == 1
            this_block = keys[which[0]]
            block_code = block_codes[this_block]
            del which, keys

            #
            # Auditory events
            #
            events_auditory = mne.find_events(
                raw, stim_channel='STI101', shortest_event=1, mask=256,
                mask_type='and')
            try:
                assert len(events_auditory) > 40
            except AssertionError:
                print('Warning! There are only %d auditory events in %s.' % (len(events_auditory), raw_fname))
            if raw_fname == '/storage/Maggie/genZ/genz414_15a/raw_fif/genz414_15a_faces_learn_01_raw.fif':
                events_auditory = events_auditory[:-1]  # errant extra event
            # debounce
#            keep = np.concatenate([
#                  [True],
#                  np.diff(events_auditory[:, 0]) / raw.info['sfreq'] > 0.02])
#            if not keep.all():
#               print('    Debouncing %d trigger(s)' % ((~keep).sum(),))
#            events_auditory = events_auditory[keep]
            deltas = np.diff(events_auditory[:, 0]) / raw.info['sfreq']
            bins = [0., 0.74, 0.8, 6.4, 6.6, np.inf]
            hist = np.histogram(deltas, bins)[0]
            if '_learn_' in raw_fname:
                assert len(events_auditory) == 420, len(events_auditory)
                assert np.allclose(hist, [0, 419, 0, 0, 0], atol=1)
            else:
                assert len(events_auditory) == n_resp * 3, len(events_auditory)
                want = [0, 46, 22, 0, 0]
                if verbose:
                    if not np.allclose(hist, want):
                        print('    Auditory timing deviations %s -> %s in %s'
                              % (want, hist, op.basename(raw_fname)))

            #encode the syllable and learn/test type
            if oi % 2 == 0:  # learn
                assert block_code == block_codes['learn']
                aud_number = np.arange(len(events_auditory)) % 3 + 1
                assert len(aud_number) % 3 == 0
                assert np.in1d(aud_number, [1, 2, 3]).all()
            else:
                assert block_code == block_codes['test']
                idx = blocks[oi] - 4
                aud_number = test_trigs[idx]
                assert np.in1d(aud_number, np.arange(1, 13)).all()
                assert len(events_auditory) == len(aud_number)




           #
           # Output all events
           #
            events = events[np.argsort(events[:, 0])]
            np.diff(events[:,0])
            assert (np.diff(events[:, 0]) > 0).all()
            mne.write_events(eve_fnames[ri], events)
            
        assert blocks_used.all()
        extra = '    ' if verbose else ' '
        print(extra + ' : '.join(beh_print))
        # Write out the behavioral CSV
        with open(op.join(subj, '%s_behavioral.txt' % (subj,)), 'wb') as fid:
            fid.write('vis,want,got,correct,rt\n'.encode())
            for row in csv:
                fid.write(('%s,%d,%d,%d,%d\n' % tuple(row)).encode())


def pick_aud_cov_events(events):
    """Pick (auditory) events for the noise covariance."""
    assert len(events) > 10
    events = events[np.in1d(events[:, 2], aud_numbers)]
    assert len(events) % 3 == 0  # correct number of auditory trials
    events = events[::3]  # only take first of each triplet for cov
    assert len(events) > 10
    return events



"""
#
# Parse auditory TAB files for the blocks that were run
#
try:
    tab_aud = glob.glob(
        op.join('data_audio', subj.split('_')[1] + '_*.tab'))
    assert len(tab_aud) == 1, len(tab_aud)
    blocks = []
    block_sep = '\tblock\t'
    for fname in tab_aud:
        with open(fname, 'rb') as fid:
            for line in fid:
                if block_sep in line:
                    val = int(
                        line.split(block_sep)[-1].encode().strip())
                    blocks.append(val)
    blocks = np.array(blocks).tolist()
except Exception:
    # XXX eventually we should fix all subjects ...
    blocks = want_blocks
    print(': unverified')
else:
    assert blocks[:6] == want_blocks, blocks
    print(': verified')
# tab_aud = sum((read_tab(tab_fname) for tab_fname in tab_aud), [])
# want = 420 * 3 + n_resp * 3
# assert len(tab_aud) == want, (len(tab_aud), want)
#
# Parse visual TAB files
#
tab_vis = glob.glob(
    op.join('data_visual', subj.split('_')[1] + '_*.tab'))
assert len(tab_vis) == 3, len(tab_vis)
tab_vis = [read_tab_raw(tab_fname) for tab_fname in tab_vis]
v_bounds = np.cumsum([0] + [len(t) for t in tab_vis])
tab_vis = sum(tab_vis, [])
assert len(tab_vis) == v_bounds[-1]
v_names = np.array([t[1] for t in tab_vis], np.unicode)
# v_press_idx = np.where(v_names == 'keypress')[0]
# v_resp_idx = np.where(v_names == 'resp')[0]
v_trial_id_idx = np.where(v_names == 'trial_id')[0]
v_expected_idx = np.where(v_names == 'expected')[0]
v_responded_idx = np.where(v_names == 'responded')[0]
img_flip_idx = np.where(v_names == 'play')[0]
assert (v_names[img_flip_idx + 1] == 'flip').all()
assert len(v_trial_id_idx) == len(v_expected_idx)
assert len(v_trial_id_idx) == len(v_responded_idx)
del v_names, v_trial_id_idx, v_expected_idx, v_responded_idx
del img_flip_idx
"""
