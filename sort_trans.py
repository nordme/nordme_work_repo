# -*- coding: utf-8 -*-

import os
import os.path as op
import shutil

parent_dir = '/brainstudio/MEG/genz/genz_proc/active/trans/'

files = os.listdir(parent_dir)
files.sort()

subjects = [op.join((file.strip('-trans.fif')) + 'a') for file in files if 'genz' in file]

# put trans folders into resting subject folders unless there's already a trans folder there

resting_dir = '/brainstudio/MEG/genz/genz_proc/resting/'

for dir in os.listdir(resting_dir):
    if op.isdir(op.join(resting_dir + dir + '/trans/')):
        print('Subject %s already has a resting trans folder.' % dir)
    elif 'genz' in dir:
        try:
            os.mkdir(op.join(resting_dir + dir + '/trans/'))
            print('Made a trans directory at %s' % op.join(resting_dir + dir + '/trans/'))
        except PermissionError:
            print('Need permission for subject %s.' % dir)


# sort trans files into resting trans folders for subjects that don't already have a trans file

for subject in subjects:
    target_dir = op.join('/brainstudio/MEG/genz/genz_proc/resting/' + subject + '/trans/')
    if op.isfile(op.join(target_dir + subject + '-trans.fif')):
        print('Subject %s already has a resting trans file.' % subject)
    elif not op.isfile(op.join(target_dir + subject + '-trans.fif')):
            print('Check out subject %s' % dir)
    elif op.isdir('/brainstudio/MEG/genz/genz_proc/resting/%s' % subject):
        try:
            shutil.copy(op.join(parent_dir + subject + '-trans.fif'), target_dir)
            print('Put trans file in for subject %s.' % subject)
        except PermissionError:
            print('Need permission for subject %s.' % subject)
        except IsADirectoryError:
            print('Probably need permission for subject %s.' % subject)
    else:
        print('Hmm. Check the folder for %s.' % subject)


# code for checking if each subject in the resting directory has a trans file

for dir in os.listdir(resting_dir):
    if op.isfile(op.join(resting_dir + '/%s/' % dir + 'trans/' + '%s-trans.fif' % dir)):
        print('Subject %s already has a resting trans file.' % dir)
    elif not op.isfile(op.join(resting_dir + '/%s/' % dir + 'trans/' + '%s-trans.fif' % dir)):
            print('Check out subject %s' % dir)






