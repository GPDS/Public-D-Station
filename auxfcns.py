# -*- coding: utf-8 -*-

import pandas as pd
from os import listdir			 # Used to obtain the files in their directories
from os.path import isfile, join # Also used to do file operations
import sys
import re
import numpy as np
import openpyxl                  # Package to work with .xlsx - See documentation when working with a big amount of data

#Package by me (rafaelds9)
from dstationplotlib import *


#Importing configuration
import configparser

config = configparser.ConfigParser()
config.read('config.ini')	
# Reading variables from config file
test_op = str(config['default']['test_op'])
#


#Function to read only the first N columns of a dataframe
def front(self, n):
	return self.iloc[:, :n]

pd.DataFrame.front = front
#

# Function to relate the raw data file segments (col names)
# with the actual segments in the AHA (American Heart Association) model 
def segmentName(segmentColor, chamber, op):
	
	if op != test_op:
		if chamber == '2CH':

			if 'RED' in segmentColor:
				return "Red - Basal Anterior"

			elif 'BLUE' in segmentColor:
				return "Blue - Mid Anterior"

			elif 'MAGENTA' in segmentColor:
				return "Magenta - Apical Anterior"

			elif 'GREEN' in segmentColor:
				return "Green - Apical Inferior"

			elif 'CYAN' in segmentColor:
				return "Cyan - Mid Inferior"

			elif 'YELLOW' in segmentColor:
				return "Yellow - Basal Inferior"

			else:
				return "\nERROR - Color could not be identified\n"

		elif chamber == '4CH':

			if 'RED' in segmentColor:
				return "Red - Basal Anterolateral"

			elif 'BLUE' in segmentColor:
				return "Blue - Mid Anterolateral"

			elif 'MAGENTA' in segmentColor:
				return "Magenta - Apical Anterolateral"

			elif 'GREEN' in segmentColor:
				return "Green -Apical Inferoseptal"

			elif 'CYAN' in segmentColor:
				return "Cyan - Mid Inferoseptal"

			elif 'YELLOW' in segmentColor:
				return "Yellow - Basal Inferoseptal"

			else:
				return "\nERROR - Color could not be identified\n"

		elif chamber == 'APLAX':

			if 'RED' in segmentColor:
				return "Red - Basal Anteroseptal"

			elif 'BLUE' in segmentColor:
				return "Blue - Mid Anteroseptal"

			elif 'MAGENTA' in segmentColor:
				return "Magenta - Apical Anteroseptal"

			elif 'GREEN' in segmentColor:
				return "Green - Apical Inferolateral"

			elif 'CYAN' in segmentColor:
				return "Cyan - Mid Inferolateral"

			elif 'YELLOW' in segmentColor:
				return "Yellow - Basal Inferolateral"

			else:
				return "\nERROR - Color could not be identified\n"

		else:
			return "\nERROR - Vision could not be identified\n"
	
	#For simulations from CircAdapt (following our strain curves export method)
	else:
		if chamber == '2CH':

			if 'RED' in segmentColor:
				return "Red - Apical Lateral"

			elif 'BLUE' in segmentColor:
				return "Blue - Apical Inferior"

			elif 'MAGENTA' in segmentColor:
				return "Magenta - Apical Anterior"

			elif 'GREEN' in segmentColor:
				return "Green - Mid Anterolateral"

			elif 'CYAN' in segmentColor:
				return "Cyan - Mid Inferolateral"

			elif 'YELLOW' in segmentColor:
				return "Yellow - Mid Inferior"

			else:
				return "\nERROR - Color could not be identified\n"

		elif chamber == '4CH':

			if 'RED' in segmentColor:
				return "Red - Mid Anterior"

			elif 'BLUE' in segmentColor:
				return "Blue - Basal Anterolateral"

			elif 'MAGENTA' in segmentColor:
				return "Magenta - Basal Inferolateral"

			elif 'GREEN' in segmentColor:
				return "Green -Basal Inferior"

			elif 'CYAN' in segmentColor:
				return "Cyan - Basal Anterior"

			elif 'YELLOW' in segmentColor:
				return "Yellow - Apical Septal"

			else:
				return "\nERROR - Color could not be identified\n"

		elif chamber == 'APLAX':

			if 'RED' in segmentColor:
				return "Red - Mid Inferoseptal"

			elif 'BLUE' in segmentColor:
				return "Blue - Mid Anteroseptal"

			elif 'MAGENTA' in segmentColor:
				return "Magenta - Basal Inferoseptal"

			elif 'GREEN' in segmentColor:
				return "Green - Basal Anteroseptal"

			else:
				return "\nERROR - Color could not be identified\n"

		else:
			return "\nERROR - Vision could not be identified\n"


