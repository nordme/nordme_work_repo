import csv
import numpy as np
import os.path as op


times = ['t1', 't2']
#conds = ['rest', 'faces', 'fpos', 'fneg']
bands = {'theta': [4, 7], 'alpha': [8, 12], 'beta': [13, 30], 'gamma': [31, 55]}
conds = ['rest']
#bands = {'altbeta': [16, 26]}
metrics = ['dl', 'dc', 'phi']
parc = 'aparc'

id_path = '/home/erica/Documents/MEG_Center/genz/g_ids.csv'
ids = []
with open(id_path, 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        if not row[0] == 'id':
            ids.append(row[0])

header = [f'{time}_{cond}-{band[0]}{met}' for time in times
          for cond in conds
          for band in bands.keys()
          for met in metrics]

#main_path = '/media/erica/data1/genz_stats/conn/genz_conn_allmet_alln_altbeta.csv'
#dl_path = '/media/erica/data1/genz_stats/conn/delta_l_15_HCPMMP1_alln_altbeta.csv'
#dc_path = '/media/erica/data1/genz_stats/conn/delta_c_15_HCPMMP1_alln_altbeta.csv'
#phi_path = '/media/erica/data1/genz_stats/conn/phi_15_HCPMMP1_alln_altbeta.csv'

main_path = f'/media/erica/data1/genz_stats/conn/genz_conn_{parc}_allmet_alln.csv'
dl_path = f'/media/erica/data1/genz_stats/conn/delta_l_15_{parc}_alln.csv'
dc_path = f'/media/erica/data1/genz_stats/conn/delta_c_15_{parc}_alln.csv'
phi_path = f'/media/erica/data1/genz_stats/conn/phi_15_{parc}_alln.csv'

dl = []
dc = []
phi = []

for mi, (met, mpath) in enumerate(zip([dl, dc, phi], [dl_path, dc_path, phi_path])):
    with open(mpath, 'r') as rf:
        mreader = csv.reader(rf)
        for mrow in mreader:
            met.append(mrow)

tcb = len(times) * len(conds) * len(bands)
assert len(dl[0]) == len(dc[0]) == len(phi[0]) == tcb

with open(main_path, 'w') as f:
    full_head = ['id', 'gen'] + header
    writer = csv.writer(f)
    # write header
    writer.writerow(full_head)
    for idi, id in enumerate(ids):
        print(f'Writing subject {id}')
        gen = 'f' if int(id) % 2 == 0 else 'm'
        row = [id, gen]
        for ii in np.arange(tcb):
            for mi, met in enumerate([dl, dc, phi]):
                row.append(met[idi][ii])
        assert len(row) == (tcb*3)+2
        writer.writerow(row)


