# -*- coding: utf-8 -*-

import os
import os.path as op
import mne

subjects = ['genz424_15a']

for subject in subjects:
    print('     Starting Watershed BEM  process...')
    run_subprocess(['mne', 'watershed_bem', '--subject', subject,
                    '--preflood', '12', '--overwrite'],)
