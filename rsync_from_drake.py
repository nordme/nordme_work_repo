from pathlib import Path
import subprocess

anat_dir = Path('/media/erica/data2/anat_subjects')

for dir in anat_dir.iterdir():
    dir_name = dir.parts[-1]
    if dir_name.startswith('genz') and dir_name.endswith('a'):
        label_path = dir / 'label'
        if label_path.exists():
            print(f'subject {dir_name} has a complete anat file')
        else:
            source_l = f'nordme@drake.ilabs.uw.edu:/storage/anat/subjects/{dir_name}/label/'
            dest_l = f'/media/erica/data2/anat_subjects/{dir_name}/label/'
            source_s = f'nordme@drake.ilabs.uw.edu:/storage/anat/subjects/{dir_name}/label/'
            dest_s = f'/media/erica/data2/anat_subjects/{dir_name}/label/'
            args_l = ['rsync', '-rvu', source_l, dest_l]
            args_s = ['rsync', '-rvu', source_s, dest_s]
            print(f'Starting {dir_name} rsync')
            subprocess.run(args_l)
            subprocess.run(args_s)

