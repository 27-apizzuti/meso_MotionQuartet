"""Read BrainVoyager vmr and export nifti.
VMP --> first map: horizontal > vertical. 
In BrainVoyager it overlays on VMR x2 but the map itseflf is a 0.7, that's why we load 0.7 VMR. Therefore, we upsample and convert to nifti"""

import os
import numpy as np
import nibabel as nb
import bvbabel
import pprint
from scipy import ndimage

STUDY_PATH = "D:\\Exp-MotionQuartet\\MRI_MQ\\BOLD"
SUB = ["sub-01", "sub-03", "sub-04", "sub-06", "sub-07", "sub-08", "sub-09", "sub-10"]
TASK = ['Phy', 'Amb']
# =============================================================================

for su in SUB:
    PATH_VMR = os.path.join(STUDY_PATH, su, 'derivatives', 'anat')

    if su == 'sub-09':
        FILE_VMR = os.path.join(PATH_VMR, "sub-09_sess-02_acq-mp2rage_UNI_denoised_IIHC_bvbabel_SSbet_BFC.vmr")
    elif su == 'sub-10':
        FILE_VMR = os.path.join(PATH_VMR, 'sub-10_sess-01_acq-mp2rage_UNI_denoised_IIHC_bvbabel_SSbet_BFC.vmr')
    elif su == 'sub-04':
        FILE_VMR = os.path.join(PATH_VMR, 'sub-04_sess-01_acq-mp2rage_UNI_denoised_IIHC.vmr')
    else:
        FILE_VMR = os.path.join(PATH_VMR, '{}_sess-01_acq-mp2rage_UNI_denoised_IIHC.vmr'.format(su))

    for tas in TASK:
        if tas == 'Amb':
            FILE = os.path.join(STUDY_PATH, su, 'derivatives', 'func', 'Stats', 'Amb', '{}_amb_maps_wholeBrain.vmp'.format(su))
        else:
            FILE = os.path.join(STUDY_PATH, su, 'derivatives', 'func', 'Stats', 'Phy', '{}_phy_maps_wholeBrain.vmp'.format(su))

        #// Load VMR
        header_vmr, data_vmr = bvbabel.vmr.read_vmr(FILE_VMR)
        dims = np.shape(data_vmr)
        print(dims)

        # Load VMP
        print('Working on {}'.format(FILE))
        header, data = bvbabel.vmp.read_vmp(FILE)
        n_map = np.shape(data)[-1]
        new_data = np.zeros((dims[0], dims[1], dims[2], n_map), dtype=np.double)

        #// See header information
        pprint.pprint(header)

        #// Adjusting axes according to BV convention
        header["XEnd"] = int(header["XEnd"] / 2)
        header["XStart"] = int(header["XStart"] / 2)

        header["YEnd"] = int(header["YEnd"]/ 2)
        header["YStart"] = int(header["YStart"] / 2)

        header["ZEnd"] = int(header["ZEnd"] / 2)
        header["ZStart"] = int(header["ZStart"] / 2)

        # // Add data
        mXStart = dims[0] -header["ZEnd"]-1
        mXEnd = dims[0] -header["ZStart"]-1

        mYStart = dims[1] -header["XEnd"]-1
        mYEnd = dims[1] -header["XStart"]-1

        mZStart = dims[2] -header["YEnd"]-1
        mZEnd = dims[2] -header["YStart"]-1

        new_data[mXStart:mXEnd, mYStart:mYEnd, mZStart:mZEnd, :] = data

        basename = FILE.split(os.extsep, 1)[0]
        outname = "{}_bvbabel.nii.gz".format(basename)
        img = nb.Nifti1Image(new_data, affine=np.eye(4))
        nb.save(img, outname)
        #
        # # # // Zoom
        # zoom_data = np.zeros([dims[0]*2, dims[1]*2,dims[2]*2, 3], dtype=np.float32)
        # for it in range(0, 3):
        #     temp = new_data[..., it]
        #     zoom_data[..., it] = ndimage.zoom(temp, 2, output=np.float32)

        # basename = FILE.split(os.extsep, 1)[0]
        # outname = "{}_bvbabel_res2x_float32.nii.gz".format(basename)
        # img = nb.Nifti1Image(zoom_data, affine=np.eye(4))
        # nb.save(img, outname)

print("Finished.")
