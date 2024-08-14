"""Plot betas per each predictor: Horizontal, Vertical, Flicker
It is not used for any final figure
Note that you can input:
    BETAS: sub-01_depth_vs_Phy_LH_V1_clusters_betas.npy and sub-01_depth_vs_Phy_LH_V1_betas.npy
    BETAS PSC: sub-01_depth_vs_Phy_LH_V1_clusters_BETAS_PSC.npy and sub-01_depth_vs_Phy_LH_V1_BETAS_PSC.npy"""

import os
import numpy as np
from scipy.stats import sem
import nibabel as nb
from glob import glob
import matplotlib.pyplot as plt

STUDY_PATH = 'D:\\Exp-MotionQuartet\\MRI_MQ\\BOLD'
SUBJ = ['sub-01', 'sub-03', 'sub-04', 'sub-06', 'sub-07', 'sub-08', 'sub-09', 'sub-10']
HEMIS = ['LH', 'RH']
ROIS = ['V1', 'hMT']

CLUSTERS = ['Horizontal', 'Vertical']
colors_1 = ['#de2d26', '#fee0d2']
colors_2 = ['#3182bd', '#deebf7']

# colors_V1 = ['#7570b3', 'gray']
# colors_hMT = ['#d95f02', 'gray']

hatch_patterns = ['', '']
DPI = 300
PATH_OUT = os.path.join(STUDY_PATH, 'Results', 'Betas')
betas_type = 'BETAS_PSC'     #'betas'

fig, axs = plt.subplots(2,2, figsize=(1920*2/DPI, 1200*2/DPI), dpi=DPI)
categories_1 = ['Physical', 'Ambiguous']

# ------------------------------------------------------------------------------
for it_ro, ro in enumerate(ROIS):
    
    for it_clu, clust in enumerate(CLUSTERS):
        
        # Create output structure
        betas_preds = np.zeros([len(SUBJ)*len(HEMIS), 2])     # Mean betas per cluster during its preferrend condition
        
        i = 0
    
        for it_hemi, hemi in enumerate(HEMIS):
    
            for it_su, su in enumerate(SUBJ):
                PATH_IN =  os.path.join(STUDY_PATH, su, 'derivatives', 'func', 'Stats', 'Betas_Layers')
    
                # Load betas 
                betas_amb = np.load(os.path.join(PATH_IN, "{}_depth_vs_Amb_{}_{}_phy_clusters_{}_active_suppression.npy".format(su, hemi, ro, betas_type)), allow_pickle=True).item()
                betas_phy = np.load(os.path.join(PATH_IN, "{}_depth_vs_Phy_{}_{}_phy_clusters_{}_active_suppression.npy".format(su, hemi, ro, betas_type)), allow_pickle=True).item()
    
                print('Working on {} {}'.format(su, ro))
    
                # Fill in
                betas_preds[i, 0] = np.mean(betas_phy["{}_clust".format(clust)]["{}".format(clust)]["betas"])
                betas_preds[i, 1] = np.mean(betas_amb["{}_clust".format(clust)]["{}".format(clust)]["betas"]) 

    
                i = i +1
    
    
        # Create a bar plot
        if clust == 'Horizontal':
            colors = colors_1
        else:
            colors = colors_2
        for it in range(len(categories_1)):
            axs[it_ro, it_clu].bar(categories_1[it], np.mean(betas_preds[:, it], axis=0), yerr=sem(betas_preds[:, it], axis=0), alpha=0.5, color=colors[it])
            
        axs[it_ro, it_clu].grid(axis='y', linestyle='--', alpha=0.7)
        
        # Add labels and title
        axs[it_ro, it_clu].tick_params(axis='x', labelsize=20)  # Set the labelsize parameter to increase the label size
        axs[it_ro, it_clu].tick_params(axis='y', labelsize=20)  # Set the labelsize parameter to increase the label size
    
        axs[it_ro, it_clu].set_ylabel('Percent signal change', fontsize=20)
        axs[it_ro, it_clu].set_ylim([-1, 3])

                     
plt.tight_layout()
# Show the plot
fig.savefig(os.path.join(PATH_OUT, 'V1_hMT_bilateral_betas_comparison_PhyAmb_nsub_{}_clusters_BETAS_PSC'.format(len(SUBJ), betas_type)), bbox_inches='tight')
fig.savefig(os.path.join(PATH_OUT, 'V1_hMT_bilateral_betas_comparison_PhyAmb_nsub_{}_clusters_BETAS_PSC.svg'.format(len(SUBJ), betas_type)), format='svg', bbox_inches='tight')


print("Finished.")
