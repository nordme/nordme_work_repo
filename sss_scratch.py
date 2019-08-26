import mnefun
import numpy as np
import os
import os.path as op
import mne

m01 = '/home/nordme/data/cHPI_test/mmf_test/mmf_test_01_raw.fif'
m01 = mne.io.read_raw_fif(m01, allow_maxshield=True)
sws_ssh = 'nordme@kasga.ilabs.uw.edu'
sws_dir = '/data07/nordme/'
fname_in = '/home/nordme/data/cHPI_test/mmf_test/mmf_test_01_raw.fif'
fname_out = '/home/nordme/data/cHPI_test/mmf_test/mmf_test_01_raw.pos'
m01_pos = mnefun.run_sss_positions(fname_in, fname_out, host=sws_ssh, work_dir=sws_dir)
head_pos = mne.chpi.read_head_pos(fname_out)
m01_sss = mne.preprocessing.maxwell_filter(raw=m01, head_pos=head_pos, origin='auto', st_correlation=0.98, st_duration=4., destination=[0., 0., 0.04], coord_frame='head')

# n nordme@kasga.ilabs.uw.edu: copyingRunning subprocess: rsync --partial -Lave ssh -p 22 --include */ --include mmf_test_01_raw.fif --exclude * /home/nordme/data/cHPI_test/mmf_test/ nordme@kasga.ilabs.uw.edu:/data07/nordme/
# running -headpos -forceRunning subprocess: ssh -p 22 nordme@kasga.ilabs.uw.edu /neuro/bin/util/maxfilter -f /data07/nordme/mmf_test_01_raw.fif -o /data07/nordme/temp_1566420556.7190416_raw_quat.fif -headpos -format short -hp /data07/nordme/temp_1566420556.7190416_hp.txt -force
# copyingRunning subprocess: rsync --partial --rsh ssh -p 22 nordme@kasga.ilabs.uw.edu:/data07/nordme/temp_1566420556.7190416_hp.txt /home/nordme/data/cHPI_test/mmf_test/mmf_test_01_raw.pos
# Running subprocess: ssh -p 22 nordme@kasga.ilabs.uw.edu rm -f /data07/nordme/mmf_test_01_raw.fif /data07/nordme/temp_1566420556.7190416_hp.txt /data07/nordme/temp_1566420556.7190416_raw_quat.fif
# writing (516 sec)