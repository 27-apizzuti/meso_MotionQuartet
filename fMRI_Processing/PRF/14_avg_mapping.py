import nibabel as nb
import numpy as np
from cni_tlbx import pRF
from scipy.io import loadmat
from scipy.stats import zscore
import bvbabel
import os
import glob

#// Load VTC and export NIFTI
STUDY_PATH = "/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD/"
SUB = ['sub-03']
SESS = ['sess-02']
MAPS = ['corr_fit', 'mu_x', 'mu_y', 'sigma', 'eccentricity', 'polar_angle']

for it, su in enumerate(SUB):
    PATH_IN = os.path.join(STUDY_PATH, su, "derivatives", "func", SESS[it], 'PRF_VTC_cut_2x', 'PRF')

    for map in MAPS:
        print('Loading nifti {}'.format(map))
        NII_FILE = os.path.join(STUDY_PATH, su, "derivatives", "func", SESS[0], 'PRF_VTC_cut_2x', 'PRF', '{}_{}_run-AVG.nii.gz'.format(su, map))
        nii = nb.load(NII_FILE)
        niidata1 = np.asarray(nii.dataobj)
        AVG_PRF = niidata1

        # NII_FILE = os.path.join(STUDY_PATH, su, "derivatives", "func", SESS[0], 'PRF_VTC_cut_2x', 'PRF', 'sub-01_{}_run-02.nii.gz'.format(map))
        # nii = nb.load(NII_FILE)
        # niidata2 = np.asarray(nii.dataobj)
        # AVG_PRF = (niidata1 + niidata2) / 2

        #// Save nifti
        outname = os.path.join(STUDY_PATH, su, "derivatives", "func", SESS[0], 'PRF_VTC_cut_2x', 'PRF', '{}_{}_run-AVG.nii.gz'.format(su, map))
        img = nb.Nifti1Image(AVG_PRF, affine=np.eye(4))
        nb.save(img, outname)
