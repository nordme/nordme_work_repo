import csv
import mne
import os.path as op

labels = mne.read_labels_from_annot(subject='fsaverage', parc='aparc',
                                    subjects_dir='/media/erica/data1/anat_subjects')
lnames = [l.name for l in labels if not '???' in l.name
          and not l.name.startswith('unknown')]
lnames = [name.replace('_', '-') for name in lnames]
bands = {'theta': [4, 7], 'alpha': [8, 12], 'beta': [13, 30], 'gamma': [31, 55]}
times = ['t1', 't2']

id_path = '/home/erica/Documents/MEG_Center/genz/g_ids.csv'
ids = []
with open(id_path, 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        if not row[0] == 'id':
            ids.append(row[0])

header = [f'{time}_{band}_{lname}' for time in times
          for band in bands.keys()
          for lname in lnames]
header = ['id', 'gender', 't1_age', 't2_age'] + header

main_path = '/media/erica/data1/genz_stats/power/genz_rs_power_vfix_alln.csv'

with open(main_path, 'w') as f:
    writer = csv.writer(f)
    # write header
    writer.writerow(header)
    for id in ids:
        print(f'subject {id}')
        gen = 'f' if int(id)%2==0 else 'm'
        t1a = (int(id[0])-1)*2 + 9
        t2a = t1a + 3
        row = [id, gen, t1a, t2a]
        na_fill = ['NA']*68*4
        # add t1 data to row
        t1_path = op.join('/media/erica/data1/genz/t1/rs_csvs',
                          f'genz{id}_{t1a}a_aparc_nobaseline_rs_bpower.csv')
        if op.exists(t1_path):
            with open(t1_path, 'r') as f1:
                rdr1 = csv.reader(f1, delimiter=',')
                for r in rdr1:
                    row = row + r
        else:
            row = row + na_fill
        # add t2 data to row
        t2_path = op.join('/media/erica/data1/genz/t2/twa_hp/rs_csvs',
                          f'genz{id}_{t2a}b_aparc_nobaseline_rs_bpower.csv')
        if op.exists(t2_path):
            with open(t2_path, 'r') as f2:
                rdr2 = csv.reader(f2, delimiter=',')
                for rr in rdr2:
                    row = row + rr
        else:
            row = row + na_fill
        assert len(row) == 548
        # write row
        writer.writerow(row)