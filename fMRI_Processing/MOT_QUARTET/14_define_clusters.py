"""Read BrainVoyager VMP and export nifti."""

import os
import numpy as np
import nibabel as nb
import bvbabel
import pprint
import matplotlib.pyplot as plt

SUBJ = ['sub-01', 'sub-03', 'sub-04', 'sub-06', 'sub-07', 'sub-08', 'sub-09', 'sub-10']

HEMI = ['RH', 'LH']

for su in SUBJ:
    PATH_IN = '/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD/{}/'.format(su)

    # Load t-map from ambiguous motion
    FILENAME = '{}_amb_maps_wholeBrain_TSTATS_bvbabel_res2x_float32.nii.gz'.format(su)
    FILE = os.path.join(PATH_IN, 'derivatives', 'func', 'Stats', 'Amb', FILENAME)

    # Load t-map from physical motion
    # FILENAME = '{}_phy_maps_wholeBrain_TSTATS_bvbabel_res2x_float32.nii.gz'.format(su)
    # FILE = os.path.join(PATH_IN, 'derivatives', 'func', 'Stats', 'Phy', FILENAME)

    niimap = nb.load(FILE)
    map_all = np.asarray(niimap.dataobj)

    # Load ROI definition
    for hem in HEMI:
        ROIS_FILE = '{}_visual_areas_hMT_{}_bvbabel_rim_voronoi_noCapsule.nii.gz'.format(su, hem)
        ROI_LABEL = ['hMT', 'V1']
        rois_nii = nb.load(os.path.join(PATH_IN, 'derivatives', 'anat', '04_ROI_seg', 'voronoi', ROIS_FILE))
        roi_data = np.asarray(rois_nii.dataobj)

        print(np.unique(roi_data))

        #// Separate distributions
        map = map_all[..., 0]
        idx_h = map > 0
        idx_v = map < 0

        for it, roi in enumerate(ROI_LABEL):
            idx_roi = roi_data == (it + 1)      # Find voxelswithin the ROI

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

            print('Number of Horizontal voxels above threshold {}: {}'.format(horp, np.sum(map > horp)))
            print('Number of Vertical voxels above threshold {}: {}'.format(vertp, np.sum(map < vertp)))

            print('Save clusters')
            # OUTPUTNAME = os.path.join(PATH_IN, 'derivatives', 'func', 'Stats', 'Phy', '{}_phy_maps_wholeBrain_bvbabel_res2x_float32_clusters_{}_{}.nii.gz'.format(su, hem, roi))
            OUTPUTNAME = os.path.join(PATH_IN, 'derivatives', 'func', 'Stats', 'Hyph01', '{}_amb_maps_wholeBrain_bvbabel_res2x_float32_clusters_{}_{}.nii.gz'.format(su, hem, roi))
            img = nb.Nifti1Image(clu, affine=niimap.affine, header=niimap.header)
            nb.save(img, OUTPUTNAME)