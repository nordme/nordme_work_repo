#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import os
import os.path as op
import mne
from mne.minimum_norm import (apply_inverse, read_inverse_operator)

# set important variables

#raw_dir = '/home/nordme/data/genz/genz_active/'

equalize = True

raw_dir = '/brainstudio/MEG/genz/genz_proc/active/twa_hp/'
anat_dir = '/brainstudio/MEG/genz/anatomy/'

try_eLORETA = True

if try_eLORETA:
    method = 'eLORETA'
else:
    method = 'dSPM'

subjects = [x for x in os.listdir(raw_dir) if op.isdir('%s%s' % (raw_dir, x)) and 'genz' in x]
subjects.sort()

snr = 3.
lambda2 = 1. / snr ** 2


blocks = [ 'a','f', 'e', 't']
conditions = ['l', 't']
syllables = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']



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
    
    all_epochs = [    
        # all learn blocks by syllable position (e.g. all the s01s from faces, emojis, thumbs together)
        epochs['learn/s01'],
        epochs['learn/s02'],
        epochs['learn/s03'],
    
        # learn blocks separately (i.e. s01, s02, and s03 split by faces, emojis, and thumbs)
        epochs['faces/learn/s01'],
        epochs['faces/learn/s02'],
        epochs['faces/learn/s03'],
        epochs['emojis/learn/s01'],
        epochs['emojis/learn/s02'],
        epochs['emojis/learn/s03'],
        epochs['thumbs/learn/s01'],
        epochs['thumbs/learn/s02'],
        epochs['thumbs/learn/s03'],
    
        # all test block syllables (collapsed across f/e/t)
        epochs['test/s01'],
        epochs['test/s02'],
        epochs['test/s03'],
        epochs['test/s04'],
        epochs['test/s05'],
        epochs['test/s06'],
        epochs['test/s07'],
        epochs['test/s08'],
        epochs['test/s09'],
        epochs['test/s10'],
        epochs['test/s11'],
        epochs['test/s12'],
    
        # test block syllables separated by f/e/t
        # 1,2,3 = real "words"
        # 4,5,6 = near miss words
        # 7,8,9 = near misses type 2
        # 10, 11, 12 = random syllable combos
        epochs['faces/test/s01'],
        epochs['faces/test/s02'],
        epochs['faces/test/s03'],
        epochs['faces/test/s04'],
        epochs['faces/test/s05'],
        epochs['faces/test/s06'],
        epochs['faces/test/s07'],
        epochs['faces/test/s08'],
        epochs['faces/test/s09'],
        epochs['faces/test/s10'],
        epochs['faces/test/s11'],
        epochs['faces/test/s12'],
        # emojis
        epochs['emojis/test/s01'],
        epochs['emojis/test/s02'],
        epochs['emojis/test/s03'],
        epochs['emojis/test/s04'],
        epochs['emojis/test/s05'],
        epochs['emojis/test/s06'],
        epochs['emojis/test/s07'],
        epochs['emojis/test/s08'],
        epochs['emojis/test/s09'],
        epochs['emojis/test/s10'],
        epochs['emojis/test/s11'],
        epochs['emojis/test/s12'],
        # thumbs
        epochs['thumbs/test/s01'],
        epochs['thumbs/test/s02'],
        epochs['thumbs/test/s03'],
        epochs['thumbs/test/s04'],
        epochs['thumbs/test/s05'],
        epochs['thumbs/test/s06'],
        epochs['thumbs/test/s07'],
        epochs['thumbs/test/s08'],
        epochs['thumbs/test/s09'],
        epochs['thumbs/test/s10'],
        epochs['thumbs/test/s11'],
        epochs['thumbs/test/s12']]


    codes = ['%s%s%02d' % (block, condition, syllable) 
                    for condition in conditions                
                    for block in blocks                    
                    for syllable in (range(1,13) if condition == 't' else range(1,4))]
    
   
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
