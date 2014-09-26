#!/usr/bin/env python

import sys
sys.path.append('/home/itchy/python_scripts')
import os, cloud, subprocess, time
import pecube_cloud_scripts as psc
reload(psc)

# important files
inputFile = '/home/picloud/src/Pecube/input/fault_parameters.txt'

outputFile = '/home/picloud/src/Pecube/input/fault_parameters.txt.out'

comparison_file = '/home/picloud/src/Pecube/nmtN5/Comparison.txt'

obs = '/home/picloud/src/Pecube/nmtN5/obs.txt'

# fault parameters

initFaultAs = [9.0] #, 10.0, 11.0, 12.0, 13.0, 14.0, 15.0, 16.0, 17.0, 18.0, 19.0, 20.0]

#initFaultAs = [12.0, 9.0]

accelFaultAs = [2.0] #, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.5]

#accelFaultAs = [2.0]

slipRate1FaultAs = [0.25] #, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5]

slipRate2FaultAs = [1.5] #, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5]

initFaultBs = [10.0] #, 12.0, 14.0, 16.0, 18.0, 20.0]

slipRateFaultBs = [0.5] #, 1.0, 1.5, 2.0]

# define constants (dipFaultA, dipFaultB)

dipFaultA = [0.4]

dipFaultB = [0.88]

#	define list of variable lists
faultParamsList = [[j, k, l, m, n, o] for j in initFaultAs for k in accelFaultAs for l in slipRate1FaultAs for m in slipRate2FaultAs for n in initFaultBs for o in slipRateFaultBs]


faultParamsListFiltered = []

for faultParams in faultParamsList:

	[initA, accelA, srA1, srA2, initB, srB] = faultParams
	
	netExtension = psc.calcNetExtension(initA, srA1, accelA, srA2, dipFaultA, initB, srB, dipFaultB)

#print netExtension

	if netExtension < 20:
		if netExtension > 12:
			
			faultParamsListFiltered.append(faultParams)

print len(faultParamsListFiltered)

def run_pecube_map(faultParamsListFiltered):
	[initA, accelA, srA1, srA2, initB, srB] = faultParamsListFiltered
	
	netExtension = psc.calcNetExtension(initA, srA1, accelA, srA2, dipFaultA, initB, srB, dipFaultB)
#	test for amount of extension (maybe do this with a filter function
#	or something similar when making the variable list)

#	modify input files, 
	psc.modifyInputFiles(initA, srA1, accelA, srA2, initB, srB, inputFile, outputFile)
	
	#rename fault parameters
	psc.renameFaultParams(inputFile, outputFile)

#	run pecube
	pecube_print = psc.run_pecube_cloud()
	
#	save output
	out_name = psc.save_output(comparison_file, initA, srA1, accelA, srA2, initB, srB)
	
#	calculate chi square
	chi_square = psc.calc_chi_square(obs, out_name)
	
#	append results to results file(s)	
	out_array = psc.append_info(out_name, chi_square, initA, srA1, accelA, srA2, initB, srB, netExtension)

	#cloud.files.get(out_array, '/home/itchy/src/Pecube/picloud/results/nmtN5/{}'.format(out_array))
	
	return pecube_print
	
	
t0 = time.time()

pecube_nmt_112 = cloud.map(run_pecube_map, faultParamsListFiltered, _env='natty_itchy_pecube', _type='c2')



cloud.result(pecube_nmt_112)

numpy_results_list = cloud.files.list()


print 'Pecube took', time.time() - t0, 'seconds for', len(faultParamsListFiltered), 'runs'



for numpy_result in numpy_results_list:
	cloud.files.get(numpy_result, '/home/itchy/src/Pecube/picloud/results/nmtN5/{}'.format(numpy_result))

	

