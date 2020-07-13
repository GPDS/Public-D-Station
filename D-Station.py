# -*- coding: utf-8 -*-

#Importing packages...
import pandas as pd              # Package used to work with the raw data files
import os						 # Package used to determine whether the user is using windows or linux to erase the console
import numpy as np
#

#Packages that i (https://github.com/rafaelds9) created
from auxfcns import *
from dstationplotlib import *
from dstationparameters import *
from rawdatafiles import *
from printFcns import *
#

#Importing configuration
import configparser

config = configparser.ConfigParser()
config.read('config.ini')	

# Reading variables from config file
test_op = str(config['default']['test_op'])
#



#Initializing variables (default values)
linePatient = 3   #Defines the first row in the xl file that has values
prmt = '0' #Defines the prmt value in the first run to 0 - Change with caution
#


#MAIN
os.system('cls' if os.name == 'nt' else 'clear') # Clears the terminal


idPatient = input('Patient ID: ')
print("Options:\n\t1. Strain LV, Strain Rate LV and ECG\n\t2. Strain LV, Strain LA and ECG")
print("\t3. Strain LV, Strain Rate LA and ECG\n\t4. Strain LV, Strain RV and ECG")
print("\t5. Strain LV, Strain Rate LV and ECG (without SR files)\n\t"+test_op+". Test Option")
op = input("Option: ")


# Used to debug - comment the corresponding line in the block above
#idPatient = 'Aristoteles'
#op = "5"					

#Opens the raw data files and assigns them to dataframes
#Header times are assigned to a numpy array
txt1, txt2, txt3, txtMid, txtMid2, txtMid3, strain_rate_lv4ch, strain_rate_lv2ch, strain_rate_lv3ch, headerTimes = openRawDataFiles(idPatient, op)


# Opens the spreadsheet with the valve times and reads the line corresponding to the patient 
sheet, linePatient, wb = openSheet('Patients_DB.xlsx', idPatient)


# Checks whether the ECG points were already selected
# if so allow the user to verify or chenge them
# if not selected opens a plot for their selection
verifyECG(txt1, strain_rate_lv4ch, headerTimes[0], sheet, linePatient, op, None)


# Reads the valve tto select themimes from the spreadsheet
valveTimes = valveTimesRead(headerTimes,sheet,linePatient)


#If not a simulation, the heart phases are determined
if op != test_op: 
	phasesTimes, LAphasesTimes = phaseSeg(valveTimes, sheet, linePatient)


#Now everything is printed

# Clears the terminal
os.system('cls' if os.name == 'nt' else 'clear') 

print("Patient: ", idPatient )
print("\nLM_Time: ", headerTimes[0][0]*1000, "ms")
print("RM_Time: ", headerTimes[0][1]*1000, "ms")


printValveTimes(valveTimes)


if op != test_op:
	printPhaseTimes(phasesTimes)

	if op == "2" or op == "3":
		printLAPhaseTimes(LAphasesTimes)
else:
	phasesTimes = np.zeros([9])
	LAphasesTimes = np.zeros([3])



systolicTime = (valveTimes[0][3]-valveTimes[0][1])

print("\nSystolic Time: ", round(systolicTime*1000,1))
print("Diastolic Time: ", round((headerTimes[0][1] - systolicTime)*1000),1)
print("Systolic Time/Diastolic Time ratio: ",round((systolicTime/(headerTimes[0][1] - systolicTime)),1))


outGLS = GLS_calc(txt1, txt2, txt3, op, prmt, phasesTimes, valveTimes)
outMD = MD_calc(txt1, txt2, txt3, op, prmt, phasesTimes, valveTimes)


if(op != test_op):
	averageLongStrain = avgPhaseStrainVar(txt1, txt2, txt3, op, phasesTimes)
else:
	print("\nPhase segmentation was not performed, therefore you cannot calculate the average strain variation per phase")
	

#Loop where the user can select the parmeters and plots he wishes to see
while True: 		
	
	print("\n\nParameters:\n\t1. Global Longitudinal Strain\n\t2. Mechanical Dispersion")
	print("\t3. Average Strain variation during each phase")
	print("\t4. Show plot w/o any parameters\n\t5. Show additional parameters values\n\t0. Terminate program")
	prmt = input("Parameter: ")
	

	#DEBUG - Comment the block above and uncomment the line below
	#prmt = '2' 

	#Calculates the GLS
	if prmt == "1":               
		_,_,_,_,gls_values = GLS_calc(txt1, txt2, txt3, op, prmt, phasesTimes, valveTimes)
		POIPlot(txt1, txt2, txt3, txtMid, strain_rate_lv4ch, strain_rate_lv2ch, strain_rate_lv3ch, prmt, op, valveTimes, phasesTimes, LAphasesTimes, outGLS, True)
		
		#Comment the line below after debug
		#print(gls_values) 			
		
		DR_bullseye(gls_values, op, prmt)
		#Comment the line below after debug
		#break 

	#Calculates the MD
	elif prmt == "2":			  
		_,_,_,_,md_values = MD_calc(txt1, txt2, txt3, op, prmt, phasesTimes, valveTimes)
		POIPlot(txt1, txt2, txt3, txtMid, strain_rate_lv4ch, strain_rate_lv2ch, strain_rate_lv3ch, prmt, op, valveTimes, phasesTimes, LAphasesTimes, outMD, True)
		#Comment the line below after debug
		#print(md_values) 
		
		DR_bullseye(md_values, op, prmt)
		
		#Comment the line below after debug
		#break 

	elif prmt == "3":
		if(op != test_op):
			avgPhaseStrainVarPlot(txt1, txt2, txt3, txtMid, op, averageLongStrain, valveTimes, phasesTimes, True)
		else:
			print("\nPhase segmentation was not performed, therefore you cannot calculate the phase strain variation")
		
		#Comment the line below after debug
		#break

	elif prmt == "4":
		print("\nPlot w/o any parameters")
		POIPlot(txt1, txt2, txt3, txtMid, strain_rate_lv4ch, strain_rate_lv2ch, strain_rate_lv3ch, prmt, op, valveTimes, phasesTimes,  LAphasesTimes, None, True)
		
		#Comment the line below after debug
		#break

	elif prmt == "5":
		moreInfo(linePatient)

	elif prmt == "0":
		break

	else:
		print("\n\nInvalid option\n\n\n")
		continue
	print("\n")


saveAndCloseSheet(linePatient, sheet, wb, headerTimes, phasesTimes, systolicTime, outGLS, outMD)
#print("\n\nRan successfully\n")