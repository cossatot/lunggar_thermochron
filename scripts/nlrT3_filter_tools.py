import numpy as nmp
import pecube_tools as pt
import os
import matplotlib.pyplot as plt


if os.name == 'nt':
	results_array = nmp.load('C:\\itchy\\code_repos\\pt_working\\results\\nlrT3_results.npy')
elif os.name == 'posix':
#	results_array = nmp.load('/media/4C307D4D22E94879/school/tibet/lunggar/kurt/pecube/nlrT2/nlr_results.npy')
	results_array = nmp.load('/home/itchy/src/Pecube/nlrT3/picloud/new_runs/nlr_results.npy')
 
#results_array = nmp.load('nlrT2_results.py')

# column indices for fault parameters
init_col = 14
accel_col = 15
sr1_col = 16
sr2_col = 17
net_extension_col = 18

fault_dip = 0.37


# input observations and error calculations (larger of analytical and lab error)

# last 2 observations are dummies based on Woodruff et al.
aHe_obs = nmp.array([0.,0.,0.,0.,0.])#,0.,0.])

aHe_sd_err = nmp.array([30.,30.,30.,30.,30.])#,0.,0.])

#zHe_obs = nmp.array([2.524, 3.226, 2.717, 2.79, 3.524])#, 6.5, 9.5])
zHe_obs = nmp.array([3.524, 3.226, 2.717, 2.79, 3.524])#, 6.5, 9.5])

zHe_sd_err = nmp.array([0.231, 0.258, 0.217, 0.223, 1.794])#, 3.0, 4.0])
#zHe_sd_err = nmp.array([1.231, 0.258, 0.217, 0.223, 1.794])

elev_obs = nmp.array([5689, 5436, 5335, 5197, 5172])#, 6036, 6309])

elev_pred = nmp.array([5626, 5467, 5393, 5274, 5251])#, 5961, 6342])

num_obs = len(zHe_obs)



# filtering parameters

num_aHe_outliers = 0

num_zHe_outliers = 0

aHe_lab_err = 0.06 * aHe_obs

zHe_lab_err = 0.05 * zHe_obs

aHe_err = pt.max_errors(aHe_sd_err, aHe_lab_err)

zHe_err = pt.max_errors(zHe_sd_err, zHe_lab_err)

aHe_first_obs = 0

zHe_first_obs = 1

num_chronometers = 2

obs_interval = num_chronometers

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

first_obs = zHe_first_obs
num_outliers = num_zHe_outliers

# filter zHe runs
zHe_successful_runs = pt.filter_ages(results_array, obs_age_lo, obs_age_hi, 
                                     first_obs, obs_interval, num_obs,
                                     num_outliers)
                                       
# aHe run variables
aHe_sigma = 1 #sigma, 1 or 2
if aHe_sigma == 1:
	obs_age_lo = aHe_1sd_err_lo
	obs_age_hi = aHe_1sd_err_hi
	
elif aHe_sigma == 2:
	obs_age_lo = aHe_2sd_err_lo
	obs_age_hi = aHe_2sd_err_hi

first_obs = aHe_first_obs
num_outliers = num_aHe_outliers

# filter aHe runs
aHe_successful_runs = pt.filter_ages(results_array, obs_age_lo, obs_age_hi,
                                     first_obs, obs_interval, num_obs,
                                     num_outliers)
                                       

all_successful_runs = pt.combine_successful_runs(zHe_successful_runs,
                                                 aHe_successful_runs)

filtered_runs = pt.filter_results(results_array, all_successful_runs)


nlrT3_init = filtered_runs[:,init_col]
nlrT3_accel = filtered_runs[:,accel_col]
nlrT3_sr1 = filtered_runs[:,sr1_col]
nlrT3_sr2 = filtered_runs[:,sr2_col]
nlrT3_extension = filtered_runs[:,net_extension_col]

num_filtered = filtered_runs.shape[0]

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
pt.make_ext_histories(fig2, 'nlrT3', time_vector, er_w_time_array,
                             cum_ext_w_time_array)

plt.show()
