"""
GLM-hMT Localizer in BrainVoyager

"""
import os
print("Hello!")

STUDY_PATH = "D:\\Exp-MotionQuartet\\MRI_MQ\\BOLD"
SUBJ = ['sub-09']

for si in SUBJ:
    PATH_VMR = os.path.join(STUDY_PATH, si, 'derivatives', 'anat')
    PATH_VTC = os.path.join(STUDY_PATH, si, 'derivatives', 'func', 'sess-01', 'loc01', 'GLM')

    if si == 'sub-09':
        docVMR = brainvoyager.open(os.path.join(PATH_VMR, si + '_sess-02_acq-mp2rage_UNI_denoised_IIHC_bvbabel_SSbet_BFC_res2x.vmr'))
    elif si == 'sub-10':
        docVMR = brainvoyager.open(os.path.join(PATH_VMR, si + '_sess-01_acq-mp2rage_UNI_denoised_bvbabel_SSbet_BFC_res2x.vmr'))
    else:
        docVMR = brainvoyager.open(os.path.join(PATH_VMR, si + '_sess-01_acq-mp2rage_UNI_denoised_IIHC_bvbabel_SSbet_BFC_res2x.vmr'))

    vtc_filename = '{}_task-loc_acq-2depimb2_run-01_SCSTBL_3DMCTS_bvbabel_warped_THPGLMF3c_res2x.vtc'.format(si)

    docVMR.link_vtc(os.path.join(PATH_VTC, vtc_filename))
    docVMR.link_protocol(os.path.join(STUDY_PATH, si, 'Protocols', 'sess-01', 'Localizer', 'Protocol_{}_Localizer_Run01.prt'.format(si)))
    docVMR.clear_run_designmatrix()

    #// Set predictors
    if si == 'sub-01':
        docVMR.add_predictor("Flicker")
        docVMR.set_predictor_values_from_condition("Flicker", "Flicker", 1)
        docVMR.apply_hrf_to_predictor("Flicker")

        docVMR.add_predictor("Horizontal")
        docVMR.set_predictor_values_from_condition("Horizontal", "Horizontal", 1)
        docVMR.apply_hrf_to_predictor("Horizontal")

        docVMR.add_predictor("Vertical")
        docVMR.set_predictor_values_from_condition("Vertical", "Vertical", 1)
        docVMR.apply_hrf_to_predictor("Vertical")

        docVMR.add_predictor("Diag45")
        docVMR.set_predictor_values_from_condition("Diag45", "Diag45", 1)
        docVMR.apply_hrf_to_predictor("Diag45")

        docVMR.add_predictor("Diag135")
        docVMR.set_predictor_values_from_condition("Diag135", "Diag135", 1)
        docVMR.apply_hrf_to_predictor("Diag135")

    else:

        docVMR.add_predictor("Center")
        docVMR.set_predictor_values_from_condition("Center", "Center", 1)
        docVMR.apply_hrf_to_predictor("Center")

    #// Save design matrix and run GLM
    docVMR.save_run_designmatrix(os.path.join(PATH_VTC, 'designMatrix_loc.sdm'))
    docVMR.serial_correlation_correction_level = 2
    docVMR.compute_run_glm()
    docVMR.show_glm()
    docVMR.save_glm(os.path.join(PATH_VTC, si + '_loc.glm'))

    #// Create contrast map
    docVMR.clear_contrasts()

    if si == 'sub-01':
        docVMR.add_contrast("[Horizontal +1] + [Vertical +1] + [Diag45 +1] + [Diag135 +1] vs [Flicker -4]")
        docVMR.set_contrast_string("-4 +1 +1 +1 +1")
    else:
        docVMR.add_contrast("[Center +1]")
        docVMR.set_contrast_string("+1")

    docVMR.show_glm(True)
    docVMR.save_maps(os.path.join(PATH_VTC, si + '_loc.vmp'))

    docVMR.close()
