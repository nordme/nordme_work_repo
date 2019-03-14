# -*- coding: utf-8 -*-

import os
import os.path as op
import shutil

parent_dir = '/brainstudio/MEG/genz/genz_proc/active/'

dirs = os.listdir(parent_dir)
dirs.sort()
dirs.remove('genz_score.py')

subjects = [dir for dir in dirs if 'genz' in dir]

# put trans folders into resting subject folders unless there's already a trans folder there

resting_dir = '/brainstudio/MEG/genz/genz_proc/resting/'

# sort trans files into resting raw folders for subjects that don't already have a prebad file

for subject in subjects:
    target_dir = op.join(resting_dir, subject, 'raw')
    if op.isfile(op.join(target_dir + subject + '_prebad.txt')):
        print('Subject %s already has a prebad file.' % subject)
    elif not op.isfile(op.join(target_dir + subject + '_prebad.txt')):
            print('Check out subject %s' % dir)
    elif op.isdir('/brainstudio/MEG/genz/genz_proc/resting/%s' % subject):
        try:
            shutil.copy(op.join(parent_dir, subject, 'raw', subject + '_prebad.txt'), target_dir)
            print('Put prebad file in for subject %s.' % subject)
        except PermissionError:
            print('Need permission for subject %s.' % subject)
        except IsADirectoryError:
            print('Probably need permission for subject %s.' % subject)
    else:
        print('Hmm. Check the folder for %s.' % subject)



