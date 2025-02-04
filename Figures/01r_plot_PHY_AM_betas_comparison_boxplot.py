import os
import numpy as np
from scipy.stats import sem, wilcoxon
import matplotlib.pyplot as plt

STUDY_PATH = '/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD'
SUBJ = ['sub-01', 'sub-03', 'sub-04', 'sub-06', 'sub-07', 'sub-08', 'sub-09', 'sub-10']
HEMIS = ['LH', 'RH']
ROIS = ['V1', 'hMT']

CLUSTERS = ['Horizontal', 'Vertical']
colors_1 = ['#de2d26', '#fee0d2']
colors_2 = ['#3182bd', '#deebf7']

DPI = 300
PATH_OUT = os.path.join(STUDY_PATH, 'Results', 'Betas')
betas_type = 'BETAS_PSC'  # 'betas'

fig, axs = plt.subplots(2, 2, figsize=(1920 * 2 / DPI, 1200 * 2 / DPI), dpi=DPI)
categories_1 = ['Physical', 'Ambiguous']

# -------------------------------------------------------------------------------
# Collect p-values for FDR correction
p_values = []
plot_indices = []  # Keep track of axes indices for annotating corrected p-values

for it_ro, ro in enumerate(ROIS):
    for it_clu, clust in enumerate(CLUSTERS):

        # Create output structure
        betas_preds = np.zeros([len(SUBJ) * len(HEMIS), 2])  # Mean betas per condition

        i = 0
        for it_hemi, hemi in enumerate(HEMIS):
            for it_su, su in enumerate(SUBJ):
                PATH_IN = os.path.join(STUDY_PATH, su, 'derivatives', 'func', 'Stats', 'Betas_Layers')

                # Load betas
                betas_amb = np.load(
                    os.path.join(PATH_IN, "{}_depth_vs_Amb_{}_{}_phy_clusters_{}_active_suppression.npy".format(
                        su, hemi, ro, betas_type)), allow_pickle=True).item()
                betas_phy = np.load(
                    os.path.join(PATH_IN, "{}_depth_vs_Phy_{}_{}_phy_clusters_{}_active_suppression.npy".format(
                        su, hemi, ro, betas_type)), allow_pickle=True).item()

                # print('Working on {} {}'.format(su, ro))

                # Fill in
                betas_preds[i, 0] = np.mean(betas_phy["{}_clust".format(clust)]["{}".format(clust)]["betas"])
                betas_preds[i, 1] = np.mean(betas_amb["{}_clust".format(clust)]["{}".format(clust)]["betas"])
                i += 1

        # Perform wilcoxon test
        print(np.shape(betas_preds))
        stat, p_value = wilcoxon(betas_preds[:, 0], betas_preds[:, 1])
        p_values.append(p_value)  # Collect p-values
        plot_indices.append((it_ro, it_clu))  # Save subplot index for annotation
        print('For {} ROI and cluster {}, test results are {} {}'.format(ro, clust, stat, p_value))

        # Create boxplot
        data = [betas_preds[:, 0], betas_preds[:, 1]]
        colors = colors_1 if clust == 'Horizontal' else colors_2
        axs[it_ro, it_clu].boxplot(
            data, patch_artist=True,
            boxprops=dict(facecolor=colors[0], alpha=0.5),
            medianprops=dict(color='black', linewidth=2),
            positions=[0, 1], widths=0.6
        )

        # Add connecting lines for within-participant effects
        for row in betas_preds:
            axs[it_ro, it_clu].plot([0, 1], row, color='gray', alpha=0.6)

# # Annotate p-values
# for idx, (it_ro, it_clu) in enumerate(plot_indices):
#     y_max = 3.5  # Adjust y_max if necessary to fit annotation
#     axs[it_ro, it_clu].annotate(
#         f'p = {p_values[idx]:.3g}', xy=(0.5, y_max),
#         xycoords='data', ha='center', fontsize=12, color='black',
#         bbox=dict(boxstyle='round,pad=0.3', edgecolor='black', facecolor='white', alpha=0.8)
#             )
# Formatting
for ax in axs.flat:
    ax.set_xticks([0, 1])
    ax.set_xticklabels(categories_1, fontsize=15)
    ax.set_ylabel('Percent signal change', fontsize=15)
    ax.tick_params(axis='y', labelsize=12)
    ax.grid(axis='y', linestyle='--', alpha=0.7)

plt.tight_layout()
plt.savefig(os.path.join(PATH_OUT, 'Betas_Boxplot_single_subjects_revision.png'), dpi=DPI)
fig.savefig(os.path.join(PATH_OUT, 'Betas_Boxplot_single_subjects_revision.svg'.format(len(SUBJ), betas_type)), format='svg', bbox_inches='tight')
plt.show()
