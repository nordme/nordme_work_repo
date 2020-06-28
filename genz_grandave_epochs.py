#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 19 11:30:50 2020

@author: erica
"""


import mne
import os
import os.path as op
import numpy as np

base_dir = '/media/erica/data/genz/group_data/auditory/'
save_dir = op.join(base_dir, 'grandave_epochs')

subjects = [x for x in os.listdir(base_dir) if op.isdir('%s%s' % (base_dir, x)) and 'genz' in x]
subjects.sort()


blocks = [ 'a','f', 'e', 't']
conditions = ['l', 't']
ages = ['allage', '9', '11', '13', '15', '17']
genders = ['both', 'male', 'female']

codes = ['%s%s%02d' % (block, condition, syllable) 
                    for condition in conditions                
                    for block in blocks                    
                    for syllable in (range(1,13) if condition == 't' else range(1,4))]

evks_list = ['%s_%s_%s' % (gender, age, code)
             for gender in genders
             for age in ages
             for code in codes]

print(evks_list)


