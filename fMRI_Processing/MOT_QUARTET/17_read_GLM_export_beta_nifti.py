"""Read BrainVoyager GLM and export Nifti."""

import os
import numpy as np
import nibabel as nb
import bvbabel
import pprint
from glob import glob
from scipy import ndimage


SUBJ = ['sub-01', 'sub-03', 'sub-04', 'sub-06', 'sub-07', 'sub-08', 'sub-09', 'sub-10']
STUDY_PATH = "/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD/"
TASK = ['Amb']

for ta in TASK:
    for si in SUBJ:
        print('Working on {} {}'.format(si, ta))
        PATH_VMR = os.path.join(STUDY_PATH, si, 'derivatives', 'anat')
        if si == 'sub-09':
            FILE_VMR = os.path.join(PATH_VMR, "sub-09_sess-02_acq-mp2rage_UNI_denoised_IIHC_bvbabel_SSbet_BFC.vmr")
        elif si == 'sub-10':
            FILE_VMR = os.path.join(PATH_VMR, 'sub-10_sess-01_acq-mp2rage_UNI_denoised_IIHC_bvbabel_SSbet_BFC.vmr')
        elif si == 'sub-04':
            FILE_VMR = os.path.join(PATH_VMR, 'sub-04_sess-01_acq-mp2rage_UNI_denoised_IIHC.vmr')
        else:
            FILE_VMR = os.path.join(PATH_VMR, '{}_sess-01_acq-mp2rage_UNI_denoised_IIHC.vmr'.format(si))

        PATH_GLM = os.path.join(STUDY_PATH, si, 'derivatives', 'func', 'Stats', '{}'.format(ta))
        os.chdir(PATH_GLM)
        print(PATH_GLM)
        FILE =  glob("{}_task-amb_VTC_N-*_FFX_AR-2_4preds_PSC_only.glm".format(si))[0]
        # FILE =  glob("{}_task-{}_VTC_N-*_PSC_AR-2_3pred.glm".format(si, ta))[0]
        print(FILE)
        # =============================================================================
        # Load VMR
        header_vmr, data_vmr = bvbabel.vmr.read_vmr(FILE_VMR)
        dims = np.shape(data_vmr)


        # Load glm
        header, data_R2, data_SS, data_beta, data_fitted, data_arlag = bvbabel.glm.read_glm(FILE)
        new_data = np.zeros((dims[0], dims[1], dims[2], np.shape(data_beta)[-1]), dtype=np.double)
        # See header information
        pprint.pprint(header)

        # -----------------------------------------------------------------------------
        # Export nifti
        basename = FILE.split(os.extsep, 1)[0]

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

        new_data[mXStart:mXEnd, mYStart:mYEnd, mZStart:mZEnd, :] = data_beta

        # // Zoom each beta predictor AMBIGUOUS MOTION : Flicker[1], Nuisance [2], Horizontal[3], Vertical[4]
        if ta == 'Amb':
            dims = np.shape(new_data)
            print('Zoom')
            zoom_data = np.zeros([dims[0]*2, dims[1]*2,dims[2]*2, 3], dtype=np.float32)
            
            # %% Flicker
            temp = new_data[..., 0]
            zoom_data[..., 0] = ndimage.zoom(temp, 2, output=np.float32)
            
            # %% Horizontal
            temp = new_data[..., 2]
            zoom_data[..., 1] = ndimage.zoom(temp, 2, output=np.float32)

            # %% Flicker
            temp = new_data[..., 3]
            zoom_data[..., 2] = ndimage.zoom(temp, 2, output=np.float32)

            # // Save
            print('Save')
            basename = FILE.split(os.extsep, 1)[0]
            outname = "{}_BETAS_PSC_only_4predictors_bvbabel_res2x_float32.nii.gz".format(basename)
            img = nb.Nifti1Image(zoom_data, affine=np.eye(4))
            nb.save(img, outname)

            print("Finished.")
        else:
            # // Zoom each beta predictor PHYSICAL MOTION : Flicker[1], Horizontal[2], Vertical[3]
            dims = np.shape(new_data)
            print('Zoom')
            zoom_data = np.zeros([dims[0]*2, dims[1]*2,dims[2]*2, 3], dtype=np.float32)

            for it in range(0, 3):
                temp = new_data[..., it]
                zoom_data[..., it] = ndimage.zoom(temp, 2, output=np.float32)

            # // Save
            print('Save')
            basename = FILE.split(os.extsep, 1)[0]
            outname = "{}_BETAS_PSC_3predictors_bvbabel_res2x_float32.nii.gz".format(basename)
            img = nb.Nifti1Image(zoom_data, affine=np.eye(4))
            nb.save(img, outname)

            print("Finished.")