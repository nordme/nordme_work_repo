import os.path as op
import numpy as np
import matplotlib.pyplot as plt

class StimEnv:          # the environment
    def __init__(self):
        stim_file = '/data/genz/genz_t2_b1_43.txt'
        syllables = {'eu': '0_0', 'ea': '0_1', 'ke': '0_2',     # word 1
                     'ee': '1_0', 'ku': '1_1', 'soe': '1_2',    # word 2
                     'uu': '2_0', 'sa': '2_1', 'ai': '2_2'}     # word 3
        with open(stim_file, 'r') as sf:
            lines = [line.split('_')[0] for line in sf.readlines()]
        self.stim_list = [syllables[s] for s in lines]
        self.stim_list.append(None)
        self.syl = self.stim_list[0]
        self.si = 0

    def transition(self):
        syl_idx = self.si
        new_syl = self.stim_list[syl_idx+1]
        self.syl = new_syl
        self.si += 1
        return new_syl


class AudCortex:  # the learning agent
    def __init__(self, alpha=0.9, delta=0.7, beta=0.1):
        self.tps = np.zeros(shape=(9, 9))    # transitional probabilities count
        self.syl_actv = {'0_0': 1, '0_1': 1, '0_2': 1,      # syls begin with
                         '1_0': 1, '1_1': 1, '1_2': 1,      # maximum activ.
                         '2_0': 1, '2_1': 1, '2_2': 1
                         }
        self.syl_disp = {'0_0': -1, '0_1': -1, '0_2': -1,
                         '1_0': -1, '1_1': -1, '1_2': -1,
                         '2_0': -1, '2_1': -1, '2_2': -1
                         }
        self.alpha = alpha
        self.delta = delta
        self.beta = beta

    def learn(self, old_syl, new_syl):
        b = self.beta
        a = self.alpha
        d = self.delta
        from_idx = int(old_syl[0]) * 3 + int(old_syl[-1])
        to_idx = int(new_syl[0]) * 3 + int(new_syl[-1])
        self.tps[from_idx][to_idx] += 1
        all_trans = self.tps.sum()
        all_froms = sum(self.tps[from_idx])
        all_tp = int(self.tps[from_idx][to_idx])
        tp_pct = all_tp / all_trans  # gives change over time
        tp_r = all_tp / all_froms  # tpr is just the syl differentiating factor

        old_a = self.syl_actv[new_syl]
        new_a = old_a - ((tp_pct * tp_r * 0.01) / old_a)
        self.syl_actv[new_syl] = new_a

        old_d = self.syl_disp[new_syl]
        new_d = old_d + ((tp_pct * tp_r * 0.01) / abs(old_d))
        self.syl_disp[new_syl] = new_d

def sl_loop(stim, ctx, n=10):
#    s_curves = [[[], [], []], [[],[],[]], [[],[],[]]]
    s_curves = [[], [], []]
    if n is None:
        n = len(stim.stim_list)
    for i in np.arange(n):
        print(i)
        old_syl = stim.syl
        new_syl = stim.transition()
        ctx.learn(old_syl, new_syl)
        i1 = int(new_syl[0])
        i2 = int(new_syl[-1])
#        s_curves[i1][i2].append([ctx.syl_actv[new_syl], ctx.syl_disp[new_syl]])
#        s_curves[i1][i2].append(ctx.syl_actv[new_syl])
        s_curves[i2].append(ctx.syl_actv[new_syl])
        print(ctx.syl_disp)
#        print(ctx.syl_actv)
#        print(ctx.tps)
    return s_curves


stm = StimEnv()
crtx = AudCortex()
curves = sl_loop(stm, crtx, n=385)

fig, axes = plt.subplots()
colors = ['dodgerblue', 'limegreen', 'purple']
for s in curves:
    for i in (0, 1, 2):
        y = np.array(s[i])
        y = y[0:7]
        x = np.arange(7)
        axes.plot(x, y, color=colors[i])

y1 = np.array(curves[0])
y1 = y1[0:125]
x1 = np.arange(125)
p1, = axes.plot(x1, y1, color=colors[0], label='Syl 0')
y2 = np.array(curves[1])
y2 = y2[0:125]
p2, = axes.plot(x1, y2, color=colors[1], label='Syl 1')
y3 = np.array(curves[2])
y3 = y3[0:125]
p3, = axes.plot(x1, y3, color=colors[2], label='Syl 2')
axes.legend(handles=[p1, p2, p3])
axes.set_xlabel('Epochs')
axes.set_ylabel('Activation Weight')
