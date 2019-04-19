#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import os
import os.path as op
import mne
from mne.minimum_norm import (apply_inverse, read_inverse_operator)

# set important variables

raw_dir = '/home/nordme/data/genz/genz_active/'
# raw_dir = '/brainstudio/MEG/genz/genz_proc/active/'
anat_dir = '/brainstudio/MEG/genz/anatomy/'

try_eLORETA = True

if try_eLORETA:
    method = 'eLORETA'
else:
    method = 'dSPM'

subjects = ['genz111_9a',
            'genz115_9a',
            'genz130_9a',
            'genz131_9a',
            'genz225_11a',
            'genz232_11a',
            'genz334_13a',
            # 'genz335_13a',
            'genz429_15a',
            'genz430_15a',
            'genz529_17a',
            #'genz530_17a'
            ]

snr = 3.
lambda2 = 1. / snr ** 2

for subject in subjects:
    # create directories and paths
    sub_path = op.join(raw_dir, subject)

    if not op.isdir(op.join(sub_path, '%s_stc' % method)):
        os.mkdir(op.join(sub_path, '%s_stc' % method))

    if not op.isdir(op.join(sub_path, '%s_stc' % method, 'visual')):
        os.mkdir(op.join(sub_path, '%s_stc' % method, 'visual'))

    if not op.isdir(op.join(sub_path, '%s_stc' % method, 'auditory')):
        os.mkdir(op.join(sub_path, '%s_stc' % method, 'auditory'))

    if not op.isdir(op.join(sub_path, 'inverse', 'visual')):
         os.mkdir(op.join(sub_path, 'inverse', 'visual'))

    if not op.isdir(op.join(sub_path, 'inverse', 'auditory')):
        os.mkdir(op.join(sub_path, 'inverse', 'auditory'))

    stc_path = op.join(sub_path, '%s_stc' % method, 'auditory')
    epo_path = op.join(sub_path, 'epochs', 'All_80-sss_%s-epo.fif' % subject)
    ave_path = op.join(sub_path, 'inverse', 'auditory')
    inv_path = op.join(sub_path, 'inverse', '%s_aud-80-sss-meg-erm-fixed-inv.fif' % subject)
    src_path = op.join(anat_dir, subject, 'bem', '%s-oct-6-src.fif' % subject)

    # read in inverse and compute morph matrix for later application
    inv = read_inverse_operator(inv_path)
    src = mne.read_source_spaces(src_path)
    morph = mne.compute_source_morph(src, subject_from=subject, subject_to='fsaverage',
                                     subjects_dir=anat_dir, spacing=5)
    morph.save(op.join(sub_path, '%s_stc' % method, '%s_source_morph.h5' % subject), overwrite=True)


    # AUDITORY STCS

    # create appropriate groups of epochs

    epochs = mne.read_epochs(epo_path)

    # code pattern:  block, condition, syllable position
    # a = all blocks, f = faces, e = emojis, t = thumbs; l = learn condition, t = test condition

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

    # all test block syllables (collapsed across f/e/t)
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
    # 4,5,6 = near miss words
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
        # make the stc
        stc = apply_inverse(ave, inv, method=method, lambda2=lambda2)
        stc.save(op.join(stc_path, '%s_%s' % (code, subject)))
        # make morphed stcs for use in difference movies
        morphed_stc = morph.apply(stc)
        morphed_stc.save(op.join(stc_path, '%s_%s_morphed' % (code, subject)))



    # VISUAL STCS

    FRN_path = op.join(sub_path, 'epochs', 'All_80-sss_%s-FRN-epo.fif' % subject)
    SPN_path = op.join(sub_path, 'epochs', 'All_80-sss_%s-SPN-epo.fif' % subject)

    vave_path = op.join(sub_path, 'inverse', 'visual')
    vstc_path = op.join(sub_path, '%s_stc' % method, 'visual')
    vinv_path = op.join(sub_path, 'inverse', '%s_vis-80-sss-meg-erm-fixed-inv.fif' % subject)

    vinv = read_inverse_operator(vinv_path)

    # create appropriate groups of epochs

    FRN = mne.read_epochs(FRN_path)
    SPN = mne.read_epochs(SPN_path)

    epoch = ['FRN', 'SPN']

    blocks = ['faces', 'emojis', 'thumbs', 'allblocks']

    feedback = ['correct', 'incorrect', 'bothfdbk']

    vis_conds = [[e, b, f] for e in epoch for b in blocks for f in feedback]

    vis_epochs = []

    for [e,b,f] in vis_conds:
        if 'FRN' in e:
            if 'allblocks' in b:
                if 'bothfdbk' in f:
                    epoch = FRN['learn']
                    vis_epochs.append([epoch, [e,b,f]])
                else:
                    epoch = FRN['learn/%s' % f]
                    vis_epochs.append([epoch, [e,b,f]])
            else:
                if 'bothfdbk' in f:
                    epoch = FRN['%s' % b]
                    vis_epochs.append([epoch, [e,b,f]])
                else:
                    epoch = FRN['%s/learn/%s' % (b, f)]
                    vis_epochs.append([epoch, [e,b,f]])
        else:
            if 'allblocks' in b:
                if 'bothfdbk' in f:
                    epoch = SPN['learn']
                    vis_epochs.append([epoch, [e,b,f]])
                else:
                    epoch = SPN['learn/%s' % f]
                    vis_epochs.append([epoch, [e,b,f]])
            else:
                if 'bothfdbk' in f:
                    epoch = SPN['%s' % b]
                    vis_epochs.append([epoch, [e,b,f]])
                else:
                    epoch = SPN['%s/learn/%s' % (b, f)]
                    vis_epochs.append([epoch, [e,b,f]])

    for ve, [e, b, f] in vis_epochs:
        vcode = '%s_%s_%s' % (e, b, f)
        print('Creating averages for subject %s %s' % (subject, vcode))
        ave = ve[0].average(method='mean')
        ave.save(op.join(vave_path, '%s_%s-ave.fif' % (vcode, subject)))
        # make the stc
        stc = apply_inverse(ave, vinv, method=method, lambda2=lambda2)
        stc.save(op.join(vstc_path, '%s_%s' % (vcode, subject)))
        # make morphed stcs for use in difference movies
        morphed_stc = morph.apply(stc)
        morphed_stc.save(op.join(vstc_path, '%s_%s_morphed' % (vcode, subject)))
