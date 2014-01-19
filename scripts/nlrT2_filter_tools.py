import numpy as nmp
import pecube_tools as pt
import os
import matplotlib.pyplot as plt


if os.name == 'nt':
	results_array = nmp.load('C:\\itchy\\code_repos\\pt_working\\results\\nlrT2_results.npy')
elif os.name == 'posix':
#	results_array = nmp.load('/media/4C307D4D22E94879/school/tibet/lunggar/kurt/pecube/nlrT2/nlr_results.npy')
	results_array = nmp.load('/home/itchy/src/Pecube/nlrT2/picloud/new_runs/nlr_results.npy')
 
#results_array = nmp.load('nlrT2_results.py')

fault_dip = [0.47]

# column indices for fault parameters
init_col = 36
accel_col = 37
sr1_col = 38
sr2_col = 39
net_extension_col = 40


# input observations and error calculations (larger of analytical and lab error)

aHe_obs = nmp.array([0.48, 0.64, 2.065, 0., 0., 0., 0., 0., 2.972, 0., 0.,
                     0., 0., 0., 3.722])#, 0., 0., 0.])

aHe_sd_err = nmp.array([0.09, 0.1, 0.97, 0,0,0,0,0, 1.67,0,0,0,0,0, 2.67])#, 0., 0., 0.])

zHe_obs = nmp.array([3.369, 4.774, 2.657, 3.322, 3.202, 3.441, 3.148, 2.819,
                     2.746, 3.417, 2.343, 3.032, 3.134, 3.069, 5.045])#, 5.5, 8., 9.5])

zHe_sd_err = nmp.array([0.27, 1.71, 0.21, 0.68, 0.26, 0.28, 0.33, 0.75, 0.41,
                        1.15, 0.51, 0.60, 1.10, 0.25, 2.24])#, 3., 3., 3.])

elev_obs = nmp.array([5130, 5147, 5174, 5217, 5226, 5235, 5237, 5267, 5287,
                      5377, 5382, 5389, 5418, 5420, 5509])#, 5688, 5833, 6198])

elev_pred = nmp.array([5211, 5230, 5277, 5334, 5208, 5213, 5213, 5253, 5293,
                       5348, 5316, 5370, 5599, 5373, 5764])#, 5833, 6134, 6245])

num_obs = len(zHe_obs)



# filtering parameters

num_aHe_outliers = 2

num_zHe_outliers = 0

aHe_lab_err = 0.06 * aHe_obs

zHe_lab_err = 0.05 * zHe_obs

aHe_err = pt.max_errors(aHe_sd_err, aHe_lab_err)

zHe_err = pt.max_errors(zHe_sd_err, zHe_lab_err)

aHe_first_result = 0

zHe_first_result = 1

num_chronometers = 2

result_interval = num_chronometers

# error bounds
aHe_1sd_err_lo = aHe_obs - aHe_err
aHe_2sd_err_lo = aHe_obs - 2 * aHe_err
aHe_1sd_err_hi = aHe_obs + aHe_err
aHe_2sd_err_hi = aHe_obs + 2 * aHe_err

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


num_outliers = num_zHe_outliers
zHe_index = pt.get_result_index(zHe_first_result, result_interval, num_obs)
# filter zHe runs
zHe_successful_runs = pt.filter_ages(results_array, obs_age_lo, obs_age_hi, 
                                     zHe_first_result, result_interval,
                                     num_obs, num_outliers)
                                       
# aHe run variables
aHe_sigma = 1 #sigma, 1 or 2
if aHe_sigma == 1:
	obs_age_lo = aHe_1sd_err_lo
	obs_age_hi = aHe_1sd_err_hi
	
elif aHe_sigma == 2:
	obs_age_lo = aHe_2sd_err_lo
	obs_age_hi = aHe_2sd_err_hi


num_outliers = num_aHe_outliers
aHe_index = pt.get_result_index(aHe_first_result, result_interval, num_obs)
# filter aHe runs
aHe_successful_runs = pt.filter_ages(results_array, obs_age_lo, obs_age_hi,
                                     aHe_first_result, result_interval,
                                     num_obs, num_outliers)
                                       

all_successful_runs = pt.combine_successful_runs(zHe_successful_runs,
                                                 aHe_successful_runs)

filtered_runs = pt.filter_results(results_array, all_successful_runs)

num_filtered = filtered_runs.shape[0]

aHe_success_ages = pt.get_chronometer_results(filtered_runs, aHe_index)
zHe_success_ages = pt.get_chronometer_results(filtered_runs, zHe_index)

nlrT2_aHe_success = aHe_success_ages
nlrT2_zHe_success = zHe_success_ages

nlrT2_init = filtered_runs[:,init_col]
nlrT2_accel = filtered_runs[:,accel_col]
nlrT2_sr1 = filtered_runs[:,sr1_col]
nlrT2_sr2 = filtered_runs[:,sr2_col]
nlrT2_extension = filtered_runs[:,net_extension_col]


print 'You got', results_array.shape[0], 'total runs.'
print 'You got', len(zHe_successful_runs), 'good zircon runs.'
print 'You got', len(aHe_successful_runs), 'good apatite runs.'    
print 'You got', num_filtered, 'good total runs!'


# make histories
time_start = 20.
time_stop = 0.
time_step = 0.01

time_vector = pt.make_time_vector(time_start = time_start,
                                  time_stop = time_stop, time_step = time_step,
                                  decimals = 3)
times = len(time_vector)

er_w_time_array = nmp.zeros((times, num_filtered))
cum_ext_w_time_array = nmp.zeros((times, num_filtered))

for i in range(num_filtered):
    init = filtered_runs[i,init_col] 
    accel = filtered_runs[i,accel_col]
    er1 = filtered_runs[i,sr1_col] * nmp.cos(fault_dip)
    er2 = filtered_runs[i,sr2_col] * nmp.cos(fault_dip)
	
    er_w_time_array[:,i] = pt.make_slip_rate_w_time(init, accel, er1, er2,
                                                    time_vector = time_vector)

    cum_ext_w_time_array[:,i] = pt.get_cum_vector(er_w_time_array[:,i],
                                                  time_step)




fig1 = plt.figure(1)
pt.make_fault_histograms(fig1, filtered_runs, init_col, sr1_col, accel_col,
                                sr2_col)

fig2 = plt.figure(2)
pt.make_ext_histories(fig2, 'nlrT2', time_vector, er_w_time_array,
                             cum_ext_w_time_array)

plt.show()

