#!/usr/bin/env python

import numpy as nmp
import subprocess, os, cloud


def calcNetExtension(initA, accel, srA1, srA2, dipFaultA, initB, srB1, srB2, dipFaultB):
	"""
	imports fault slip information and indicates whether net slip is
	under 25 km
	"""
	# fault A extension
	slipA1 = (initA - accel) * srA1
	
	slipA2 = accel * srA2
	
	netSlipA = slipA1 + slipA2
	
	netExtensionA = netSlipA * nmp.cos(dipFaultA)
	
	#fault B extension
	slipB1 = (initB - accel) * srB1
	
	slipB2 = accel * srB2
	
	netSlipB = slipB1 + slipB2
	
	netExtensionB = netSlipB * nmp.cos(dipFaultB)	

	
	# total extension
	
	netExtension = netExtensionA + netExtensionB
	
	return netExtension

######################################################################################
	

def modifyInputFiles(initA, accel, srA1, srA2, initB, srB1, srB2, inputFile, outputFile):
    """
    take Pecube input files and modify parameters based on 
    the loop inputs from main script
    """
    #print 'writing input files'
    
    paramLineFaultA1 = 27  #line numbers for fault inputs
	
    paramLineFaultA2 = 28
	
    paramLineFaultB1 = 58
    
    paramLineFaultB2 = 59
    
    # modifications to fault A1
    datamod1 = '{} '.format(initA)
    datamod2 = '{} '.format(accel)
    datamod3 = '{} \n'.format(srA1)
    
    # modifications to fault A2
    datamod4 = '{} '.format(accel)
    datamod5 = '0. '
    datamod6 = '{} \n'.format(srA2)
    
    # modifications to fault B    
    datamod7 = '{} '.format(initB)
    datamod8 = '{} '.format(accel)
    datamod9 = '{} \n'.format(srB1)
    
    # modifications to fault B    
    datamod10 = '{} '.format(accel)
    datamod11 = '0. '
    datamod12 = '{} \n'.format(srB2)    
    
    
    start_point = 0   # start_point = len('-1.00 -1.00 -1.00 ')  

    inputFile = open(inputFile, 'r')
 
    outputFile = open(outputFile, 'w+')

    lineno = 0              # line tracker

    while 1: 
    
        line = inputFile.readline()  # grab a line
	
        if not line: break	 # end of file reached	
		
        lineno = lineno + 1          # current working line
   	
        if lineno == paramLineFaultA1:     # are we there yet?

            # here's the working bit that makes the sustitution.

            modifiedline = line[:start_point] + datamod1 + datamod2 + datamod3
           
            outputFile.write(modifiedline)
    	     
        elif lineno == paramLineFaultA2:
            
            modifiedline = line[:start_point] + datamod4 + datamod5 + datamod6
            
            outputFile.write(modifiedline)
        
        elif lineno == paramLineFaultB1:
            
            modifiedline = line[:start_point] + datamod7 + datamod8 + datamod9
            
            outputFile.write(modifiedline)              
                    
        elif lineno == paramLineFaultB2:
            
            modifiedline = line[:start_point] + datamod10 + datamod11 + datamod12
            
            outputFile.write(modifiedline)       
        
        else:
 
            outputFile.write(line)      # copy line as it is into temp file
			
             
 		
    inputFile.close()                   # done with it.
 
    outputFile.close()                  # rename afterward with the original name
    
    #print 'done writing'    
    
    #return(inputFile, outputFile)
	
	
	
####################################################################################

def renameFaultParams(inputFile, outputFile):
    """
    replace old inputfile with new outputfile via calling bash
    """
    #print 'replacing files'        
    subprocess.call("cp {} {}".format(outputFile, inputFile), shell=True)
    #print 'done'


#################################################################################

def runPecube():
    
    #print 'running Pecube'
    subprocess.call("bin/Pecube", shell=True)
    #print 'done with Pecube'


################################################################################    
    

def save_output(comparison_file, initA, accel, srA1, srA2, initB, srB1, srB2):
    
    #print 'saving output'    
    
    out_name = '/home/picloud/src/Pecube/cctrN/pred_{}_{}_{}_{}_{}_{}_{}.txt'.format(initA, 
        accel, srA1, srA2, initB, srB1, srB2)
    
    file_out = open(out_name, 'w+')
    
    comparison_file = open(comparison_file, 'r')
    
    lines = comparison_file.readlines()
    
    comparison_file.close()
    
    new_file = open('/home/picloud/src/Pecube/cctrN/new_file2.txt', 'w+')
    
    new_file.writelines([item for item in lines[1:]])
    
    new_file.close()

    new_file = open('/home/picloud/src/Pecube/cctrN/new_file2.txt', 'r')
	
    column = 9
    
    for line in new_file:
        
        line = line.strip()
        sline = line.split()
        file_out.write(sline[column] + '\n')
        
    new_file.close()
        
    file_out.close()
       
    #print 'done'
    
    return out_name
    
    
    
################################################################################


def calc_chi_square(obs, out_name):
    
    #print 'calculating chi square misfit'

    zHe_predicted = nmp.loadtxt(open(out_name))
    
    zHe_observed = nmp.loadtxt(open(obs))
    
    chi_square = sum((zHe_observed - zHe_predicted)**2 / zHe_observed) / 8
    
    #print 'done'
    
    return chi_square
    
################################################################################


def append_info(out_name, chi_square, initA, accel, srA1, srA2, initB, srB1, srB2, netExtension):
    
    #print 'making numpy matrices'

    in_array = nmp.loadtxt(open(out_name))
    
    out_array = '/home/picloud/src/Pecube/cctrN/run_{}_{}_{}_{}_{}_{}_{}.npy'.format(initA, 
        accel, srA1, srA2, initB, srB1, srB2)
        
    nmp.save(out_array, in_array)
    
    out_array_temp = nmp.load(out_array)
    
    out_array_temp = nmp.append(out_array_temp, [initA, accel, srA1, srA2, initB, srB1, srB2, chi_square, netExtension])
        
    nmp.save(out_array, out_array_temp)
    
    cloud.files.put(out_array)
    
    return out_array
    
    #print 'done'
    
################################################################################

def change_directory():
	subprocess.call("cd /home/picloud/src/Pecube", shell=True)
	directory = subprocess.call("pwd", shell=True)
	print directory
	
	
################################################################################

def change_dir_python():
	os.chdir('/home/picloud/src/Pecube')

	
################################################################################

def mkdir_test(test_dir):
	subprocess.call('mkdir {}'.format(test_dir), shell=True)
	
	

################################################################################

#def dir_list(natty_path):

def run_pecube_cloud():
	#os.chdir('/home/picloud/src/Pecube')
	pecube_print = subprocess.check_output("cd /home/picloud/src/Pecube && bin/Pecube", shell=True)
	return pecube_print
	
################################################################################

def dir_list():
	os.chdir('/home/picloud/src/Pecube/input/')
	dirlist = os.listdir(os.getcwd() )
	return dirlist
	
	
    
