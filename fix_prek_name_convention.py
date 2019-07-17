# -*- coding: utf-8 -*-

"""This script looks up folders in a given directory,
chooses folders and files that follow our old naming conventions,
and renames them with the new convention."""

import os
import os.path as op

do_subfolders=True

# get and sort all the folders from a directory

# parent_dir = '/storage/anat/subjects/w/preflood_12/'
# parent_dir = '/home/nordme/MEG_data/rsMEG/'
parent_dir = '/storage/prek/'

print("Fetching folders from %s" % parent_dir)

folders = os.listdir(parent_dir)
folders.sort()
print(folders)

# choose folders to rename; rename folders; compile list of genz folders
prek_folders = []

for folder in folders:
    if 'PREK_' in folder:
        try:
            os.rename(op.join(parent_dir + folder),
                  op.join(parent_dir + (folder.replace('PREK_', 'prek_'))))
            prek_folders.append(folder.replace('PREK_', 'prek_'))
        except OSError:
            print('We have a duplicate: %s' % folder)
    elif 'prek' in folder:
        prek_folders.append(folder)
print('Our prek folders are: %s' % prek_folders)

# create a list of sub-folders to search for files to rename
# fyi some subjects have two recording dates

sub_folders = []

if do_subfolders:
    for folder in prek_folders:
        sub_path = op.join(parent_dir, folder)
        subs = [x for x in os.listdir(sub_path) if op.isdir(op.join(sub_path, x)) and not 'raw' in x]
        print(subs)
        for sub in subs:
            sub_folders.append(op.join(parent_dir + '%s/' % folder + '%s/' % sub))
            try:
                os.rename(op.join(parent_dir, folder, sub),
                          op.join(parent_dir, folder, 'raw_fif'))
            except:
                print('got a second raw_fif file')
            
        
                