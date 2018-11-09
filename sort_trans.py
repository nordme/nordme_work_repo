# -*- coding: utf-8 -*-

import os
import os.path as op
import shutil

parent_dir = '/brainstudio/MEG/genz/genz_proc/active/trans/'

files = os.listdir(parent_dir)
files.sort()

subjects = [op.join((file.strip('-trans.fif')) + 'a') for file in files if 'genz' in file]

# put trans files into active subject folders unless there's already a trans file there

active_dir = '/brainstudio/MEG/genz/genz_proc/active/'

for dir in os.listdir(active_dir):
    if op.isdir(op.join(active_dir + dir + '/trans/')):
        print('Subject %s already has an active trans folder.' % dir)
    elif 'genz' in dir:
        try:
            os.mkdir(op.join(active_dir + dir + '/trans/'))
        except PermissionError:
            print('Need permission for subject %s.' % dir)


# sort trans files into active trans folders for subjects that don't already have a trans file

for subject in subjects:
    target_dir = op.join('/brainstudio/MEG/genz/genz_proc/active/' + subject + '/trans/')
    if op.isfile(op.join(target_dir + subject + '-trans.fif')):
        print('Subject %s already has an active trans file.' % subject)
    elif op.isdir('/brainstudio/MEG/genz/genz_proc/active/%s' % subject):
        try:
            shutil.copy(op.join(parent_dir + subject + '-trans.fif'), target_dir)
        except PermissionError:
            print('Need permission for subject %s.' % subject)
        except IsADirectoryError:
            print('Probably need permission for subject %s.' % subject)
    else:
        print('Hmm. Check the folder for %s.' % subject)



# put trans files into resting state subject folders that don't already have one

resting_dir = '/brainstudio/MEG/genz/genz_proc/resting/'

for dir in os.listdir(resting_dir):
    if op.isdir(op.join(resting_dir + dir + '/trans/')):
        print('Subject %s already has a resting trans folder.' % dir)
    elif 'genz' in dir:
        try:
            os.mkdir(op.join(resting_dir + dir + '/trans/'))
        except PermissionError:
            print('Need permission for subject %s.' % dir)


# sort trans files into trans folders for resting state subjects that don't already have a trans file

for subject in subjects:
    rest_dir = op.join('/brainstudio/MEG/genz/genz_proc/resting/' + subject + '/trans/')
    if op.isfile(op.join(rest_dir + subject + '-trans.fif')):
        print('Subject %s already has a resting trans file.' % subject)
    elif op.isdir('/brainstudio/MEG/genz/genz_proc/resting/%s' % subject):
        shutil.copy(op.join(parent_dir + subject + '-trans.fif'), rest_dir)
    else:
        print('Hmm. Check the resting state folder for %s.' % subject)



