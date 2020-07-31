# -*- coding: utf-8 -*-

# A package created for the D-Station (https://gpdsifpb.github.io/D-Station/)
# containing the functions used to calculate its parameters


import pandas as pd			# Package used to work with the raw data files (Used in GLS_calc, MD_calc, IVA_calc)
import numpy as np			# Used in the mean and standard deviance calculation (GLS_calc and MD_calc)
import openpyxl				# Used in the moreInfo function
import string				# Used in the moreInfo function

from auxfcns import *

#Importing configuration
import configparser
config = configparser.ConfigParser()
config.read('config.ini')

# Reading variables from config file
test_op = str(config['default']['test_op'])


onlyNEG = 1  #control - to use only the negative peaks in peak detection


def valveTimesRead(headerTimes, sheet, linePatient):

	valveTimes = np.zeros((2,4))

	AVC_sheet = int(sheet['T'+str(linePatient)].value)/1000
	auxSheet = np.array(['Q','R','S','T'])
	for it_row in range(2):
		for it_col in range(4):
			if it_row == 0 and it_col == 3:
				valveTimes[it_row][it_col] = headerTimes[0][2]
			elif it_row == 0:
				valveTimes[it_row][it_col] = round((int(sheet[auxSheet[it_col]+str(linePatient)].value)/1000)+(headerTimes[0][2]-AVC_sheet),3)
			else:
				valveTimes[it_row][it_col] = round((int(sheet[auxSheet[it_col]+str(linePatient)].value)/1000)+(headerTimes[0][2]-AVC_sheet+headerTimes[0][1]),3)
	
	return valveTimes



def phaseSeg(valveTimes, sheet, linePatient):

	phasesTimes = np.zeros(9) #Creates the array to store these values
	LAPhasesTimes = np.zeros(3)


	phasesTimes[0]=(int(sheet['U'+str(linePatient)].value)/1000)	#EMC1 = Onset QRS 1(ms)/1000
	phasesTimes[1]=valveTimes[0][1]         						#IVC1 = MVC(ms)/1000 + LM_Time
	phasesTimes[2]=valveTimes[0][2] 								#EjectionTime1 = AVO(ms)/1000 + LM_Time
	phasesTimes[3]=valveTimes[0][3]           						#IVR = AVC(ms)/1000 + LM_Time
	phasesTimes[4]=valveTimes[0][0]             					#E = MVO(ms)/1000 + LM_Time
	phasesTimes[5]=(int(sheet['V'+str(linePatient)].value)/1000)    #A = Onset P(ms)/1000
	phasesTimes[6]=(int(sheet['W'+str(linePatient)].value)/1000)    #EMC2 = Onset QRS 2(ms)/1000
	phasesTimes[7]=valveTimes[1][1]          						#IVC2 = MVC(ms)/1000 + RM_Time
	phasesTimes[8]=valveTimes[1][2] 								#EjectionTime2 = AVO(ms)/1000 + RM_Time
	
	LAPhasesTimes[0]=phasesTimes[1] 
	LAPhasesTimes[1]=phasesTimes[4]
	LAPhasesTimes[2]=phasesTimes[5]
	

	return phasesTimes, LAPhasesTimes



#Colocar no valveTimes headers do circadapt

