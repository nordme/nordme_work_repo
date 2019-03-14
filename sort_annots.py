# -*- coding: utf-8 -*-

import os
import os.path as op
import shutil

parent_dir = '/brainstudio/MEG/genz/genz_proc/active/'

dirs = os.listdir(parent_dir)
dirs.sort()
dirs.remove('genz_score.py')

subjects = [dir for dir in dirs if 'genz' in dir]

# sort annot files into resting raw folders for subjects that don't already have annot files

for subject in subjects:
    target_dir = op.join(parent_dir, 'twa_hp', subject, 'raw_fif')
    files = os.listdir(op.join(parent_dir, subject, 'raw_fif'))
    annot_files = [f for f in files if 'custom-annot' in f]
    for f in annot_files:
        try:
            shutil.copy(op.join(parent_dir, subject, 'raw_fif', f), target_dir)
            print('Put annot file in for subject %s.' % subject)
        except PermissionError:
            print('Need permission for subject %s.' % subject)
        except IsADirectoryError:
            print('Probably need permission for subject %s.' % subject)
        else:
            print('Hmm. Check the folder for %s.' % subject)