# This script upsample to 0.35 iso mm the anatomical VMR and v16 file

import numpy as np
import os
from scipy import ndimage
import bvbabel
from pprint import pprint
import nibabel as nb
print("Hello.")

# =============================================================================
STUDY_PATH = "/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD"
SUBJ = [ "sub-07"]
SESS = ["sess-01"]

for su in SUBJ:
    for se in SESS:
        print('Working on {}, {}'.format(su, se))

        #// Open VMR
        file_vmr = os.path.join(STUDY_PATH, su, "derivatives", "anat", "{}_sess-01_acq-mp2rage_UNI_denoised_IIHC_bvbabel_SSbet_BFC.vmr".format(su))
        # file_v16 = os.path.join(STUDY_PATH, su, "derivatives", "anat", "{}_sess-01_acq-mp2rage_UNI_denoised_IIHC.v16".format(su))


        # // Make the VMR double resolution (0.35 iso mm)
        header, data = bvbabel.vmr.read_vmr(file_vmr)
        result = ndimage.zoom(data, 2)

        header['DimX'] = header['DimX']*2
        header['DimY'] = header['DimY']*2
        header['DimZ'] = header['DimZ']*2
        header['VoxelSizeX'] = header['VoxelSizeX'] / 2
        header['VoxelSizeY'] = header['VoxelSizeY'] / 2
        header['VoxelSizeZ'] = header['VoxelSizeZ'] / 2

        FILE_OUT = os.path.join(STUDY_PATH, su, "derivatives", "anat", "{}_sess-01_acq-mp2rage_UNI_denoised_IIHC_bvbabel_SSbet_BFC_res2x.vmr".format(su))
        bvbabel.vmr.write_vmr(FILE_OUT, header, result)

        # #// Open v16 and make double resolution
        # FILE_OUT = os.path.join(STUDY_PATH, su, "derivatives", "anat", "{}_sess-01_acq-mp2rage_inv2_res2x.v16".format(su))
        # header, data = bvbabel.v16.read_v16(file_v16)

        # result = ndimage.zoom(data, 2)
        # header['DimX'] = header['DimX']*2
        # header['DimY'] = header['DimY']*2
        # header['DimZ'] = header['DimZ']*2
        # bvbabel.v16.write_v16(FILE_OUT, header, result)
        #

#
# FILENAME = "/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD/sub-06/derivatives/anat/01_SubcorticalMask/sub-06_sess-01_acq-mp2rage_UNI_denoised_IIHC_bvbabel_SS_BFC_Nocereb.nii.gz"
# nii =  nb.load(FILENAME)
# data = np.asarray(nii.dataobj)
# result = ndimage.zoom(data, 2, dtype=np.float32)
# outname = "/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD/sub-06/derivatives/anat/01_SubcorticalMask/sub-06_sess-01_acq-mp2rage_UNI_denoised_IIHC_bvbabel_SS_BFC_Nocereb_res2x.nii.gz"
# img = nb.Nifti1Image(result, affine=np.eye(4))
# nb.save(img, outname)
