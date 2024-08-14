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
DUR_MIN = 3    # 4
DUR_MAX = 5  # 100
STAT = 'mean'
ROIS = ['V1', 'hMT']
TASK = 'amb'

# Plot preparation
DPI = 300
x2 = np.arange(0, (DUR_MIN+1)*2)
OUTDIR = "D:\\Exp-MotionQuartet\\MRI_MQ\\BOLD\\Results\\ERA_carpet-{}".format(TASK)
if not os.path.exists(OUTDIR):
    os.makedirs(OUTDIR)

fig, axes = plt.subplots(2, 2, figsize=(1920*2/DPI, 1200*2/DPI), dpi=DPI)
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

        NII_FLICK = "D:\\Exp-MotionQuartet\\MRI_MQ\\BOLD\\{}\\derivatives\\func\\Stats\\carpet-{}\\ROI-wise_carpet\\{}_VOICarpet_normalized-t0_ERAperROI_dur_{}_{}_cond-1_{}.nii.gz".format(su, TASK, su, DUR_MIN, DUR_MAX, STAT)

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
   
    # Plot average
    # DUR_MAX = 5
    axes[itro, 0].errorbar(x2[::2], np.nanmean(hor_hor[:, 0:DUR_MIN+1], axis=0), sem(hor_hor[:, 0:DUR_MIN+1], axis=0), color='red', linewidth=2)
    axes[itro, 0].errorbar(x2[::2], np.nanmean(ver_hor[:, 0:DUR_MIN+1], axis=0), sem(ver_hor[:, 0:DUR_MIN+1], axis=0), color='blue', linewidth=2)
    axes[itro, 0].set_xticks(x2[::2])
    axes[itro, 0].set_xticklabels(x2[::2])
    axes[itro, 0].set_ylabel("% fMRI (a.u.)", fontsize=20)
    axes[itro, 0].set_xlabel("Time [s]", fontsize=20)
    axes[itro, 0].tick_params(axis='x', labelsize=20)
    axes[itro, 0].tick_params(axis='y', labelsize=20)


    if TASK == 'phy':
        if ro == 'V1':
            axes[itro, 0].set_ylim([-3, 3])
        else:
            axes[itro, 0].set_ylim([-1, 1])
    else:
        axes[itro, 0].set_ylim([-0.4, 0.8])

    # axes[itro, 0].axvspan(0, 10, color='gray', alpha=0.06)
    axes[itro, 0].axhline(y=0, linestyle='--', color='black', linewidth=0.5)
    axes[itro, 0].set_title('Horizontal epochs - {}'.format(ro))
    if TASK == 'phy':
        if ro == 'V1':
            axes[itro, 1].set_ylim([-3, 3])
        else:
            axes[itro, 1].set_ylim([-1, 1])
    else:
        axes[itro, 1].set_ylim([-0.4, 0.8])
    axes[itro, 1].errorbar(x2[::2], np.nanmean(hor_ver[:, 0:DUR_MIN+1], axis=0), sem(hor_ver[:, 0:DUR_MIN+1], axis=0), color='red', linewidth=2)
    axes[itro, 1].errorbar(x2[::2], np.nanmean(ver_ver[:, 0:DUR_MIN+1], axis=0), sem(ver_ver[:, 0:DUR_MIN+1], axis=0), color='blue', linewidth=2)
    axes[itro, 1].set_xticks(x2[::2])
    axes[itro, 1].set_xticklabels(x2[::2])
    axes[itro, 1].set_ylabel("% fMRI (a.u.)", fontsize=20)
    axes[itro, 1].set_xlabel("Time [s]", fontsize=20)
    # axes[itro, 0].axvspan(0, 10, color='gray', alpha=0.06)
    axes[itro, 1].axhline(y=0, linestyle='--', color='black', linewidth=0.5)
    axes[itro, 1].set_title('Vertical epochs - {}'.format(ro))
    axes[itro, 1].tick_params(axis='x', labelsize=20)
    axes[itro, 1].tick_params(axis='y', labelsize=20)



# plt.suptitle('Event-related averages for {} condition'.format(TASK), fontsize=14)
plt.tight_layout()
fig.savefig(os.path.join(OUTDIR, 'ROIwise_Figure_ERA_group_average_V1_hMT_dur_{}_{}_{}'.format(DUR_MIN, DUR_MAX, STAT)), bbox_inches='tight')  
print("\nFinished.")