# Function that checks if there is a raw data associated with the patient
# and visualization chosen, opens it and returns the dataframe and
# the corresponding header times  
def openRawData(exams_path, heartChamber, strainType, visualization):


	exam = '_not_found_' # Default state
	try:
		#Lists the txt files in the directory pointed by exams_path
		list_txtfiles = [f for f in listdir(exams_path+'/'+heartChamber) if isfile(join(exams_path+'/'+heartChamber, f))] 
		for f in list_txtfiles:
			if(visualization in f and strainType in f):
				exam = f

		#Opens the txt as pandas dataframe	
		txt=pd.read_csv(exams_path+'/'+heartChamber+'/'+exam, sep='\t', engine='python', skiprows=3, index_col=0)
	
		# Useless column is removed from the txt files
		txt.drop('Unnamed: 1', axis=1, inplace=True)


		#Opens the txt as file to obtain the times (LM,RM,ES)
		txt_file = open(exams_path+'/'+heartChamber+'/'+exam, 'r')
		times = np.array(re.findall("\d+\.\d+", txt_file.readlines()[2])) #Times are obtained
		times = times.astype('float64')
		txt_file.close()

		return txt, times

	# I may put something in case the times are not available

	except FileNotFoundError:
		print(heartChamber, " ", visualization," file not found in the ", exams_path,"/", heartChamber,"/\' directory.", sep='')
		print("\n\nEnding process.\n")
		sys.exit(1)


# Function that takes the reference ES_Time (end systolic time) and the ES_Time
# of the file to times of the dataframe so they are with the same ES_Time as
# the reference. This is done by shifting the index based on the difference
def syncStrain(txt, refESTime, oldESTime):

	txt=txt.copy(deep=True) #Aparentemente não é necessario
	txt.index = txt.index-(oldESTime-refESTime)

	return txt


# Opens the spreadsheet and reads the line corresponding to the idPatient inputed
def openSheet(sheetName, idPatient):

	#ADD TRY-EXCEPT routines later

	#opens the xl file where the patient data is

	wb = openpyxl.load_workbook(sheetName)					
	sheet = wb['Sheet1']

	#Determines the current patient row
	for cell in sheet['A']:
		#checks if that the cell is not empty.
		if(cell.value is not None): 
			#Checks if the value of the cell contains the idPatient
			if idPatient == cell.value: 
				patientLine = format(cell.row)

	return sheet, patientLine, wb


