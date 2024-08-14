"""Read BrainVoyager VMP and export nifti."""

import os
import numpy as np
import nibabel as nb
import bvbabel
import pprint
import matplotlib.pyplot as plt

SUB = 'sub-01'
hem = 'LH'

PATH_IN = '/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD/{}/'.format(SUB)
# Load t-map from physical motion
FILENAME = '{}_Amb_maps_wholeBrain_bvbabel_res2x_float32.nii.gz'.format(SUB)
FILE = os.path.join(PATH_IN, 'derivatives', 'func', 'Stats', 'Amb', FILENAME)

niimap = nb.load(FILE)
map_all = np.asarray(niimap.dataobj)

# Load ROI definition
ROIS_FILE = '{}_visual_areas_hMT_{}_bvbabel_rim_cortMask_voronoi_noCapsule.nii.gz'.format(SUB, hem)
ROI_LABEL = ['hMT', 'V1']
rois_nii = nb.load(os.path.join(PATH_IN, 'derivatives', 'anat', '05_ROI_seg', 'voronoi', ROIS_FILE))
roi_data = np.asarray(rois_nii.dataobj)

print(np.unique(roi_data))

#// Separate distributions
map = map_all[..., 0]
idx_h = map > 0
idx_v = map < 0

for it, roi in enumerate(ROI_LABEL):
    idx_roi = roi_data == (it + 1)      # Find voxels within the ROI

    hor = map[idx_h*idx_roi]
    vert = map[idx_v*idx_roi]

    print('Highest t-value horizotal for {}: {}'.format(roi, np.max(hor)))
    print('Highest t-value vertical for {}: {}'.format(roi, np.min(vert)))

    #//Find 95 percentile from the 2 distributions within the ROI
    # horp = np.percentile(hor, 95)
    # vertp = np.percentile(np.abs(vert), 95)
    # vertp = vertp *-1
    #
    # idx_h_p = map > horp
    # idx_v_p = map < vertp

    #//Mask voxels below percentile threshold within the ROI
    clu = np.zeros(np.shape(map), dtype=np.int8)
    clu[idx_h * idx_roi] = 1
    clu[idx_v* idx_roi] = 2

    # print('Number of Horizontal voxels above threshold {}: {}'.format(horp, np.sum(map > horp)))
    # print('Number of Vertical voxels above threshold {}: {}'.format(vertp, np.sum(map < vertp)))

    print('Save clusters')
    OUTPUTNAME = os.path.join(PATH_IN, 'derivatives', 'func', 'Stats', 'Amb', '{}_Amb_maps_wholeBrain_bvbabel_res2x_float32_clusters_{}_{}_winner.nii.gz'.format(SUB, hem, roi))
    img = nb.Nifti1Image(clu, affine=niimap.affine, header=niimap.header)
    nb.save(img, OUTPUTNAME)

    # # # // Plotting here
    # fig, axs = plt.subplots(1, 2, sharey=True, tight_layout=True)
    # n_bins = 100
    # axs[0].hist(vert, bins=n_bins)
    # axs[1].hist(hor, bins=n_bins)
    #
    # axs[0].set_ylabel('Vertical voxels')
    # axs[1].set_ylabel('Horizontal voxels')
    #
    # axs[0].set_xlabel('t-values')
    # axs[1].set_xlabel('t-values')
    # plt.savefig(os.path.join(PATH_IN, '{}_Cluster_distributions_{}_{}.png'.format(SUB, hem, roi)))
