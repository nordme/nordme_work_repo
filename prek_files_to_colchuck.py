# -*- coding: utf-8 -*-


import os
import os.path as op
import shutil

dir = '/home/nordme/data/prek/fixed_hp/'
target_dir = '/mnt/scratch/prek/pre_camp/fixed_hp/'

subjects = [x for x in os.listdir(dir) if op.isdir(op.join(dir, x)) and 'prek' in x]
subjects.sort()

move_old = True
rsync_new = True

if move_old:
    for subject in subjects:
        raw_dir = op.join(target_dir, subject, 'raw_fif')
        old_files = os.listdir(raw_dir)
        old_source =
        old_dest =
        shutil.move(old_source, old_dest)

if rsync_new:
    for subject in subjects:
        source_dir = op.join(dir, subject, 'raw_fif')
