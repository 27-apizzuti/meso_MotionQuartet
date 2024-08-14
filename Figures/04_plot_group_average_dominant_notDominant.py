"""Compute event related averages for each ROI.

Designed for the 7 T motion quartet experiment data (2024).
"""

import os
import numpy as np
import nibabel as nb
import matplotlib.pyplot as plt
from scipy.stats import sem


# Conditions
SUBJ = ['sub-01', 'sub-03', 'sub-04', 'sub-06', 'sub-07', 'sub-08', 'sub-09', 'sub-10']
DUR_MIN = 5       # 4  3 
DUR_MAX = 100       # 100   5
STAT = 'mean'
ROIS = ['V1', 'hMT']
TASK = 'amb'
COLOR_AREA = ['#7570b3', '#d95f02']

# Plot preparation
DPI = 300
x2 = np.arange(0, (DUR_MIN+1)*2)
print(x2)
OUTDIR = "D:\\Exp-MotionQuartet\\MRI_MQ\\BOLD\\Results\\ERA_carpet-{}".format(TASK)
if not os.path.exists(OUTDIR):
    os.makedirs(OUTDIR)

fig, axes = plt.subplots(1, 2, figsize=(1920*2/DPI, 1200*2/DPI), dpi=DPI)
# =============================================================================

for itro, ro in enumerate(ROIS):
    
    # Initialize output structure
    hor_hor = np.zeros([len(SUBJ), DUR_MAX])
    ver_hor = np.zeros([len(SUBJ), DUR_MAX])

    hor_ver = np.zeros([len(SUBJ), DUR_MAX])
    ver_ver = np.zeros([len(SUBJ), DUR_MAX])

    print('New array {}'.format(np.shape(hor_hor)))

    for it, su in enumerate(SUBJ):
        NII_HOR = "D:\\Exp-MotionQuartet\\MRI_MQ\\BOLD\\{}\\derivatives\\func\\Stats\\carpet-{}\\ROI-wise_carpet\\{}_VOICarpet_normalized-t0_ERAperROI_dur_{}_{}_cond-2_{}.nii.gz".format(su, TASK, su, DUR_MIN, DUR_MAX, STAT)

        NII_VER = "D:\\Exp-MotionQuartet\\MRI_MQ\\BOLD\\{}\\derivatives\\func\\Stats\\carpet-{}\\ROI-wise_carpet\\{}_VOICarpet_normalized-t0_ERAperROI_dur_{}_{}_cond-3_{}.nii.gz".format(su, TASK, su, DUR_MIN, DUR_MAX, STAT)

        print('Plot ERA for {} {}'.format(su, ro))
        
        # Load conditions
        nii_hori = nb.load(NII_HOR)
        data_hori = np.asarray(nii_hori.dataobj)

        # Load conditions
        nii_ver = nb.load(NII_VER)
        data_ver = np.asarray(nii_ver.dataobj)
        print('Trial {}'.format(np.shape(data_hori[:, 0])))

        # Extract clusters per ROI
        if ro == 'V1':
            hor_hor[it, :] = data_hori[:, 0]
            ver_hor[it, :] = data_hori[:, 1]
            
            hor_ver[it, :] = data_ver[:, 0]
            ver_ver[it, :] = data_ver[:, 1]

        else:
            hor_hor[it, :] = data_hori[:, 2]
            ver_hor[it, :] = data_hori[:, 3]
            
            hor_ver[it, :] = data_ver[:, 2]
            ver_ver[it, :] = data_ver[:, 3]

    # MERGE CLUSTERS
    dominant = (hor_hor + ver_ver) / 2
    not_dominant = (ver_hor + hor_ver) / 2
    
    # Plot average
    # DUR_MAX = 5
    axes[itro].errorbar(x2[::2], np.nanmean(dominant[:, 0:DUR_MIN+1], axis=0), sem(dominant[:, 0:DUR_MIN+1], axis=0), color=COLOR_AREA[itro], linewidth=2)
    axes[itro].errorbar(x2[::2], np.nanmean(not_dominant[:, 0:DUR_MIN+1], axis=0), sem(not_dominant[:, 0:DUR_MIN+1], axis=0), color='black', linewidth=2)
    axes[itro].set_xticks(x2[::2])
    axes[itro].set_xticklabels(x2[::2])
    axes[itro].set_ylabel("% fMRI (a.u.)", fontsize=20)
    axes[itro].set_xlabel("Time [s]", fontsize=20)
    axes[itro].axhline(y=0, linestyle='--', color='black', linewidth=0.5)
    axes[itro].set_title('{}'.format(ro), fontsize=20)
    axes[itro].set_ylim([-3, 3])
    axes[itro].tick_params(axis='x', labelsize=20)
    axes[itro].tick_params(axis='y', labelsize=20)

    # if TASK == 'phy':
      
    #     axes[itro].set_ylim([-3, 3])
       
    # else:
    #     axes[itro].set_ylim([-0.4, 0.8])    
   
# plt.suptitle('Event-related averages for {} condition'.format(TASK), fontsize=14)
plt.tight_layout()
fig.savefig(os.path.join(OUTDIR, 'testROIwise_Figure_ERA_group_average_V1_hMT_dur_{}_{}_{}_dominant_notDominant'.format(DUR_MIN, DUR_MAX, STAT)), bbox_inches='tight')  
# fig.savefig(os.path.join(OUTDIR, 'ROIwise_Figure_ERA_group_average_V1_hMT_dur_{}_{}_{}_dominant_notDominant.svg'.format(DUR_MIN, DUR_MAX, STAT)), format='svg', bbox_inches='tight')  

print("\nFinished.")
