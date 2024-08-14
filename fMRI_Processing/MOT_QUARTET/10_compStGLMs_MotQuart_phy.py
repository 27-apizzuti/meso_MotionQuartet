"""
GLM-Axis of Motion Pilot

    Compute GLM in BrainVoyager single run Physical Motion
"""

import os
import glob
print("Hello!")

# =============================================================================

STUDY_PATH = "D:\\Exp-MotionQuartet\\MRI_MQ\\BOLD"
SUBJ = ["sub-04"]
SESS = ["sess-01", "sess-02"]

for si in SUBJ:
    PATH_VMR = os.path.join(STUDY_PATH, si, 'derivatives', 'anat')
    for se in SESS:
        PATH_VTC = os.path.join(STUDY_PATH, si, 'derivatives', 'func', '{}'.format(se), 'MOT_VTC_cut_2x')
        PATH_GLM = os.path.join(STUDY_PATH, si, 'derivatives', 'func', '{}'.format(se), 'MOT_VTC_cut_2x', 'GLM')

        if not os.path.exists(PATH_GLM):
            os.mkdir(PATH_GLM)

        run_vtc = glob.glob(os.path.join(PATH_VTC, '*phy*fix*.vtc'))
        for vtc in run_vtc:
            if si == 'sub-09':
                docVMR = brainvoyager.open(os.path.join(STUDY_PATH, si, "derivatives", "anat", "{}_sess-02_acq-mp2rage_UNI_denoised_IIHC_bvbabel_SSbet_BFC_res2x.vmr".format(si)))
            elif si == 'sub-10':
                docVMR = brainvoyager.open(os.path.join(PATH_VMR, si + '_sess-01_acq-mp2rage_UNI_denoised_bvbabel_SSbet_BFC_res2x.vmr'))
            elif si == 'sub-04':
                docVMR = brainvoyager.open(os.path.join(PATH_VMR, si + '_sess-01_acq-mp2rage_UNI_denoised_IIHC_res2x.vmr'))
            else:
                docVMR = brainvoyager.open(os.path.join(PATH_VMR, si + '_sess-01_acq-mp2rage_UNI_denoised_IIHC_bvbabel_SSbet_BFC_res2x.vmr'))
            print('Linking {}'.format(vtc))
            docVMR.link_vtc(vtc)
            docVTC = brainvoyager.active_document
            nr_volumes = docVTC.n_volumes
            print(nr_volumes)

            if nr_volumes == 308:
                basename = vtc.split(os.extsep, 1)[0]
                filename = basename.split("\\")[-1]

                docVMR.link_protocol(os.path.join(STUDY_PATH, 'Protocol_Exp1_Phys_MotQuart.prt'))
                docVMR.clear_run_designmatrix()

                #// Set predictors
                docVMR.add_predictor("Flicker")
                docVMR.set_predictor_values_from_condition("Flicker", "Flicker", 1)
                docVMR.apply_hrf_to_predictor("Flicker")

                docVMR.add_predictor("Horizontal")
                docVMR.set_predictor_values_from_condition("Horizontal", "Horizontal", 1)
                docVMR.apply_hrf_to_predictor("Horizontal")

                docVMR.add_predictor("Vertical")
                docVMR.set_predictor_values_from_condition("Vertical", "Vertical", 1)
                docVMR.apply_hrf_to_predictor("Vertical")

                #// Save design matrix and run GLM
                print(os.path.join(PATH_GLM, '{}_designMatrix.sdm'.format(filename)))
                docVMR.save_run_designmatrix(os.path.join(PATH_GLM, '{}_designMatrix.sdm'.format(filename)))
                docVMR.serial_correlation_correction_level = 2
                docVMR.compute_run_glm()
                docVMR.show_glm()
                docVMR.save_glm(os.path.join(PATH_GLM, '{}.glm'.format(filename)))

                #// Create contrast map
                docVMR.clear_contrasts()
                docVMR.add_contrast("[Horizontal +1] + [Vertical +1] vs [Flicker -2]")
                docVMR.set_contrast_string("-2 +1 +1")
                docVMR.add_contrast("[Horizontal +1] vs [Vertical +1]")
                docVMR.set_contrast_string("0 +1 -1")
                docVMR.add_contrast("[Horizontal +1] vs [Flicker +1]")
                docVMR.set_contrast_string("-1 +1 0")
                docVMR.add_contrast("[Vertical +1] vs [Flicker +1]")
                docVMR.set_contrast_string("-1 0 1")

                docVMR.show_glm(True)
                docVMR.save_maps(os.path.join(PATH_GLM, '{}.vmp'.format(filename)))

                docVMR.close()
