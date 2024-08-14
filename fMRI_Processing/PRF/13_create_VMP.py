import nibabel as nb
import numpy as np
import bvbabel
import os
import glob
from pprint import pprint
from copy import copy

STUDY_PATH = "/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD/"
SUB = ["sub-09"]
SESS = ['sess-02']
VMP_TEMPLATE = "/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD/pRF_mapping_template.vmp"
MAPS = ['corr_fit', 'mu_x', 'mu_y', 'sigma', 'eccentricity', 'polar_angle']
VMR_dims = [int(240), int(320), int(320)]
RUNS = ['AVG']
for su in SUB:
    for run in RUNS:
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

        for it, map in enumerate(MAPS):
            # Load nifti map
            NII_FILE = os.path.join(STUDY_PATH, su, "derivatives", "func", SESS[0], 'PRF_VTC_cut_2x', 'PRF', '{}_{}_run-{}_radious5.nii.gz'.format(su, map, run))
            nii = nb.load(NII_FILE)
            niidata = np.asarray(nii.dataobj)
            new_data[..., it] = niidata
        new_header['Map'][1]['UpperThreshold'] = 5.4
        new_header['Map'][2]['UpperThreshold'] = 5.4
        new_header['Map'][3]['UpperThreshold'] = 2
        new_header['Map'][4]['UpperThreshold'] = 5.4
        # print(data)
        # print(new_data)
        # print(np.shape(new_data))
        # print(np.shape(data_vtc))


        #// Save VMP
        # print(np.shape(new_data))
        pprint(new_header)
        OUTNAME = os.path.join(STUDY_PATH, su, "derivatives", "func", SESS[0], 'PRF_VTC_cut_2x', 'PRF', '{}_prf_mapping_run-{}_radious5.vmp'.format(su, run))
        print(OUTNAME)
        bvbabel.vmp.write_vmp(OUTNAME, new_header, new_data)
