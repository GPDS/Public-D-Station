# -*- coding: utf-8 -*-

import pandas as pd
from os import listdir			 # Used to obtain the files in their directories
from os.path import isfile, join # Also used to do file operations
import sys
import re
import numpy as np
import openpyxl                  # Package to work with .xlsx - See documentation when working with a big amount of data

#Package that i (rafaelds9) created
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


def segmentName(segmentColor, chamber):

	if chamber == '2CH':

		if 'RED' in segmentColor:
			return "Red - Basal Anterior"

		elif 'BLUE' in segmentColor:
			return "Blue - Medium Anterior"

		elif 'MAGENTA' in segmentColor:
			return "Magenta - Apical Anterior"

		elif 'GREEN' in segmentColor:
			return "Green - Apical Inferior"

		elif 'CYAN' in segmentColor:
			return "Cyan - Medium Inferior"

		elif 'YELLOW' in segmentColor:
			return "Yellow - Basal Inferior"

		else:
			return "\nERROR - Color could not be identified\n"

	elif chamber == '4CH':

		if 'RED' in segmentColor:
			return "Red - Basal Anterolateral"

		elif 'BLUE' in segmentColor:
			return "Blue - Medium Anterolateral"

		elif 'MAGENTA' in segmentColor:
			return "Magenta - Apical Anterolateral"

		elif 'GREEN' in segmentColor:
			return "Green -Apical Inferoseptal"

		elif 'CYAN' in segmentColor:
			return "Cyan - Medium Inferoseptal"

		elif 'YELLOW' in segmentColor:
			return "Yellow - Basal Inferoseptal"

		else:
			return "\nERROR - Color could not be identified\n"

	elif chamber == 'APLAX':

		if 'RED' in segmentColor:
			return "Red - Basal Anteroseptal"

		elif 'BLUE' in segmentColor:
			return "Blue - Medium Anteroseptal"

		elif 'MAGENTA' in segmentColor:
			return "Magenta - Apical Anteroseptal"

		elif 'GREEN' in segmentColor:
			return "Green - Apical Inferolateral"

		elif 'CYAN' in segmentColor:
			return "Cyan - Medium Inferolateral"

		elif 'YELLOW' in segmentColor:
			return "Yellow - Basal Inferolateral"

		else:
			return "\nERROR - Color could not be identified\n"

	else:
		return "\nERROR - Vision could not be identified\n"



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



def syncStrain(txt, refESTime, oldESTime):

	txt=txt.copy(deep=True) #Aparentemente não é necessario
	txt.index = txt.index-(oldESTime-refESTime)

	return txt



def openSheet(sheetName, idPatient):

	#ADD TRY-EXCEPT routines later

	#opens the xl file where the patient data is

	wb = openpyxl.load_workbook(sheetName)					
	sheet = wb['Sheet1']

	#Determines the current patient row
	for cell in sheet['A']:
		if(cell.value is not None): #check if that the cell is not empty.
			if idPatient == cell.value: #Check if the value of the cell contains the idPatient
				patientLine = format(cell.row)

	return sheet, patientLine, wb



def verifyECG(txt1, strain_rate_lv4ch, headerTimesTxt1 , sheet, linePatient, op, decision):
	#Checks if the ECG points were selected

	EcgOk = 0	#Defines if the ECG has its points correctly or should be marked/rechecked
	MarkPoints = 1 # For future use

	auxSheetColumns = ['U', 'V', 'W']
	pointsECG = np.zeros(3) #OnsetQRS1, OnsetP, OnsetQRS2

	tcolunas1=int(((txt1.size/len(txt1.index))))			#Checks the ammount of columns in the dataframe
	tcolunas_strain_rate_lv4ch = int(((strain_rate_lv4ch.size/len(strain_rate_lv4ch.index))))

	#Sort para detectar o menor index dentre os arquivospara que um gráfico não fique sobrando
	END_Time0 = sorted([txt1.index[len(txt1.index)-1], strain_rate_lv4ch.index[len(strain_rate_lv4ch.index)-1]])[1]


	if op != test_op and MarkPoints:
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
	


