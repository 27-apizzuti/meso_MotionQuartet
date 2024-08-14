""""This script evaluates the behavioral data acquired to evaluate the goodness of the participant.
It compute how many runs of unambiguous stimulus corrisponds to 3 runs of ambiguous.
NOTE: In 1 run of unambiguous there are 240s for each motion."""

import pandas as pd
import numpy as np
import glob
import os
import matplotlib.pyplot as plt
import math

PATH_IN = "D:\\Exp-MotionQuartet\\MRI_MQ\\BOLD"
SUBJ = ['sub-04']
SESS = [4]
TIME_UNAMB = 240

RunToAcquire = np.zeros(len(SUBJ))
TotGoodPeriods = np.zeros((len(SUBJ), 2))
N_unambigous = np.zeros((len(SUBJ), 2))
UnBalanceLev = np.zeros(len(SUBJ))       # Time_spent_in_hor / Time_spent_in_ver [averaged across run]
PercPeriodDur_AllSbj = [[], []]
UsefulTime = [[], []]

for itersu, su in enumerate(SUBJ):
    for se in SESS:

        FILE_NAMES = glob.glob(os.fspath(os.path.join(PATH_IN, su, 'Protocols', 'sess-0{}'.format(se), 'Exp1_amb_MotQuart', 'Logging', '*.log')))
        N_RUNS = len(FILE_NAMES)
        my_dpi = 96
        fig, axs = plt.subplots(nrows=N_RUNS, ncols=2, figsize=(1920/my_dpi, 1080/my_dpi), dpi=my_dpi)
    
        TotPeriods_stat = np.zeros((3, 2, N_RUNS))
        GoodPeriods_stat = np.zeros((3, 2, N_RUNS))
    
        temp_PercPeriodDur = [[], []]  # append subject-specific data across runs
        temp_UsefulTime = [[], []]
    
        for r in range(0, N_RUNS):
    
            # Extract run information
            basename = os.path.splitext(FILE_NAMES[r])
            corename = basename[0].split("\\")[-1]
            temp = corename.split("_")
            for it in temp:
                if (it == 'Run0{}'.format(r+1)):
                    info_run = it
    
            # //Read log file
            df = pd.read_table(FILE_NAMES[r], skiprows=18, delimiter = "\t")   # put back to skiprows=18
            print("================================")
            print("Subject {}, {},  {}".format(su, se, info_run))
    
            # Loop through list_keypress
            switch_time = []
            switch_motion = []
    
            # Find part I need in the log file
            df_array = df.values
    
            start_condition0 = df_array[:, -1] == 'StartOfCondition0'   # initial fixation & final fixation
            start_condition1 = df_array[:, -1] == 'StartOfCondition1'   # baseline
            start_condition2 = df_array[:, -1] == 'StartOfCondition2'   # motion quartet
            start_condition3 = df_array[:, -1] == 'StartOfCondition3'   # final fixation
            qexit_condition = df_array[:, -1] == "User pressed quit"
            end_of_run = df_array[:, -1] == "EndOf{}".format(info_run)
    
            key1 = df_array[:, -1] == 'Keypress: 1'   # 1 Horizontal || Jasmina mistakes [2, 3]
            key2 = df_array[:, -1] == 'Keypress: 2'   # 2 Vertical
    
            idx = start_condition0 + start_condition1 + start_condition2 + start_condition3 + qexit_condition + key1 + key2 + end_of_run
    
            # Create a small version of df_array
            df_array_short = df_array[idx, : ]
    
            # Find perceptual periods
            exit_condition = np.where(df_array_short == "EndOf{}".format(info_run))  # Usually the exit condition is signed by the final Fixation
            myexit = exit_condition[0][-1]

            # Find Horizontal and Vertical periods
            i = 0
    
            while i < myexit + 1:
    
                if df_array_short[i, -1] == "Keypress: 1": #|| 2  Jasmina mistakes
                    expect_cond = "Keypress: 2" #|| 3  Jasmina mistakes
    
                    # Check end condition
                    if df_array_short[i+1, -1] == expect_cond:
                        time = float(df_array_short[i+1, 0]) - float(df_array_short[i, 0])
                        switch_time.append(time)
                        switch_motion.append("Horizontal")
    
                    elif df_array_short[i+1, -1] == "StartOfCondition1":   # Edge case
                        time = float(df_array_short[i+1, 0]) - float(df_array_short[i, 0])
                        switch_time.append(time)
                        switch_motion.append("Horizontal_Baseline")
    
                elif (df_array_short[i, -1] == "Keypress: 2"): # || 3 Jasmina mistakes
                    expect_cond = "Keypress: 1" # || 2 Jasmina mistakes
    
                    # Check end condition
                    if df_array_short[i+1, -1] == expect_cond:
                        time = float(df_array_short[i+1, 0]) - float(df_array_short[i, 0])
                        switch_time.append(time)
                        switch_motion.append("Vertical")
    
                    elif df_array_short[i+1, -1] == "StartOfCondition1":   # Edge case
                        time = float(df_array_short[i+1, 0]) - float(df_array_short[i, 0])
                        switch_time.append(time)
                        switch_motion.append("Vertical_Baseline")
                i = i + 1
    
    
            # Make a summary
            switch_time = np.asarray(switch_time)
    
            # Mean lenght of percetual periods during ambiguous motion experiment
    
            idx_hor = ((np.asarray(switch_motion) == 'Horizontal_Baseline')* (switch_time > 6)) + (np.asarray(switch_motion) == 'Horizontal')
            idx_ver = ((np.asarray(switch_motion) == 'Vertical_Baseline')* (switch_time > 6)) + (np.asarray(switch_motion) == 'Vertical')
    
            idx = [[idx_hor], [idx_ver]]
            label = ['Horizontal', 'Vertical']
    
    
            for it, i in enumerate(idx):
                # print(it, i)
                x = np.asarray(i[0]).T
                temp_PercPeriodDur[it].append(switch_time[x])
    
                # Total periods
                TotPeriods_stat[0, it, r] = np.mean(switch_time[x])    # mean
                TotPeriods_stat[1, it, r] = np.median(switch_time[x])  # median
                TotPeriods_stat[2, it, r] = np.sum(x)  # n
    
                # Count good periods
                temp_switch_time = switch_time[x]
                idx_good = temp_switch_time > 6   # Period lasts for 3 VASO TR
                GoodPeriods_stat[0, it, r] = (np.sum(idx_good)/np.sum(x)) *100  # n_good
                GoodPeriods_stat[1, it, r] = np.median(switch_time[x])  # median
                GoodPeriods_stat[2, it, r] = np.sum(temp_switch_time[idx_good])
    
                temp_UsefulTime[it].append(GoodPeriods_stat[0, it, r])
                
                # Make plot
                if N_RUNS == 1:
                    hist_bins = math.ceil((np.max((switch_time[x])) - np.min((switch_time[x]))) / 2)  # bin width =2xs
                    axs[it].hist(switch_time[x], bins=hist_bins)
                    axs[it].set_xlabel("Time Duration [s]")
                    axs[it].set_ylabel("Number of periods")
                    axs[it].set_title("run-{} {}, N of tot. periods: {}, Useful periods: {:.1f}%, Useful time: {:.1f}s".format(r, label[it], np.sum(x), GoodPeriods_stat[0, it, r], GoodPeriods_stat[2, it, r]))
                    axs[it].axvline(x=np.median(switch_time[x]), color='k', linestyle='--', label='Median: {:.1f}s'.format(np.median(switch_time[x])))
                    axs[it].axvline(x=np.mean(switch_time[x]), color='blue', linestyle='--', label='Mean: {:.1f}s'.format(np.mean(switch_time[x])))
                    axs[it].axvline(x=6, color='red', linestyle='-', label='threshold: 7.5s')
    
                    axs[it].legend()
                    
                else:
                    hist_bins = math.ceil((np.max((switch_time[x])) - np.min((switch_time[x]))) / 2)  # bin width =2xs
                    axs[r, it].hist(switch_time[x], bins=hist_bins)
                    axs[r, it].set_xlabel("Time Duration [s]")
                    axs[r, it].set_ylabel("Number of periods")
                    axs[r, it].set_title("run-{} {}, N of tot. periods: {}, Useful periods: {:.1f}%, Useful time: {:.1f}s".format(r, label[it], np.sum(x), GoodPeriods_stat[0, it, r], GoodPeriods_stat[2, it, r]))
                    axs[r, it].axvline(x=np.median(switch_time[x]), color='k', linestyle='--', label='Median: {:.1f}s'.format(np.median(switch_time[x])))
                    axs[r, it].axvline(x=np.mean(switch_time[x]), color='blue', linestyle='--', label='Mean: {:.1f}s'.format(np.mean(switch_time[x])))
                    axs[r, it].axvline(x=6, color='red', linestyle='-', label='threshold: 6s')
                    axs[r, it].legend()
                        
               
                fig.tight_layout()
    
                print("For {}, {}, Percentage of good data with respect to the total for {}: {} %".format(su, r, label[it], GoodPeriods_stat[0, it, r]))
                print("For {}, {}, {} Median: {} %".format(su, r, label[it], TotPeriods_stat[1, it, r]))
    
            if GoodPeriods_stat[2, 0, r] < GoodPeriods_stat[2, 1, r]:
                score2 = 1- (GoodPeriods_stat[2, 0, r]/GoodPeriods_stat[2, 1, r])
            else:
                score2 = 1- (GoodPeriods_stat[2, 1, r]/GoodPeriods_stat[2, 0, r])
    
            print("For {}, {}, 1- UnBalance level: {:.2f} [0=perfect] ".format(su, r, score2))
            UnBalanceLev[itersu] = UnBalanceLev[itersu] + score2
    
        UsefulTime[0].append(np.mean(np.array(temp_UsefulTime[0])))
        UsefulTime[1].append(np.mean(np.array(temp_UsefulTime[1])))
    
    
        # PercPeriodDur_AllSbj[0].append(np.array([*temp_PercPeriodDur[0][0], *temp_PercPeriodDur[0][1], *temp_PercPeriodDur[0][2]]))
        # PercPeriodDur_AllSbj[1].append(np.array([*temp_PercPeriodDur[1][0], *temp_PercPeriodDur[1][1], *temp_PercPeriodDur[1][2]]))
    
        UnBalanceLev[itersu] = UnBalanceLev[itersu]/N_RUNS   # score 2
        TotGoodPeriods[itersu, :] = np.sum(GoodPeriods_stat[2, :, :], axis=1)
    
        N_unambigous[itersu, :] = np.sum(GoodPeriods_stat[2, :, :], axis=1) / TIME_UNAMB
    
        RunToAcquire[itersu] = np.max([ [2-N_unambigous[itersu, 0]], [2-N_unambigous[itersu, 1]] ])    # score 1
        plt.suptitle('Subject {} \n RunToAcquire: {:.1f} | 1 - UnBalance: {:.2f} \n Horizontal: 3 AMB = {:.1f} UNAMB | Vertical: 3 AMB = {:.1f} UNAMB'.format(su, RunToAcquire[itersu], UnBalanceLev[itersu], N_unambigous[itersu, 0], N_unambigous[itersu, 1]), y=1.08)
    
        print("================================")
        print("For {}, time hor motion (on 3runs) corrisponds {} runs of unambig motion".format(su, N_unambigous[itersu, 0]))
        print("For {}, time ver motion (on 3runs) corrisponds {} runs of unambig motion".format(su, N_unambigous[itersu, 1]))
        print("For {}, 1-unbalance level {:.1f}".format(su, UnBalanceLev[itersu]))
    
        plt.savefig(os.path.join(PATH_IN, su, 'Protocols', 'sess-0{}'.format(se), "{}_fMRI_behavioral_data_complete.png".format(su)), bbox_inches='tight', dpi=my_dpi)
