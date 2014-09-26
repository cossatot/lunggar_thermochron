# -*- coding: utf-8 -*-
"""
Created on Wed Jun 20 22:11:56 2012

@author: itchy
"""

import sys
sys.path.append('/home/itchy/python_scripts')
import cloud, time
import numpy as nmp
import pecube_scripts_nlrT2 as psc

inputFile = '/home/picloud/src/Pecube/input/fault_parameters.txt'

outputFile = '/home/picloud/src/Pecube/input/fault_parameters.txt.out'

comparison_file = '/home/picloud/src/Pecube/nlrT2/Comparison.txt'


# fault parameters

initFaultAs = [8.0, 9.0, 10.0, 11.0, 12.0, 13.0, 14.0, 15.0, 16.0, 17.0, 18.0] #, 19.0, 20.0]

accelFaults = [2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0, 7.5]
#accelFaults = [3.0, 4.0, 5.0] #, 6.0, 7.0, 8.0]


slipRate1FaultAs = [0., 0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5]

slipRate2FaultAs = [0.5, 0.75, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5]

dipFaultA = [0.4716]

faultParamsList = [[j, k, l, m] for j in initFaultAs for k in accelFaults for l in slipRate1FaultAs for m in slipRate2FaultAs]

faultParamsListFiltered = []

for faultParams in faultParamsList:

    [initA, accel, srA1, srA2] = faultParams
    netExtension = psc.calcNetExtension(initA, accel, srA1, srA2, dipFaultA)    
    if netExtension < 18:
        if netExtension >13:
            faultParamsListFiltered.append(faultParams)
            

print len(faultParamsList), 'total params'

print len(faultParamsListFiltered), 'filtered params'            

def run_pecube_map(faultParamsListFiltered):    
    [initA, accel, srA1, srA2] = faultParamsListFiltered
    
    netExtension = psc.calcNetExtension(initA, accel, srA1, srA2, dipFaultA)
    
    psc.modifyInputFiles(initA, accel, srA1, srA2, inputFile, outputFile)
    
    psc.renameFaultParams(inputFile, outputFile)
    
    pecube_print = psc.run_pecube_cloud()
    
    out_name = psc.save_output(comparison_file, initA, accel, srA1, srA2)
    
    out_array_name = psc.append_info(out_name, initA, accel, srA1, srA2, netExtension)				
    
    #cloud.files.get(out_array_name, '/home/itchy/src/Pecube/nlrT2/picloud/{}'.format(out_array_name))
    #cloud.files.get(out_array_name)
    
    return out_array_name
    
    

t0 = time.time()

pecube_nlrT2_fixed_runs = cloud.map(run_pecube_map, faultParamsListFiltered,
                                    _env='nlr_pecube_clone2')

nlrT2_fixed_runs = cloud.result(pecube_nlrT2_fixed_runs)


print 'Pecube took', time.time() - t0, 'seconds for', len(faultParamsListFiltered), 'runs'

#t1 = time.time()
#pecube_nlrT2_files = cloud.map(get_files_map, faultParamsListFiltered)

