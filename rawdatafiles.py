# -*- coding: utf-8 -*-

import pandas as pd              # Package used to work with the raw data files
import re                        # Used to obtain the LM, RM and ES Times in the raw data files
from auxfcns import *			 # Contains openRawData used in openRawDataFiles


#Importing configuration
import configparser
config = configparser.ConfigParser()
config.read('config.ini')


def openRawDataFiles(idPatient, op):
	#I should describe this function here

	test_op = str(config['default']['test_op'])


	#Creating a np array to later export all time arrays
	headerTimes = np.zeros((5,3))

	#Default state for the txtMids 
	txtMid2 = 0	 
	txtMid3 = 0

	#Checks if the file is on the patient's or simulation' directory
	if op != test_op:					 
		exams_path = ('Patients/'+idPatient)
	else:
		exams_path = ('Simulations/'+idPatient)


	#Left Ventricle - Longitudinal Strain
	txt1, headerTimes[0] = openRawData(exams_path, 'LV', 'SL', '4CH')

	txt2, headerTimes[1] = openRawData(exams_path, 'LV', 'SL', '2CH')
	txt2 = syncStrain(txt2, headerTimes[0][2], headerTimes[1][2])

	txt3, headerTimes[2] = openRawData(exams_path, 'LV', 'SL', 'APLAX')
	txt3 = syncStrain(txt3, headerTimes[0][2], headerTimes[2][2])


	if op == "1":
		#Left Ventricle - Longitudinal Strain Rate
		txtMid1, headerTimes[3] = openRawData(exams_path, 'LV', 'SrL', '4CH')
		txtMid1 = syncStrain(txtMid1, headerTimes[0][2], headerTimes[3][2])

	elif op == "2":
		# Left Atrium - Longitudinal Strain
		txtMid1, headerTimes[3] = openRawData(exams_path, 'LA', 'SL', '4CH')
		txtMid1 = syncStrain(txtMid1, headerTimes[0][2], headerTimes[3][2])

		#txtMid2, headerTimes[4] = openRawData(exams_path, 'LA', 'SL', '2CH')
		#txtMid2 = syncStrain(txtMid2, headerTimes[0][2], headerTimes[4][2])

	elif op == "3":
		# Left Atrium - Longitudinal Strain Rate
		txtMid1, headerTimes[3] = openRawData(exams_path, 'LA', 'SrL', '4CH')
		txtMid1 = syncStrain(txtMid1, headerTimes[0][2], headerTimes[3][2])

	elif op == "4":
		# Right Ventricle - Longitudinal Strain
		txtMid1, headerTimes[3] = openRawData(exams_path, 'RV', 'SL', '4CH')
		txtMid1 = syncStrain(txtMid1, headerTimes[0][2], headerTimes[3][2])

	
	else: 
		# Left Ventricle - Longitudinal Strain Rate (obtained by the strain curves) 
		#(forCircAdapt simulations or default case)
		if op != "5" and op != test_op:
			print("Invalid Option. Using default option (5)\n\n") 

		txtMid1 = txt1.truediv(txt1.index.to_series().diff(), axis = 0)/100
		txtMid2 = txt2.diff().truediv(txt2.index.to_series().diff(), axis = 0)/100
		txtMid3 = txt3.diff().truediv(txt3.index.to_series().diff(), axis = 0)/100

		print("\nImportant: Obtaining Strain Rate curves by the differences between strain points\n")


	#Estimates SR to use in the first plot (POI selection)
	txtSRLV4CH = txt1.truediv(txt1.index.to_series().diff(), axis = 0)/100 
	txtSRLV2CH = txt2.truediv(txt1.index.to_series().diff(), axis = 0)/100 
	txtSRLVAPLAX = txt3.truediv(txt1.index.to_series().diff(), axis = 0)/100


	return txt1, txt2, txt3, txtMid1, txtMid2, txtMid3, txtSRLV4CH, txtSRLV2CH, txtSRLVAPLAX, headerTimes 