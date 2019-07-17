# -*- coding: utf-8 -*-
#
import os
import os.path as op
import shutil
import numpy as np


target_dir = '/home/nordme/data/genz_active/'
raw_dir = '/brainstudio/MEG/genz/genz_proc/active/'
trans_dir = '/brainstudio/MEG/genz/genz_proc/active/trans/'

do_annots = True
do_raws = False

# Get all the subject directories from active and the raw / trans dirs

subjs = [d for d in os.listdir(raw_dir) if op.isdir(op.join(raw_dir, d)) and 'genz' in d]
subjs.sort()

raw_list = []
prebads = []

if do_raws:
    for subject in subjs:
        target_path = op.join(target_dir, subject)
        if op.isdir(target_path):
            print('Subject %s has a subject directory.' % subject)
        else:
            os.mkdir(target_path)

        raw_path = op.join(target_dir, subject, 'raw_fif')
        if op.isdir(raw_path):
            print('Subject %s has a raw directory.' % subject)
        else:
            os.mkdir(raw_path)

        files = os.listdir(op.join(raw_dir, subject, 'raw_fif'))
        for file in files:
            print('Working on files for subject %s.' % subject)
            if 'raw.fif' in file:
                raw_source = op.join(raw_dir, subject, 'raw_fif', file)
                raw_dest = op.join(target_dir, subject, 'raw_fif', file)
                shutil.copyfile(raw_source, raw_dest)
                print('Added raw file %s to subject %s' % (file, subject))
            elif 'prebad' in file:
                pb_source = op.join(raw_dir, subject, 'raw_fif', file)
                pb_dest = op.join(target_dir, subject, 'raw_fif', file)
                shutil.copyfile(pb_source, pb_dest)
                print('Added prebad file to subject %s' % subject)
            elif 'erm' in file:
                erm_source = op.join(raw_dir, subject, 'raw_fif', file)
                erm_dest = op.join(target_dir, subject, 'raw_fif', file)
                shutil.copyfile(erm_source, erm_dest)
                print('Added erm to subject %s' % subject)
            else:
                pass



# add in custom annotations
if do_annots:
    for subject in subjs:
        target_path = op.join(target_dir, subject)
        if op.isdir(target_path):
            print('Subject %s has a subject directory.' % subject)
        else:
            os.mkdir(target_path)

        raw_path = op.join(target_dir, subject, 'raw_fif')
        if op.isdir(raw_path):
            print('Subject %s has a raw directory.' % subject)
        else:
            os.mkdir(raw_path)

        files = os.listdir(op.join(raw_dir, subject, 'raw_fif'))
        for file in files:
            if 'custom-annot' in file:
                an_source = op.join(raw_dir, subject, 'raw_fif', file)
                an_dest = op.join(target_dir, subject, 'raw_fif', file)
                shutil.copyfile(an_source, an_dest)
                print('Added custom annotations file %s to subject %s' % (file, subject))
            else:
                pass
