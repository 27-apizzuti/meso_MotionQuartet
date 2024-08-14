"""Read BrainVoyager FMR file format and save first volume for each run.
   Check motion correction"""

import os
import numpy as np
import nibabel as nb
import bvbabel
import glob
import matplotlib.pyplot as plt
from pprint import pprint
# =============================================================================
STUDY_PATH = "/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD"
SUBJ = ["sub-09"]
SESS = [2]
TASK = ["prf01"]

for su in SUBJ:
    PATH_FMR = os.path.join(STUDY_PATH, su, 'derivatives', 'func')

    for se in SESS:
        # path_in = os.path.join(PATH_FMR, 'sess-0{}'.format(se))
        # path_run = os.path.join(path_in, 'prf01', 'topup_prf')
        # nii = nb.load(os.path.join(path_run, 'sub-09_task-prf_acq-2depimb2_run-01_SCSTBL_3DMCTS_bvbabel_undist.nii.gz'))
        # data = np.asarray(nii.dataobj)
        #
        # print('Save reference nifti')
        # outname1 = os.path.join(path_run, 'sub-09_task-prf_acq-2depimb2_run-01_SCSTBL_3DMCTS_bvbabel_undist_reference_bvbabel.nii.gz')
        # data = data[..., 0:1]
        # img = nb.Nifti1Image(data, affine=nii.affine, header=nii.header)
        # nb.save(img, outname1)

        path_in = os.path.join(PATH_FMR, 'sess-0{}'.format(se))
        path_run = os.path.join(path_in, 'prf01', '01_ANTS')
        nii = nb.load(os.path.join(path_run, 'sub-09_prf_run-01_first_vol_manual_aligned.nii.gz'))
        data = np.asarray(nii.dataobj)

        new_data = np.zeros([np.shape(data)[0], np.shape(data)[1],np.shape(data)[2],2])
        outname1 = os.path.join(path_run, 'sub-09_prf_run-01_first_vol_manual_aligned_test_2vols.nii.gz')
        print(outname1)
        new_data[..., 0] = data
        new_data[..., 1] = data
        print(np.shape(new_data))
        img = nb.Nifti1Image(new_data, affine=nii.affine, header=nii.header)
        nb.save(img, outname1)


        # nifti_file = "/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD/{}/sourcedata/sess-01/NIFTI/func/{}_sess-01_task-loc_acq-2depimb3_run-01.nii".format(su, su)
        # nii = nb.load(nifti_file) # // We take the header from here
        #
        # for tas in TASK:
        #     runs = glob.glob("{}/{}*/".format(path_in, tas), recursive=True)
        #     for path_run in runs:
        #         print(path_run)
        #         temp = path_run.split("/")[-2]
        #
        #         # FMR = glob.glob(os.path.join(path_run, '*01.fmr'))[0]
        #         FMR = glob.glob(os.path.join(path_run, '{}*_run-01_SCSTBL_3DMCTS.fmr'.format(su)))[0]
        #         basename = FMR.split(os.extsep, 1)[0]
        #         filename = basename.split("/")[-1]
        #         outname1 = "{}_reference_bvbabel.nii.gz".format(basename)
        #         outname2 = os.path.join(path_run, "{}_bvbabel_test.nii.gz".format(filename))
        #
        #         # Load FMR
        #         print('Read {}'.format(FMR))
        #         header, datafmr = bvbabel.fmr.read_fmr(FMR, rearrange_data_axes=False)
        #         pprint(header)
        #         nslices = header['NrOfSlices']
        #         nvol = header['NrOfVolumes']
        #         resY = header['ResolutionY']
        #         resX = header['ResolutionX']
        #         datafmr = np.transpose(datafmr, (3, 2, 0, 1))
        #         datafmr=datafmr[:,::-1,:,:]
        #         # datafmr=datafmr[:,:,:,:]

                #// Save first volume as NIFTI
                # print('Save reference nifti')
                # datafmr1 = datafmr[..., 0:1]
                # img = nb.Nifti1Image(datafmr1, affine=nii.affine, header=nii.header)
                # nb.save(img, outname1)

                #// Save all time course for topup
                # print('Save time course nifti')
                # img = nb.Nifti1Image(datafmr, affine=nii.affine, header=nii.header)
                # nb.save(img, outname2)


print("Finished.")
