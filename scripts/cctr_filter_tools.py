# -*- coding: utf-8 -*-
"""
Created on Sat Aug 25 15:37:30 2012

@author: Richard
"""

import numpy as nmp
import pecube_tools as pt
import os
import matplotlib.pyplot as plt

if os.name == 'nt':
    results_array = nmp.load('C:\\school\\tibet\\lunggar\\thermo\\pecube\\cctr_picloud_results\\cctr_all_runs.npy')



# column indices for fault parameters
initA_col = 8
initB_col = 12
accel_col = 9
srA1_col = 10
srA2_col = 11
srB1_col = 13
srB2_col = 14
net_extension_col = 16

fault_A_dip = 0.88
fault_B_dip = 0.88


# input observations and error calculations (larger of analytical and lab error)


zHe_obs = nmp.array([7.33, 7.16, 7.25, 6.27, 5.99, 5.33, 5.33, 5.96])

zHe_sd_err = nmp.array([0.6, 0.29, 0.39, 0.88, 0.17, 0.63, 0.33, 0.61])

elev_obs = nmp.array([5979, 5848, 5826, 5719, 5633, 5622, 5490, 5477])

elev_pred = nmp.array([5965, 5996, 5898, 5746, 5759, 5614, 5638, 5618])

lon = nmp.array([83.4355, 83.4372, 83.4556, 83.4642, 83.4744, 83.4833, 83.4857, 83.5125])

num_obs = len(zHe_obs)



# filtering parameters

num_zHe_outliers = 0


zHe_lab_err = 0.05 * zHe_obs


zHe_err = pt.max_errors(zHe_sd_err, zHe_lab_err)

zHe_first_result = 0

num_chronometers = 1

result_interval = num_chronometers

# error bounds

zHe_1sd_err_lo = zHe_obs - zHe_err
zHe_2sd_err_lo = zHe_obs - 2 * zHe_err
zHe_1sd_err_hi = zHe_obs + zHe_err
zHe_2sd_err_hi = zHe_obs + 2 * zHe_err


# zHe run variables
zHe_sigma = 2 #sigma, 1 or 2
if zHe_sigma == 1:
	obs_age_lo = zHe_1sd_err_lo
	obs_age_hi = zHe_1sd_err_hi
	
elif zHe_sigma == 2:
	obs_age_lo = zHe_2sd_err_lo
	obs_age_hi = zHe_2sd_err_hi

first_result = zHe_first_result
num_outliers = num_zHe_outliers
zHe_index = pt.get_result_index(zHe_first_result, result_interval, num_obs)

# filter zHe runs
zHe_successful_runs = pt.filter_ages(results_array, obs_age_lo, obs_age_hi, 
                                     first_result, result_interval, num_obs,
                                     num_outliers)
                                       

                                       

all_successful_runs = pt.combine_successful_runs(zHe_successful_runs)

filtered_runs = pt.filter_results(results_array, all_successful_runs)

num_filtered = filtered_runs.shape[0]

zHe_success_ages = pt.get_chronometer_results(filtered_runs, zHe_index)

#aHe_err = 

print 'You got', results_array.shape[0], 'total runs.'
print 'You got', len(zHe_successful_runs), 'good zircon runs.'
   
print 'You got', num_filtered, 'good total runs!'




# make histories
time_start = 20.
time_stop = 0.
time_step = 0.01

time_vector = pt.make_time_vector(time_start = time_start,
                                  time_stop = time_stop, time_step = time_step,
                                  decimals = 3)
times = len(time_vector)

er_w_time_array_A = nmp.zeros((times, num_filtered))
er_w_time_array_B = nmp.zeros((times, num_filtered))

cum_ext_w_time_array_A = nmp.zeros((times, num_filtered))
cum_ext_w_time_array_B = nmp.zeros((times, num_filtered))

for i in range(num_filtered):
    initA = filtered_runs[i,initA_col]
    initB = filtered_runs[i,initB_col]
    accel = filtered_runs[i,accel_col]
    erA1 = filtered_runs[i,srA1_col] * nmp.cos(fault_A_dip)
    erB1 = filtered_runs[i,srB1_col] * nmp.cos(fault_B_dip)
    #er1 = erA1 + erB1
    erA2 = filtered_runs[i,srA2_col] * nmp.cos(fault_A_dip)
    erB2 = filtered_runs[i,srB2_col] * nmp.cos(fault_B_dip)
    #er2 = erA2 + erB2
	
    er_w_time_array_A[:,i] = pt.make_slip_rate_w_time(initA, accel, erA1, erA2,
                                                    time_vector = time_vector)
    
    er_w_time_array_B[:,i] = pt.make_slip_rate_w_time(initB, accel, erB1, erB2,
                                                    time_vector = time_vector)

    cum_ext_w_time_array_A[:,i] = pt.get_cum_vector(er_w_time_array_A[:,i],
                                                  time_step)

    cum_ext_w_time_array_B[:,i] = pt.get_cum_vector(er_w_time_array_B[:,i],
                                                  time_step)

    er_w_time_array = er_w_time_array_A + er_w_time_array_B
    
    cum_ext_w_time_array = cum_ext_w_time_array_A + cum_ext_w_time_array_B

# make plots
fig1 = plt.figure(1)
pt.make_fault_histograms(fig1, filtered_runs, initA_col, srA1_col, accel_col,
                                srA2_col)


fig2 = plt.figure(2)
pt.make_fault_histograms(fig2, filtered_runs, initB_col, srB1_col, accel_col,
                                srB2_col)


fig3 = plt.figure(3)
pt.make_ext_histories(fig3, 'cctr', time_vector, er_w_time_array,
                             cum_ext_w_time_array)