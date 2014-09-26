#!/usr/bin/env python

import sys
sys.path.append('/home/itchy/python_scripts')
import os, cloud, subprocess, time
import pecube_cloud_scripts_cctr as psc
reload(psc)

# important files
inputFile = '/home/picloud/src/Pecube/input/fault_parameters.txt'

outputFile = '/home/picloud/src/Pecube/input/fault_parameters.txt.out'

comparison_file = '/home/picloud/src/Pecube/cctrN/Comparison.txt'

obs = '/home/picloud/src/Pecube/cctrN/obs.txt'

# fault parameters

initFaultAs = [10.0, 11.0, 12.0, 13.0, 14.0, 15.0, 16.0, 17.0, 18.0] #, 19.0, 20.0]

accelFaults = [3.0, 4.0, 5.0, 6.0]

slipRate1FaultAs = [0.5, 1.0, 1.5, 2.0]

slipRate2FaultAs = [0.5, 1.0, 1.5, 2.0, 3.0]

initFaultBs = [10.0, 11.0, 12.0, 13.0, 14.0, 15.0, 16.0, 17.0, 18.0] #, 19.0, 20.0]

slipRate1FaultBs = [0.5, 1.0, 1.5, 2.0]

slipRate2FaultBs = [0.5, 1.0, 1.5, 2.0, 3.0]

#accelFaultBs = [3.0, 4.0, 5.0, 6.0]


# 	define constants (dipFaultA, dipFaultB)
dipFaultA = [0.88]

dipFaultB = [0.88]


#t0 = time.time()

#	define list of variable lists
faultParamsList = [[j, k, l, m, n, o, p] for j in initFaultAs for k in accelFaults for l in slipRate1FaultAs for m in slipRate2FaultAs for n in initFaultBs for o in slipRate1FaultBs for p in slipRate2FaultBs ]

#t1 = time.time()


#print t1-t0, 's to generate fault list'
# filter variables
faultParamsListFiltered = []

for faultParams in faultParamsList:

	[initA, accel, srA1, srA2, initB, srB1, srB2] = faultParams
	
	netExtension = psc.calcNetExtension(initA, accel, srA1, srA2, dipFaultA, initB, srB1, srB2, dipFaultB)

#print netExtension

	if netExtension < 10.5:
		if netExtension >10:
			
			faultParamsListFiltered.append(faultParams)
			
print len(faultParamsListFiltered)



def run_pecube_map(faultParamsListFiltered):
	[initA, accel, srA1, srA2, initB, srB1, srB2] = faultParamsListFiltered
	
	netExtension = psc.calcNetExtension(initA, accel, srA1, srA2, dipFaultA, initB, srB1, srB2, dipFaultB)
#	test for amount of extension (maybe do this with a filter function
#	or something similar when making the variable list)

#	modify input files, 
	psc.modifyInputFiles(initA, accel, srA1, srA2, initB, srB1, srB2, inputFile, outputFile)
	
	#rename fault parameters
	psc.renameFaultParams(inputFile, outputFile)

#	run pecube
	pecube_print = psc.run_pecube_cloud()
	
#	save output
	out_name = psc.save_output(comparison_file, initA, accel, srA1, srA2, initB, srB1, srB2)
	
#	calculate chi square
	chi_square = psc.calc_chi_square(obs, out_name)
	
#	append results to results file(s)	
	out_array = psc.append_info(out_name, chi_square, initA, accel, srA1, srA2, initB, srB1, srB2, netExtension)

	#cloud.files.get(out_array, '/home/itchy/src/Pecube/picloud/results/cctrN/{}'.format(out_array))
	
	return pecube_print
	
	
t0 = time.time()

pecube_cctr_105_10 = cloud.map(run_pecube_map, faultParamsListFiltered, _env='natty_itchy_pecube')



cloud.result(pecube_cctr_105_10)

#numpy_results_list = cloud.files.list()


print 'Pecube took', time.time() - t0, 'seconds for', len(faultParamsListFiltered), 'runs'

t1 = time.time()

for faultParams in faultParamsListFiltered:
	[initA, accel, srA1, srA2, initB, srB1, srB2] = faultParams
	filename = 'run_{}_{}_{}_{}_{}_{}_{}.npy'.format(initA, 
        accel, srA1, srA2, initB, srB1, srB2)
	cloud.files.get(filename, '/home/itchy/src/Pecube/picloud/results/cctrN/runs_16_15/{}'.format(filename))
	
print 'Done!  Picloud took', time.time()-t1, 'seconds to transfer files.'
