#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 19 13:47:37 2019

@author: nordme
"""

import os
import os.path as op

# get and sort all the folders from a directory

# parent_dir = '/home/nordme/resting/'
# parent_dir = '/home/nordme/MEG_data/rsMEG/'
parent_dir = '/brainstudio/MEG/genz/genz_proc/active/'

print("Fetching folders from %s" % parent_dir)

folders = os.listdir(parent_dir)
folders.sort()

# choose folders to rename; rename folders; compile list of genz folders
genz_folders = []

for folder in folders:
    if 'genz' in folder and op.isdir(op.join(parent_dir, folder)):
        genz_folders.append(folder)
print('Our genz folders are: %s' % genz_folders)

# create a list of sub-folders to search for files to rename
# fyi some subjects have two recording dates

sub_folders = []

for folder in genz_folders:
        files = os.listdir(op.join(parent_dir, folder, 'raw_fif'))
        for file in files:
            if 'erm_raw' in file:
                try:
                    os.rename(op.join(parent_dir, folder, 'raw_fif', file), op.join(parent_dir, 
                              folder, 'raw_fif', (file.replace('erm_raw', 'erm_01_raw'))))
                    print('Renamed file: %s' % file)
                except OSError:
                    print('Perhaps a duplicate: %s' % file)