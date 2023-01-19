#!/usr/bin/env python3

import functions as funcs

import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import pickle


#%%  Import data
# with open('data/data_L30_eps20_N10.pkl', 'rb') as f:
with open('data/data_L40_eps20_N10.pkl', 'rb') as f:
    data_dict = pickle.load(f)

Xvec_full0 = data_dict['Xvec_full0']
Yvec_full0 = data_dict['Yvec_full0']
Xvec_full = data_dict['Xvec_full']
Yvec_full = data_dict['Yvec_full']
Lx = data_dict['Lx']
Ly = data_dict['Ly']
ef  = data_dict['ef']
phi = data_dict['phi']
eps = data_dict['eps']
Chern_full = data_dict['Chern_full']
list_Chern_full = data_dict['list_Chern_full']
N_samples = len(list_Chern_full)


#%%  Cut out borders, choose random points
border = 4
Npoints = 100

# Choosen all "bulk" points
_, _, bulk_points, (box_x_min,box_x_max), (box_y_min,box_y_max) = \
    funcs.getSubsystemCutout(Lx-2*border, Ly-2*border, Xvec_full0, Yvec_full0)

# Border box vectors, for plotting
box_vec = lambda b: [b[0], b[1], b[1], b[0], b[0]]
box_vec_x = box_vec((box_x_min, box_x_max))
box_vec_y = box_vec((box_y_min, box_y_max))[::-1]

# All the bulk points
Xvec_bulk = Xvec_full[bulk_points]
Yvec_bulk = Yvec_full[bulk_points]
C_bulk    = Chern_full[bulk_points]

# Or maybe a heart?
chosenHeart = funcs.giveChosenHeart(Xvec_full, Yvec_full)
Xvec_heart = Xvec_full[chosenHeart]
Yvec_heart = Yvec_full[chosenHeart]
C_heart    = Chern_full[chosenHeart]

list_C_bulk = []
list_C_c    = []
list_X      = []
list_Y      = []

for i,C_full in enumerate(list_Chern_full):
    # Cut out the borders
    C_bulk = C_full[bulk_points]

    # Choose points randomly
    chosen_points = funcs.chooseRandomBulkPoints(Xvec_bulk, Yvec_bulk, Lx, Npoints, seed=100+i, border=0)
    X_c = Xvec_bulk[chosen_points]
    Y_c = Yvec_bulk[chosen_points]
    C_c =    C_bulk[chosen_points]
    
    list_C_bulk.append(C_bulk)
    list_C_c.append(C_c)
    list_X.append(X_c)
    list_Y.append(Y_c)

hist_C_bulk = np.array([c for C_b in list_C_bulk for c in C_b])
hist_C_c    = np.array([c for C_c in list_C_c for c in C_c])    


#%%  Plotting
fig, ax = plt.subplots(2, 2, figsize=(9, 7), tight_layout=True)

# Set visuals
plt.rcParams.update({"text.usetex": True, "font.family": "serif"})

# Background points in small, faint grey
ax[0,0].scatter(Xvec_full, Yvec_full, 1, 'grey')
ax[0,1].scatter(Xvec_full, Yvec_full, 1, 'grey')

# Indicate the borders for "bulk points"
# ax[0,0].plot(box_vec_x, box_vec_y, '-r', lw=2)
ax[0,1].plot(box_vec_x, box_vec_y, '-r', lw=2)

# Scatter plots and colorbars
# sc_f = ax[0,0].scatter(Xvec_bulk, Yvec_bulk, 18, c=C_bulk)
sc_f = ax[0,0].scatter(Xvec_heart, Yvec_heart, 15, c=C_heart, cmap=mpl.colormaps['Reds'], vmin=0.66, vmax=1.17)
sc_c = ax[0,1].scatter(X_c, Y_c, 18, c=C_c)

# Colorbars
# cb_f = plt.colorbar(sc_f, ax=ax[0,0], ticks=[0.9, 1, 1.1])
cb_f = plt.colorbar(sc_f, ax=ax[0,0], ticks=[0.7, 0.8, 0.9, 1, 1.1])
cb_c = plt.colorbar(sc_c, ax=ax[0,1], ticks=[0.9, 1, 1.1])

# Colorbar labels
cb_f.set_label('$\mathcal{C}(\mathbf{r})$', fontsize=15, c='r')
cb_c.set_label('$\mathcal{C}(\mathbf{r})$', fontsize=15)

