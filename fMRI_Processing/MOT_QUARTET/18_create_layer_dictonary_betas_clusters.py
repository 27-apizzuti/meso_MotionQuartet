"""Create dictionary to store data for plotting layer profiles"""

import os
import numpy as np
import nibabel as nb
import bvbabel
import pprint
from glob import glob

SUB = ['sub-01', 'sub-03', 'sub-04', 'sub-06', 'sub-07', 'sub-08', 'sub-09', 'sub-10']
HEMI = ['LH', 'RH']
CONDITION = ['Phy', 'Amb']
ROI = ['hMT', 'V1']
# ------------------------------------------------------------------------------
for su in SUB:
    PATH_IN = 'D:\\Exp-MotionQuartet\\MRI_MQ\\BOLD\\{}\\'.format(su)
    PATH_OUT =  os.path.join(PATH_IN, 'derivatives', 'func', 'Stats', 'Betas_Layers')
    if not os.path.exists(PATH_OUT):
        os.mkdir(PATH_OUT)

    for hem in HEMI:
        for ro in ROI:
            for co in CONDITION:

                # // Load PSC
                # Load betas
                PATH_GLM = os.path.join(PATH_IN, 'derivatives', 'func', 'Stats', '{}'.format(co))
                os.chdir(PATH_GLM)

                FILE =  glob('{}_task-*_VTC_N-*_BETAS_PSC_bvbabel_res2x_float32.nii.gz'.format(su))[0]
                niimap = nb.load(os.path.join(PATH_GLM, FILE))
                betas_all = np.asarray(niimap.dataobj)

                betas_fli = betas_all[..., 0]
                betas_hor = betas_all[..., 1]
                betas_ver = betas_all[..., 2]

                #// Load cluster mask
                FILENAME = '{}_phy_maps_wholeBrain_bvbabel_res2x_float32_clusters_{}_{}_UVD_max_filter.nii.gz'.format(su, hem, ro)
                mask_nii = nb.load(os.path.join(PATH_IN, 'derivatives', 'func', 'Stats', 'Hyph01', FILENAME))
                mas = np.asarray(mask_nii.dataobj)
                idx = mas > 0
                idx_hor = (mas == 1)
                idx_ver = (mas == 2)

                #// Load metric file
                PATH1 = os.path.join(PATH_IN, 'derivatives', 'anat', '06_CorticalLayers')
                os.chdir(PATH1)
                myfile = glob('*metric_equivol*')[0]
                metr_nii = nb.load(os.path.join(PATH1, '{}'.format(myfile)))
                metr = np.asarray(metr_nii.dataobj)

                #// Initiate dictionary
                print('Preparing dictionary for: {} {} {} condition'.format(su, hem, co))
                subj_dict = {"Flicker":{}, "Horizontal":{}, "Vertical":{}}

                #// Fill in
                subj_dict["Flicker"]["Metric"] = metr[idx]
                subj_dict["Flicker"]["betas"] = betas_fli[idx]

                subj_dict["Horizontal"]["Metric"] = metr[idx_hor]
                subj_dict["Horizontal"]["betas"] = betas_hor[idx_hor]

                subj_dict["Vertical"]["Metric"] = metr[idx_ver]
                subj_dict["Vertical"]["betas"] = betas_ver[idx_ver]

                np.save(os.path.join(PATH_OUT, "{}_depth_vs_{}_{}_{}_clusters_BETAS_PSC.npy".format(su, co, hem, ro)), subj_dict)
