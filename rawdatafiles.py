# -*- coding: utf-8 -*-

import pandas as pd              # Package used to work with the raw data files
import re                        # Used to obtain the LM, RM and ES Times in the raw data files
#from os import listdir			 # Used to obtain the files in their directories
#from os.path import isfile, join # Also used to do file operations
from auxfcns import *			 # Contains openRawData used in openRawDataFiles



def openRawDataFiles(idPatient, op, test_op):
	#I should describe this function here

	#Creating a np array to later export all time arrays
	headerTimes = np.zeros((5,3))

	txtMid2 = 0	#Default state  
	txtMid3 = 0	#Default state  

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
		txtMid1, headerTimes[3] = openRawData(exams_path, 'LV', 'SL', '4CH')
		txtMid1 = syncStrain(txtMid1, headerTimes[0][2], headerTimes[3][2])

		txtMid2, headerTimes[4] = openRawData(exams_path, 'LA', 'SL', '2CH')
		txtMid2 = syncStrain(txtMid2, headerTimes[0][2], headerTimes[4][2])

	elif op == "3":
		# Left Atrium - Longitudinal Strain Rate
		txtMid1, headerTimes[3] = openRawData(exams_path, 'LA', 'SrL', '4CH')
		txtMid1 = syncStrain(txtMid1, headerTimes[0][2], headerTimes[3][2])

	elif op == "4":
		# Right Ventricle - Longitudinal Strain
		txtMid1, headerTimes[3] = openRawData(exams_path, 'RV', 'SL', '4CH')
		txtMid1 = syncStrain(txtMid1, headerTimes[0][2], headerTimes[3][2])

	else: # Left Ventricle - Longitudinal Strain Rate (obtained by the strain curves) 
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

	
"""
def openfiles(exams_path, op, test_op, AVCpatient):     #Script to open the raw data files exported from proprietary software

	#Lists used to store the values extracted from the raw data files
	LM_Time = []
	RM_Time = []
	ES_Time = []

	list_txtfiles = [f for f in listdir(exams_path) if isfile(join(exams_path, f))] #Lists the txt files in the directory pointed by exams_path

	if op == "1":                   #Strain LV, SR LV and ECG
		for f in list_txtfiles:     #Lists the txt files in the exams_path
			if ('4CH_SL_TRACE' in f) or ('4CH_SL4CH STRAIN_TRACE' in f) or ('4CH_Peak dose_SL_TRACE' in f):     #Looks for the 4CH strain file
				txt1=pd.read_csv(exams_path+'/'+f, sep='\t', engine='python', skiprows=3, index_col=0)          #Opens the 4CH strain file
			if ('4CH_SrL' in f) or ('4CH_SrL4CH SR LV_TRACE' in f) or ('4CH_SrL4CH SR_TRACE' in f) or ('4CH_Peak dose_SrL_TRACE' in f):
				txt_mid=pd.read_csv(exams_path+'/'+f, sep='\t', engine='python', skiprows=3, index_col=0)
				strain_rate_lv4ch = txt_mid                                                                      #Opens the 4CH SR file - Used in the first plot
			if ('2CH_SL_TRACE' in f) or ('2CH_SL2CH STRAIN_TRACE' in f) or ('2CH_Low dose_SL_TRACE' in f):
				txt2=pd.read_csv(exams_path+'/'+f, sep='\t', engine='python', skiprows=3, index_col=0)
			if ('APLAX_SL_TRACE' in f) or ('APLAX_SL3CH STRAIN_TRACE' in f) or ('APLAX_Low dose_SL_TRACE' in f):
				txt3=pd.read_csv(exams_path+'/'+f, sep='\t', engine='python', skiprows=3, index_col=0)

	elif op == "2":                                                                                                #Similar to the if above
		for f in list_txtfiles:
			if ('4CH_SL_TRACE' in f) or ('4CH_SL4CH STRAIN_TRACE' in f) or ('4CH_Peak dose_SL_TRACE' in f):
				txt1=pd.read_csv(exams_path+'/'+f, sep='\t', engine='python', skiprows=3, index_col=0)
			if ('4CH_SL4CH ATRIO ESQUERD_TRACE' in f) or ('4CH_Peak dose_SLLA_TRACE' in f):
				txt_mid=pd.read_csv(exams_path+'/'+f, sep='\t', engine='python', skiprows=3, index_col=0)
			if ('4CH_SrL' in f) or ('4CH_SrL4CH SR LV_TRACE' in f) or ('4CH_SrL4CH SR_TRACE' in f) or ('4CH_Peak dose_SrL_TRACE' in f):
				strain_rate_lv4ch=pd.read_csv(exams_path+'/'+f, sep='\t', engine='python', skiprows=3, index_col=0)
			if ('2CH_SL_TRACE' in f) or ('2CH_SL2CH STRAIN_TRACE' in f) or ('2CH_Low dose_SL_TRACE' in f):
				txt2=pd.read_csv(exams_path+'/'+f, sep='\t', engine='python', skiprows=3, index_col=0)
			if ('APLAX_SL_TRACE' in f) or ('APLAX_SL3CH STRAIN_TRACE' in f) or ('APLAX_Low dose_SL_TRACE' in f):
				txt3=pd.read_csv(exams_path+'/'+f, sep='\t', engine='python', skiprows=3, index_col=0)

	elif op == "3":                                                                                                 #Similar to the if above
		for f in list_txtfiles:
			if ('4CH_SL_TRACE' in f) or ('4CH_SL4CH STRAIN_TRACE' in f) or ('4CH_Peak dose_SL_TRACE' in f):
				txt1=pd.read_csv(exams_path+'/'+f, sep='\t', engine='python', skiprows=3, index_col=0)
			if '4CH_SrL4CH SR ATRIO_TRACE' in f:
				txt_mid=pd.read_csv(exams_path+'/'+f, sep='\t', engine='python', skiprows=3, index_col=0)
				strain_rate_lv4ch = txt_mid
			if ('4CH_SrL' in f) or ('4CH_SrL4CH SR LV_TRACE' in f) or ('4CH_SrL4CH SR_TRACE' in f) or ('4CH_Peak dose_SrL_TRACE' in f):
				strain_rate_lv4ch=pd.read_csv(exams_path+'/'+f, sep='\t', engine='python', skiprows=3, index_col=0)
			if ('2CH_SL_TRACE' in f) or ('2CH_SL2CH STRAIN_TRACE' in f) or ('2CH_Low dose_SL_TRACE' in f):
				txt2=pd.read_csv(exams_path+'/'+f, sep='\t', engine='python', skiprows=3, index_col=0)
			if ('APLAX_SL_TRACE' in f) or ('APLAX_SL3CH STRAIN_TRACE' in f) or ('APLAX_Low dose_SL_TRACE' in f):
				txt3=pd.read_csv(exams_path+'/'+f, sep='\t', engine='python', skiprows=3, index_col=0)

	elif op == "4":                                                                                                 #Similar to the if above
		for f in list_txtfiles:
			if ('4CH_SL_TRACE' in f) or ('4CH_SL4CH STRAIN_TRACE' in f) or ('4CH_Peak dose_SL_TRACE' in f):
				txt1=pd.read_csv(exams_path+'/'+f, sep='\t', engine='python', skiprows=3, index_col=0)
			if '4CH_SLVD_TRACE' in f:
				txt_mid=pd.read_csv(exams_path+'/'+f, sep='\t', engine='python', skiprows=3, index_col=0)
				strain_rate_lv4ch = txt_mid
			if ('4CH_SrL' in f) or ('4CH_SrL4CH SR LV_TRACE' in f) or ('4CH_SrL4CH SR_TRACE' in f) or ('4CH_Peak dose_SrL_TRACE' in f):
				strain_rate_lv4ch=pd.read_csv(exams_path+'/'+f, sep='\t', engine='python', skiprows=3, index_col=0)
			if ('2CH_SL_TRACE' in f) or ('2CH_SL2CH STRAIN_TRACE' in f) or ('2CH_Low dose_SL_TRACE' in f):
				txt2=pd.read_csv(exams_path+'/'+f, sep='\t', engine='python', skiprows=3, index_col=0)
			if ('APLAX_SL_TRACE' in f) or ('APLAX_SL3CH STRAIN_TRACE' in f) or ('APLAX_Low dose_SL_TRACE' in f):
				txt3=pd.read_csv(exams_path+'/'+f, sep='\t', engine='python', skiprows=3, index_col=0)

	elif op == "5":                                                                                         #Similar to the if above
		for f in list_txtfiles:
			if ('4CH_SL_TRACE' in f) or ('4CH_SL4CH STRAIN_TRACE' in f) or ('4CH_Peak dose_SL_TRACE' in f):
				txt1=pd.read_csv(exams_path+'/'+f, sep='\t', engine='python', skiprows=3, index_col=0)
			if ('2CH_SL_TRACE' in f) or ('2CH_SL2CH STRAIN_TRACE' in f) or ('2CH_Low dose_SL_TRACE' in f):
				txt2=pd.read_csv(exams_path+'/'+f, sep='\t', engine='python', skiprows=3, index_col=0)
			if ('APLAX_SL_TRACE' in f) or ('APLAX_SL3CH STRAIN_TRACE' in f) or ('APLAX_Low dose_SL_TRACE' in f):
				txt3=pd.read_csv(exams_path+'/'+f, sep='\t', engine='python', skiprows=3, index_col=0)

	elif op == test_op:                                                                                     #Here the simulations are opened
		for f in list_txtfiles:
			if '4CH_teste' in f:
				txt1=pd.read_csv(exams_path+'/'+f, sep='\t', engine='python', skiprows=3, index_col=0)
				txt_mid=txt1.diff()
			if '2CH_teste' in f:
				txt2=pd.read_csv(exams_path+'/'+f, sep='\t', engine='python', skiprows=3, index_col=0)
			if 'APLAX_teste' in f:
				txt3=pd.read_csv(exams_path+'/'+f, sep='\t', engine='python', skiprows=3, index_col=0)

	else:                                                                                                   #Default option, equal to op == 1
		for f in list_txtfiles:
			if '4CH_SL_TRACE' in f:
				txt1=pd.read_csv(exams_path+'/'+f, sep='\t', engine='python', skiprows=3, index_col=0)
			if '4CH_SrL4CH SR LV_TRACE' in f:
				txt_mid=pd.read_csv(exams_path+'/'+f, sep='\t', engine='python', skiprows=3, index_col=0)
				strain_rate_lv4ch = txt_mid
			if '2CH_SL_TRACE' in f:
				txt2=pd.read_csv(exams_path+'/'+f, sep='\t', engine='python', skiprows=3, index_col=0)
			if 'APLAX_SL_TRACE' in f:
				txt3=pd.read_csv(exams_path+'/'+f, sep='\t', engine='python', skiprows=3, index_col=0)


	for f in list_txtfiles:
		if ('4CH_SL_TRACE' in f) or ('4CH_SL4CH STRAIN_TRACE' in f) or ('4CH_Peak dose_SL_TRACE' in f) or ('4CH_teste' in f):
			txt_original = open(exams_path+'/'+f, 'r')
			numbers = re.findall("\d+\.\d+", txt_original.readlines()[2]) #Values are extracted from the line 3 of the txt file - LM_Time, ES_Time e RM_Time
			txt_original.close()
			LM_Time.append(float(numbers[0]))
			RM_Time.append(float(numbers[1]))
			ES_Time.append(float(numbers[2]))

	for f in list_txtfiles:
		if ('2CH_SL_TRACE' in f) or ('2CH_SL2CH STRAIN_TRACE' in f) or ('2CH_Low dose_SL_TRACE' in f) or ('2CH_teste' in f):
			txt_original = open(exams_path+'/'+f, 'r')
			numbers = re.findall("\d+\.\d+", txt_original.readlines()[2]) #Values are extracted from the line 3 of the txt file - LM_Time, ES_Time e RM_Time
			txt_original.close()
			LM_Time.append(float(numbers[0]))
			RM_Time.append(float(numbers[1]))
			ES_Time.append(float(numbers[2]))

	for f in list_txtfiles:
		if ('APLAX_SL_TRACE' in f) or ('APLAX_SL3CH STRAIN_TRACE' in f) or ('APLAX_Low dose_SL_TRACE' in f) or ('APLAX_teste' in f):
			txt_original = open(exams_path+'/'+f, 'r')
			numbers = re.findall("\d+\.\d+", txt_original.readlines()[2]) #Values are extracted from the line 3 of the txt file - LM_Time, ES_Time e RM_Time
			txt_original.close()
			LM_Time.append(float(numbers[0]))
			RM_Time.append(float(numbers[1]))
			ES_Time.append(float(numbers[2]))
	#Fim da abertura dos .txt

	txt1.drop('Unnamed: 1', axis=1, inplace=True) #Useless column is removed from the txt files
	txt2.drop('Unnamed: 1', axis=1, inplace=True)
	txt3.drop('Unnamed: 1', axis=1, inplace=True)
	if op != "5" and op != test_op:
		txt_mid.drop('Unnamed: 1', axis=1, inplace=True)
	#strain_rate_lv4ch.drop('Unnamed: 1', axis=1, inplace=True)

#Formats the raw data files
	#Syncs the ES_Times from the raw data files with the txt1
	txt2_mod=txt2.copy(deep=True)
	txt2_mod.index = txt2_mod.index-(ES_Time[1]-ES_Time[0])

	txt3_mod=txt3.copy(deep=True)
	txt3_mod.index = txt3_mod.index-(ES_Time[2]-ES_Time[0])


	if op == "5" or op == test_op:							#Obtains the SR from the strain curves if it's necessary
		txt_mid=txt1.diff()
		strain_rate_lv4ch = txt_mid.truediv(txt1.index.to_series().diff(), axis = 0)/100
	strain_rate_lv2ch = txt2_mod.diff().truediv(txt2_mod.index.to_series().diff(), axis = 0)/100
	strain_rate_lv3ch = txt3_mod.diff().truediv(txt3_mod.index.to_series().diff(), axis = 0)/100

	return txt1, txt2, txt3, txt_mid, txt2_mod, txt3_mod, strain_rate_lv4ch, strain_rate_lv2ch, strain_rate_lv3ch, LM_Time, RM_Time, ES_Time

"""