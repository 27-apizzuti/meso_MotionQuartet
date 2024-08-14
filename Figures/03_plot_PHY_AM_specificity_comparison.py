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
CONDITIONS = ['Phy', 'Amb']

PATH_OUT = os.path.join(STUDY_PATH, 'Results', 'Betas')
betas_type = 'BETAS_PSC'     #'betas'


n_subj = len(SUBJ)
# ------------------------------------------------------------------------------
SpecROI = []
for it_ro, ro in enumerate(ROIS):
    
    specficity = np.zeros([len(SUBJ)*len(HEMIS), 2])
    for it_hemi, hemi in enumerate(HEMIS):

        for it_su, su in enumerate(SUBJ):
            PATH_IN =  os.path.join(STUDY_PATH, su, 'derivatives', 'func', 'Stats', 'Betas_Layers')

            # Load betas 
            for it_cond, cond in enumerate(CONDITIONS):
                betas_phy = np.load(os.path.join(PATH_IN, "{}_depth_vs_{}_{}_{}_phy_clusters_{}_active_suppression.npy".format(su, cond, hemi, ro, betas_type)), allow_pickle=True).item()
                vox_tvalue1 = np.asarray([betas_phy['Horizontal_clust']['Horizontal']['betas'], betas_phy['Horizontal_clust']['Vertical']['betas']])
                vox_tvalue2 = np.asarray([betas_phy['Vertical_clust']['Horizontal']['betas'], betas_phy['Vertical_clust']['Vertical']['betas']])
                vox_tvalue =  np.transpose(np.hstack((vox_tvalue1, vox_tvalue2)))
                
                # Compute Metric #2: Divergence-Specificity
                # print('Compute specificity')
                
                # NOTE: [0-45° max] --> normalized into [0-1]
                t_asc = np.sort(vox_tvalue, axis=1)
                v = [0, 1]              # reference axis (winning)
                vox_div = np.zeros([t_asc.shape[0]])
        
                for iterVox in range(0, t_asc.shape[0]):
                    u = t_asc[iterVox, :]
                    if np.sum(u) > 0:
                        c = np.dot(u,v)/np.linalg.norm(u)/np.linalg.norm(v) # -> cosine of the angle
                        angle = np.arccos(np.clip(c, -1, 1))                # -> radiants
                        angle_degree = angle * 180 / np.pi                  # -> degree
                        if angle_degree < 0:
                            print("Vectors: {}, {}".format(u, v))
                        vox_div[iterVox] = angle_degree / 45                # -> normalization
                        vox_div[iterVox] = 1 - vox_div[iterVox]             # -> inverted
                        if vox_div[iterVox] > 1:
                            print("Vectors: {}, {}; spec. {}, angle: {}".format(u, v, vox_div[iterVox], angle_degree))
                
                # vox_div[vox_div == 0] = np.nan
                meanspec = np.nanmean(vox_div)
                print(np.sum(vox_div == 0)/t_asc.shape[0])
                # print('Mean specificity for {} hemi {}: {}'.format(su, hemi, meanspec))
                
                specficity[(it_su + (it_hemi*n_subj)), it_cond] = meanspec
                
    # Save both ROIs
    SpecROI.append(specficity)
    
# Plotting specificity            
colors = ['#7570b3', '#7570b3', '#d95f02', '#d95f02']
# hatch_patterns = ['', '//', '', '//']
DPI = 300
fig, axs = plt.subplots(figsize=(1920*2/DPI, 1200*2/DPI), dpi=DPI)
categories_1 = ['Phys-V1', 'Amb-V1', 'Phys-hMT+', 'Amb-hMT+']
data = np.hstack((SpecROI[0], SpecROI[1]))

# axs.bar(categories_1, np.mean(data,axis=0), yerr=sem(data,axis=0), color=colors, hatch=hatch_patterns, alpha=0.6)
axs.bar(categories_1, np.mean(data,axis=0), yerr=sem(data,axis=0), color=colors,  alpha=0.6)
axs.grid(axis='y', linestyle='--', alpha=0.7)
# Add labels and title
axs.tick_params(axis='x', labelsize=20)  # Set the labelsize parameter to increase the label size
axs.tick_params(axis='y', labelsize=20)  # Set the labelsize parameter to increase the label size

axs.set_ylabel('Specificity', fontsize=20)
  
# plt.tight_layout()
# Show the plot
# axs.show()
fig.savefig(os.path.join(PATH_OUT, 'V1_hMT_bilateral_betas_SPECIFICITY_nsub_8_clusters_BETAS_PSC.jpeg'), format='jpeg', bbox_inches='tight')
fig.savefig("test.svg", format="svg")

fig.savefig(os.path.join(PATH_OUT, 'V1_hMT_bilateral_betas_SPECIFICITY_nsub_{}_clusters_BETAS_PSC.svg'.format(len(SUBJ), betas_type)), format='svg', bbox_inches='tight')


