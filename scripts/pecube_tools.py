"""
module for filtering of Pecube/picloud data, making plots, 
deformation histories, etc.

"""
import numpy as nmp
import matplotlib.pyplot as plt

# filtering functions
def max_errors(sd_err, lab_err):
    """Makes an error array composed of the larger of the lab error
    (from the standard deviation of the analytical standard) or the
    standard deviation of the individual aliquot ages for each sample

    Returns: error array
    """
    num_obs = len(sd_err)
    err_array = nmp.zeros(num_obs)

    for s in nmp.arange(num_obs):
        err_array[s] = nmp.maximum(sd_err[s], lab_err[s])
        
        # make very wide (1 Gy) error bars for no data (obs of 0)
        if err_array[s] == 0:
        	err_array[s] = 10
	
    return err_array


def get_result_index(first_result, result_interval, num_obs):
    """Gets the indices of the thermochronometer of interest"""
    last_result = first_result + (num_obs -1) * result_interval
    stop_result = last_result + result_interval
    result_index = nmp.arange(first_result, stop_result, result_interval)
    
    return result_index
    

def check_fits(result_row, obs_age_lo, obs_age_hi, first_result,
               result_interval, num_obs):
    """Checks whether each modeled sample fits the observed age within error
    and returns array with 1 (True: fits) or 0 (False: doesn't fit) for each 
    sample in the model
    """
    err_index = nmp.arange(num_obs)
    result_index = get_result_index(first_result, result_interval, num_obs)
    success_array = nmp.zeros(num_obs)

    for i in err_index:
        res = result_index[i]
        if obs_age_lo[i] <= result_row[res] <= obs_age_hi[i]:
            success_array[i] = 1
			
    return success_array
	
	
def filter_ages(results_array, obs_age_lo, obs_age_hi, first_result,
                result_interval, num_obs, num_outliers):
    """Takes results array and filters them, so that passing runs have
    (num_obs - num_outliers) successes.  A success means that for a sample,
    the model age is within error of the observed age

    Returns: row indices for filtered (passing) rows
    """ 
    #TODO:  Make these args keyword args so that they are less confusing to type    
    
    num_rows = results_array.shape[0]
    enough_fits = num_obs - num_outliers
    successful_runs = list([])

    for i in range(num_rows):
        result_row = results_array[i,:]
        success_array = check_fits(result_row, obs_age_lo, obs_age_hi,
                                   first_result, result_interval, num_obs)
	
        if nmp.sum(success_array) >= enough_fits:
            successful_runs.append(i)
	
	#success_array = filter_results(results_array, successful_runs)
	
    return successful_runs


def combine_successful_runs(*args):
    """Takes 2 lists of successful runs (e.g. from two thermochronometers
    and finds common elements.  In the future will be updated to handle more
    thermochronometers, probably with a loop.
    
    Arguments: row indices for successful fits
    
    Returns: array containing row indices for successful runs with all
    thermochronometers.
    """
    if len(args) == 1:
        all_successful_runs = nmp.array(args[0])

        
    elif len(args) == 2:
        list0 = nmp.array(args[0])
        list1 = nmp.array(args[1])
        all_successful_runs = list0[nmp.in1d(list0, list1)]
        
    elif len(args) == 0:
        print 'This function needs some arguments!'
        
    else:
        print 'too many lists!  For now only 2 please.'
        
    return all_successful_runs

			
def filter_results(results_array, all_successful_runs):
    """Makes new array of only successful runs"""    
    filtered_runs = results_array[all_successful_runs, :]
    return filtered_runs
    

def get_chronometer_results(result_array, result_index):
    """Returns array of only one chronometer from larger result array"""
    chron_results = result_array[:,result_index]
    return chron_results
    

def calc_chi_square(obs, pred, num_obs):
    """Calculates chi-quare"""

    data_exists = obs != 0.	
    obs_data = obs[data_exists]
    pred_data = pred[data_exists]
    chi_square = sum((obs_data - pred_data)**2 / obs_data) / num_obs

    return chi_square
	

#TODO: make function to filter results where slip rate is constant during accel


# fault history functions
def make_time_vector(time_start = 20., time_stop = 0., time_step = 0.01,
    decimals = 3):
    """Makes a vector of dates in the past.  Default is time range from 20 Ma
    to 0 Ma (present) with a 10 ky time step. Also rounds to specified decimals
    to avoid problems with floating point errors when indexing, default = 3.
    For shorter time steps, this should be changed.
     
    Returns time vector"""
    
	# make sure default args are floats
    time_start = nmp.float(time_start)
    time_stop = nmp.float(time_stop)
    time_step = nmp.float(time_step)
	
	# make vector of times (Ma)		
    num = ( (time_start - time_stop) / time_step) + 1
    time_vector = nmp.linspace(time_start, time_stop, num=num)
    
    # Rounds to specified precision
    time_vector = nmp.around(time_vector, decimals = decimals)    
    
    return time_vector


def make_slip_rate_w_time(init, accel, sr1, sr2, time_vector = 'None',
                          fault_stop = 0.):
    """Defines a slip rate history based on fault initiation, acceleration,
    and slip rate values.

    Returns vector of slip rates at specified time intervals.
    """

    # make a time vector with default values if one hasn't been made
    if time_vector == 'None':
    #print 'I am making a time vector for you but not giving it to you.'
	time_vector = make_time_vector()	
	
    # get indexes from time vector for where the rates change
    init_index = nmp.where(time_vector == init)
    init_index = int(init_index[0])
    accel_index = nmp.where(time_vector == accel)
    accel_index = int(accel_index[0])
    fs_index = nmp.where(time_vector == fault_stop)
    fs_index = int(fs_index[0])
	
    # make empty sr w/ time vector and fill it with rates
    slip_rate_w_time = nmp.zeros(len(time_vector))
    slip_rate_w_time[init_index : accel_index] = sr1
    slip_rate_w_time[accel_index : fs_index + 1] = sr2

    return slip_rate_w_time
	

