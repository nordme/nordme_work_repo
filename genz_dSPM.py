#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import os
import os.path as op
import mne
import numpy as np
from mne.minimum_norm import (apply_inverse, read_inverse_operator)

# set important variables

#raw_dir = '/home/nordme/data/genz/genz_active/'

equalize = True
do_vis = True
do_aud = True

# raw_dir = '/brainstudio/MEG/genz/genz_proc/active/twa_hp/'
# anat_dir = '/brainstudio/MEG/genz/anatomy/'

raw_dir = '/storage/genz_active/t1/twa_hp/'
anat_dir = '/storage/anat/subjects/'

# raw_dir = '/home/nordme/data/genz/'
# anat_dir = '/home/nordme/data/genz/anat'

try_eLORETA = False

if try_eLORETA:
    method = 'eLORETA'
else:
    method = 'dSPM'

#skip = ['genz125_9a', 'genz218_11a']
# subjects = [x for x in os.listdir(raw_dir) if op.isdir('%s%s' % (raw_dir, x)) and 'genz' in x and not np.in1d(x, skip)]
subjects = ['genz125_9a', 'genz218_11a']
subjects.sort()

snr = 3.
lambda2 = 1. / snr ** 2

# prep lists of epoch conditions and codes for the conditions

blocks = [ 'a','f', 'e', 't']
conditions = ['l', 't']
syllables = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']

bnames = [ '','faces/', 'emojis/', 'thumbs/']
cnames = ['learn', 'test']

epoch_names = ['%s%s/s%02d' % (bname, cname, sname)
         for cname in cnames
         for bname in bnames
         for sname in (range(1, 13) if cname == 'test' else range(1, 4))]

# code pattern:  block, condition, syllable position
# a = all blocks, f = faces, e = emojis, t = thumbs; l = learn condition, t = test condition

codes = ['%s%s%02d' % (block, condition, syllable)
         for condition in conditions
         for block in blocks
         for syllable in (range(1, 13) if condition == 't' else range(1, 4))]

# create stcs

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
    inv_path = op.join(sub_path, 'inverse', '%s_aud-80-sss-meg-fixed-inv.fif' % subject)
    src_path = op.join(anat_dir, subject, 'bem', '%s-oct-6-src.fif' % subject)

    # read in inverse and compute morph matrix for later application
    inv = read_inverse_operator(inv_path)
    src = mne.read_source_spaces(src_path)
    morph = mne.compute_source_morph(inv['src'], subject_from=subject, subject_to='fsaverage',
                                     subjects_dir=anat_dir, spacing=5)
    morph.save(op.join(sub_path, '%s_stc' % method, '%s_source_morph.h5' % subject), overwrite=True)

    # AUDITORY STCS

    # create appropriate groups of epochs

    epochs = mne.read_epochs(epo_path)

    aud_epochs = []

    for name in epoch_names:
        aud_epochs.append(epochs[name])

    print('Creating stcs for subject %s' % subject)
    if do_aud:
        for code, epoch in zip(codes, aud_epochs):
            # make individual evoked files by averaging the epochs
            print('Creating averages for subject %s %s' % (subject, code))
            ave = epoch.average(method='mean')
            ave.save(op.join(ave_path, '%s_%s-ave.fif' % (code, subject)))
            # make the stc
            stc = apply_inverse(ave, inv, method=method, lambda2=lambda2)
            stc.save(op.join(stc_path, '%s_%s' % (code, subject)))
            # make morphed stcs for use in movies
            morphed_stc = morph.apply(stc)
            morphed_stc.save(op.join(stc_path, '%s_%s_morphed' % (code, subject)))

    # VISUAL STCS
    if do_vis:
        vis_path = op.join(sub_path, 'epochs', 'All_80-sss_%s-vis-epo.fif' % subject)
        vave_path = op.join(sub_path, 'inverse', 'visual')
        vstc_path = op.join(sub_path, '%s_stc' % method, 'visual')
        vinv_path = op.join(sub_path, 'inverse', '%s_vis-80-sss-meg-fixed-inv.fif' % subject)

        vinv = read_inverse_operator(vinv_path)
        vis_epochs = mne.read_epochs(vis_path)

        blocks = ['faces', 'emojis', 'thumbs', 'allblocks']

        feedback = ['correct', 'incorrect', 'bothfdbk']

        for b in blocks:
            for f in feedback:
                vcode = '%s_%s' % (b, f)
                print('Creating averages for subject %s %s' % (subject, vcode))
                b_insert = '' if b == 'allblocks' else '/' + b
                f_insert = '' if f == 'bothfdbk' else '/' + f
                ave = vis_epochs['vis%s%s' % (b_insert, f_insert)].average(method='mean')
                ave.save(op.join(vave_path, '%s_%s-ave.fif' % (vcode, subject)))
                # make the stc
                stc = apply_inverse(ave, vinv, method=method, lambda2=lambda2)
                stc.save(op.join(vstc_path, '%s_%s' % (vcode, subject)))
                # make morphed stcs for use in difference movies
                morphed_stc = morph.apply(stc)
                morphed_stc.save(op.join(vstc_path, '%s_%s_morphed' % (vcode, subject)))
