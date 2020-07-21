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
import numpy as np
import itertools
from os import path as op

# set what type of run you want to do
fixed_or_twa = 'fixed'
vis_or_aud = 'vis'
by_all = True
by_gender = True
resp = 'vis'  # 'FRN' or 'SPN'; applies to vis only
do_test = False   # whether or not to include test conditions in the epochs file

# establish key variables
ages = ['9a', '11a', '13a', '15a', '17a', 'allage', 'nonines']
# ages = ['9a']
data_path = '/storage/genz_active/t1/%s_hp/' % fixed_or_twa
avg_path = op.join(data_path, 'group_averages', '%s' % vis_or_aud)
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
conditions = ['learn', 'test'] if do_test else ['learn']
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
    if age == 'allage':
        subjs = all_subjects
    if age == 'nonines':
        subjs = [x for x in all_subjects if not np.in1d(x, nine)]
    subjs.sort()
    print('Age %s: %s' % (age, subjs))
    gaves = []
    m_evokeds = []
    f_evokeds = []
    if by_gender:
        for j, (cond, name) in enumerate(zip(conditions, names)):
            print('Starting condition %s.' % name)
            fc_ev = []
            mc_ev = []
            for subj in subjs:
                print('Adding subjects %s.' % subj)
                if int(subj[4:7]) % 2 == 0:  # if the subject number is even, the subject is a girl
                    gender = 'f'
                else:
                    gender = 'm'
                evoked_file = op.join(data_path, '%s' % subj, 'inverse', '%s_%d-sss_eq_%s-ave.fif' % (analysis, lpf, subj))
                evoked = mne.read_evokeds(evoked_file, condition=cond, baseline=(None, 0))
#                if proj == 'proj_on':
#                    evoked = mne.read_evokeds(evoked_file, condition=cond, baseline=(None, 0))
#                else:
#                    e = mne.read_evokeds(evoked_file, condition=cond, baseline=(None, 0))
#                    evoked = e.copy().del_proj()
                assert evoked.comment == cond
                if gender == 'f':
                    fc_ev.append(evoked)
                else:
                    mc_ev.append(evoked)
            print('For condition %s' % name)
            print('fc_ev: %s' % len(fc_ev))
            print('mc_ev: %s' % len(mc_ev))
            f_evokeds.append(mne.grand_average(fc_ev))
            f_evokeds[j].comment = 'f_%s' % cond
            m_evokeds.append(mne.grand_average(mc_ev))
            m_evokeds[j].comment = 'm_%s' % cond
        insert = '-learn' if not do_test else ''
        f_save = op.join(avg_path, 'f' + '%s_%s_%s_N%d%s-ave.fif' % (vis_or_aud, age, analysis, len(fc_ev), insert))
        m_save = op.join(avg_path, 'm' + '%s_%s_%s_N%d%s-ave.fif' % (vis_or_aud, age, analysis, len(mc_ev), insert))
        print('All done with age %s! Saving the gender grand averages.' % age)
        mne.write_evokeds(f_save, f_evokeds)
        mne.write_evokeds(m_save, m_evokeds)

    if by_all:
        for j, (cond, name) in enumerate(zip(conditions, names)):
            evokeds = []
            for subj in subjs:
                evoked_file = op.join(data_path, '%s' %subj, 'inverse', '%s_%d-sss_eq_%s-ave.fif' % (analysis, lpf, subj))
                evoked = mne.read_evokeds(evoked_file, condition=cond, baseline=(None, 0))
#                if proj == 'proj_on':
#                    evoked = mne.read_evokeds(evoked_file, condition=cond, baseline=(None, 0))
#                else:
#                    e = mne.read_evokeds(evoked_file, condition=cond, baseline=(None, 0))
#                    evoked = e.copy().del_proj()
                assert evoked.comment == cond
                evokeds.append(evoked)
            gaves.append(mne.grand_average(evokeds))
            gaves[j].comment = cond
            insert = '-learn' if not do_test else ''
            all_save = op.join(avg_path, '%s_%s_%s_N%d%s-ave.fif' % (vis_or_aud, age, analysis, len(subjs), insert))
            mne.write_evokeds(all_save, gaves)

