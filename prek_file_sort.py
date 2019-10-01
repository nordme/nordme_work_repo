# -*- coding: utf-8 -*-
#
import os
import os.path as op
import shutil
import numpy as np

target_dir = '/home/nordme/data/prek/post_camp/'
raw_dir = '/home/nordme/data/prek/post_camp/fixed_hp/'
trans_dir = '/home/nordme/prek/trans/'


do_raws = False
force_prebads = True
fixed_or_twa = 'twa_hp'
raw_subdirs = True

subjects = [d for d in os.listdir(raw_dir) if op.isdir(op.join(raw_dir, d)) and 'prek' in d]
subjects.sort()


if do_raws:
    for subject in subjects:
        subject_path = op.join(target_dir, fixed_or_twa, subject)
        if op.isdir(subject_path):
            print('Subject %s has a subject directory.' % subject)
        else:
            os.mkdir(subject_path)

        raw_path = op.join(subject_path, 'raw_fif')
        if op.isdir(raw_path):
            print('Subject %s has a raw directory.' % subject)
        else:
            os.mkdir(raw_path)

        if raw_subdirs:
            sub_dir = ['raw_fif']
        else:
            sub_dirs = os.listdir(op.join(raw_dir, subject))
            sub_dirs.sort()
            if len(sub_dirs) == 2:
                sub_dir = [sub_dirs[0] if sub_dirs[0]>sub_dirs[1] else sub_dirs[1]]
            else:
                print('Subject %s has an unexpected number of recording dates. Manually check raws, please.' % subject)
                sub_dir = [sub_dirs[-1]]

        files = os.listdir(op.join(raw_dir, subject, sub_dir[0]))

        for file in files:
            print('Working on files for subject %s.' % subject)
            if op.exists(op.join(raw_path, file)):
                print('Subject %s already has file %s.' % (subject, file))
            elif 'raw.fif' in file:
                raw_source = op.join(raw_dir, subject, sub_dir[0], file)
                raw_dest = op.join(raw_path, file)
                shutil.copyfile(raw_source, raw_dest)
                print('Added raw file %s to subject %s' % (file, subject))
            elif 'prebad' in file:
                pb_source = op.join(raw_dir, subject, sub_dir[0], file)
                pb_dest = op.join(raw_path, file)
                shutil.copyfile(pb_source, pb_dest)
                print('Added prebad file to subject %s' % subject)
            elif 'erm' in file:
                erm_source = op.join(raw_dir, subject, sub_dir[0], file)
                erm_dest = op.join(raw_path, file)
                shutil.copyfile(erm_source, erm_dest)
                print('Added erm to subject %s' % subject)
            elif 'custom-annot' in file:
                annot_source = op.join(raw_dir, subject, sub_dir[0], file)
                annot_dest = op.join(raw_path, file)
                shutil.copyfil(annot_source, annot_dest)
                print('Added annot file to subject %s.' % subject)
            else:
                pass

if force_prebads:
    for subject in subjects:
        subject_path = op.join(target_dir, fixed_or_twa, subject)
        if op.isdir(subject_path):
            print('Subject %s has a subject directory.' % subject)
        else:
            os.mkdir(subject_path)

        raw_path = op.join(subject_path, 'raw_fif')
        if op.isdir(raw_path):
            print('Subject %s has a raw directory.' % subject)
        else:
            os.mkdir(raw_path)

        if raw_subdirs:
            sub_dir = ['raw_fif']
        else:
            sub_dirs = os.listdir(op.join(raw_dir, subject))
            sub_dirs.sort()
            if len(sub_dirs) == 2:
                sub_dir = [sub_dirs[0] if sub_dirs[0] > sub_dirs[1] else sub_dirs[1]]
            else:
                print('Subject %s has an unexpected number of recording dates. Manually check raws, please.' % subject)
                sub_dir = [sub_dirs[-1]]

        files = os.listdir(op.join(raw_dir, subject, sub_dir[0]))

        for file in files:
            if 'prebad' in file:
                pb_source = op.join(raw_dir, subject, sub_dir[0], file)
                pb_dest = op.join(raw_path, file)
                shutil.copyfile(pb_source, pb_dest)
                print('Added prebad file to subject %s' % subject)
            else:
                pass