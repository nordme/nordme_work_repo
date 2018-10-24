# -*- coding: utf-8 -*-

"""This script looks up folders in a given directory,
chooses folders and files that follow our old genz naming conventions,
and renames them with the new convention."""

import os
import os.path as op

# get and sort all the folders from a directory

# parent_dir = '/mnt/meg/genz/meg/'
parent_dir = '/home/nordme/MEG_data/rsMEG/'

print("Fetching folders from %s" % parent_dir)

folders = os.listdir(parent_dir)
folders.sort()

# choose folders to rename; rename folders; compile list of genz folders
genz_folders = []

for folder in folders:
    if 'genz_' in folder:
        os.rename(op.join(parent_dir + folder),
                  op.join(parent_dir + (folder.replace('genz_', 'genz'))))
        genz_folders.append(folder.replace('genz_', 'genz'))
    elif 'genz' in folder:
        genz_folders.append(folder)
print('Our genz folders are: %s' % genz_folders)

# create a list of sub-folders to search for files to rename
# fyi some subjects have two recording dates

sub_folders = []

for folder in genz_folders:
    subs = os.listdir(parent_dir + '%s/' % folder)
    for sub in subs:
        sub_folders.append(op.join(parent_dir + '%s/' % folder + '%s/' % sub))

    # for sub in subs:
        # if 'raw_fif' in sub:
            # sub_folders.append(op.join(parent_dir + '%s/' % folder + '%s/' % sub))

# find files in the sub_folders to rename and do the renaming

for s in sub_folders:
    files1 = os.listdir(s)
    for file in files1:
        if 'genz_' in file:
            os.rename(op.join(s + file), op.join(s +
                                                 (file.replace('genz_', 'genz'))))
            print('Renamed file: %s' % file)

for s in sub_folders:
    files2 = os.listdir(s)
    for file in files2:
        if 'resting_state' in file:
            os.rename(op.join(s + file), op.join(s +
                                                 (file.replace('_resting_state_', '_rest_'))))
            print('Renamed file: %s' % file)