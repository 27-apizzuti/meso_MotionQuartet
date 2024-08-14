
"""
Created on Tue Apr  5 15:28:35 2022
    Extract five volumes (topup)
@author: apizz

"""

import os
import numpy as np
import nibabel as nb
import subprocess
import glob
import bvbabel
#
# NIIs = ["/mnt/g/Motion_Quartet/sub-01/derivatives/func/sess-03/topup_prf/sub-01_prf_AP_undist.nii.gz",
# "/mnt/g/Motion_Quartet/sub-03/derivatives/func/sess-02/topup_prf/sub-03_prf_AP_undist.nii.gz",
# "/mnt/g/Motion_Quartet/sub-04/derivatives/func/sess-04/topup_prf/sub-04_prf_AP_undist.nii.gz",
# "/mnt/g/Motion_Quartet/sub-05/derivatives/func/sess-02/topup_prf/sub-05_prf_AP_undist.nii.gz",
# "/mnt/g/Motion_Quartet/sub-06/derivatives/func/sess-02/topup_prf/sub-06_prf_AP_undist.nii.gz"]
#
# PATH_OUTs = ["/mnt/g/Motion_Quartet/sub-01/derivatives/func/sess-03/topup_prf/bbr",
# "/mnt/g/Motion_Quartet/sub-03/derivatives/func/sess-02/topup_prf/bbr",
# "/mnt/g/Motion_Quartet/sub-04/derivatives/func/sess-04/topup_prf/bbr",
# "/mnt/g/Motion_Quartet/sub-05/derivatives/func/sess-02/topup_prf/bbr",
# "/mnt/g/Motion_Quartet/sub-06/derivatives/func/sess-02/topup_prf/bbr"]


NIIs = ["/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD/sub-03/derivatives/func/sess-02/topup_prf/sub-03_prf_AP_undist.nii.gz"]

PATH_OUTs = ["/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD/sub-03/derivatives/func/sess-02/topup_prf/bbr"]

for it, file_nii in enumerate(NIIs):
    nii = nb.load(file_nii)
    data = np.asarray(nii.dataobj)

    data2 = np.zeros([np.shape(data)[0], np.shape(data)[1], np.shape(data)[2], 2], dtype=data.dtype)
    data2[..., 0] = data[..., 0]
    data2[..., 1] = data[..., 0]

    path_out = PATH_OUTs[it]
    if not os.path.exists(path_out):
        os.mkdir(path_out)

    basename = file_nii.split(os.extsep, 1)[0]
    outbasename = basename.split("/")[-1]
    print(outbasename)
    outname = os.path.join(path_out, "{}_2vols.nii.gz".format(outbasename))
    img = nb.Nifti1Image(data2, affine=nii.affine, header=nii.header)
    nb.save(img, outname)
