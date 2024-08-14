"""
Get 2D histogram for each file
Get overlayed layer profile across contrasts
Input: metric file (from LN2_LAYERS), t-value map
"""
import numpy as np
import nibabel as nb
import matplotlib.pyplot as plt
import matplotlib as mpl
import os
from glob import glob
from scipy.stats import sem
from my_layer_profiles import *
from pprint import pprint
from matplotlib.ticker import FormatStrFormatter

# -------------------------------------------------------------------------
# Define input
# -------------------------------------------------------------------------
STUDY_PATH = "D:\\Exp-MotionQuartet\\MRI_MQ\\BOLD"
SUBJ = ['sub-01', 'sub-03', 'sub-04', 'sub-06', 'sub-07', 'sub-08', 'sub-09', 'sub-10']
HEMIS = ['LH', 'RH']
N_LAYERS = 3
DPI = 300
ROI = ['V1']
PATH_OUT = os.path.join(STUDY_PATH, 'Results', 'Betas')
x = np.arange(1, N_LAYERS+1)
CLUSTERS = ['Horizontal', 'Vertical']

for itro, ro in enumerate(ROI):
    fig, axs = plt.subplots(2, 2, figsize=(1920*2/DPI, 1920*2/DPI), dpi=DPI)
    
    # Create output structure
    for it_clu, clust in enumerate(CLUSTERS):
        betas_preds = np.zeros([N_LAYERS, len(SUBJ)*len(HEMIS), 2])
        i = 0
        
        for su in SUBJ:
            # // Load data to plot
            PATH_IN = os.path.join(STUDY_PATH, su, 'derivatives', 'func', 'Stats', 'Betas_Layers')
        
            for it_hem, hem in enumerate(HEMIS):
                
                print('Working on {} {} {}'.format(su, ro, hem))
                betas_amb = np.load(os.path.join(PATH_IN, "{}_depth_vs_Amb_{}_{}_phy_clusters_BETAS_PSC_active_suppression.npy".format(su, hem, ro)), allow_pickle=True).item()
                
                if clust == 'Horizontal':
                
                    # Subtracting the horizontal - vertical betas
                    betas_amb_dom =  (betas_amb["{}_clust".format(clust)]["Horizontal".format(clust)]["betas"])
                    betas_amb_not_dom = (betas_amb["{}_clust".format(clust)]["Vertical".format(clust)]["betas"])
                    col_dom = 'red'
                    col_not_dom = 'blue'
                    metric = betas_amb["{}_clust".format(clust)]["Horizontal"]["Metric"]
                    
                else:
                    betas_amb_dom =  (betas_amb["{}_clust".format(clust)]["Vertical".format(clust)]["betas"])
                    betas_amb_not_dom = (betas_amb["{}_clust".format(clust)]["Horizontal".format(clust)]["betas"])
                    metric = betas_amb["{}_clust".format(clust)]["Vertical"]["Metric"]

                    col_dom = 'blue'
                    col_not_dom = 'red'
                    
                layers = my_layer_profiles(metric, N_LAYERS)
                layers_data = np.unique(layers)
    
                for it in layers_data:
    
                    it = int(it)
                    idx = (layers==it).astype(bool)
    
                    #// Trovo i voxels nei layers
                    betas_preds[it-1, i, 0] = np.nanmean(betas_amb_dom[idx])
                    betas_preds[it-1, i, 1] = np.nanmean(betas_amb_not_dom[idx])
    
                i = i +1
    
        #//Plotting magic here
        dom = betas_preds[:, :, 0]
        not_dom = betas_preds[:, :, 1]
        beta_diff = dom - not_dom
 
        axs[0, it_clu].errorbar(x, np.mean(dom, axis=1), yerr=sem(dom, axis=1), linewidth=2, color=col_dom)
        axs[0, it_clu].errorbar(x, np.mean(not_dom, axis=1), yerr=sem(not_dom, axis=1), linewidth=2, linestyle='dotted', color=col_not_dom)
        axs[1, it_clu].errorbar(x, np.mean(beta_diff, axis=1), yerr=sem(beta_diff, axis=1), linewidth=2, color='black')
    
        # Set y-limits
        axs[0, it_clu].set_ylim([-2, 3.5])
        axs[1, it_clu].set_ylim([-2, 3.5])

        # Adjustments
        axs[0, it_clu].tick_params(axis='x', labelsize=18)
        axs[0, it_clu].tick_params(axis='y', labelsize=18)
        
        axs[1, it_clu].tick_params(axis='x', labelsize=18)
        axs[1, it_clu].tick_params(axis='y', labelsize=18)
        axs[0, it_clu].yaxis.set_major_formatter(FormatStrFormatter('%.1f'))
        axs[1, it_clu].yaxis.set_major_formatter(FormatStrFormatter('%.1f'))
        
        # Set grid
        axs[0, it_clu].grid(axis='y', linestyle='--', alpha=0.7)
        axs[1, it_clu].grid(axis='y', linestyle='--', alpha=0.7)
        
        # Set x-label
        axs[0, it_clu].set_xlabel("Cortical layers (1=deep layer)", fontsize=20)
        axs[0, it_clu].set_xticks(x)
        axs[1, it_clu].set_xlabel("Cortical layers (1=deep layer)", fontsize=20)
        axs[1, it_clu].set_xticks(x)
        
        # Set y-label
        axs[0, it_clu].set_ylabel("Betas PSC", fontsize=20)
        axs[1, it_clu].set_ylabel("Betas PSC", fontsize=20)
       
    
    fig.suptitle('Group average layer profiles {} '.format(ro), fontsize=22, x=0.5, y=1.05)
    plt.tight_layout()
    fig.savefig(os.path.join(PATH_OUT, 'Group_average_{}_bilteral_{}_layers_{}_betas_PSC_cluster_dom_minus_suppressed.svg'.format(su, ro, N_LAYERS)), bbox_inches='tight')
