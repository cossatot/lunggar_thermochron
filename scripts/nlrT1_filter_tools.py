import numpy as nmp
import pecube_tools as pt
import os
import matplotlib.pyplot as plt


if os.name == 'nt':
	results_array = nmp.load('C:\\itchy\\code_repos\\pt_working\\results\\nlrT1_results.npy')
elif os.name == 'posix':
#	results_array = nmp.load('/media/4C307D4D22E94879/school/tibet/lunggar/kurt/pecube/nlrT2/nlr_results.npy')
	results_array = nmp.load('/home/itchy/src/Pecube/nlrT1/picloud/new_runs/nlrT1_results.npy')
 
#results_array = nmp.load('nlrT2_results.py')

# column indices for fault parameters
init_col = 20
accel_col = 21
sr1_col = 22
sr2_col = 23
net_extension_col = 24

fault_dip = 0.434631204


# input observations and error calculations (larger of analytical and lab error)

# last 3 observations are dummies based on Woodruff et al.
#aHe_obs = nmp.array([3.830, 3.789, 3.205, 2.717, 2.694, 0.0, 1.770, 4., 5., 6.5])
aHe_obs = nmp.array([3.830, 3.789, 3.205, 2.717, 2.694, 0.0, 1.770])

#aHe_sd_err = nmp.array([0.441, 0.769, 0.549, 0.434, 1.173, 0.0, .01, 2.0, 2., 2.0])
aHe_sd_err = nmp.array([0.441, 0.769, 0.549, 0.434, 1.173, 0.0, .01]) #,20.,20.,20.])


#zHe_obs = nmp.array([3.758, 5.557, 3.979, 4.376, 3.765, 3.923, 3.498, 6.5, 7.5, 9.5])
zHe_obs = nmp.array([3.758, 5.557, 3.979, 4.376, 3.765, 3.923, 3.498])


#zHe_sd_err = nmp.array([0.372, 1.177, 0.470, 0.350, 0.301, 0.322, 0.321, 2., 2., 2.,])
zHe_sd_err = nmp.array([0.372, 1.177, 0.470, 0.350,0.301, 0.322, 0.321])

elev_obs = nmp.array([5896, 5800, 5726, 5708, 5687, 5386, 5199])#, 5842, 6021, 6222])

elev_pred = nmp.array([5826, 5816, 5660, 5620, 5576, 5416])#, 5194, 5978, 6263])

lon = nmp.array([83.5008, 83.5013, 83.5090, 83.5105, 83.5121, 83.5260, 83.5384]) #,83.4847, 83.4706, 83.4520])

num_obs = len(zHe_obs)



# filtering parameters

num_aHe_outliers = 0

num_zHe_outliers = 1

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
aHe_sigma = 2 #sigma, 1 or 2
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
nlrT1_aHe_success = aHe_success_ages
nlrT1_zHe_success = zHe_success_ages

nlrT1_init = filtered_runs[:,init_col]
nlrT1_accel = filtered_runs[:,accel_col]
nlrT1_sr1 = filtered_runs[:,sr1_col]
nlrT1_sr2 = filtered_runs[:,sr2_col]
nlrT1_extension = filtered_runs[:,net_extension_col]

#nlrT1_lat = nmp.mean[lat]

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
#plt.title('NLR Transect 1')
pt.make_fault_histograms(fig1, filtered_runs, init_col, sr1_col, accel_col,
                                sr2_col)

fig2 = plt.figure(2)
pt.make_ext_histories(fig2, 'nlrT1', time_vector, er_w_time_array,
                             cum_ext_w_time_array)
                             

fig3 = plt.figure(3)
pt.lon_elev_plots(fig3, zHe_success_ages.T, zHe_obs, zHe_err* 2, lon, elev_obs)

fig4 = plt.figure(4)
pt.lon_elev_plots(fig4, aHe_success_ages.T, aHe_obs, aHe_err* 2, lon, elev_obs)
#plt.title('NLR Transect 1')

plt.show()
