from pathlib import Path
import mne
import matplotlib
matplotlib.use('Qt5Agg')

subjects_dir = Path('/media/erica/data1/anat_subjects')
subjects = ["ANTS6-0Months",]

for subject in subjects:
    #surfs = mne.bem.make_watershed_bem(subject, subjects_dir=subjects_dir)

    # conductivity in order: skin, skull, csf, grey matter
    b_model = mne.make_bem_model(subject, ico=4, subjects_dir=subjects_dir,
                                 conductivity=(0.3, 0.006, 0.3))
                                #conductivity=(0.3, 0.006, 1.79, 0.3))
    
    b_sol = mne.make_bem_solution(b_model,)

    slices = [60, 80, 120, 160]

    bem_plot = mne.viz.plot_bem(subject, subjects_dir=subjects_dir, 
                                slices=slices, 
                                brain_surfaces=['curv'])
    
    bem_plot.show()

    
