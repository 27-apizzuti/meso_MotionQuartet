import nibabel as nb
import numpy as np
from cni_tlbx import pRF
from scipy.io import loadmat
from scipy.stats import zscore
import bvbabel
import os
import glob

STUDY_PATH = "/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD/"
SUB = ["sub-09"]
SESS = ['sess-02']
PROT_PATH = "/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD/prot_seed_1.mat"

prot = loadmat(PROT_PATH)["prot"]
prot = prot.astype(np.float32) / 255
tr = 1
RUNS = ['AVG']

for it, su in enumerate(SUB):
    PATH_IN = os.path.join(STUDY_PATH, su, "derivatives", "func", SESS[it], 'PRF_VTC_cut_2x')
    PATH_OUT = os.path.join(PATH_IN, 'PRF')
    if not os.path.exists(PATH_OUT):
        os.mkdir(PATH_OUT)

    #1. Load nifti
    for ru in RUNS:
        nifti = glob.glob(os.path.join(PATH_IN, '{}_task-prf_acq-2depimb2_run-{}_SCSTBL_3DMCTS_bvbabel_undist_THPGLMF3c_{}_BBR_res2x.nii'.format(su, ru, SESS[it])))[0]
        nii = nb.load(nifti)
        header = nii.header
        data = np.asarray(nii.dataobj)

        # extra volumes can be discarded
        data = data[..., :prot.shape[-1]]
        data = data.transpose(3, 0, 1, 2)

        #2. Parameter instantiation
        parameters = {"f_sampling": 1 / tr,
                      "h_stimulus": prot.shape[0],
                      "w_stimulus": prot.shape[1],
                      "n_samples": data.shape[0],
                      "n_rows": data.shape[1],
                      "n_cols": data.shape[2],
                      "n_slices": data.shape[3]}
        model = pRF(parameters)

        #3. Generate time course
        model.set_stimulus(prot)
        model.create_timecourses(use_slope=False,
                                 max_radius=5.4,
                                 num_xy=20,
                                 min_sigma=0.1,
                                 max_sigma=2.0,
                                 num_size=20,
                                 sampling="linear")
        #// Change max radious from 5.4 to 10
        #4. Mapping
        results = model.mapping(data, threshold=-np.inf)

        #5. Saving results
        for key, value in results.items():
            outputname = os.path.join(PATH_OUT, '{}_{}_run-{}_radious5.nii.gz'.format(su, key, ru))
            results_nii = nb.Nifti1Image(value, affine=np.eye(4))
            nb.save(results_nii, outputname)