# Function to check if the ECG times (QRS Onset1, P Onset and QRS Onset2) 
# were already selected. If they were, the user may check if they are 
# correct or change them. If there were not selected, the it will plot
# the ECG curve so the user can select these points 
def verifyECG(txt1, strain_rate_lv4ch, headerTimesTxt1 , sheet, linePatient, op, decision):

	# Defines if the ECG has its points correctly or should be marked/rechecked
	EcgOk = 0	

	# For future use
	MarkPoints = 1 

	auxSheetColumns = ['U', 'V', 'W']

	# [OnsetQRS1, OnsetP, OnsetQRS2]
	pointsECG = np.zeros(3) #

	#Checks the ammount of columns in the dataframe
	tcolunas1=int(((txt1.size/len(txt1.index))))			
	tcolunas_strain_rate_lv4ch = int(((strain_rate_lv4ch.size/len(strain_rate_lv4ch.index))))

	# Detects the smallest index in the dataframes
	END_Time0 = min([txt1.index[len(txt1.index)-1], strain_rate_lv4ch.index[len(strain_rate_lv4ch.index)-1]])

	# If not a simulation and MarkPoints == 1
	if op != test_op and MarkPoints:
		# If all the values are present
		if sheet['U'+linePatient].value is not None and sheet['V'+linePatient].value is not None and sheet['W'+linePatient].value is not None:
			
			while EcgOk == 0:

				if decision != None:
					print("\n1. Verify the stored Onset QRS1, P Onset and Onset QRS 2 values.")
					print("2. Change the stored Onset QRS1, P Onset and Onset QRS 2 values.")
					print("3. Use the stored values without verifying.")
					decision = input("Option: ")
			

				if(decision == '1'):
					for it in range(3):
						pointsECG[it] = sheet[auxSheetColumns[it]+linePatient].value/1000

					print("\nAre the presented timepoints (in red) correct? Close the figure and answer: ")
					ecgVerification(txt1, headerTimesTxt1, END_Time0, pointsECG)
					decision = input("Are they correct? [Y]es or [N]o? ")

					if(decision == 'n' or decision == 'N'):
						EcgOk = 0
						decision = 0

					else:
						EcgOk = 1

				elif(decision == '2'):
						print("\n\nSelect Onset QRS 1, onset P, onset QRS 2 (in this order)")
						pointsECG = PlotClick(txt1, tcolunas1, headerTimesTxt1, END_Time0, op, strain_rate_lv4ch,tcolunas_strain_rate_lv4ch)
						for it in range(3):
							sheet[auxSheetColumns[it]+str(linePatient)] = round(pointsECG[it],0) # Writes the ECG points on the sheet
						EcgOk = 1

				else:
					EcgOk = 1
				

		else:
			print("\n\nSelect Onset QRS 1, onset P, onset QRS 2 (in this order)")
			pointsECG = PlotClick(txt1, tcolunas1, headerTimesTxt1, END_Time0, op, strain_rate_lv4ch,tcolunas_strain_rate_lv4ch)
			for it in range(3):
				sheet[auxSheetColumns[it]+str(linePatient)] = round(pointsECG[it],0) # Writes the ECG points on the sheet


# Saves the values calculated in the line corresponding to the idPatient
def saveAndCloseSheet(linePatient, sheet, wb, headerTimes, phasesTimes, systolicTime, outGLS, outMD):
	
	auxSheetCols = np.array(['X', 'Y', 'Z', 'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'AG', 'AH', 'AI', 'AJ', 'AK'])
	for it in range(auxSheetCols.size):
		if it < 9:
			sheet[auxSheetCols[it] + str(linePatient)] = round(phasesTimes[it]*1000)
		elif it == 9 and systolicTime != None:
			sheet[auxSheetCols[it] + str(linePatient)] = (systolicTime*1000)
		elif it == 10 and systolicTime != None:
			sheet[auxSheetCols[it] + str(linePatient)] = ((headerTimes[0][1] - systolicTime)*1000)
		elif it == 11 and systolicTime != None:
			sheet[auxSheetCols[it] + str(linePatient)] = (systolicTime/(headerTimes[0][1] - systolicTime))
		elif it == 12 and outGLS != None:
			sheet[auxSheetCols[it] + str(linePatient)] = outGLS[0]
		elif it == 13 and outMD != None:
			sheet[auxSheetCols[it] + str(linePatient)] = outMD[0]

	wb.save("Patients_DB.xlsx")		#Parameters are saved in the xl file
	


