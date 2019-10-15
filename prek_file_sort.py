# -*- coding: utf-8 -*-
#
import os
import os.path as op
import shutil
import numpy as np

# pre_camp: twa_hp; erp to erp dir, then pskt to pskt dir
# pre_camp: fixed_hp; pskt to pskt dir

# post_camp: twa_hp: erp to erp dir, then pskt to pskt dir
# post_camp: fixed_hp; pskt to pskt dir

# do_trans = True
do_raws = True
force_prebads = False  # Enables user just to copy prebads but not all raw files
pre_or_post = 'pre'
fixed_or_twa = 'twa_hp'
erp_or_pskt = 'erp'
raw_subdirs = True  # whether the source directory has date subdirectories or a 'raw_fif' subdirectory

target_dir = '/mnt/scratch/prek/%s_camp/%s/%s/' % (pre_or_post, fixed_or_twa, erp_or_pskt)
source_dir = '/mnt/scratch/prek/%s_camp/twa_hp/' % (pre_or_post)
# trans_dir = '/home/nordme/prek/trans/'

subjects = [d for d in os.listdir(source_dir) if op.isdir(op.join(source_dir, d)) and 'prek' in d]
subjects.sort()


if do_raws:
    for subject in subjects:
        subject_path = op.join(target_dir, subject)
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
            sub_dirs = os.listdir(op.join(source_dir, subject))
            sub_dirs.sort()
            if len(sub_dirs) == 2:
                sub_dir = [sub_dirs[0] if sub_dirs[0]>sub_dirs[1] else sub_dirs[1]]
            else:
                print('Subject %s has an unexpected number of recording dates. Manually check raws, please.' % subject)
                sub_dir = [sub_dirs[-1]]

        files = os.listdir(op.join(source_dir, subject, sub_dir[0]))

        for file in files:
            print('Working on files for subject %s.' % subject)
            if op.exists(op.join(raw_path, file)):
                print('Subject %s already has file %s.' % (subject, file))
            elif 'raw.fif' in file:
                raw_source = op.join(source_dir, subject, sub_dir[0], file)
                raw_dest = op.join(raw_path, file)
                shutil.copyfile(raw_source, raw_dest)
                print('Added raw file %s to subject %s' % (file, subject))
            elif 'prebad' in file:
                pb_source = op.join(source_dir, subject, sub_dir[0], file)
                pb_dest = op.join(raw_path, file)
                shutil.copyfile(pb_source, pb_dest)
                print('Added prebad file to subject %s' % subject)
            elif 'erm' in file:
                erm_source = op.join(source_dir, subject, sub_dir[0], file)
                erm_dest = op.join(raw_path, file)
                shutil.copyfile(erm_source, erm_dest)
                print('Added erm to subject %s' % subject)
            elif 'custom-annot' in file:
                annot_source = op.join(source_dir, subject, sub_dir[0], file)
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
            sub_dirs = os.listdir(op.join(source_dir, subject))
            sub_dirs.sort()
            if len(sub_dirs) == 2:
                sub_dir = [sub_dirs[0] if sub_dirs[0] > sub_dirs[1] else sub_dirs[1]]
            else:
                print('Subject %s has an unexpected number of recording dates. Manually check raws, please.' % subject)
                sub_dir = [sub_dirs[-1]]

        files = os.listdir(op.join(source_dir, subject, sub_dir[0]))

        for file in files:
            if 'prebad' in file:
                pb_source = op.join(source_dir, subject, sub_dir[0], file)
                pb_dest = op.join(raw_path, file)
                shutil.copyfile(pb_source, pb_dest)
                print('Added prebad file to subject %s' % subject)
            else:
                pass