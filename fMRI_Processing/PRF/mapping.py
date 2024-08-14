import nibabel as nib
import numpy as np
from cni_tlbx import pRF
from scipy.io import loadmat
from scipy.stats import zscore


def map_prfs(prot, data, mask, tr):
    parameters = {"f_sampling": 1 / tr,
                  "h_stimulus": prot.shape[0],
                  "w_stimulus": prot.shape[1],
                  "n_samples": data.shape[0],
                  "n_rows": data.shape[1],
                  "n_cols": data.shape[2],
                  "n_slices": data.shape[3]}

    model = pRF(parameters)
    model.set_stimulus(prot)

    model.create_timecourses(use_slope=False,
                             max_radius=5.4,
                             num_xy=20,
                             min_sigma=0.1,
                             max_sigma=2.0,
                             num_size=20,
                             sampling="linear")

    results = model.mapping(data, threshold=-np.inf, mask=mask)
    # dict: corr_fit, mu_x, mu_y, sigma, eccentricity, polar_angle

    # ranges: corr_fit [0, 1], mu_xy [-5.4°, 5.4°], sigma [min°, max°],
    #         eccentricity [0.0°, 7.6°], polar_angle [-pi, pi]

    # polar_angle: right horizontal meridian = 0.0
    #              left horizontal meridian = +-pi
    #              lower vertical meridian = -pi/2
    #              upper vertical meridian = +pi/2


def main():
    base_path = "/media/alex/Data/saliency_fmri/new/"

    prot_path = base_path + "scripts/experiment/main/sub-01/protocols/09CB.mat"
    data_path = base_path + "main/bids/derivatives/fmriprep/sub-01/func/sub-01_task-09CB_acq-EP3D_dir-AP_run-9_space-T1w_desc-preproc_bold_clean.nii.gz"
    mask_path = base_path + "main/bids/derivatives/fmriprep/sub-01/func/sub-01_task-09CB_acq-EP3D_dir-AP_run-9_space-T1w_desc-brain_mask.nii.gz"

    # 10 TRs of rest at start and end
    prot = loadmat(prot_path)["prot"]
    prot = prot.astype(np.float32) / 255
    # shape: (height, width, volumes)

    data_nii = nib.load(data_path)
    data = data_nii.get_fdata()
    data = data.astype(np.float32)

    # extra volumes can be discarded
    data = data[..., :prot.shape[-1]]

    data = data.transpose(3, 0, 1, 2)
    data = zscore(data, axis=0, ddof=1)
    # shape: (volumes, rows, cols, slices)

    mask_nii = nib.load(mask_path)
    mask = mask_nii.get_fdata()
    mask = mask.astype(bool)
    # shape: (rows, cols, slices)

    map_prfs(prot, data, mask, tr=2.879924)


if __name__ == "__main__":
    main()
