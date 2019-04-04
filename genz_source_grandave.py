#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import os
import os.path as op
import mne
import numpy as np

from itertools import product

### SOURCE SPACE GRAND AVERAGES SCRIPT
# set important variables

raw_dir = '/home/nordme/data/genz/genz_active/'
# raw_dir = '/brainstudio/MEG/genz/genz_proc/active/'
anat_dir = '/brainstudio/MEG/genz/anatomy/'

subjects = []

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

ages = ['all', '9', '11', '13', '15', '17']

feml = [[], [], [], [], [], []]

male = [[], [], [], [], [], []]

both = [[], [], [], [], [], []]

genders = [both, male, feml]

gender_names = ['both', 'male', 'feml']

master_list = []

for i, age in enumerate(ages):
    feml[i] = [sub for sub in subjects if '%sa' % age in sub and int(sub[4:7]) % 2 == 0]
    male[i] = [sub for sub in subjects if '%sa' % age in sub and int(sub[4:7]) % 2 != 0]
    both[i] = [sub for sub in subjects if '%sa' % age in sub]
    feml[0] = [sub for sub in subjects if int(sub[4:7]) % 2 == 0]
    male[0] = [sub for sub in subjects if int(sub[4:7]) % 2 != 0]
    both[0] = [sub for sub in subjects]

for gender, gender_name in zip(genders, gender_names):
    for i in range[0:6]:
        master_list.append([gender_name, '%d' % (i*2+7), gender[i]])

for list in master_list:
    gname, age, subjects = list
        for subject in subjects:
            for code in codes:
                stc_ave = 0
                ave_path = op.join(raw_dir, 'stc_aves', '%s_%s_%s' % (gname, age, code))
                for subject in subjects:
                    stc_path = op.join(raw_dir, subject, 'stc', '%s_%s' % (code, subject))
                    stc = mne.read_source_estimate(stc_path)
                    stc_ave += stc
                stc_ave /= len(subjects)
                assert stc_ave.data.ndim == 2 and stc_ave.data.shape[0] == 8196
                stc_ave.save(ave_path)



























if by_gender:
    for j, (stc, code) in enumerate(zip(stcs, codes)):
        m_evokeds = []
        f_evokeds = []
        for subj in subjs:
            if int(subj[4:7]) % 2 == 0:  # if the subject number is even, the subject is a girl
                gender = 'f'
            else:
                gender = 'm'
            evoked_file = op.join(data_path, '%s' % subj, 'inverse',
                                  '%s_%d-sss_eq_%s-ave.fif'
                                  % (analysis, lpf, subj))
            evoked = mne.read_evokeds(evoked_file, condition=cond,
                                      baseline=(None, 0))
            assert evoked.comment == cond
            if gender == 'f':
                f_evokeds.append(evoked)
            else:
                m_evokeds.append(evoked)
        print('f_evokeds: %s' % len(f_evokeds))
        print('m_evokeds: %s' % len(m_evokeds))
        f_gaves.append(mne.grand_average(f_evokeds))
        f_gaves[j].comment = 'f_%s' % cond
        m_gaves.append(mne.grand_average(m_evokeds))
        m_gaves[j].comment = 'm_%s' % cond
    mne.write_evokeds(op.join(avg_path, 'f' + 'AUD_%s_%s_N%d-ave.fif'
                              % (age, analysis, len(f_evokeds))), f_gaves)
    mne.write_evokeds(op.join(avg_path, 'm' + 'AUD_%s_%s_N%d-ave.fif'
                              % (age, analysis, len(m_evokeds))), m_gaves)


if by_all:
    for j, (cond, name) in enumerate(zip(conditions, names)):
        evokeds = []
        for subj in subjs:
            evoked_file = op.join(data_path, '%s' %subj, 'inverse',
                                  '%s_%d-sss_eq_%s-ave.fif'
                                  % (analysis, lpf, subj))
            evoked = mne.read_evokeds(evoked_file, condition=cond,
                                      baseline=(None,0))
            assert evoked.comment == cond
            evokeds.append(evoked)
        gaves.append(mne.grand_average(evokeds))
        gaves[j].comment = cond
        mne.write_evokeds(op.join(avg_path, 'AUD_%s_%s_N%d-ave.fif'
                                  % (age, analysis, len(subjs))), gaves)


