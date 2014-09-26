
import sys
sys.path.append('/home/itchy/python_scripts')
import cloud, time
import numpy as nmp
import pecube_scripts_nlrT4 as psc

inputFile = '/home/picloud/src/Pecube/input/fault_parameters.txt'

outputFile = '/home/picloud/src/Pecube/input/fault_parameters.txt.out'

comparison_file = '/home/picloud/src/Pecube/nlrT4/Comparison.txt'


# fault parameters

initFaultAs = [5.0, 5.5, 6.0, 6.5, 7.0]
#[8.0, 9.0, 10.0, 12.0, 14.0]#, 16.0]#, 16.0, 17.0, 18.0]

initFaultBs = [5.0, 6.0, 7.0]
#[8.0, 9.0, 10.0, 12.0, 14.0]#, 16.0]#, 16.0, 17.0, 18.0]

accelFaults = [2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5]#, 6.0]
#accelFaults = [3.0, 4.0, 5.0] #, 6.0, 7.0, 8.0]


slipRate1FaultAs = [0., 0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0]#, 1.5, 2.0, 2.5, 3.0, 3.5]

slipRate2FaultAs = [0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0]#, 5.0]

slipRate1FaultBs = [0., 0.25, 0.5, 0.75, 1.0]#, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0]#, 1.5, 2.0, 2.5, 3.0, 3.5]

slipRate2FaultBs = [0.25, 0.5, 0.75, 1.0]#, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0]#, 3.0]#, 4.0, 5.0]



dipFaultA = [0.84]

dipFaultB = [0.93]

t0 = time.time()

faultParamsList = [[j, k, l, m, n, o, p] for j in initFaultAs for k in initFaultBs for l in accelFaults for m in slipRate1FaultAs for n in slipRate2FaultAs for o in slipRate1FaultBs for p in slipRate2FaultBs]

t1 = time.time()

print t1-t0, 's to generate fault list'
print len(faultParamsList)



# filter variables
faultParamsListFiltered = []
nlrT4_run_list = []

for faultParams in faultParamsList:

	[initA, initB, accel, srA1, srA2, srB1, srB2] = faultParams
	
	netExtensionA = psc.calcNetExtension(initA, accel, srA1, srA2, dipFaultA)
	
	netExtensionB = psc.calcNetExtension(initB, accel, srB1, srB2, dipFaultB)
	
	netExtension = netExtensionA + netExtensionB

#print netExtension

	if 5 < netExtension < 7.5 and initA > accel and initB > accel and srB1 == srB2:
		
		faultParamsListFiltered.append(faultParams)
		run_name = 'nlrT4_{}_{}_{}_{}_{}_{}_{}.npy'.format(initA, initB, accel, srA1, srA2, srB1, srB2)
		nlrT4_run_list.append(run_name)


t2 = time.time()
print t2-t1, 's to cut list to', len(faultParamsListFiltered), 'items'

def run_pecube_map(faultParamsListFiltered):    
    [initA, initB, accel, srA1, srA2, srB1, srB2] = faultParamsListFiltered
    
    #netExtension = psc.calcNetExtension(initA, accel, srA1, srA2, dipFaultA)
    netExtensionA = psc.calcNetExtension(initA, accel, srA1, srA2, dipFaultA)
    netExtensionB = psc.calcNetExtension(initB, accel, srB1, srB2, dipFaultB)
    netExtension = netExtensionA + netExtensionB
	
    psc.modifyInputFiles(initA, initB, accel, srA1, srA2, srB1, srB2, inputFile,
                         outputFile)
    
    psc.renameFaultParams(inputFile, outputFile)
    
    pecube_print = psc.run_pecube_cloud()
    
    out_name = psc.save_output(comparison_file, initA, initB, accel, srA1,
                               srA2, srB1, srB2, netExtension)
    
    out_array_name = psc.append_info(out_name, initA, initB, accel, srA1, srA2,
                                     srB1, srB2, netExtension)				

    return out_array_name
   

t3 = time.time()

#pecube_nlrT4_runs_decel = cloud.map(run_pecube_map, faultParamsListFiltered,
#                              _env='nlr_pecube_clone2')
                              
#run_list = cloud.result(pecube_nlrT4_runs_decel)


print 'Pecube took', time.time() - t3, 'seconds for', len(faultParamsListFiltered), 'runs'

