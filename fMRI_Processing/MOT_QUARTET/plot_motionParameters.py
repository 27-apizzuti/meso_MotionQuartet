"""Check motion correction"""

import os
import numpy as np
import glob
import matplotlib.pyplot as plt
import pandas as pd
import bvbabel
import pprint
# =============================================================================
STUDY_PATH = "/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD/"
SUBJ = ["sub-05"]
SESS = [3]
TASK = ["phy", "amb", "rest"]

# Figure specification
plt.style.use('dark_background')
DPI = 300
colors = ['r', 'g', 'b', 'y', 'm', 'c']
labels = ['TranslationX', 'TranslationY', 'TranslationZ', 'RotationX', 'RotationY', 'RotationZ']
n_parameters = 6

for su in SUBJ:
    PATH_FMR = os.path.join(STUDY_PATH, su, 'derivatives', 'func')
    for se in SESS:
        path_in = os.path.join(PATH_FMR, 'sess-0{}'.format(se))

        for tas in TASK:
            runs = glob.glob("{}/{}*/".format(path_in, tas), recursive=True)
            print(runs)
            for path_run in runs:
                temp = path_run.split("/")[-2]
                if temp == 'phy00':
                    print('{} not included in the plot'.format(temp))
                else:
                    fig, ax = plt.subplots(2, 1, figsize=(1920*2/DPI, 1080*2/DPI), dpi=DPI)
                    # Read the data
                    print('Work on {}'.format(temp))
                    FILE_NAMES = glob.glob(os.path.join(path_run, '*3DMC.sdm'))[0]
                    basename = FILE_NAMES.split(os.extsep, 1)[0]
                    filename = basename.split("/")[-1]

                    header, data = bvbabel.sdm.read_sdm(FILE_NAMES)
                    dims = np.shape(data[0]["ValuesOfPredictor"])
                    df_array = np.zeros([dims[0], 6])
                    df_array2 = np.zeros([dims[0], 6])
                    offset = np.zeros([1, 6])
                    for predictor in range(0, 6):
                        df_array[:, predictor] = data[predictor]["ValuesOfPredictor"]
                        offset[0, predictor] = data[predictor]["ValuesOfPredictor"][0]
                        df_array2[:, predictor] = data[predictor]["ValuesOfPredictor"] - offset[0, predictor]
                    mymax = np.max(np.max(df_array))
                    mymin= np.min(np.min(df_array))

                    mymax2 = np.max(np.max(df_array2))
                    mymin2= np.min(np.min(df_array2))

                    # // Plot
                    for it in range(n_parameters):
                        ax[0].plot(np.transpose(df_array[:, it]), color=colors[it], label=labels[it])
                        ax[0].set_ylim(np.floor(mymin), np.ceil(mymax))
                        ax[0].set_xlabel('Number of volumes')
                        ax[0].set_ylabel('Motion in mm')

                        ax[1].plot(np.transpose(df_array2[:, it]), color=colors[it], label=labels[it])
                        ax[1].set_ylim(np.floor(mymin2), np.ceil(mymax2))
                        ax[1].set_xlabel('Number of volumes')
                        ax[1].set_ylabel('Motion in mm')

                    ax[0].axhline(y = mymin, color = 'w', linestyle = '--')
                    ax[0].axhline(y = mymax, color = 'w', linestyle = '--')
                    ax[1].axhline(y = mymin2, color = 'w', linestyle = '--')
                    ax[1].axhline(y = mymax2, color = 'w', linestyle = '--')

                    ax[0].set_title('{} corrected with phy01'.format(temp))
                    ax[1].set_title('Across runs offset [mm, deg]: Tx {:.2f} Ty {:.2f} Tz {:.2f} Rx {:.2f} Ry {:.2f} Rz {:.2f}'.format(offset[0, 0] ,offset[0, 1], offset[0, 2], offset[0, 3], offset[0, 4], offset[0, 5]))
                    handles, labels = ax[0].get_legend_handles_labels()
                    handles, labels = ax[1].get_legend_handles_labels()
                    fig.legend(handles, labels, loc='upper right')

                    # Add the main title
                    fig.suptitle("Plot motion {} ses-{} {}".format(su, se, temp), fontsize=15)

                    plt.tight_layout()
                    fig.subplots_adjust(top=0.9)
                    plt.savefig(os.path.join(path_run, '{}.png'.format(filename)))
                    # plt.show()

print("Finished.")
