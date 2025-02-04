import os
import numpy as np
import nibabel as nb
import matplotlib.pyplot as plt
from scipy.stats import spearmanr, wilcoxon


# Conditions
SUBJ = ['sub-01', 'sub-03', 'sub-04', 'sub-06', 'sub-07', 'sub-08', 'sub-09', 'sub-10']
DUR_MIN = 4       # Duration minimum
DUR_MAX = 100     # Duration maximum
STAT = 'mean'
ROIS = ['V1', 'hMT']
TASK = 'amb'
COLOR_AREA = ['#7570b3', '#d95f02']

# Plot preparation
DPI = 300
x2 = np.arange(0, (DUR_MIN+1)*2)
print(x2)
OUTDIR = "/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD/Results/ERA_carpet-{}".format(TASK)
if not os.path.exists(OUTDIR):
    os.makedirs(OUTDIR)

fig, axes = plt.subplots(1, 2, figsize=(1920*2/DPI, 1200*2/DPI), dpi=DPI)
# =============================================================================

# Store values for statistical comparison
dominant_data = {'V1': [], 'hMT': []}
not_dominant_data = {'V1': [], 'hMT': []}

for itro, ro in enumerate(ROIS):

    # Initialize output structure
    hor_hor = np.zeros([len(SUBJ), DUR_MAX])
    ver_hor = np.zeros([len(SUBJ), DUR_MAX])
    hor_ver = np.zeros([len(SUBJ), DUR_MAX])
    ver_ver = np.zeros([len(SUBJ), DUR_MAX])

    print('New array {}'.format(np.shape(hor_hor)))

    for it, su in enumerate(SUBJ):
        NII_HOR = "/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD/{}/derivatives/func/Stats/carpet-{}/ROI-wise_carpet/{}_VOICarpet_normalized-t0_ERAperROI_dur_{}_{}_cond-2_{}.nii.gz".format(su, TASK, su, DUR_MIN, DUR_MAX, STAT)
        NII_VER = "/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD/{}/derivatives/func/Stats/carpet-{}/ROI-wise_carpet/{}_VOICarpet_normalized-t0_ERAperROI_dur_{}_{}_cond-3_{}.nii.gz".format(su, TASK, su, DUR_MIN, DUR_MAX, STAT)

        print('Plot ERA for {} {}'.format(su, ro))

        # Load conditions
        nii_hori = nb.load(NII_HOR)
        data_hori = np.asarray(nii_hori.dataobj)
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

    # Store data for statistical comparison
    dominant_data[ro] = dominant[:, 0:DUR_MIN+1]
    not_dominant_data[ro] = not_dominant[:, 0:DUR_MIN+1]

# Test dominant vs not dominant time course similarity
# For V1
correlations = np.zeros(len(SUBJ))

for it in range(0, len(SUBJ)):

    ts1 = dominant_data['V1'][it, :]
    ts2 = not_dominant_data['V1'][it, :]
    n = len(ts1)

    r, _ = spearmanr(ts1, ts2)            # Compute correlation

    z = 0.5 * np.log((1 + r) / (1 - r))  # Fisher's Z transformation
    correlations[it] = r

# Test for significance
# Perform Wilcoxon signed-rank test to check if median correlation differs from zero
stat, p_value = wilcoxon(correlations)
print(correlations)
print(p_value)

# For hMT
correlations = np.zeros(len(SUBJ))

for it in range(0, len(SUBJ)):

    ts1 = dominant_data['hMT'][it, :]
    ts2 = not_dominant_data['hMT'][it, :]

    r, _ = spearmanr(ts1, ts2)            # Compute correlation

    z = 0.5 * np.log((1 + r) / (1 - r))  # Fisher's Z transformation
    correlations[it] = r

# Test for significance
# Perform Wilcoxon signed-rank test to check if median correlation differs from zero
stat, p_value = wilcoxon(correlations)
print(correlations)
print(p_value)

# For V1 vs hMT
correlations = np.zeros(len(SUBJ))

for it in range(0, len(SUBJ)):

    ts1 = (dominant_data['V1'][it, :] + not_dominant_data['V1'][it, :]) /2
    ts2 = (dominant_data['hMT'][it, :] + not_dominant_data['hMT'][it, :]) /2

    r, _ = spearmanr(ts1, ts2)            # Compute correlation

    z = 0.5 * np.log((1 + r) / (1 - r))  # Fisher's Z transformation
    correlations[it] = r

# Test for significance
# Perform Wilcoxon signed-rank test to check if median correlation differs from zero
stat, p_value = wilcoxon(correlations)
print(correlations)
print(p_value)
