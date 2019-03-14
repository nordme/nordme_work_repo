# -*- coding: utf-8 -*-
#
import os
import os.path as op
import shutil
import fnmatch as fn
import numpy as np


target_dir = '/brainstudio/MEG/genz/genz_proc/active/fix/'
raw_dir = '/brainstudio/MEG/genz/'
trans_dir = '/brainstudio/MEG/genz/genz_proc/active/trans/'

sub_dir = []

all_files = []
rs_list = []
erm_list = []
bads = ['genz318_13a']

# Search all the genz subject directories on brainstudio for erms and resting states.
# Eliminate pilot subjects.
# Make lists attaching the subject names to the appropriate sub-directories and files.

# subjs = [d for d in os.listdir(raw_dir) if 'genz' in d]

active_subjs = [d for d in os.listdir(target_dir) if 'genz' in d]
# subjs.sort()
active_subjs.sort()

# we need the sub_
for subject in active_subjs:
    sub = [s for s in os.listdir(target_dir + subject + '/raw_fif/') if op.isfile(op.join(raw_dir + subject + '/%s' %s))] # list of files in raw_fif
    # print(sub)
    for file in sub:
        source = op.join(target_dir + subject + '/raw_fif/' + '/%s' % file)
        dest = op.join(target_dir, 'old', file)
        if '.pos' in file:
               shutil.move(source, dest)
        elif '-annot' in file:
                shutil.move(source, dest)
        elif '-counts.h5' in file:
                shutil.move(source, dest)
        else:
            pass