#Calculates the Global Longitudinal Strain of from the LV Strain curves = mean of the peak systolic strain of all curves
def GLS_calc(txt1, txt2, txt3, op, prmt, phasesTimes, valveTimes):

	#Checks the ammount of columns in the dataframe
	tcolunas1 = txt1.shape[1]			
	tcolunas2 = txt2.shape[1]		
	tcolunas3 = txt3.shape[1]		
	

	if op != test_op:
		#If it's a real patient - slices from the EMC until the AVC from the raw data files
		txt1_s = txt1[(txt1.index >= phasesTimes[0]) & (txt1.index <= valveTimes[0][3])]		
		txt2_s = txt2[(txt2.index >= phasesTimes[0]) & (txt2.index <= valveTimes[0][3])]
		txt3_s = txt3[(txt3.index >= phasesTimes[0]) & (txt3.index <= valveTimes[0][3])]
	else: 
		txt1_s = txt1[(txt1.index >= 0) & (txt1.index <= valveTimes[0][3])]		
		txt2_s = txt2[(txt2.index >= 0) & (txt2.index <= valveTimes[0][3])]
		txt3_s = txt3[(txt3.index >= 0) & (txt3.index <= valveTimes[0][3])]

	#Shows detailed info about the GLS
	if prmt == '1':																	
		print("\n\nPeak systolic strain:\n")
	

	#List that stores the peak systolic points
	gls = []																		
	
	colours=list(txt2_s)

	#auxiliates the function segmentName below
	chamber = '2CH' 
	for colour_it in range(0,tcolunas2-2):
		if(round(txt2_s[colours[colour_it]].max(),2) < (-0.75*(round(txt2_s[colours[colour_it]].min(),2)))) or onlyNEG:
			if prmt == '1':
				print("\t[NEG] 2CH:", segmentName(colours[colour_it],chamber, op),":",round(txt2_s[colours[colour_it]].min(),2),"%","\t","Time:",round(txt2_s[colours[colour_it]].idxmin(),3),"s")
			gls.append(txt2_s[colours[colour_it]].min())								#Peak systolic points in 2CH are appended to list
		else:
			if prmt == '1':
				print("\t[POS] 2CH:", segmentName(colours[colour_it],chamber, op),":",round(txt2_s[colours[colour_it]].max(),2),"%","\t","Time:",round(txt2_s[colours[colour_it]].idxmax(),3),"s")
			gls.append(txt2_s[colours[colour_it]].max())								#Peak systolic points in 2CH are appended to list

	if prmt == '1':
		print("\n")

	colours=list(txt1_s)
	chamber = '4CH'

	for colour_it in range(0,tcolunas1-2):
		if(round(txt1_s[colours[colour_it]].max(),2) < (-0.75*(round(txt1_s[colours[colour_it]].min(),2)))) or onlyNEG:
			if prmt == '1':
				print("\t[NEG] 4CH:", segmentName(colours[colour_it],chamber, op),":",round(txt1_s[colours[colour_it]].min(),2),"%","\t","Time:",round(txt1_s[colours[colour_it]].idxmin(),3),"s")
			gls.append(txt1_s[colours[colour_it]].min())								#Peak systolic points in 4CH are appended to list
		else:
			if prmt == '1':
				print("\t[POS] 4CH:", segmentName(colours[colour_it],chamber, op),":",round(txt1_s[colours[colour_it]].max(),2),"%","\t","Time:",round(txt1_s[colours[colour_it]].idxmax(),3),"s")
			gls.append(txt1_s[colours[colour_it]].max())

	if prmt == '1':
		print("\n")

	colours=list(txt3_s)
	chamber = 'APLAX'
	
	for colour_it in range(0,tcolunas3-2):
		if(round(txt3_s[colours[colour_it]].max(),2) < (-0.75*(round(txt3_s[colours[colour_it]].min(),2)))) or onlyNEG:
			if prmt == '1':
				print("\t[NEG] APLAX:", segmentName(colours[colour_it],chamber, op),":",round(txt3_s[colours[colour_it]].min(),2),"%","\t","Time:",round(txt3_s[colours[colour_it]].idxmin(),3),"s")
			gls.append(txt3_s[colours[colour_it]].min())								#Peak systolic points in APLAX are appended to list
		else:
			if prmt == '1':
				print("\t[POS] APLAX:", segmentName(colours[colour_it],chamber, op),":",round(txt3_s[colours[colour_it]].max(),2),"%","\t","Time:",round(txt3_s[colours[colour_it]].idxmax(),3),"s")
			gls.append(txt3_s[colours[colour_it]].max())


	if op != test_op:
		print("\n\nIMPORTANT: USING THE 18-SEGMENT MODEL")
	else: 
		print("\n\nIMPORTANT: USING THE 16-SEGMENT MODEL")
	gls_values = gls

	#GLS is calculated as the mean of all the peak systolic strain values
	gls=round(np.mean(gls),1)					

	if prmt == '1':
		print("\n")
	print("\nGlobal Longitudinal Strain: ", gls,"%")

	#Returns the GLS value and the peak systolic points (txt1_s - 4CH, txt2_s - 2CH and txt3_s - APLAX) to be plotted later
	return gls, txt1_s, txt2_s, txt3_s, gls_values


