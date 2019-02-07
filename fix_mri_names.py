# -*- coding: utf-8 -*-

"""This script looks up folders in a given directory,
chooses genz folders and files that follow mri naming conventions,
and renames them with the new convention."""

import os
import os.path as op
import fnmatch as fm

# get and sort all the folders from a directory

parent_dir = '/brainstudio/MEG/genz/anatomy/fix/'
# parent_dir = '/home/nordme/MEG_data/rsMEG/'

print("Fetching folders from %s" % parent_dir)

folders = os.listdir(parent_dir)
folders.sort()

# choose folders to rename; rename folders; compile list of genz folders
genz_folders = []

for folder in folders:
    if 'sub-' in folder:
        try:
            os.rename(op.join(parent_dir + folder),
                      op.join(parent_dir + (folder.replace('sub-genz', 'genz'))))
            print('Renaming %s' % folder)
        except FileNotFoundError:
            print('File %s not found.' % folder)
            print('%s' % op.join(parent_dir + (folder.replace('sub-genz', 'genz'))))
        genz_folders.append(folder.replace('sub-genz', 'genz'))


folders = os.listdir(parent_dir)
folders.sort()

for folder in folders:
    if 'ses-1' in folder:
        try:
            os.rename(op.join(parent_dir + folder),
                      op.join(parent_dir + (folder.replace('_ses-1_freesurfer_adult_bnmprage', '_'))))
            print('Renaming %s' % folder)
        except FileNotFoundError:
            print('File %s not found.' % folder)
            print('%s' % op.join(parent_dir + (folder.replace('_ses-1_freesurfer_adult_bnmprage', '_'))))

print('Our genz folders are: %s' % genz_folders)


folders = os.listdir(parent_dir)
folders.sort()

# add the age suffixes

for folder in folders:
    if 'genz' in folder:
        if fm.fnmatch(folder, 'genz5*'):
            if fm.fnmatch(folder, 'genz530*'):
                pass
            else:
                os.rename(op.join(parent_dir + folder), op.join(parent_dir + folder + '17a'))
        elif fm.fnmatch(folder, 'genz4*'):
            os.rename(op.join(parent_dir + folder), op.join(parent_dir + folder + '15a'))
        elif fm.fnmatch(folder, 'genz3*'):
            os.rename(op.join(parent_dir + folder), op.join(parent_dir + folder + '13a'))
        elif fm.fnmatch(folder, 'genz2*'):
            os.rename(op.join(parent_dir + folder), op.join(parent_dir + folder + '11a'))
        elif fm.fnmatch(folder, 'genz1*'):
            os.rename(op.join(parent_dir + folder), op.join(parent_dir + folder + '9a'))
        else:
            raise ValueError('Hey, this folder name is weird. Look at %s' % folder)