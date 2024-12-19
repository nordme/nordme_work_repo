import os
import os.path as op
import numpy as np
import mne
from mne_bids import BIDSPath, write_raw_bids

skip = ['prek_1714', 'prek_1936']
subjects = sorted([x for x in os.listdir('/media/erica/data1/pfc')
            if x.startswith('prek') and x not in skip])
orig_dir = '/media/erica/data1/pfc'
bdir = '/media/erica/data1/pfc/bids'
#sessions = ['pre', 'post']
sessions = ['pre']
tasks = ['erp', 'pskt_01', 'pskt_02']
eids = [
    dict(faces=1, cars=2, words=3, aliens=4, button=64,),
    dict(onset=1)
]

for sub in subjects:
    bids_sub = sub.replace('_', '')
    for ses in sessions:
        erm_path = op.join(orig_dir, sub, 'raw_fif', f'{sub}_erm_raw.fif')
        eraw = mne.io.read_raw_fif(erm_path, allow_maxshield=True)
        for task in tasks:
            b_task = task.replace('_', '')
            # load raw
            raw_path = op.join(orig_dir, sub, 'raw_fif',
                               f'{sub}_{task}_{ses}_raw.fif')
            raw = mne.io.read_raw_fif(raw_path, allow_maxshield=True)
            erm = eraw if task == 'erp' else None
            ev1 = mne.find_events(raw, mask=3)
            ev2 = mne.find_events(raw, mask=4)
            ev3 = mne.find_events(raw, mask=64)
            evs = np.vstack((ev1, ev2, ev3)) if task=='erp' else ev1
            eid = eids[0] if task == 'erp' else eids[1]
            # set BIDS Path
            bp = BIDSPath(subject=bids_sub, session=ses, task=b_task, datatype='meg', root=bdir)
            # write file
            write_raw_bids(raw, bids_path=bp, events=evs, event_id=eid, overwrite=True)
        # write prebad
