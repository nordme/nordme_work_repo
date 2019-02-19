# -*- coding: utf-8 -*-
#
import os
import os.path as op
import shutil
import fnmatch as fn
import numpy as np


target_dir = '/brainstudio/MEG/genz/genz_proc/active/'
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

subjs = [d for d in os.listdir(raw_dir) if 'genz' in d]
active_subjs = [d for d in os.listdir(target_dir) if 'genz' in d]
subjs.sort()
active_subjs.sort()

for bad in bads:
    try:
        subjs.remove(bad)
        print('Removing bad subject %s' % bad)
    except ValueError:
        pass

erm_sort = [subj for subj in subjs if np.in1d(subj, active_subjs)]

print(erm_sort)

for subject in erm_sort:
    sub = [s for s in os.listdir(raw_dir + subject) if op.isdir(op.join(raw_dir + subject + '/%s' %s))] # list of date folders
    # print(sub)
    for s in sub:
        files = os.listdir(op.join(raw_dir + subject + '/%s' % s))
        for file in files:
            if 'erm' in file:
                erm_list.append((subject, s, file))
            else:
                pass


# See if resting state and erm files exist in the target directory; if non-existent, add

for s, d, f in erm_list:
    erm_source = op.join(raw_dir + s + '/%s/' %d + f)
    # print(erm_source)
    erm_dest = op.join(target_dir + s + '/raw_fif/' + f)
    # print(erm_dest)
    if op.isfile(erm_dest):
        print('Subject %s already has an erm file.' % s)
    else:
        shutil.copy(erm_source, erm_dest)
        print('added erm file to subject %s' % s)



