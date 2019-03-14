# -*- coding: utf-8 -*-
#
import os
import os.path as op
import shutil
import fnmatch as fn
import numpy as np


target_dir = '/brainstudio/MEG/genz/genz_proc/active/twa_hp/'
raw_dir = '/brainstudio/MEG/genz/genz_proc/active/'
trans_dir = '/brainstudio/MEG/genz/genz_proc/active/trans/'



# Get all the subject directories from active and the raw / trans dirs

subjs = [d for d in os.listdir(raw_dir) if 'genz' in d]
subjs.remove('genz_score.py')
subjs.sort()

raw_list = []
prebads = []

for subject in subjs:
    raw = [s for s in os.listdir(raw_dir + subject) if 'raw_fif' in s]
    # print(sub)
    for s in raw:
        files = os.listdir(op.join(raw_dir + subject + '/%s' % s))
        for file in files:
            if 'raw.fif' in file:
                raw_list.append((subject, s, file))
            elif 'prebad' in file:
                prebads.append((subject, s, file))
            else:
                pass


# See if resting state and erm files exist in the target directory; if non-existent, add
    
for s, d, f in prebads:
    pb_source = op.join(raw_dir + s + '/raw_fif/' + f)
    # print(erm_source)
    pb_dest = op.join(target_dir + s + '/raw_fif/' + f)
    raw_fif = op.join(target_dir + s + '/raw_fif/')
    # print(erm_dest)
    if op.exists(raw_fif):
        print('Ready.')
    else:    
        os.makedirs(raw_fif)
    if op.exists(pb_dest):
        print('%s has prebad file %s' % (s, f))
    else:    
       shutil.copy(pb_source, pb_dest)
       print('added prebad file to subject %s' % s)