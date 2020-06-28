#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Scoring function for GenZ pilot data.

Unified:

- ten-thousands: (10000-20000):  type (emojis/faces/thumbs)
- hundreds digit (100-200):      learn or test

Auditory triggers:

- ones+tens digit (1-12):        auditory syllable onset

Visual triggers:

- thousands (1000-2000):         feedback correct/incorrect

"""

from __future__ import print_function

import glob  # noqa, analysis:ignore
import os.path as op

import numpy as np

import mne
from mnefun._paths import get_raw_fnames, get_event_fnames
import expyfun
from expyfun.io import read_tab, read_tab_raw  # noqa, analysis:ignore


# trial type
learn_or_test = dict(learn=100, test=200)
# visual condition (also hard-coded correct=1000 / incorrect=2000 below)
vis_blocks = dict(emojis=10000, faces=20000, thumbs=30000)
feedback_codes = dict(correct=1000, incorrect=2000)
#
# Auditory coding
#

aud_names = ['aud/%s/%s/s%02d' % (vis, block, ii)
             for vis in ('emojis', 'faces', 'thumbs')
             for block in ('learn', 'test')
             for ii in range(1, 13 if block == 'test' else 4)]

aud_numbers = [vis_blocks[name.split('/')[1]] +
               learn_or_test[name.split('/')[2]] +
               int(name.split('/')[3][1:])
               for name in aud_names]
# manual list
aud_numbers_manual = [
    10101, 10102, 10103,
    10201, 10202, 10203, 10204, 10205, 10206, 10207, 10208, 10209, 10210, 10211, 10212,  # noqa
    20101, 20102, 20103,
    20201, 20202, 20203, 20204, 20205, 20206, 20207, 20208, 20209, 20210, 20211, 20212,  # noqa
    30101, 30102, 30103,
    30201, 30202, 30203, 30204, 30205, 30206, 30207, 30208, 30209, 30210, 30211, 30212,  # noqa
]
assert aud_numbers == aud_numbers_manual

#
# Visual coding
#
vis_names = ['vis/%s/%s/%s' % (vis, block, correct)
             for vis in ('emojis', 'faces', 'thumbs')
             for block in ('learn', 'test')
             for correct in ('correct', 'incorrect')]
vis_numbers = [vis_blocks[name.split('/')[1]] +
               learn_or_test[name.split('/')[2]] +
               feedback_codes[name.split('/')[3]]
               for name in vis_names]
vis_numbers_manual = [
    11100, 12100, 11200, 12200,
    21100, 22100, 21200, 22200,
    31100, 32100, 31200, 32200,
]
assert vis_numbers == vis_numbers_manual

#
# Visual trial onset coding
#
vis_onset_number = 99999

# Combine the lists
aud_in_names = aud_names + ['vis_onset']
aud_in_numbers = aud_numbers + [vis_onset_number]
assert len(set(aud_in_numbers)) == len(aud_in_numbers)
assert len(aud_in_numbers) == len(aud_in_names)

# There are 4 pseudowords for each block:
# pseudowords = [['sae-aa-ku', 'oeoe-ke-yy', 'ie-ky-soe', 'ko-ei-ae'],
#               ['sa-ia-ui', 'ue-kae-si', 'koe-ai-ee', 'ka-ke-so'],
#               ['ua-se-au', 'eu-sy-ii', 'iu-ea-ki', 'oo-su-aeae']]

# T2 pseudowords

pseudowords = [['aa-ka-su', 'si-au-ui', 'ai-ki-oeoe', 'sae-uu-yy'],
               ['iu-koe-ee', 'ku-ie-so', 'ua-ky-ii', 'ae-oo-sa'],
               ['ea-soe-ei', 'se-eu-sy', 'ue-ko-aeae', 'ke-ia-kae']]


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
    # create
    for ii in range(3):
        fname_check = op.join('lists',
                              'block%d_short_test_triggers_t2.txt' % (ii + 1,))
        wav_names = op.join('lists',
                            'block%d_short_test_t2.txt' % (ii + 1,))
        wavs = np.loadtxt(wav_names, np.unicode)
        wavs = [r.split('_')[0] for r in wavs]
        syllable_trigs = np.loadtxt(fname_check, int, skiprows=1)
        assert len(wavs) == len(syllable_trigs) == n_resp * 3
        test_trigs.append(syllable_trigs)   # test_trigs always has language 1, language 2, language 3 order
        # 1-2-3: exact syllable sequence presented during learning block.
        # Each 1-2-3 trigger is a 'pseudoword' that should have been learned
        # during learning block. There should be four instances of a correct psuedoword in the test block.
        # Let's verify this:
        mask = ((syllable_trigs[:-2] == 1) &      # find the real pseudowords where the subject should answer 'yes'
                (syllable_trigs[1:-1] == 2) &
                (syllable_trigs[2:] == 3))
        word_offsets = np.where(mask)[0]           # returns the indices of the real psuedowords
        assert len(word_offsets) == 4
        want_resp.append(~mask[::3] + 1)            # Generate the perfect answer sequence, 1 being yes and 2 being no
        assert len(want_resp[-1]) == n_resp, len(want_resp[-1])
        words = ['-'.join(wavs[oi:oi + 3]) for oi in word_offsets]
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

        # read in the subject's condition to pair f / e/ t with l1 / l2 / l3 for behavioral scoring
        hits = 0
        misses = 0
        false_alarms = 0
        correct_rejections = 0
        condition_list = []
        with open(op.join(p.work_dir, 'genz_subject_condition_t2.txt')) as search:
            line = [line for line in search if subj[4:] in line.lower().rstrip()]
            line = line[0].lower().rstrip()
            for i in [-3, -2, -1]:  # the last three letters (condition letters) of the txt line
                condition_list.append(
                    [line[i], i + 4])  # the number is the language number paired with the block letter
            print('Subject %s has the following pairing of languages and blocks: \n %s' %(subj, condition_list))

        for ri, raw_fname in enumerate(raw_fnames):
            raw = mne.io.read_raw_fif(raw_fname, allow_maxshield='yes')
            print('Scoring file %s' % raw_fname)

            # encode learn/test (condition) type
            if 'learn' in raw_fname:
                condition_code = 100
                condition = 'learn'
            else:
                condition_code = 200
                condition = 'test'

            # encode emojis / faces/ thumbs (block) type

            if 'emojis' in raw_fname:
                block = 'emojis'
                block_code = 10000
            elif 'faces' in raw_fname:
                block = 'faces'
                block_code = 20000
            elif 'thumbs' in raw_fname:
                block = 'thumbs'
                block = 30000
            else:
                print('Hmm, the file names for subject %s seems to not contain block info. Check manually please.' % subject)

            #
            # Auditory scoring
            #
            events_auditory = mne.find_events(
                raw, stim_channel='STI101', shortest_event=1, mask=256,
                mask_type='and')

            # Perform checks on auditory events found
            assert len(events_auditory) > 40
            intervals_between_stim_onsets = np.diff(events_auditory[:, 0]) / raw.info['sfreq']
            bins = [0., 0.74, 0.8, 6.4, 6.6, np.inf]
            hist = np.histogram(intervals_between_stim_onsets, bins)[0]

            if '_learn_' in raw_fname:
                assert len(events_auditory) == 420, len(events_auditory)
                assert np.allclose(hist, [0, 419, 0, 0, 0], atol=1)
            else:
                assert len(events_auditory) == n_resp * 3
                want = [0, 46, 22, 0, 0]
                if verbose:
                    if not np.allclose(hist, want):
                        print('    Auditory timing deviations %s -> %s in %s'
                              % (want, hist, op.basename(raw_fname)))

            # encode the auditory syllables
            if condition == 'learn':
                assert condition_code == learn_or_test['learn']
                syl_codes = np.arange(len(events_auditory)) % 3 + 1
                assert np.in1d(syl_codes, [1,2,3]).all()
            else:
                assert condition_code == learn_or_test['test']
                idx = [x[1] for x in condition_list if x[0] == block]  # the idx is the l1 / l2 / l3 number
                idx = idx[0] - 1
                syl_codes = test_trigs[idx]

                # Assess behavioral performance
                want_presses = want_resp[idx]
                presses = mne.find_events(raw, 'STI101', mask=48,
                                          mask_type='and')
                # some subjects press blue and yellow nearly simultaneously
                # we are considering only the first button pressed for behav
                # so we eliminate the conflicting second button press
                presses[:, 2] >>= 4
                assert np.in1d(presses[:, 2], [1, 2]).all()
                press_slots = np.searchsorted(
                    events_auditory[:, 0], presses[:, 0], 'right')
                got_presses = list()
                got_rts = list()
                for pi in range(n_resp):
                    ii = 3 * (pi + 1)
                    idx = np.where(press_slots == ii)[0]
                    if len(idx) == 0:
                        press = 0
                        rt = -1
                    else:
                        press = presses[idx[0], 2]
                        rt = (presses[idx[0], 0] -
                              events_auditory[ii - 1, 0]) / raw.info['sfreq']
                        rt *= 1e3  # ms
                    got_presses.append(press)
                    got_rts.append(rt)
                assert len(got_presses) == n_resp, len(got_presses)
                assert len(want_presses) == n_resp, len(want_presses)
                assert len(got_rts) == n_resp, len(got_rts)
                got_presses = np.array(got_presses)
                pc = (got_presses == want_presses).mean() * 100
                hit = (got_presses[want_presses == 1] == 1)
                beh_print += ['%s %4.1f%% (%d/%d)' % (block.ljust(6), pc,
                                                      hit.sum(), len(hit))]
                csv.extend([[block, w, g, w == g, r]
                            for w, g, r in
                            zip(want_presses, got_presses, got_rts)])

                # determine value of variables for calculating dprime
                for gp, wp in zip(got_presses, want_presses):
                    if gp == wp == 1:
                        hits += 1
                    elif gp == wp == 2:
                        correct_rejections += 1
                    elif gp != wp and gp == 1:
                        false_alarms += 1
                    elif gp != wp and gp == 2:
                        misses += 1

            events_auditory[:, 2] = (condition_code + block_code + syl_codes)
            assert np.in1d(events_auditory[:, 2], aud_numbers).all()

            #
            # Visual scoring
            #
            events_visual = mne.find_events(
                raw, stim_channel='STI101', shortest_event=1, mask=1,
                mask_type='and')

            # perform checks on visual events found
            intervals_between_stim_onsets = np.diff(events_visual[:, 0]) / raw.info['sfreq']
            hist = np.histogram(intervals_between_stim_onsets, bins)[0]
            n_vis = len(events_visual)
            if '_learn_' in raw_fname:
                assert n_vis in range(46, 51), n_vis
                assert np.allclose(hist, [0, 0, 0, n_vis - 1, 0], atol=1)
            else:
                assert n_vis == 0, n_vis

            # encode feedback type
            correctness_visual = mne.find_events(
                raw, stim_channel='STI101', shortest_event=1, mask=12,
                mask_type='and')
            #  these can differ by one if the trial is stopped in between them
            # ADD WARNING Or HANDLING
            if len(correctness_visual) == len(events_visual) + 1:
                correctness_visual = correctness_visual[:-1]
            else:
                assert (correctness_visual[:, 0] < events_visual[:, 0]).all()
            correctness_visual = correctness_visual[:, 2]  # just need the type
            assert np.in1d(correctness_visual, [4, 8]).all()
            correctness_visual //= 4  # 1=correct, 2=incorrect
            correctness_visual *= 1000
            assert np.in1d(correctness_visual, [1000, 2000]).all()
            correct = [x for x in correctness_visual if x == 1000]
            incorrect = [x for x in correctness_visual if x == 2000]
            try:
                assert len(correct) == len(incorrect)
            except AssertionError:
                print('Subject %s for file %s has unequal visual feedback: %s correct and %s incorrect.' %
                      (subj, raw_fname, len(correct), len(incorrect)))
            events_visual[:, 2] = (condition_code + block_code +
                                   correctness_visual)
            assert np.in1d(events_visual[:, 2], vis_numbers).all()

            # check to make sure these are mapped properly
            for id_ in np.unique(events_visual[:, 2]):
                idx = vis_numbers.index(id_)
                assert block in vis_names[idx]

            # get the onset of the visual trials (time-locked to the response
            # question mark, which should be 5 sec before the feedback event)
            events_visual_onset = events_visual.copy()
            events_visual_onset[:, 2] = vis_onset_number
            events_visual_onset[:, 0] -= int(round(raw.info['sfreq'] * 5.))

            # Deal with simultaneous events before we concatenate events
            raw = mne.io.read_raw_fif(raw_fname, allow_maxshield='yes')
            presses = mne.find_events(raw, 'STI101', mask=48,
                                      mask_type='and', shortest_event=1)

            a_v_bads = np.in1d(events_auditory[:, 0], events_visual[:, 0])
            p_v_bads = np.in1d(events_visual[:, 0], presses[:, 0])
            p_a_bads = np.in1d(presses[:, 0], events_auditory[:, 0])

            print('Simultaneous events: %s, %s, %s' %
                  (events_auditory[a_v_bads], events_visual[p_v_bads], presses[p_a_bads]))

            events_auditory[a_v_bads, 0] += 1  # push the auditory event forward if conflict with visual event

            events_visual[p_v_bads, 0] += 1  # push the visual event forward if conflict with button press

            presses[p_a_bads, 0] += 1  # push the button press forward if conflict with auditory event

            # build up overall events set
            events = np.concatenate((events_auditory, events_visual))

            # eliminate more duplicate events from creating visual onset
            bads = np.in1d(events_visual_onset[:, 0], events[:, 0])
            events_visual_onset[bads, 0] += 1  # push it 1 samp
            assert not np.in1d(events_visual_onset[:, 0], events[:, 0]).any()
            assert (events_visual_onset[:, 0] > 0.).all()

            # continue building overall events set
            events = np.concatenate((events, events_visual_onset))

            # check that no simultaneous events made it through (e.g. created by push forwards)

            try:
                assert not np.in1d(events_auditory[:, 0], events_visual[:, 0]).any()
            except AssertionError:
                print('Simultaneous events found: auditory and visual')

            try:
                assert not np.in1d(presses[:, 0], events_visual[:, 0]).any()
            except AssertionError:
                print('Simultaneous events found: button press and visual')

            try:
                assert not np.in1d(presses[:, 0], events_auditory[:, 0]).any()
            except AssertionError:
                print('Simultaneous events found: button press and auditory')

            #
            #  Output all events
            #

            events = events[np.argsort(events[:, 0])]
            np.diff(events[:, 0])
            assert (np.diff(events[:, 0]) > 0).all()  # one last check that all events have a unique timestamp
            mne.write_events(eve_fnames[ri], events)

        assert blocks_used.all()
        extra = '    ' if verbose else ' '
        print(extra + ' : '.join(beh_print))

        # Write out the behavioral CSV
        with open(op.join(subj, '%s_behavioral.txt' % subj), 'wb') as fid:
            print('writing the behavioral csv here at %s' % op.join(subj, '%s_behavioral.txt' % subj))
            fid.write('vis,want,got,correct,rt\n'.encode())
            for row in csv:
                fid.write(('%s,%d,%d,%d,%d\n' % tuple(row)).encode())

        #### calculate dprime for Genz

        d_prime = expyfun.analyze.dprime([hits, misses, false_alarms, correct_rejections])

        with open(op.join(p.work_dir, 'genz_t1_behavioral.txt'), 'ab') as fid:
            print('Adding a line to the Genz timepoint 1 global behavioral file.\n %s, %s, %s, %s, %s, %s \n' % (
            subj, hits, misses, false_alarms, correct_rejections, d_prime))
            fid.write((('%s, %s, %s, %s, %s, %s \n' % (
            subj, hits, misses, false_alarms, correct_rejections, d_prime)).encode()))


def pick_aud_cov_events(events):
    """Pick (auditory) events for the noise covariance."""
    assert len(events) > 10
    events = events[np.in1d(events[:, 2], aud_numbers)]
    assert len(events) % 3 == 0  # correct number of auditory trials
    events = events[::3]  # only take first of each triplet for cov
    assert len(events) > 10
    return events


def pick_vis_cov_events(events):
    """Pick (visual) events for the noise covariance."""
    assert len(events) > 10
    events = events[events[:, 2] == vis_onset_number]
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