#Calculates the Mechanical Dispersion (std.deviance from all the peak strain time values in a cycle)
def MD_calc(txt1, txt2, txt3, op, prmt, phasesTimes, valveTimes):

	tcolunas1 = txt1.shape[1]			
	tcolunas2 = txt2.shape[1]		
	tcolunas3 = txt3.shape[1]

	#slices the DF to one that has points from LM to RM time
	if op != test_op:
		txt1_sliced_onsets = txt1[(txt1.index >= phasesTimes[0]) & (txt1.index < phasesTimes[6])] 
		txt2_sliced_onsets = txt2[(txt2.index >= phasesTimes[0]) & (txt2.index < phasesTimes[6])]
		txt3_sliced_onsets = txt3[(txt3.index >= phasesTimes[0]) & (txt3.index < phasesTimes[6])]
	else: 
		txt1_sliced_onsets = txt1 
		txt2_sliced_onsets = txt2
		txt3_sliced_onsets = txt3

	global_minima_times = [] #List that will store the peak strain points

	if prmt == '2':
		print("\n\nTimes of peak negative strain:")

	if prmt == '2':
		print("\n")
	colours=list(txt2_sliced_onsets)
	chamber = '2CH'
	for colour_it in range(0,tcolunas2-2):
		if(round(txt2_sliced_onsets[colours[colour_it]].max(),2) < (-0.75*(round(txt2_sliced_onsets[colours[colour_it]].min(),2)))) or onlyNEG:
			if prmt == '2':
				print("\t[NEG]2CH:", segmentName(colours[colour_it],chamber, op),":",round(txt2_sliced_onsets[colours[colour_it]].idxmin(),3),"ms") #Selects the peak strain points - 2CH
			global_minima_times.append(txt2_sliced_onsets[colours[colour_it]].idxmin())			#Peak Strain poins are appended to global_minima_times
		else:
			if prmt == '2':
				print("\t[POS]2CH:", segmentName(colours[colour_it],chamber, op),":",round(txt2_sliced_onsets[colours[colour_it]].idxmax(),3),"ms")
			global_minima_times.append(txt2_sliced_onsets[colours[colour_it]].idxmax())

	if prmt == '2':
		print("\n")
	colours=list(txt1_sliced_onsets)
	chamber = '4CH'
	for colour_it in range(0,tcolunas1-2):
		if(round(txt1_sliced_onsets[colours[colour_it]].max(),2) < (-0.75*(round(txt1_sliced_onsets[colours[colour_it]].min(),2)))) or onlyNEG:
			if prmt == '2':
				print("\t[NEG]4CH:", segmentName(colours[colour_it],chamber, op),":",round(txt1_sliced_onsets[colours[colour_it]].idxmin(),3),"ms") #Selects the peak strain points - 4CH
			global_minima_times.append(txt1_sliced_onsets[colours[colour_it]].idxmin())			#Peak Strain poins are appended to global_minima_times
		else:
			if prmt == '2':
				print("\t[POS]4CH:", segmentName(colours[colour_it],chamber, op),":",round(txt1_sliced_onsets[colours[colour_it]].idxmax(),3),"ms")
			global_minima_times.append(txt1_sliced_onsets[colours[colour_it]].idxmax())

	if prmt == '2':
		print("\n")
	colours=list(txt3_sliced_onsets)
	chamber = 'APLAX'
	for colour_it in range(0,tcolunas3-2):
		if(round(txt3_sliced_onsets[colours[colour_it]].max(),2) < (-0.75*(round(txt3_sliced_onsets[colours[colour_it]].min(),2)))) or onlyNEG:
			if prmt == '2':
				print("\t[NEG]APLAX:", segmentName(colours[colour_it],chamber, op),":",round(txt3_sliced_onsets[colours[colour_it]].idxmin(),3),"ms") #Selects the peak strain points - APLAX
			global_minima_times.append(txt3_sliced_onsets[colours[colour_it]].idxmin())			#Peak Strain poins are appended to global_minima_times
		else:
			if prmt == '2':
				print("\t[POS]APLAX:", segmentName(colours[colour_it],chamber, op),":",round(txt3_sliced_onsets[colours[colour_it]].idxmax(),3),"ms")
			global_minima_times.append(txt3_sliced_onsets[colours[colour_it]].idxmax())

	if prmt == '2':
		print("\n")

	if op != test_op:
		print("\n\nIMPORTANT: USING THE 18-SEGMENT MODEL")
	else: 
		print("\n\nIMPORTANT: USING THE 16-SEGMENT MODEL")

	md = round(np.std(global_minima_times,dtype=np.float64,ddof=1)*1000, 1)	#MD is calculated as the std.dev from the sample(ddof=1) of all the peak strain times
	print("Mechanical Dispersion: ", md, "ms")

	#Returns the MD value and the peak strain points (txt1_sliced_onsets - 4CH, txt2_sliced_onsets - 2CH and txt3_sliced_onsets - APLAX) to be plotted later
	return md, txt1_sliced_onsets, txt2_sliced_onsets, txt3_sliced_onsets, global_minima_times


