#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import os
import os.path as op
import mne
import numpy as np
from mne.minimum_norm import (apply_inverse, read_inverse_operator)

# set important variables

raw_dir = '/home/nordme/data/genz/genz_active/'
# raw_dir = '/brainstudio/MEG/genz/genz_proc/active/'
anat_dir = '/brainstudio/MEG/genz/anatomy/'

method = 'dSPM'

subjects = ['genz131_9a']

for subject in subjects:
    sub_path = op.join(raw_dir, subject)
    epo_path = op.join(sub_path, 'epochs', 'All_80-sss_%s-epo.fif' % subject)
    ave_path = op.join(sub_path, 'inverse')
    inv_path = op.join(sub_path, 'inverse', '%s_aud-80-sss-meg-erm-fixed-inv.fif' % subject)
    inv = read_inverse_operator(inv_path)

    all_epochs = []

    # create directories needed for saving the stcs
    if not op.isdir(op.join(sub_path, 'stc')):
        os.mkdir(op.join(sub_path, 'stc'))
    stc_path = op.join(sub_path, 'stc')

    # create appropriate groups of epochs
    epochs = mne.read_epochs(epo_path)

    # all learn blocks by syllable position (e.g. all the s01s from faces, emojis, thumbs together)
    al01 = epochs['learn/s01']
    al02 = epochs['learn/s02']
    al03 = epochs['learn/s03']

    # learn blocks separately (i.e. s01, s02, and s03 split by faces, emojis, and thumbs)
    fl01 = epochs['faces/learn/s01']
    fl02 = epochs['faces/learn/s02']
    fl03 = epochs['faces/learn/s03']
    el01 = epochs['emojis/learn/s01']
    el02 = epochs['emojis/learn/s02']
    el03 = epochs['emojis/learn/s03']
    tl01 = epochs['thumbs/learn/s01']
    tl02 = epochs['thumbs/learn/s02']
    tl03 = epochs['thumbs/learn/s03']

    # test block syllables separated by f/e/t
    # 1,2,3 = real "words"
    ft01 = epochs['faces/test/s01']
    ft02 = epochs['faces/test/s02']
    ft03 = epochs['faces/test/s03']
    et01 = epochs['emojis/test/s01']
    et02 = epochs['emojis/test/s02']
    et03 = epochs['emojis/test/s03']
    tt01 = epochs['thumbs/test/s01']
    tt02 = epochs['thumbs/test/s02']
    tt03 = epochs['thumbs/test/s03']
    # 4,5,6 = near misses
    ft04 = epochs['faces/test/s04']
    ft05 = epochs['faces/test/s05']
    ft06 = epochs['faces/test/s06']
    et04 = epochs['emojis/test/s04']
    et05 = epochs['emojis/test/s05']
    et06 = epochs['emojis/test/s06']
    tt04 = epochs['thumbs/test/s04']
    tt05 = epochs['thumbs/test/s05']
    tt06 = epochs['thumbs/test/s06']
    # 7,8,9 = near misses
    ft07 = epochs['faces/test/s07']
    ft08 = epochs['faces/test/s08']
    ft09 = epochs['faces/test/s09']
    et07 = epochs['emojis/test/s07']
    et08 = epochs['emojis/test/s08']
    et09 = epochs['emojis/test/s09']
    tt07 = epochs['thumbs/test/s07']
    tt08 = epochs['thumbs/test/s08']
    tt09 = epochs['thumbs/test/s09']
    # 10, 11, 12 = random syllable combos
    ft10 = epochs['faces/test/s10']
    ft11 = epochs['faces/test/s11']
    ft12 = epochs['faces/test/s12']
    et10 = epochs['emojis/test/s10']
    et11 = epochs['emojis/test/s11']
    et12 = epochs['emojis/test/s12']
    tt10 = epochs['thumbs/test/s10']
    tt11 = epochs['thumbs/test/s11']
    tt12 = epochs['thumbs/test/s12']
    # test block syllables (collapsed across f/e/t)
    at01 = epochs['test/s01']
    at02 = epochs['test/s02']
    at03 = epochs['test/s03']
    at04 = epochs['test/s04']
    at05 = epochs['test/s05']
    at06 = epochs['test/s06']
    at07 = epochs['test/s07']
    at08 = epochs['test/s08']
    at09 = epochs['test/s09']
    at10 = epochs['test/s10']
    at11 = epochs['test/s11']
    at12 = epochs['test/s12']


    all_epochs = [al01,
                  al02,
                  al03,
                  fl01,
                  fl02,
                  fl03,
                  el01,
                  el02,
                  el03,
                  tl01,
                  tl02,
                  tl03,
                  ft01,
                  ft02,
                  ft03,
                  et01,
                  et02,
                  et03,
                  tt01,
                  tt02,
                  tt03,
                  ft04,
                  ft05,
                  ft06,
                  et04,
                  et05,
                  et06,
                  tt04,
                  tt05,
                  tt06,
                  ft07,
                  ft08,
                  ft09,
                  et07,
                  et08,
                  et09,
                  tt07,
                  tt08,
                  tt09,
                  ft10,
                  ft11,
                  ft12,
                  et10,
                  et11,
                  et12,
                  tt10,
                  tt11,
                  tt12,
                  at01,
                  at02,
                  at03,
                  at04,
                  at05,
                  at06,
                  at07,
                  at08,
                  at09,
                  at10,
                  at11,
                  at12]

    codes = ['al01',
             'al02',
             'al03',
             'fl01',
             'fl02',
             'fl03',
             'el01',
             'el02',
             'el03',
             'tl01',
             'tl02',
             'tl03',
             'ft01',
             'ft02',
             'ft03',
             'et01',
             'et02',
             'et03',
             'tt01',
             'tt02',
             'tt03',
             'ft04',
             'ft05',
             'ft06',
             'et04',
             'et05',
             'et06',
             'tt04',
             'tt05',
             'tt06',
             'ft07',
             'ft08',
             'ft09',
             'et07',
             'et08',
             'et09',
             'tt07',
             'tt08',
             'tt09',
             'ft10',
             'ft11',
             'ft12',
             'et10',
             'et11',
             'et12',
             'tt10',
             'tt11',
             'tt12',
             'at01',
             'at02',
             'at03',
             'at04',
             'at05',
             'at06',
             'at07',
             'at08',
             'at09',
             'at10',
             'at11',
             'at12']

    print('Creating stcs for subject %s' % subject)

    for code, epoch in zip(codes, all_epochs):
        # average the epochs into evokeds
        print('Creating averages for subject %s %s' % (subject, code))
        ave = epoch.average(method='mean')
        ave.save(op.join(ave_path, '%s_%s-ave.fif' % (code, subject)))
        # all_aves.append(op.join(ave_path, '%s_%s-ave.fif' % (code, subject)))
        # read in the evoked file
        evk = mne.read_evokeds(op.join(ave_path, '%s_%s-ave.fif' % (code, subject)))
        # make the stc
        stc = apply_inverse(evk[0], inv, method=method)
        stc.save(op.join(stc_path, '%s_%s' % (code, subject)))
        # do morphing to generate morphed stcs for use in difference movies
        stc_for_morph = mne.read_source_estimate(op.join(stc_path, '%s_%s' % (code, subject)))
        morph = mne.compute_source_morph(stc_for_morph, subject_from=subject, subject_to='fsaverage',
                                         subjects_dir=anat_dir, spacing=6).apply(stc_for_morph)
        morph.save(op.join(raw_dir, subject, 'stc', '%s_%s_morphed' % (code, subject)))














