#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import os
import os.path as op
import mne
import numpy as np


### SOURCE SPACE GRAND AVERAGES SCRIPT
# set important variables


signed = False

method = 'eLORETA'

skip_visual = False

skip_auditory = True

if signed:
    tag = '/signed/'
    ext = '_signed'
else:
   tag = '/'
   ext = ''

# raw_dir = '/home/nordme/data/genz/genz_active/'
# raw_dir = '/brainstudio/MEG/genz/genz_proc/active/'
raw_dir = '/brainstudio/MEG/genz/genz_proc/active/twa_hp/'
anat_dir = '/brainstudio/MEG/genz/anatomy/'

subjects = [x for x in os.listdir(raw_dir) if op.isdir('%s%s' % (raw_dir, x)) and 'genz' in x]
subjects.sort()

blocks = [ 'a','f', 'e', 't']
conditions = ['l', 't']

codes = ['%s%s%02d' % (block, condition, syllable) 
                    for condition in conditions                
                    for block in blocks                    
                    for syllable in (range(1,13) if condition == 't' else range(1,4))]

ages = ['all', '9', '11', '13', '15', '17']

feml = [[], [], [], [], [], []]

male = [[], [], [], [], [], []]

both = [[], [], [], [], [], []]

genders = [both, male, feml]

gender_names = ['both', 'male', 'female']

master_list = []

# create subject pools (gender x age) since each grand average will need to draw on a different set of subjects
# index 0 corresponds to subjects of all ages
for i, age in enumerate(ages):
    feml[i] = [sub for sub in subjects if '%sa' % age in sub and int(sub[4:7]) % 2 == 0]
    male[i] = [sub for sub in subjects if '%sa' % age in sub and int(sub[4:7]) % 2 != 0]
    both[i] = [sub for sub in subjects if '%sa' % age in sub]
    feml[0] = [sub for sub in subjects if int(sub[4:7]) % 2 == 0]
    male[0] = [sub for sub in subjects if int(sub[4:7]) % 2 != 0]
    both[0] = [sub for sub in subjects]
    print('Finished creating age pool %s for stc averaging.' % age)

# make a master list of subject pools to average over
# with handy entries that include the list of relevant subjects as well as the gender and age
for gender, gender_name in zip(genders, gender_names):
    for i in [0]:
        master_list.append([gender_name, 'allage', gender[i]])
    for i in np.arange(1, 6):
        master_list.append([gender_name, '%d' % (i*2+7), gender[i]])
        print('Added %s %d to master list of subject pools.' % (gender_name, i))

# create visual grand averages

epoch = ['FRN', 'SPN']

blocks = ['faces', 'emojis', 'thumbs', 'allblocks']

feedback = ['correct', 'incorrect', 'bothfdbk']

vis_conds = [[e, b, f] for e in epoch for b in blocks for f in feedback]

vcodes = ['%s_%s_%s' % (e, b, f) for e in epoch for b in blocks for f in feedback]

vave_dir = op.join(raw_dir, '%s_ave' % method, 'visual%s' % tag)

aave_dir = op.join(raw_dir, '%s_ave' % method, 'auditory%s' % tag)

if skip_visual:
    print('Skipping visual grand aves.')
else:
    print('Beginning work on visual stcs.')
    for list in master_list:
        gname, age, subjects = list
        print('Working on visuals for group %s %s.' % (gname, age))
        for vcode in vcodes:
            save_path = op.join(vave_dir, '%s_%s_%s%s' % (gname, age, vcode, ext))
            stc_ave = 0
            for subject in subjects:
                stc_path = op.join(raw_dir, subject, '%s_stc' % method, 'visual', '%s_%s_morphed' % (vcode, subject))
                stc = mne.read_source_estimate(stc_path)
                if signed:
                    stc_ave += stc
                else:
                    stc_ave += abs(stc)
            try:
                stc_ave /= len(subjects)
                assert stc_ave.data.ndim == 2 and stc_ave.data.shape[0] == 20484
                stc_ave.save(save_path)
                print('Saved stc ave %s.' % save_path)
            except ZeroDivisionError:
                print('Hmm. Looks like we need subjects for group %s %s.' % (gname, age))


# create auditory grand averages
if skip_auditory:
    print('Skipping auditory grand aves.')
else:
    print('Starting work on auditory grand averages.')
    for list in master_list:
        gname, age, subjects = list
        print('Working on group %s %s.' % (gname, age))
        for code in codes:
            save_path = op.join(aave_dir, '%s_%s_%s%s' % (gname, age, code, ext))
            stc_ave = 0
            for subject in subjects:
                stc_path = op.join(raw_dir, subject, '%s_stc' % method, 'auditory', '%s_%s_morphed' % (code, subject))
                stc = mne.read_source_estimate(stc_path)
                if signed:
                    stc_ave += stc
                else:
                    stc_ave += abs(stc)
            try:
                stc_ave /= len(subjects)
                assert stc_ave.data.ndim == 2 and stc_ave.data.shape[0] == 20484
                stc_ave.save(save_path)
                print('Saved stc ave %s.' % save_path)
            except ZeroDivisionError:
                print('Hmm. Looks like we need subjects for group %s %s.' % (gname, age))