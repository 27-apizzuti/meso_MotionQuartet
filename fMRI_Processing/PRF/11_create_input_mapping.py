import nibabel as nb
import numpy as np
# from cni_tlbx import pRF
from scipy.io import loadmat
from scipy.stats import zscore
import bvbabel
import os
import glob

#// Load VTC and export NIFTI
STUDY_PATH = "/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD/"
SUB = ["sub-09"]
SESS = ['sess-02']
N_RUNS = 2

for it, su in enumerate(SUB):
    PATH_IN = os.path.join(STUDY_PATH, su, "derivatives", "func", SESS[it], 'PRF_VTC_cut_2x')
    VTCs = glob.glob(os.path.join(PATH_IN, '*res2x.vtc'))
    new_data = []

    for file_vtc in VTCs:
        print('Loading nifti {}'.format(file_vtc))
        header, data = bvbabel.vtc.read_vtc(file_vtc, rearrange_data_axes=False)
        data = np.transpose(data, [0, 2, 1, 3])
        data = data[::-1, ::-1, ::-1]
        # data = zscore(data, axis=-1, ddof=1)
        new_data.append(data)
    new_data_arr = np.asarray(new_data)
    print(np.shape(new_data_arr))
    AVG_PRF = np.mean(new_data_arr, axis=0)
    print(np.shape(AVG_PRF))

    #// Save nifti
    # basename = file_vtc.split(os.extsep, 1)[0]
    outname = os.path.join(PATH_IN, "{}_task-prf_acq-2depimb2_run-AVG_SCSTBL_3DMCTS_bvbabel_undist_THPGLMF3c_{}_BBR_res2x".format(su, SESS[it]))
    img = nb.Nifti1Image(AVG_PRF, affine=np.eye(4))
    nb.save(img, outname)
#
# #// Just save single runs
# for it, su in enumerate(SUB):
#     PATH_IN = os.path.join(STUDY_PATH, su, "derivatives", "func", SESS[it], 'PRF_VTC_cut_2x')
#     VTCs = glob.glob(os.path.join(PATH_IN, '*run-02*res2x.vtc'))
#     new_data = []
#
#     for file_vtc in VTCs:
#         print('Loading nifti {}'.format(file_vtc))
#         header, data = bvbabel.vtc.read_vtc(file_vtc, rearrange_data_axes=False)
#         data = np.transpose(data, [0, 2, 1, 3])
#         data = data[::-1, ::-1, ::-1]
#         # data = zscore(data, axis=-1, ddof=1)
#         new_data.append(data)
    #
    #
    # #// Save nifti
    # basename = file_vtc.split(os.extsep, 1)[0]
    # outname = os.path.join(PATH_IN, "{}_task-prf_acq-2depimb2_run-02_SCSTBL_3DMCTS_bvbabel_undist_THPGLMF3c_{}_BBR_res2x".format(su, SESS[it]))
    # img = nb.Nifti1Image(data, affine=np.eye(4))
    # nb.save(img, outname)
