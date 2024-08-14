"""
GLM-Axis of Motion Pilot

    Compute GLM in BrainVoyager single run Physical Motion
"""

import os
import glob
print("Hello!")

# =============================================================================

STUDY_PATH = "D:\\Exp-MotionQuartet\\MRI_MQ\\BOLD"
SUBJ = ['sub-01', 'sub-03', 'sub-04', 'sub-06', 'sub-07', 'sub-08', 'sub-09','sub-10']
SESS = ['sess-01', 'sess-02']

for si in SUBJ:
    PATH_VMR = os.path.join(STUDY_PATH, si, 'derivatives', 'anat')
    if si == 'sub-01':
        docVMR = brainvoyager.open(os.path.join(PATH_VMR, 'sub-01_sess-01_acq-mp2rage_UNI_denoised_IIHC_res2x_bvbabel_SS.vmr'))
        print(os.path.join(PATH_VMR, 'sub-01_sess-01_acq-mp2rage_UNI_denoised_IIHC_res2x_bvbabel_SS.vmr'))
    elif si == 'sub-03':
        docVMR = brainvoyager.open(os.path.join(PATH_VMR, 'sub-03_sess-01_acq-mp2rage_UNI_denoised_IIHC_res2x.vmr'))
    elif si == 'sub-06':
        docVMR = brainvoyager.open(os.path.join(PATH_VMR, 'sub-06_sess-01_acq-mp2rage_UNI_denoised_IIHC_res2x.vmr'))
    elif si == 'sub-07':
        docVMR = brainvoyager.open(os.path.join(PATH_VMR, 'sub-07_sess-01_acq-mp2rage_UNI_denoised_IIHC_bvbabel_SSbet_BFC_res2x.vmr'))

    elif si == 'sub-08':
        docVMR = brainvoyager.open(os.path.join(PATH_VMR, 'sub-08_sess-01_acq-mp2rage_UNI_denoised_IIHC_bvbabel_SSbet_BFC_res2x.vmr'))
    elif si == 'sub-09':
        docVMR = brainvoyager.open(os.path.join(STUDY_PATH, si, "derivatives", "anat", "{}_sess-02_acq-mp2rage_UNI_denoised_IIHC_bvbabel_SSbet_BFC_res2x.vmr".format(si)))
    elif si == 'sub-10':
        docVMR = brainvoyager.open(os.path.join(PATH_VMR, si + '_sess-01_acq-mp2rage_UNI_denoised_bvbabel_SSbet_BFC_res2x.vmr'))
    elif si == 'sub-04':
        docVMR = brainvoyager.open(os.path.join(PATH_VMR, si + '_sess-01_acq-mp2rage_UNI_denoised_IIHC_res2x.vmr'))
    else:
        docVMR = brainvoyager.open(os.path.join(PATH_VMR, si + '_sess-01_acq-mp2rage_UNI_denoised_IIHC_bvbabel_SSbet_BFC_res2x.vmr'))
    docVMR.clear_multistudy_glm_definition()
    ntot = 0

    for se in SESS:
        PATH_VTC = os.path.join(STUDY_PATH, si, 'derivatives', 'func', '{}'.format(se), 'MOT_VTC_cut_2x')
        PATH_GLM = os.path.join(STUDY_PATH, si, 'derivatives', 'func', '{}'.format(se), 'MOT_VTC_cut_2x', 'GLM-fix')
        PATH_OUT = os.path.join(STUDY_PATH, si, 'derivatives', 'func', 'Stats')
        if not os.path.exists(PATH_OUT):
            os.mkdir(PATH_OUT)
        PATH_OUT = os.path.join(STUDY_PATH, si, 'derivatives', 'func', 'Stats', 'Amb')
        if not os.path.exists(PATH_OUT):
            os.mkdir(PATH_OUT)
        run_vtc = glob.glob(os.path.join(PATH_VTC, '*amb*fix*.vtc'))
        n = len(run_vtc)
        #// Find run number
        for vtc in run_vtc:
            temp = vtc.split('\\')[-1]
            file = temp.split('_')[3]
            runid = file.split('-')[-1]
            filename = temp.split('.')[0]
            print(filename)

            docVMR.link_vtc(vtc)
            docVTC = brainvoyager.active_document
            nr_volumes = docVTC.n_volumes
            # print(nr_volumes)
            sdm = os.path.join(PATH_GLM, '{}_designMatrix.sdm'.format(filename))
            docVMR.add_study_and_dm(vtc, sdm)

        ntot = ntot + n

    print('Running GLM')
    docVMR.serial_correlation_correction_level = 2 # 1 -> AR(1), 2 -> AR(2)
    docVMR.psc_transform_studies = True
    docVMR.z_transform_studies = False   # This was 'True'
    docVMR.z_transform_studies_baseline_only = False
    docVMR.separate_subject_predictors = False
    docVMR.separate_study_predictors = False # This was 'True'
    docVMR.save_multistudy_glm_definition_file(os.path.join(PATH_OUT, '{}_task-amb_VTC_N-{}_FFX_AR-2_4preds_PSC_only.mdm'.format(si, ntot)))
    docVMR.compute_multistudy_glm()
    docVMR.save_glm(os.path.join(PATH_OUT, '{}_task-amb_VTC_N-{}_FFX_AR-2_4preds_PSC_only.glm'.format(si, ntot)))
    docVMR.show_glm()
        # doc.close()
