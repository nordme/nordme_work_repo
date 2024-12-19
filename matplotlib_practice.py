
import numpy as np
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt

np.random.seed = 123456
im = [np.random.random((50, 50))*i for i in np.arange(0.1, 10.1, 0.1)]

fig = plt.figure()
sf = fig.subfigures(5, 3, hspace=0.05, )
for ri in [1, 2]:
    for ci in [0, 1, 2]:
        sf[ri, ci].set_facecolor('0.85')

for ai in [1, 2, 3, 4]:
    for bi in [0, 1, 2]:
        axes = sf[ai, bi].subplots(2, 2, sharex='all', sharey='row')
        pop_keys = ['left', 'right'] if bi==1 else [['left', None, 'right'][bi]]
        #args = dict(left=0.1, bottom=0.1, right=0.9, top=0.9, wspace=0.05, hspace=0.0)
        #for k in pop_keys: # we only want to add extra space to outer axes
        #    args.pop(k)
        sf[ai, bi].subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.85,
                                   wspace=0.05, hspace=0.0)
        sf[ai, bi].set
        for ci in [0, 1]:
            for di in [0, 1]:
                idx = ai + bi + ci + di
                axes[ci, di].plot(np.arange(100), np.arange(100)*1.5, color='b')
                axes[ci, di].set_xlabel(f'ai={ai}, bi={bi}, ci={ci}, di={di}')

