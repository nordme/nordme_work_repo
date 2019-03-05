#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 11 11:03:42 2018

@author: mdclarke
"""



"""
Created on Mon Jul  9 23:33:22 2018

@author: mdclarke

script to create grand averages for genZ data. 
"""
# 115 215 320 413 415 419 517 519 THUMBS LEARN

import mne
from os import path as op

data_path = '/brainstudio/MEG/genz/genz_proc/active/'
# data_path = '/home/nordme/data/genz/genz_active/'
save_path = '/brainstudio/MEG/genz/genz_proc/active/grand_ave/'
lpf = 80

subjs = ['genz105_9a',
         'genz106_9a',
         'genz108_9a',
         'genz110_9a',
         'genz111_9a',
         'genz112_9a',
         'genz113_9a',
         'genz114_9a',
         #'genz115_9a',
         'genz116_9a',
         'genz117_9a',
         'genz118_9a',
         'genz119_9a',
         'genz120_9a',
         'genz122_9a',
         'genz123_9a',
         'genz124_9a',
         'genz125_9a',
         'genz126_9a',
         'genz128_9a',
         'genz130_9a',
         'genz131_9a',
         'genz133_9a']

analysis = 'FRN'
conditions = ['vis']
age_group = '9a'

do_split = True
do_all = True

if do_all:
    for cond in conditions:
        evokeds = []
        for subj in subjs:
            evoked_file = op.join(data_path, '%s' % subj, 'inverse',
                                '%s_%d-sss_eq_%s-ave.fif' % (analysis, lpf, subj))
            evoked = mne.read_evokeds(evoked_file, condition=cond, baseline=(None,0))
            assert evoked.comment == cond
            evokeds.append(evoked)
        grndavr = mne.grand_average(evokeds)
        mne.Evoked.save(grndavr, op.join(save_path, '%s_%s-N%d-ave.fif'
                                         % (age_group, analysis, len(subjs))))
if do_split:

    conditions = ['vis/emojis/learn/correct',
                  'vis/emojis/learn/incorrect',
                  'vis/faces/learn/correct',
                  'vis/faces/learn/incorrect',
                  'vis/thumbs/learn/correct',
                  'vis/thumbs/learn/incorrect']

    for i, cond in enumerate(conditions):
        split_evokeds = []
        for subj in subjs:
            split_file = op.join(data_path, '%s' % subj, 'inverse',
                                  '%s-Split_%d-sss_eq_%s-ave.fif' % (analysis, lpf, subj))
            evoked = mne.read_evokeds(split_file, condition=cond, baseline=(None, 0))
            assert evoked.comment == cond
            split_evokeds.append(evoked)
        grndavr = mne.grand_average(split_evokeds)
        mne.Evoked.save(grndavr, op.join(save_path, '%s_%s-N%d-%d-ave.fif'
                                         % (age_group, analysis, len(subjs), i)))
        print('Created file %s' % op.join(save_path, '%s_%s-N%d-%d-ave.fif' % (age_group, analysis, len(subjs), i)))