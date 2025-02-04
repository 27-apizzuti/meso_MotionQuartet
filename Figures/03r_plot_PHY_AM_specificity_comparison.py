import os
import numpy as np
from scipy.stats import sem, wilcoxon
import matplotlib.pyplot as plt

STUDY_PATH = '/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD'
SUBJ = ['sub-01', 'sub-03', 'sub-04', 'sub-06', 'sub-07', 'sub-08', 'sub-09', 'sub-10']
HEMIS = ['LH', 'RH']
ROIS = ['V1', 'hMT']
CONDITIONS = ['Phy', 'Amb']

PATH_OUT = os.path.join(STUDY_PATH, 'Results', 'Betas')
betas_type = 'BETAS_PSC'

n_subj = len(SUBJ)

# Initialize list to hold specificity values for each ROI
SpecROI = []
for ro in ROIS:
    specificity = np.zeros([len(SUBJ) * len(HEMIS), 2])  # Rows: subj/hemis, Columns: conditions
    for it_hemi, hemi in enumerate(HEMIS):
        for it_su, su in enumerate(SUBJ):
            PATH_IN = os.path.join(STUDY_PATH, su, 'derivatives', 'func', 'Stats', 'Betas_Layers')

            for it_cond, cond in enumerate(CONDITIONS):
                betas_phy = np.load(
                    os.path.join(PATH_IN, f"{su}_depth_vs_{cond}_{hemi}_{ro}_phy_clusters_{betas_type}_active_suppression.npy"),
                    allow_pickle=True
                ).item()
                vox_tvalue1 = np.asarray([betas_phy['Horizontal_clust']['Horizontal']['betas'],
                                           betas_phy['Horizontal_clust']['Vertical']['betas']])
                vox_tvalue2 = np.asarray([betas_phy['Vertical_clust']['Horizontal']['betas'],
                                           betas_phy['Vertical_clust']['Vertical']['betas']])
                vox_tvalue = np.transpose(np.hstack((vox_tvalue1, vox_tvalue2)))

                # Compute specificity metric
                t_asc = np.sort(vox_tvalue, axis=1)
                v = [0, 1]
                vox_div = np.zeros([t_asc.shape[0]])
                for iterVox in range(0, t_asc.shape[0]):
                    u = t_asc[iterVox, :]
                    if np.sum(u) > 0:
                        c = np.dot(u, v) / np.linalg.norm(u) / np.linalg.norm(v)
                        angle = np.arccos(np.clip(c, -1, 1))
                        angle_degree = angle * 180 / np.pi
                        vox_div[iterVox] = 1 - (angle_degree / 45)  # Normalize and invert

                # Compute specificity
                meanspec = np.nanmean(vox_div)
                specificity[(it_su + (it_hemi * n_subj)), it_cond] = meanspec
    SpecROI.append(specificity)

# Perform statistical testing (One-tailed test)
p_values = []
t_stats = []

for roi_idx, roi_data in enumerate(SpecROI):

    # Perform wilcoxon test
    print(np.shape(roi_data))
    stat, p_value = wilcoxon(roi_data[:, 0], roi_data[:, 1])

    t_stats.append(stat)
    p_values.append(p_value)

# Print t-test results
categories = ['V1', 'hMT+']
for i, roi in enumerate(categories):
    print(f"ROI: {roi}")
    print(f"  t = {t_stats[i]:.3f}, p = {p_values[i]:.5f}")

# Plotting
data = np.hstack(SpecROI)
categories = ['Phy-V1', 'Amb-V1', 'Phy-hMT+', 'Amb-hMT+']
colors = ['#7570b3', '#7570b3', '#d95f02', '#d95f02']
DPI = 300
fig, axs = plt.subplots(figsize=(1920 * 2 / DPI, 1200 * 2 / DPI), dpi=DPI)

axs.bar(categories, np.mean(data, axis=0), yerr=sem(data, axis=0), color=colors, alpha=0.6)
axs.grid(axis='y', linestyle='--', alpha=0.7)

# Add labels and title
axs.tick_params(axis='x', labelsize=20)
axs.tick_params(axis='y', labelsize=20)
axs.set_ylabel('Specificity', fontsize=20)

# Save the figure
fig.savefig(os.path.join(PATH_OUT, 'V1_hMT_bilateral_betas_SPECIFICITY_FDR_BETAS_PSC_Wilco.jpeg'), format='jpeg', bbox_inches='tight')
fig.savefig(os.path.join(PATH_OUT, 'V1_hMT_bilateral_betas_SPECIFICITY_FDR_BETAS_PSC_Wilco.svg'), format='svg', bbox_inches='tight')
plt.show()