def get_cum_vector(deform_rate_w_time, time_step = 0.01):
    """Makes vector of cumulative deformation.  Needs time step to normalize,
    defaults to 0.01 ka."""

    cum_vector = nmp.cumsum(deform_rate_w_time) * time_step
    cum_vector = nmp.hstack(([0.],cum_vector[:-1]))
    
    return cum_vector


def make_fault_params_array(input_array, init_col, accel_col, sr1_col,
                            sr2_col, stop_col = []):
    """Makes separate array of just the fault parameters for a single fault.
    Needs to be run for each fault.  These may then be concatenated.
    
    Indices:
    Init = 0
    accel = 1
    sr1 = 2
    sr2 = 3    
    """
    
    #TODO: generalize for more changes in slip rate
    
    init_column = input_array[:,init_col]
    accel_column = input_array[:,accel_col]
    sr1_column = input_array[:,sr1_col]
    sr2_column = input_array[:,sr2_col] 
    
    fault_params_array = nmp.hstack((init_column, accel_column, sr1_column,
                                     sr2_column))
    
    if stop_col != []:
    	stop_column = input_array[:,stop_col]
    	fault_params_array = nmp.hstack((fault_params_array, stop_column))
    	
    return fault_params_array

	
#def make_cum_array(



# plotting functions
def make_fault_histograms(fig, final_array, init_col, sr1_col, accel_col, sr2_col):
    fig = fig
    
    # initA
    ax1 = fig.add_subplot(221)
    bins = [7.5, 8.5, 9.5, 10.5, 11.5, 12.5, 13.5, 14.5, 15.5, 16.5, 17.5, 18.5]
    plt.hist(final_array[:,init_col], bins)
    plt.xlabel('initiation, Ma')
    
    # srA1
    ax2 = fig.add_subplot(222)
    bins = [-0.25, 0.25, 0.75, 1.25, 1.75, 2.25, 2.75, 3.25, 3.75, 4.25, 4.75,
            5.25, 5.75, 6.25, 6.75]
    plt.hist(final_array[:,sr1_col], bins)
    plt.xlabel('slip rate 1, mm/yr')
    
    # accel
    ax3 = fig.add_subplot(223)
    bins = [1.75, 2.25, 2.75, 3.25, 3.75, 4.25, 4.75, 5.25, 5.75, 6.25, 6.75]
    plt.hist(final_array[:,accel_col], bins)
    plt.xlabel('acceleration, Ma')

    # srA2
    ax4 = fig.add_subplot(224)
    bins = [0.25, 0.75, 1.25, 1.75, 2.25, 2.75, 3.25, 3.75, 4.25, 4.75, 5.25,
            5.75, 6.25, 6.75]
    plt.hist(final_array[:,sr2_col], bins)
    plt.xlabel('slip rate 2, mm/yr')
    
    return fig
    

def make_ext_histories(fig, transect, time_vector, er_w_time_array,
                              cum_ext_w_time_array, lcolor='k', lwidth=0.5):
    """Makes plots of extension rate and cumulative extension through time"""
    
    lc = lcolor
    lw = lwidth
    fig = fig
    #plt.title('extension histories, {0} transect'.format(transect))
    plt.subplots_adjust(hspace = 0.0001)
    
    # ext rate w/ time plot
    ax1 = fig.add_subplot(211)
    plt.plot(time_vector, er_w_time_array, color = lc, linewidth=lw)
    plt.gca().invert_xaxis()
    plt.ylim([0, 6])
    #plt.xlabel('time, Ma')
    plt.ylabel('extension rate, mm/a')
    
    # cumulative extension plot
    ax2 = fig.add_subplot(212, sharex=ax1)
    plt.plot(time_vector, cum_ext_w_time_array, color = lc, linewidth=lw)
    #plt.gca().invert_xaxis()
    plt.ylim([0, 25])
    plt.xlabel('time, Ma')
    plt.ylabel('cumulative extension, km')
    
    xticklabels = ax1.get_xticklabels()
    plt.setp(xticklabels, visible=False)
    
    
    return fig


def lon_elev_plots(fig, pred_ages, obs_ages, obs_err, 
                    lon, elev, symb_type = 'dot'):
    
    #red_ages = results_indices[results_array] #check on this
    
    fig.add_subplot(211)
    if symb_type == 'dot':
        plt.plot(lon, pred_ages, 'b.')
    elif symb_type == 'line':
    	plt.plot(lon, pred_ages, color = 'b')
    else:
    	print 'not a known plot type'
    
    plt.errorbar(lon, obs_ages, yerr = obs_err, fmt='o', color='k')
    plt.xlabel('longitude')
    plt.ylabel('Age (Ma)')
    
    
    fig.add_subplot(212)
    if symb_type == 'dot':
        plt.plot(pred_ages, elev, 'b.')
    elif symb_type == 'line':
    	plt.plot(pred_ages, elev, color = 'b')
    #else:
    #	print 'not a known plot type'   
    
    plt.errorbar(obs_ages, elev, xerr = obs_err, fmt='o', color='k')
    plt.xlabel('Age (Ma)')
    plt.ylabel('elev. (m)')
    
    return fig
    
    