# Bins for the histograms
acc = 0.015
bins  = [x for i in range(1000) if (x:=round(C_bulk.mean())-acc/2-i*acc) > C_bulk.min()-0.08]
bins += [x for i in range(1000) if (x:=round(C_bulk.mean())+acc/2+i*acc) < C_bulk.max()+0.08]
bins = np.sort(bins)
bins_c = bins-acc/2

# Histograms
# hb, *_   = ax[1,0].hist(C_bulk,      bins,   width=0.5*acc, density=True, color='k', alpha=1.0, ls='solid')
hH, *_     = ax[1,0].hist(C_heart,     bins,   width=0.5*acc, density=True, color='r', alpha=0.6, ls='dotted', ec='k')
#
hC, *_     = ax[1,0].hist(C_c,         bins_c, width=0.5*acc, density=True, color='k', alpha=1.0, ls='solid')
hb_tot, *_ = ax[1,1].hist(hist_C_bulk, bins,   width=0.5*acc, density=True, color='r', alpha=0.6, ls='dotted', ec='k')
hC_tot, *_ = ax[1,1].hist(hist_C_c,    bins_c, width=0.5*acc, density=True, color='k', alpha=1.0, ls='solid')

# Text boxes
# str_Cb   = r"$\mathcal{C}_{\mathrm{bulk},i}  \hspace{0.3cm}=\overline{\mathcal C}_{\mathrm{bulk},i}   (\textbf{r})\hspace{0.24cm}=$ "+f"{C_bulk.mean():.3f}"
str_CH   = r"$\mathcal{C}_{\mathrm{heart},i}  \hspace{0.1cm}=\overline{\mathcal C}_{\mathrm{heart},i}   (\textbf{r})\hspace{0.15cm}=$ "+f"{C_heart.mean():.3f}"
str_Cc   = r"$\mathcal{C}_{\mathrm{points},i}=\overline{\mathcal C}_{\mathrm{points},i}(\textbf{r})=$ "+f"{C_c.mean():.3f}"
str_Cb_tot = r"$\mathcal{C}_{\mathrm{tot,bulk}} \hspace{0.26cm}=$ "+f"{hist_C_bulk.mean():.3f}"
str_Cc_tot = r"$\mathcal{C}_{\mathrm{tot,points}} =$ "+f"{hist_C_c.mean():.3f}"
props = dict(boxstyle='round', facecolor='gold', alpha=0.2)
# ax[1,0].text(0.04, 0.89, str_Cb,   transform=ax[1,0].transAxes, c='k', fontsize=14, bbox=props)
ax[1,0].text(0.04, 0.89, str_CH,     transform=ax[1,0].transAxes, c='r', fontsize=14, bbox=props)
ax[1,0].text(0.04, 0.77, str_Cc,     transform=ax[1,0].transAxes, c='k', fontsize=14, bbox=props)
ax[1,1].text(0.05, 0.90, str_Cb_tot, transform=ax[1,1].transAxes, c='r', fontsize=14, bbox=props)
ax[1,1].text(0.05, 0.79, str_Cc_tot, transform=ax[1,1].transAxes, c='k', fontsize=14, bbox=props)

# Limits
ax[1,0].set_xlim([bins.min(), bins.max()])
ax[1,1].set_xlim([bins.min(), bins.max()])
# ax[1,0].set_ylim([0, 1.45*hb.max()])
ax[1,0].set_ylim([0, 1.45*hH.max()])
ax[1,1].set_ylim([0, 1.45*hb_tot.max()])

# Ticks
ax[0,0].set_yticks([10*y for y in range(5)])
ax[0,1].set_yticks([10*y for y in range(5)])
ax[1,0].set_yticks([])
ax[1,1].set_yticks([])

# Subfigure labels
_ = ax[0,0].text(0.02, 1.1, r'\textbf{a)}', transform=ax[0,0].transAxes, fontsize=17, verticalalignment='top')
_ = ax[0,1].text(0.02, 1.1, r'\textbf{b)}', transform=ax[0,1].transAxes, fontsize=17, verticalalignment='top')
_ = ax[1,0].text(0.02, 1.1, r'\textbf{c)}', transform=ax[1,0].transAxes, fontsize=17, verticalalignment='top')
_ = ax[1,1].text(0.02, 1.1, r'\textbf{d)}', transform=ax[1,1].transAxes, fontsize=17, verticalalignment='top')

# Save figure
# plt.savefig(f'figures/bulkHeart-vs-points_L{Lx}.pdf', dpi=400)
plt.savefig(f'figures/bulkHeart-vs-points_L{Lx}.png', dpi=200)

plt.show()