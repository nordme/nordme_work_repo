#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 11 11:03:42 2018

@author: mdclarke

script to create auditory grand averages for genZ data. 

"""
# 124 no faces learn 

import mne
import os
import itertools
from os import path as op

# set what type of run you want to do
fixed_or_twa = 'fixed'
vis_or_aud = 'aud'
by_all = True
by_gender = True
resp = 'FRN'  # 'FRN' or 'SPN'; applies to vis only

# establish key variables
ages = ['9a', '11a', '13a', '15a', '17a']
data_path = '/storage/genz_active/t1/%s_hp/' % fixed_or_twa
avg_path = op.join(data_path, 'group_averages')
analysis = 'Split' if vis_or_aud == 'aud' else resp + '-Split'
lpf = 80

# prep subject lists
all_subjects = [x for x in os.listdir(data_path) if 'genz' in x and op.isdir(data_path + x)]
nine = []
eleven = []
thirteen = []
fifteen = []
seventeen = []

for s in all_subjects:
    if '9a' in s:
        nine.append(s)
    elif '11a' in s:
        eleven.append(s)
    elif '13a' in s:
        thirteen.append(s)
    elif '15a' in s:
        fifteen.append(s)
    elif '17a' in s:
        seventeen.append(s)

# prep name and condition lists

blocks = ['emojis', 'faces', 'thumbs']
stim = ['aud', 'vis']
conditions = ['learn', 'test']
aud_syl = ['s01', 's02', 's03']
vis_fdbk = ['correct', 'incorrect']

aud_conditions = []
aud_names = []
vis_conditions = []
vis_names = []

aud_product = list(itertools.product(blocks, conditions, aud_syl))
vis_product = list(itertools.product(blocks, ['learn'], vis_fdbk))

for (b, c, s) in aud_product:
    ac = 'aud/%s/%s/%s' % (b,c,s)
    an = 'aud_%s_%s_%s' % (b,c,s)
    aud_conditions.append(ac)
    aud_names.append(an)

for (b, c, f) in vis_product:
    vc = 'vis/%s/%s/%s' % (b,c,f)
    vn = 'vis_%s_%s_%s' % (b,c,f)
    vis_conditions.append(vc)
    vis_names.append(vn)

# begin writing grand averages by age group, separated by gender if so specified
# iterate by age group, by condition code,

gaves = []
f_gaves = []
m_gaves = []

for age in ages:
    conditions = aud_conditions if vis_or_aud == 'aud' else vis_conditions
    names = aud_names if vis_or_aud == 'aud' else vis_names
    if age == '9a':
        subjs = nine
    if age == '11a':
        subjs = eleven
    if age == '13a':
        subjs = thirteen
    if age == '15a':
        subjs = fifteen
    if age == '17a':
        subjs = seventeen
    if by_gender:
        for j, (cond, name) in enumerate(zip(conditions, names)):
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
        mne.write_evokeds(op.join(avg_path, 'f' + '%s_%s_%s_N%d-ave.fif'
                                  % (vis_or_aud, age, analysis, len(f_evokeds))), f_gaves)
        mne.write_evokeds(op.join(avg_path, 'm' + '%s_%s_%s_N%d-ave.fif'
                                  % (vis_or_aud, age, analysis, len(m_evokeds))), m_gaves)

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
            mne.write_evokeds(op.join(avg_path, '%s_%s_%s_N%d-ave.fif'
                                      % (vis_or_aud, age, analysis, len(subjs))), gaves)

