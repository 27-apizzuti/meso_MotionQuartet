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
ROIS = ['V1']
categories_1 = ['Physical Motion', 'Flicker']
categories_2 = ['Ambiguous Motion', 'Flicker']
colors_V1 = ['#7570b3', 'gray']
colors_hMT = ['#d95f02', 'gray']

hatch_patterns = ['', '']
DPI = 300
PATH_OUT = os.path.join(STUDY_PATH, 'Results', 'Betas')
betas_type = 'BETAS_PSC'     #'betas'
fig, axs = plt.subplots(2,2, figsize=(1920*2/DPI, 1200*2/DPI), dpi=DPI)

# ------------------------------------------------------------------------------
for it_ro, ro in enumerate(ROIS):


    # Create output structure
    betas_preds_amb = np.zeros([len(SUBJ)*len(HEMIS), 2])     # Predictors: Categories
    betas_preds_phy = np.zeros([len(SUBJ)*len(HEMIS), 2])     # Predictors: Categories
    i = 0

    for it_hemi, hemi in enumerate(HEMIS):

        for it_su, su in enumerate(SUBJ):
            PATH_IN =  os.path.join(STUDY_PATH, su, 'derivatives', 'func', 'Stats', 'Betas_Layers')

            # Load betas 
            betas_amb = np.load(os.path.join(PATH_IN, "{}_depth_vs_Amb_{}_{}_phy_clusters_{}_active_suppression.npy".format(su, hemi, ro, betas_type)), allow_pickle=True).item()
            betas_phy = np.load(os.path.join(PATH_IN, "{}_depth_vs_Phy_{}_{}_phy_clusters_{}_active_suppression.npy".format(su, hemi, ro, betas_type)), allow_pickle=True).item()

            print('Working on {} {}'.format(su, ro))

            # Fill in
           
            betas_preds_amb[i, 0] = ( np.mean(betas_amb["Horizontal_clust"]["Horizontal"]["betas"]) + np.mean(betas_amb["Vertical_clust"]["Vertical"]["betas"]) +
                                     np.mean(betas_amb["Horizontal_clust"]["Vertical"]["betas"]) + np.mean(betas_amb["Vertical_clust"]["Horizontal"]["betas"]) )/4
            
            betas_preds_amb[i, 1] = (np.mean(np.mean(betas_amb["Horizontal_clust"]["Flicker"]["betas"])) + np.mean(betas_amb["Vertical_clust"]["Flicker"]["betas"]))/2
            
            betas_preds_phy[i, 0] = ( np.mean(betas_phy["Horizontal_clust"]["Horizontal"]["betas"]) + np.mean(betas_phy["Vertical_clust"]["Vertical"]["betas"]) +
                                     np.mean(betas_phy["Horizontal_clust"]["Vertical"]["betas"]) + np.mean(betas_phy["Vertical_clust"]["Horizontal"]["betas"]) )/4
            
            betas_preds_phy[i, 1] = (np.mean(np.mean(betas_phy["Horizontal_clust"]["Flicker"]["betas"])) + np.mean(betas_phy["Vertical_clust"]["Flicker"]["betas"]))/2
            

            i = i +1


    # Create a bar plot
    if ro == 'V1':
        colors = colors_V1
    else:
        colors = colors_hMT
        
    for it in range(len(categories_1)):
        
        axs[0, it_ro].bar(categories_1[it], np.mean(betas_preds_phy[:, it],axis=0), yerr=sem(betas_preds_phy[:, it],axis=0), color=colors[it], hatch=hatch_patterns[it], alpha=0.5)
        axs[1, it_ro].bar(categories_2[it], np.mean(betas_preds_amb[:, it],axis=0), yerr=sem(betas_preds_amb[:, it],axis=0), color=colors[it], hatch=hatch_patterns[it], alpha=0.5)

    axs[0, it_ro].grid(axis='y', linestyle='--', alpha=0.7)
    axs[1, it_ro].grid(axis='y', linestyle='--', alpha=0.7)
    
    # Add labels and title
    axs[1, it_ro].tick_params(axis='x', labelsize=20)  # Set the labelsize parameter to increase the label size
    axs[0, it_ro].tick_params(axis='y', labelsize=20)  # Set the labelsize parameter to increase the label size
    
    axs[0, it_ro].tick_params(axis='x', labelsize=20)  # Set the labelsize parameter to increase the label size
    axs[1, it_ro].tick_params(axis='y', labelsize=20)  # Set the labelsize parameter to increase the label size

    axs[0, it_ro].set_ylabel('Betas', fontsize=20)
    axs[1, it_ro].set_ylabel('Betas', fontsize=20)
    axs[0, it_ro].set_ylim([-0.5, 1.5])
    axs[1, it_ro].set_ylim([-0.5, 1.5])
   
plt.tight_layout()
# Show the plot
# axs.show()
fig.savefig(os.path.join(PATH_OUT, 'V1_hMT_bilateral_betas_comparison_nsub_{}_clusters_BETAS_PSC'.format(len(SUBJ), betas_type)), bbox_inches='tight')

print("Finished.")
