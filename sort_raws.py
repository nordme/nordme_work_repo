# -*- coding: utf-8 -*-
#
import os
import os.path as op
import shutil
import numpy as np


# target_dir = '/home/nordme/data/genz_active/'
# raw_dir = '/brainstudio/MEG/genz/genz_proc/active/'
# trans_dir = '/brainstudio/MEG/genz/genz_proc/active/trans/'

target_dir = '/media/erica/Rocstor/spi/twa_hp'
raw_dir = '/media/erica/Rocstor/spi'

do_annots = False
do_raws = True
do_trans = False

# Get all the subject directories from active and the raw / trans dirs

subjs = [d for d in os.listdir(raw_dir) if op.isdir(op.join(raw_dir, d)) and 'spi' in d]
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
            if 'raw.fif' in file or 'raw-1.fif' in file:
                raw_source = op.join(raw_dir, subject, 'raw_fif', file)
                raw_dest = op.join(target_dir, subject, 'raw_fif', file)
                if not op.exists(raw_dest):
                    shutil.copyfile(raw_source, raw_dest)
                    print('Added raw file %s to subject %s' % (file, subject))
                else:
                    print('Subject already has %s.' % file)
            elif 'prebad' in file:
                pb_source = op.join(raw_dir, subject, 'raw_fif', file)
                pb_dest = op.join(target_dir, subject, 'raw_fif', file)
                if not op.exists(pb_dest):
                    shutil.copyfile(pb_source, pb_dest)
                    print('Added prebad file to subject %s' % subject)
                else:
                    print('Subject already has %s.' % file)
            elif 'erm' in file:
                erm_source = op.join(raw_dir, subject, 'raw_fif', file)
                erm_dest = op.join(target_dir, subject, 'raw_fif', file)
                if not op.exists(erm_dest):
                    shutil.copyfile(erm_source, erm_dest)
                    print('Added erm to subject %s' % subject)
                else:
                    print('Subject already has %s.' % file)
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

if do_trans:
    for subject in subjs:
        trans_path = op.join(target_dir, subject, 'trans')
        if op.isdir(trans_path):
            print('Subject %s has a trans directory.' % subject)
        else:
            os.mkdir(trans_path)
        trans_source = op.join(raw_dir, subject, 'trans', '%s-trans.fif' % subject)
        trans_dest = op.join(trans_path, '%s-trans.fif' % subject)
        shutil.copyfile(trans_source, trans_dest)
        print('Copied trans file for subject %s.' % subject)
