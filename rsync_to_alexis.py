# -*- coding: utf-8 -*-

import os
import os.path as op
import subprocess

dest_dir = '/data08/alexis/incoming/jul_13/'
# dest_dir = '/data06/larsoner/incoming/vis/'
src_dir = '/storage/genz_active/t1/twa_hp/'

filter = 'genz'
itrbl = [x for x in os.listdir(src_dir) if filter in x and op.isdir(op.join(src_dir, x))]
itrbl.sort()
# itrbl = itrbl[81:83]

mid_dir = 'inverse'
file_pattern = 'All_80-sss_%s-vis-epo.fif'

for i in itrbl:       # subject in subjects, probably
    sub_path = op.join(dest_dir, i)
    m_dir = op.join(sub_path, mid_dir)
    mk_args1 = ['ssh', 'nordme@kasga.ilabs.uw.edu','mkdir', '-p', m_dir]
    subprocess.run(mk_args1)
    source = op.join(src_dir, i, mid_dir, file_pattern % i)
#    source = op.join(src_dir, i, mid_dir, file_pattern)
    dest = op.join('nordme@kasga.ilabs.uw.edu:' + sub_path, mid_dir, file_pattern % i)
#    dest = op.join('nordme@kasga.ilabs.uw.edu:' + sub_path, mid_dir)
    print('Working on subject %s.' % i)
    print('Sending file %s' % source)
    print('to destimation %s' % dest)
    args = ['rsync', '-rvu', source, dest]
    subprocess.run(args)