#Calculates the global strain variation in each phase
def avgPhaseStrainVar(txt1, txt2, txt3, op, phasesTimes):

	#calculates the average longitudinal strain from all the LV segments
	averageLongStrain =  (pd.concat([txt1.iloc[:,0:-2], txt2.iloc[:,0:-2], txt3.iloc[:,0:-2]], axis=1, sort = False)).mean(axis=1)

	#with pd.option_context('display.max_rows', None, 'display.max_columns', None):  #shows the entire dataframe
	#print(averageLongStrain) #for debugging


	#Adds the time points where the phase changes and interpolates in case they don't exist in the DF
	a = float('NaN')
	for it in phasesTimes:
		averageLongStrain.loc[it] = a	

	averageLongStrain = averageLongStrain.sort_index()
	averageLongStrain = averageLongStrain.interpolate(method = 'linear')
	

	#Prints the average strain values
	print("\nAverage longitudinal strain variation between:")
	auxPrintPhases = np.array(['EMC', 'IVC', 'Ejection Time', 'IVR', 'E', 'A'])

	for it in range(6):
		if it < 5:
			print("\t",auxPrintPhases[it], "and ", auxPrintPhases[it+1],": ",round(averageLongStrain.loc[phasesTimes[it+1]]-averageLongStrain.loc[phasesTimes[it]],2), "%")
		else:
			print("\t",auxPrintPhases[it-5], "and ", auxPrintPhases[it-5+1],": ",round(averageLongStrain.loc[phasesTimes[it+1]]-averageLongStrain.loc[phasesTimes[it]],2), "%")
		
	return averageLongStrain
#

#Show additional info available in the spreadsheet Patients_DB
def moreInfo(it):

	columnsList = [] #Columns in which the values that will be shown are availave
	Init_It = "L"	 #First letter after A in Patients_DB where there is additional info
	End_It = "I"	 #Last letter after B in Patients_DB where there is additional info
	num_it = 0		 #To help present which are from the 2CH and which are from 4CH

	wb = openpyxl.load_workbook('Patients_DB.xlsx')					#opens the xl file where the patient data is
	sheet = wb['Sheet1']

	for letter_It in string.ascii_uppercase:	#Puts the columns values (AA, AB, for example)
		if letter_It >= Init_It:
			columnsList.append("A"+letter_It)
	for letter_It in string.ascii_uppercase:
		if letter_It <= End_It:
			columnsList.append("B"+letter_It)


	for colIt in columnsList:
		if num_it == 0:
			print("\nParameters exported from the proprietary software:\n\n2CH:")
		if num_it == 12:
			print("\n4CH:")
		if(sheet[colIt+str(it)].value != None):		#Tests whether there is a value in that cell
			print("\t",sheet[colIt+"2"].value, ": ", sheet[colIt+str(it)].value)
		num_it = num_it + 1

