# -*- coding: utf-8 -*-

import os
import os.path as op
import shutil

just_check = False

# parent_dir = '/brainstudio/MEG/genz/genz_proc/active/trans/'
# resting_dir = '/brainstudio/MEG/genz/genz_proc/resting/'

# parent_dir = '/mnt/scratch/prek/post_camp/trans/'
parent_dir = '/mnt/scratch/prek/trans/'
dest_dir = '/mnt/scratch/prek/pre_camp/twa_hp/erp' # the directory containing the subject dirs that needs trans files

files = os.listdir(parent_dir)
files.sort()

subjects = [op.join((file.strip('-trans.fif')) + 'a') for file in files if 'genz' in file]

# code for checking if each subject in the resting directory has a trans file
if just_check:
    for subdir in os.listdir(dest_dir):
        if op.isfile(op.join(dest_dir + '/%s/' % subdir + 'trans/' + '%s-trans.fif' % subdir)):
            print('Subject %s already has a trans file.' % subdir)
        elif not op.isfile(op.join(dest_dir + '/%s/' % subdir + 'trans/' + '%s-trans.fif' % subdir)):
                print('No trans? Check out subject %s' % subdir)
else:
    # put trans folders into destination subject folders unless there's already a trans folder there
    for subdir in os.listdir(dest_dir):
        if op.isdir(op.join(dest_dir + subdir + '/trans/')):
            print('Subject %s already has a trans folder.' % subdir)
        elif 'prek' in subdir:
            try:
                os.mkdir(op.join(dest_dir + subdir + '/trans/'))
                print('Made a trans directory at %s' % op.join(dest_dir + subdir + '/trans/'))
            except PermissionError:
                print('Need permission for subject %s.' % subdir)

    # sort trans files into resting trans folders for subjects that don't already have a trans file

    for subject in subjects:
        target_dir = op.join(dest_dir, subject, '/trans/')
        if op.isfile(op.join(target_dir, '%s-trans.fif' % subject)):
            print('Subject %s already has a trans file.' % subject)
        elif op.isdir(target_dir):
            try:
                shutil.copy(op.join(parent_dir, subject + '-trans.fif'), target_dir)
                print('Put trans file in for subject %s.' % subject)
            except PermissionError:
                print('Need permission for subject %s.' % subject)
            except IsADirectoryError:
                print('Probably need permission for subject %s.' % subject)
        else:
            print('Hmm. Check the folder for %s.' % subject)









