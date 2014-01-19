import numpy as nmp
import pecube_tools as pt
import os
import matplotlib.pyplot as plt


if os.name == 'nt':
	results_array = nmp.loadtxt('C:\\itchy\\code_repos\\pt_working\\results\\nlrT4_results.csv', delimiter=',')
elif os.name == 'posix':
#	results_array = nmp.load('/media/4C307D4D22E94879/school/tibet/lunggar/kurt/pecube/nlrT2/nlr_results.npy')
	results_array = nmp.loadtxt('/home/itchy/src/Pecube/nlrT4/new_runs/nlr_results.csv', delimiter=',')
 
#results_array = nmp.load('nlrT2_results.py')

# column indices for fault parameters
initA_col = 8
initB_col = 9
accel_col = 10
srA1_col = 11
srA2_col = 12
srB1_col = 13
srB2_col = 14
net_extension_col = 15

fault_A_dip = 0.84
fault_B_dip = 0.93

# input observations and error calculations (larger of analytical and lab error)


aHe_obs = nmp.array([3.974, 0., 2.912, 2.744])

aHe_sd_err = nmp.array([0.238, 0., 0.175, 0.233])

zHe_obs = nmp.array([4.637, 4.212, 3.521, 3.425])

zHe_sd_err = nmp.array([0.371, 0.705, 0.282, 0.581])

elev_obs = nmp.array([5336, 4971, 4942, 4880])

elev_pred = nmp.array([5317, 4987, 5022, 4898])

lon = nmp.array([83.5131, 83.5624, 83.5598, 83.5667])

num_obs = len(zHe_obs)



# filtering parameters

num_aHe_outliers = 1

num_zHe_outliers = 0

aHe_lab_err = 0.06 * aHe_obs

zHe_lab_err = 0.04 * zHe_obs

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

first_result = zHe_first_result
num_outliers = num_zHe_outliers
zHe_index = pt.get_result_index(zHe_first_result, result_interval, num_obs)

# filter zHe runs
zHe_successful_runs = pt.filter_ages(results_array, obs_age_lo, obs_age_hi, 
                                     first_result, result_interval, num_obs,
                                     num_outliers)
                                       
# aHe run variables
aHe_sigma = 2 #sigma, 1 or 2
if aHe_sigma == 1:
	obs_age_lo = aHe_1sd_err_lo
	obs_age_hi = aHe_1sd_err_hi
	
elif aHe_sigma == 2:
	obs_age_lo = aHe_2sd_err_lo
	obs_age_hi = aHe_2sd_err_hi

first_result = aHe_first_result
num_outliers = num_aHe_outliers
aHe_index = pt.get_result_index(aHe_first_result, result_interval, num_obs)

# filter aHe runs
aHe_successful_runs = pt.filter_ages(results_array, obs_age_lo, obs_age_hi,
                                     first_result, result_interval, num_obs,
                                     num_outliers)
                                       

all_successful_runs = pt.combine_successful_runs(zHe_successful_runs,
                                                 aHe_successful_runs)

filtered_runs = pt.filter_results(results_array, all_successful_runs)

num_filtered = filtered_runs.shape[0]


aHe_success_ages = pt.get_chronometer_results(filtered_runs, aHe_index)
zHe_success_ages = pt.get_chronometer_results(filtered_runs, zHe_index)

nlrT4_initA = filtered_runs[:,initA_col]
nlrT4_initB = filtered_runs[:,initB_col]
nlrT4_accel = filtered_runs[:,accel_col]
nlrT4_srA1 = filtered_runs[:,srA1_col]
nlrT4_srA2 = filtered_runs[:,srA2_col]
nlrT4_srB = filtered_runs[:,srB1_col]
nlrT4_extension = filtered_runs[:,net_extension_col]

#aHe_err = 

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
plt.title('Fault A')

fig2 = plt.figure(2)

pt.make_fault_histograms(fig2, filtered_runs, initB_col, srB1_col, accel_col,
                                srB2_col)
plt.title('Fault B')

fig3 = plt.figure(3)
pt.make_ext_histories(fig3, 'nlrT4', time_vector, er_w_time_array,
                             cum_ext_w_time_array)

fig4 = plt.figure(4)
pt.lon_elev_plots(fig4, aHe_success_ages.T, aHe_obs, aHe_err * 2, lon, elev_obs)

plt.show()
