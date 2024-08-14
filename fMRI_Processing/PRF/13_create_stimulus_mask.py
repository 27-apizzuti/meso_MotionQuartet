import nibabel as nb
import numpy as np
import bvbabel
import os
import glob
from pprint import pprint
from copy import copy
from scipy import ndimage


STUDY_PATH = "/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD/"
SUB = ['sub-03', 'sub-06']
SESS = ['sess-02']
VMP_TEMPLATE = "/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD/pRF_mapping_template.vmp"
MAPS = ['corr_fit', 'mu_x', 'mu_y', 'sigma', 'eccentricity', 'polar_angle']
VMR_dims = [int(240), int(320), int(320)]
RUNS = ['AVG']

for su in SUB:
    for run in RUNS:
        print('Create stimulus PRF decoding for {}'.format(su))
        # // Load VTC
        VTC = os.path.join(STUDY_PATH, su, "derivatives", "func", SESS[0], 'PRF_VTC_cut_2x', '{}_task-prf_acq-2depimb2_run-01_SCSTBL_3DMCTS_bvbabel_undist_THPGLMF3c_{}_BBR_res2x.vtc'.format(su, SESS[0]))
        header_vtc, data_vtc = bvbabel.vtc.read_vtc(VTC, rearrange_data_axes=True)
        VTC_dims = np.shape(data_vtc)
        # // Load VMR VMP_TEMPLATE
        header, data = bvbabel.vmp.read_vmp(VMP_TEMPLATE)
        new_header = copy(header)
        # Adapting header VMP
        new_header['DimX'] = VMR_dims[0]
        new_header['DimY'] = VMR_dims[1]
        new_header['DimZ'] = VMR_dims[2]

        new_header['Resolution'] = 2
        new_header['XStart'] = header_vtc['XStart']
        new_header['YStart'] = header_vtc['YStart']
        new_header['ZStart'] = header_vtc['ZStart']

        new_header['XEnd'] = header_vtc['XEnd']
        new_header['YEnd'] = header_vtc['YEnd']
        new_header['ZEnd'] = header_vtc['ZEnd']

        # Initialize VMP data
        new_data = np.zeros([VTC_dims[0], VTC_dims[1], VTC_dims[2], 6])

        #// Load mu_x and mu_y
        nii_x = nb.load(os.path.join(STUDY_PATH, su, "derivatives", "func", SESS[0], 'PRF_VTC_cut_2x', 'PRF', '{}_mu_x_run-{}.nii.gz'.format(su, run)))
        mu_x =  np.asarray(nii_x.dataobj)
        nii_y = nb.load(os.path.join(STUDY_PATH, su, "derivatives", "func", SESS[0], 'PRF_VTC_cut_2x', 'PRF', '{}_mu_y_run-{}.nii.gz'.format(su, run)))
        mu_y =  np.asarray(nii_y.dataobj)

        #// New nifti
        dims = np.shape(mu_x)
        new_data_nii = np.zeros([dims[0], dims[1], dims[2], 3], dtype=np.int8)
        # Inducers ranges: x: abs[(2.5-3.5)] & y: abs[(3.3-4.4)]
        idx_ind = (2.5 < np.abs(mu_x)) & (np.abs(mu_x) < 3.5) & (3.3 < np.abs(mu_y)) & (np.abs(mu_y) < 4.3)

        # Perceptual horizontal path: x: (-2.5 to 2.5) & y: abs[(3.3-4.8)]
        idx_hor = (np.abs(mu_x) < 2.5) & (3.3 < np.abs(mu_y)) & (np.abs(mu_y) < 4.3)
        # Perceptual vertical path: x: abs[(2.5-3.5)] & y: (-3.3 to 3.3)
        idx_ver = (2.5 < np.abs(mu_x)) & (np.abs(mu_x) < 3.5) & (np.abs(mu_y) < 3.3)

        print(np.sum(np.sum(idx_ind * idx_hor)))
        print(np.sum(np.sum(idx_ind * idx_ver)))
        print(np.sum(np.sum(idx_ver * idx_hor)))
        #// Load 'R' and 'eccentricity' and 'polar angle'
        nii_R = nb.load(os.path.join(STUDY_PATH, su, "derivatives", "func", SESS[0], 'PRF_VTC_cut_2x', 'PRF', '{}_corr_fit_run-{}.nii.gz'.format(su, run)))
        r = np.asarray(nii_R.dataobj)
        nii_ecc = nb.load(os.path.join(STUDY_PATH, su, "derivatives", "func", SESS[0], 'PRF_VTC_cut_2x', 'PRF', '{}_eccentricity_run-{}.nii.gz'.format(su, run)))
        ecc = np.asarray(nii_ecc.dataobj)
        nii_pa = nb.load(os.path.join(STUDY_PATH, su, "derivatives", "func", SESS[0], 'PRF_VTC_cut_2x', 'PRF', '{}_polar_angle_run-{}.nii.gz'.format(su, run)))
        pa = np.asarray(nii_pa.dataobj)

        new_data[..., 0] = r

        new_data[idx_ind, 1] = 1
        new_data[idx_hor, 2] = 2
        new_data[idx_ver, 3] = 3
        new_data[..., 4] = ecc
        new_data[..., 5] = pa

        new_header['Map'][1]['MapName'] = 'Inducers'
        new_header['Map'][1]['LUTFileName'] = 'ProbMap_Red.olt'
        new_header['Map'][2]['MapName'] = 'Horizontal'
        new_header['Map'][2]['LUTFileName'] = 'ProbMap_Cyan.olt'
        new_header['Map'][3]['MapName'] = 'Vertical'
        new_header['Map'][2]['LUTFileName'] = 'ProbMap_Green.olt'

        new_header['Map'][4]['UpperThreshold'] = 8.4

        #// Save VMP
        # print(np.shape(new_data))
        pprint(new_header)
        OUTNAME = os.path.join(STUDY_PATH, su, "derivatives", "func", SESS[0], 'PRF_VTC_cut_2x', 'PRF', '{}_prf_mapping_run-{}_radious5_STIMULUS.vmp'.format(su, run))
        print(OUTNAME)
        bvbabel.vmp.write_vmp(OUTNAME, new_header, new_data)
    #
