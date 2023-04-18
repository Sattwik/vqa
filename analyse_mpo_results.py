import pickle
import os
from collections import defaultdict

import numpy as np
import matplotlib.pyplot as plt

from plotter import set_size
from matplotlib import rc
import matplotlib

matplotlib.rcParams["image.cmap"] = "inferno"
matplotlib.rcParams["axes.titlesize"] = 25
matplotlib.rcParams["axes.labelsize"] = 10
matplotlib.rcParams["legend.fontsize"] = 7
matplotlib.rcParams["font.size"] = 8
matplotlib.rcParams["xtick.labelsize"] = 8
matplotlib.rcParams["ytick.labelsize"] = 8
rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
rc('text', usetex=True)
rc('text.latex', preamble=r'\usepackage{amsmath}')
CB_color_cycle = ['#377eb8', '#ff7f00', '#4daf4a',
                  '#f781bf', '#a65628', '#984ea3',
                  '#999999', '#e41a1c', '#dede00']

data_path = "./../vqa_data/results_sattwik/results_quantumHamiltonian_cnot/"
fname = 'res.pkl'

def tree(): return defaultdict(tree)

with open(os.path.join(data_path, fname), 'rb') as result_file:
    data_dict = pickle.load(result_file)

N = 32
p = 0.1

nb_reshaped_dict = tree()
eb_reshaped_dict = tree()

for key, value in data_dict.items():
    if key[0] == N and key[1] == p:
        print('key = ', key)
        print('value = ', value)
        
        D = key[3]
        d = key[2]
        nb_reshaped_dict[D][d] = value[0]
        eb_reshaped_dict[D][d] = value[1]

width = 510/2
fig = plt.figure(figsize=set_size(width, fraction = 1, subplots = (1,1)))
ax = fig.add_subplot(111)

i_D = 0

for D, nb_dict_vs_d in nb_reshaped_dict.items():
    if D != 2 and D != 4 and D != 8:
        d_list = sorted(nb_dict_vs_d.keys())
        nb_list = [nb_dict_vs_d[d] for d in d_list]

        print('D = ', D)
        print(nb_list)

        ax.plot(d_list, np.real(nb_list), marker = '.', color = 'C' + str(i_D + 1), 
                ls = "--", label = r'D = ' + str(D), markersize = 4, lw= 0.75)            

        i_D += 1

eb_dict_vs_d = eb_reshaped_dict[2]
eb_list = [eb_dict_vs_d[d] for d in d_list]

ax.plot(d_list, eb_list, marker = '.', color = 'C' + str(0), 
        label = r'Entropic', markersize = 4, lw= 0.75)

ax.set_ylabel('Bound')
ax.set_xlabel(r'd')
ax.legend()
plt.tight_layout()
# ax.set_yscale('log')

figname = "mpo_bounds_qaoa_N_" + str(N) + "_p_" + str(p) + ".pdf"
plt.savefig(os.path.join(data_path, figname), format = 'pdf')

plt.show()