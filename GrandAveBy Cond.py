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
lpf = 80

subjs = ['genz401_15a', 'genz403_15a', 'genz405_15a', 'genz406_15a',
         'genz409_15a', 'genz411_15a', 'genz412_15a', 'genz413_15a',
         'genz414_15a', 'genz415_15a', 'genz416_15a', 'genz417_15a',
         'genz418_15a', 'genz419_15a', 'genz420_15a', 'genz421_15a',
         'genz422_15a', 'genz423_15a', 'genz424_15a', 'genz425_15a',
         'genz426_15a', 'genz427_15a', 'genz429_15a']
        
analysis = 'SPN'
conditions = ['vis']

do_split = True
do_all = False

if do_all:
    for cond in conditions:
        evokeds = []
        for subj in subjs:
            evoked_file = op.join(data_path, '%s' %subj, 'inverse',
                                '%s_%d-sss_eq_%s-ave.fif' % (analysis, lpf, subj))
            evoked = mne.read_evokeds(evoked_file, condition=cond, baseline=(None,0))
            assert evoked.comment == cond
            evokeds.append(evoked)
        grndavr = mne.grand_average(evokeds)
        mne.Evoked.save(grndavr, op.join(data_path, '15a_%s-N%d-ave.fif'
                                         % (analysis, len(subjs))))
if do_split:

    conditions = ['vis/emojis/learn/correct',
                  'vis/emojis/learn/incorrect',
                  'vis/faces/learn/correct',
                  'vis/faces/learn/incorrect',
                  'vis/thumbs/learn/correct',
                  'vis/thumbs/learn/incorrect']

blah blah blah blah blah change practice

    for i, cond in enumerate(conditions):
        split_evokeds = []
        for subj in subjs:
            split_file = op.join(data_path, '%s' % subj, 'inverse',
                                  '%s-Split_%d-sss_eq_%s-ave.fif' % (analysis, lpf, subj))
            evoked = mne.read_evokeds(split_file, condition=cond, baseline=(None, 0))
            assert evoked.comment == cond
            split_evokeds.append(evoked)
                mne.Evoked.save(grndavr, op.join('/home/nordme/GitHub/', '15a_%s-N%d-%d-ave.fif'
                                         % (analysis, len(subjs), i)))
        print('Created file %s' % op.join('/home/nordme/GitHub/', '15a_%s-N%d-%d-ave.fif' % (analysis, len(subjs), i)))
