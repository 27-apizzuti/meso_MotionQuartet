"""
GLM-Axis of Motion Pilot

    Compute GLM in BrainVoyager single run Ambiguous Motion
"""

import os
import glob
print("Hello!")

# =============================================================================

STUDY_PATH = "D:\\Exp-MotionQuartet\\MRI_MQ\\BOLD"
#STUDY_PATH = "/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD"
SUBJ = ['sub-06']
SESS = ['sess-02']

for si in SUBJ:
    PATH_VMR = os.path.join(STUDY_PATH, si, 'derivatives', 'anat')

    for se in SESS:
        PATH_VTC = os.path.join(STUDY_PATH, si, 'derivatives', 'func', '{}'.format(se), 'MOT_VTC_cut_2x')
        PATH_GLM = os.path.join(STUDY_PATH, si, 'derivatives', 'func', '{}'.format(se), 'MOT_VTC_cut_2x', 'GLM-fix')
        print(PATH_VTC)
        if not os.path.exists(PATH_GLM):
            os.mkdir(PATH_GLM)

        run_vtc = glob.glob(os.path.join(PATH_VTC, '*amb_*fix*.vtc'))

        #// Find run number
        for vtc in run_vtc:
            temp = vtc.split('\\')[-1]
            file = temp.split('_')[3]
            runid = file.split('-')[-1]
            print(runid)

            if si == 'sub-09':
                docVMR = brainvoyager.open(os.path.join(STUDY_PATH, si, "derivatives", "anat", "{}_sess-02_acq-mp2rage_UNI_denoised_IIHC_bvbabel_SSbet_BFC_res2x.vmr".format(si)))
            elif si == 'sub-10':
                docVMR = brainvoyager.open(os.path.join(PATH_VMR, si + '_sess-01_acq-mp2rage_UNI_denoised_bvbabel_SSbet_BFC_res2x.vmr'))
            elif si == 'sub-04':
                docVMR = brainvoyager.open(os.path.join(PATH_VMR, si + '_sess-01_acq-mp2rage_UNI_denoised_IIHC_res2x.vmr'))
            elif si == 'sub-01':
                docVMR = brainvoyager.open(os.path.join(PATH_VMR, si + '_sess-01_acq-mp2rage_UNI_denoised_IIHC_res2x.vmr'))
            elif si == 'sub-03':
                docVMR = brainvoyager.open(os.path.join(PATH_VMR, si + '_sess-01_acq-mp2rage_UNI_denoised_IIHC_res2x.vmr'))
            elif si == 'sub-06':
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

                docVMR.link_protocol(os.path.join(STUDY_PATH, si, 'Protocols', se, 'Exp1_Amb_MotQuart', 'Protocols', 'Protocol_{}_Protocols_{}_Run{}.prt'.format(si, se, runid)))
                print(os.path.join(STUDY_PATH, si, 'Protocols', se, 'Exp1_Amb_MotQuart', 'Protocol_{}_Protocols_{}_Run{}.prt'.format(si, se, runid)))
                docVMR.clear_run_designmatrix()

                #// Set predictors
                docVMR.add_predictor("Baseline")
                docVMR.set_predictor_values_from_condition("Baseline", "Baseline", 1)
                docVMR.apply_hrf_to_predictor("Baseline")
                
                docVMR.add_predictor("Nuisance")
                docVMR.set_predictor_values_from_condition("Nuisance", "Nuisance", 1)
                docVMR.apply_hrf_to_predictor("Nuisance")

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
                docVMR.add_contrast("[Horizontal +1] + [Vertical +1] vs [Baseline -2]")
                docVMR.set_contrast_string("-2 +1 +1")
                docVMR.add_contrast("[Horizontal +1] vs [Vertical +1]")
                docVMR.set_contrast_string("0 +1 -1")
                docVMR.add_contrast("[Horizontal +1] vs [Baseline +1]")
                docVMR.set_contrast_string("-1 +1 0")
                docVMR.add_contrast("[Vertical +1] vs [Baseline +1]")
                docVMR.set_contrast_string("-1 0 1")

                docVMR.show_glm(True)
                docVMR.save_maps(os.path.join(PATH_GLM, '{}.vmp'.format(filename)))

                docVMR.close()
