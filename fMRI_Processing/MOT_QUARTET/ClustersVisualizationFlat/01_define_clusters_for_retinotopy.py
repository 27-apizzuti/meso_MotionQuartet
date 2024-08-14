"""Define retinotopy-defined perceptual path in V1 based on physical motion
and evaluate cortical distribution"""

import os
import numpy as np
import nibabel as nb
import bvbabel
import pprint
from glob import glob
import matplotlib.pyplot as plt

SUB = ['sub-01']
HEMI = ['LH', 'RH']

for su in SUB:
    PATH_IN = "D:\\Exp-MotionQuartet\\MRI_MQ\\BOLD\\{}".format(su)

    # Load t-map from physical motion
    FILENAME = '{}_phy_maps_wholeBrain_TSTATS_bvbabel_res2x_float32.nii.gz'.format(su)
    FILE = os.path.join(PATH_IN, 'derivatives', 'func', 'Stats', 'Phy', FILENAME)

    niimap = nb.load(FILE)
    map_all = np.asarray(niimap.dataobj)

    PATH_OUT = os.path.join(PATH_IN, 'derivatives', 'func', 'Stats', 'Hyph01')
    if not os.path.exists(PATH_OUT):
        os.mkdir(PATH_OUT)

    # Load metric file
    LAY_PATH = os.path.join(PATH_IN, 'derivatives', 'anat', '06_CorticalLayers')
    os.chdir(LAY_PATH)
    metr_file =  glob("{}_RIM*metric_equivol.*".format(su))[0]
    lay_file = glob("{}_RIM*layers_equivol.*".format(su))[0]

    metr_nii= nb.load(os.path.join(LAY_PATH, metr_file))
    lay_nii= nb.load(os.path.join(LAY_PATH, lay_file))

    metr_data = np.asarray(metr_nii.dataobj)
    lay_data = np.asarray(lay_nii.dataobj)
    layers = np.unique(lay_data)[1:]
    print(layers)

    #// Separate distributions
    map = map_all[..., 0]      # Take only HORIZONTAL > VERTICAL
    idx_h = map > 0
    idx_v = map < 0

    for hem in HEMI:
        # Load ROI definition
        ROIS_FILE = '{}_visual_areas_hMT_{}_bvbabel_rim_voronoi_noCapsule.nii.gz'.format(su, hem)
        ROI_LABEL = ['V1']
        rois_nii = nb.load(os.path.join(PATH_IN, 'derivatives', 'anat', '05_ROI_seg', 'voronoi', ROIS_FILE))
        roi_data = np.asarray(rois_nii.dataobj)

        for it, roi in enumerate(ROI_LABEL):
            if roi == 'V1':
                idx_roi = roi_data == 2      # Find voxels within the ROI
            if roi == 'hMT':
                idx_roi = roi_data == 1

            hor = map[idx_h*idx_roi]
            vert = map[idx_v*idx_roi]

            print('Highest t-value horizotal for {}: {}'.format(roi, np.max(hor)))
            print('Highest t-value vertical for {}: {}'.format(roi, np.min(vert)))

            #//Find 95 percentile from the 2 distributions within the ROI
            horp = np.percentile(hor, 95)
            vertp = np.percentile(np.abs(vert), 95)
            
            vertp = vertp *-1

            idx_h_p = map > horp
            idx_v_p = map < vertp

            #//Mask voxels below percentile threshold within the ROI
            clu = np.zeros(np.shape(map), dtype=np.int8)
            clu[idx_h_p * idx_roi] = 1
            clu[idx_v_p * idx_roi] = 2

            #//Cortical location
            metr_h = metr_data[idx_h_p * idx_roi]
            metr_v = metr_data[idx_v_p * idx_roi]

            print('Number of Horizontal voxels above threshold {}: {}'.format(horp, np.sum(map > horp)))
            print('Number of Vertical voxels above threshold {}: {}'.format(vertp, np.sum(map < vertp)))

            print('Save clusters')
            OUTPUTNAME = os.path.join(PATH_OUT, '{}_phy_maps_wholeBrain_bvbabel_res2x_float32_clusters_{}_{}.nii.gz'.format(su, hem, roi))
            img = nb.Nifti1Image(clu, affine=niimap.affine, header=niimap.header)
            nb.save(img, OUTPUTNAME)

            # # // Plotting here
            fig, axs = plt.subplots(1, 2, sharey=True, tight_layout=True)
            n_bins = 3
            axs[0].hist(metr_h, bins=n_bins)
            axs[1].hist(metr_v, bins=n_bins)

            axs[0].set_ylabel('Horizontal voxels')
            axs[1].set_ylabel('Vertical voxels')

            axs[0].set_xlabel('Cortical depth')
            axs[1].set_xlabel('Cortical depth')

            plt.savefig(os.path.join(PATH_OUT, '{}_Cluster_distributions_{}_{}_cortical_depth.png'.format(su, hem, roi)))

            fig, axs = plt.subplots(1, 2, sharey=True, tight_layout=True)


            axs[0].scatter(metr_data[idx_h_p * idx_roi], map[idx_h_p * idx_roi], c='r')
            axs[1].scatter(metr_data[idx_v_p * idx_roi], map[idx_v_p * idx_roi], c='r')
            axs[0].set_ylabel('Horizontal voxels')
            axs[1].set_ylabel('Vertical voxels')

            axs[0].set_xlabel('Cortical depth')
            axs[1].set_xlabel('Cortical depth')

            # axs[0].scatter(metr_data[idx_h *idx_roi], map[idx_h * idx_roi], c='k')
            # axs[1].scatter(metr_data[idx_v *idx_roi], map[idx_v * idx_roi], c='k')

            plt.savefig(os.path.join(PATH_OUT, '{}_Cluster_scatter_{}_{}_cortical_depth.png'.format(su, hem, roi)))
