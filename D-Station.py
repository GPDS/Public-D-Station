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



#Initializing variables
linePatient = 3   #Defines the first row in the xl file that has values
prmt = '0' #Defines the prmt value in the first run to 0 - Change with caution
EcgOk = 0	#Defines if the ECG has its points correctly or should be marked/rechecked
MarkPoints = 1	#Currently 1 - to future use
#


#MAIN
os.system('cls' if os.name == 'nt' else 'clear') # Clears the terminal

"""
idPatient = input('Patient ID: ')
print("Options:\n\t1. Strain LV, Strain Rate LV and ECG\n\t2. Strain LV, Strain LA and ECG")
print("\t3. Strain LV, Strain Rate LA and ECG\n\t4. Strain LV, Strain RV and ECG")
print("\t5. Strain LV, Strain Rate LV and ECG (without SR files)\n\t"+test_op+". Test Option")
op = input("Option: ")
"""

idPatient = 'Aristoteles'	# Used to debug - commnent the idPatient line above
op = '1'					# Used to debug - comment the op line above


txt1, txt2, txt3, txtMid, txtMid2, txtMid3, strain_rate_lv4ch, strain_rate_lv2ch, strain_rate_lv3ch, headerTimes = openRawDataFiles(idPatient, op)


# =====================================================
#Posso colocar as linhas abaixo dentro das funções
#
tcolunas1=int(((txt1.size/len(txt1.index))))			#Checks the ammount of columns in the dataframe
tcolunas2=int(((txt2.size/len(txt2.index))))
tcolunas3=int(((txt3.size/len(txt3.index))))
tcolunasMid=int(((txtMid.size/len(txtMid.index))))


#Para o gráfico dos parâmetros - Início
#achar o menor entre os strains e comparar com o do meio
END_Time1 = sorted([txt1.index[len(txt1.index)-1], txt2.index[len(txt2.index)-1], txt3.index[len(txt3.index)-1],
txtMid.index[len(txtMid.index)-1]])[3]
#Para o gráfico dos parâmetros - Fim

# Sheet is open
sheet, linePatient, wb = openSheet('Patients_DB.xlsx', idPatient)

verifyECG(txt1, strain_rate_lv4ch, headerTimes[0], sheet, linePatient, op)

"""The times used are the synced with the times of txt one, meaning: The ES_Time of the txt1 = AVC and
the (ES_Time(of txt1)-AVC) is the difference between the events of the txt1 and the events in the spreadsheet
We did this because we had different ES_Times in the 3 txt files, so we synced them
"""


#Leitura dos tempos das valvulas no spreadsheet
valveTimes = valveTimesRead(headerTimes,sheet,linePatient)
#

if op != test_op: #Cálculo do tempo das fases do LV
	phasesTimes, LAphasesTimes = phaseSeg(valveTimes, sheet, linePatient)


#Now everything is printed
os.system('cls' if os.name == 'nt' else 'clear') # Clears the terminal
print("Patient: ",idPatient )
print("\nLM_Time: ",headerTimes[0][0]*1000, "ms")
print("RM_Time: ",headerTimes[0][1]*1000, "ms")


printValveTimes(valveTimes)

if op != test_op:
	printPhaseTimes(phasesTimes)

	if op == "2":
		printLAPhaseTimes(LAphasesTimes)


input('')

#I'll fix this later
"""
systolic_time = (AVCvalues1[0]-MVCvalues1[0])
print("\nSystolic Time: ", systolic_time*1000)
print("Diastolic Time: ", (headerTimes[0][1] - systolic_time)*1000)
print("Systolic Time/Diastolic Time ratio: ",round((systolic_time/(headerTimes[0][1] - systolic_time)),4))
"""

outGLS = GLS_calc(txt1, txt2, txt3, op, prmt, EMCvalues1, AVCvalues1, tcolunas1, tcolunas2, tcolunas3)
outMD = MD_calc(txt1, txt2, txt3, op, prmt, EMCvalues1, EMCvalues2, AVCvalues1, tcolunas1, tcolunas2, tcolunas3)


if(op != test_op):
	averageLongStrain = avgPhaseStrainVar(txt1, txt2, txt3, op, EMCvalues1, IVCvalues1, EjectionTimevalues1, IVRvalues,
	Evalues, Avalues, EMCvalues2, IVCvalues2, EjectionTimevalues2)
else:
	print("\nPhase segmentation was not performed, therefore you cannot calculate the phase strain variation")



#DI_calc()
#print("\n\n")

calculated_IVA = 0	#Currently not used

while True: 		#Loop where the user can select the parmeters and plots he wishes to see
	
	print("\n\nParameters:\n\t1. Global Longitudinal Strain\n\t2. Mechanical Dispersion")
	print("\t3. Average Strain variation during each phase")
	print("\t4. Show plot w/o any parameters\n\t5. Show additional parameters values\n\t0. Terminate program")
	prmt = input("Parameter: ")
	
	#prmt = '0' #Comment the line above and uncomment this to test

	if prmt == "1":               #Calculates the GLS
		_,_,_,_,gls_values = GLS_calc(txt1, txt2, txt3, op, prmt, EMCvalues1, AVCvalues1, tcolunas1, tcolunas2, tcolunas3)
		POIPlot(txt1, txt2, txt3, txtMid, strain_rate_lv4ch, strain_rate_lv2ch, strain_rate_lv3ch, tcolunas1, tcolunas2, tcolunas3, tcolunasMid, prmt,
		 				op, END_Time1, MVOvalues1, MVCvalues1, AVOvalues1, AVCvalues1, MVOvalues2, MVCvalues2, AVOvalues2, AVCvalues2,
						EMCvalues1, EMCvalues2, IVCvalues1, IVCvalues2, EjectionTimevalues1, EjectionTimevalues2, IVRvalues, Evalues, Avalues, outGLS[1],
						outGLS[2], outGLS[3])
		#print(gls_values) #Comment this line after debug			
		DR_bullseye(gls_values, prmt)
		#break #Comment this line after debug

	elif prmt == "2":			  #Calculates the MD
		_,_,_,_,md_values = MD_calc(txt1, txt2, txt3, op, prmt, EMCvalues1, EMCvalues2, AVCvalues1, tcolunas1, tcolunas2, tcolunas3)
		POIPlot(txt1, txt2, txt3, txtMid, strain_rate_lv4ch, strain_rate_lv2ch, strain_rate_lv3ch, tcolunas1, tcolunas2, tcolunas3, tcolunasMid, prmt,
						op, END_Time1, MVOvalues1, MVCvalues1, AVOvalues1, AVCvalues1, MVOvalues2, MVCvalues2, AVOvalues2, AVCvalues2,
						EMCvalues1, EMCvalues2, IVCvalues1, IVCvalues2, EjectionTimevalues1, EjectionTimevalues2, IVRvalues, Evalues, Avalues, outMD[1],
						outMD[2],outMD[3])
		#print(md_values) #Comment this line after debug
		DR_bullseye(md_values, prmt)
		# break #Comment this line after debug


	elif prmt == "3":
		if(op != test_op):
			avgPhaseStrainVarPlot(txt1, txt2, txt3, op, averageLongStrain, tcolunas1, tcolunas2, tcolunas3, END_Time1, MVOvalues1,
			MVCvalues1, AVOvalues1, AVCvalues1, MVOvalues2, MVCvalues2, AVOvalues2, AVCvalues2, EMCvalues1, EMCvalues2, IVCvalues1, IVCvalues2,
			EjectionTimevalues1,EjectionTimevalues2, IVRvalues, Evalues, Avalues)
		else:
			print("\nPhase segmentation was not performed, therefore you cannot calculate the phase strain variation and also not plot linePatient")

	#elif prmt == "3": #DI - Not working right now/to be added later
	#    DI_calc()
	#    DR_bullseye(BullseyeAux)
		#Ver a barra

	elif prmt == "4":
		print("\nPlot w/o any parameters")
		POIPlot(txt1, txt2, txt3, txtMid, strain_rate_lv4ch, strain_rate_lv2ch, strain_rate_lv3ch, tcolunas1, tcolunas2, tcolunas3, tcolunasMid, prmt, op,
		END_Time1, MVOvalues1, MVCvalues1,
		AVOvalues1, AVCvalues1, MVOvalues2, MVCvalues2, AVOvalues2, AVCvalues2, EMCvalues1, EMCvalues2, IVCvalues1, IVCvalues2, EjectionTimevalues1,
		EjectionTimevalues2, IVRvalues, Evalues, Avalues, None, None, None)
		#break # for debugging purposes, comment later

	elif prmt == "5":
		moreInfo(linePatient)

	#elif prmt == "8":		#IVA - Not working right now/to be implemented later
		#IVA_calc()
		#break

	elif prmt == "0":
		break

	else:
		print("\n\nInvalid option\n\n\n")
		continue
	print("\n")


"""
sheet['X'+str(linePatient)] = round(EMCvalues1[0]*1000)
sheet['Y'+str(linePatient)] = round(IVCvalues1[0]*1000)
sheet['Z'+str(linePatient)] = round(EjectionTimevalues1[0]*1000)
sheet['AA'+str(linePatient)] = round(IVRvalues[0]*1000)
sheet['AB'+str(linePatient)] = round(Evalues[0]*1000)
sheet['AC'+str(linePatient)] = round(Avalues[0]*1000)
sheet['AD'+str(linePatient)] = round(EMCvalues2[0]*1000)
sheet['AE'+str(linePatient)] = round(IVCvalues2[0]*1000)
sheet['AF'+str(linePatient)] = round(EjectionTimevalues2[0]*1000)
sheet['AG'+str(linePatient)] = (systolic_time*1000)
sheet['AH'+str(linePatient)] = ((headerTimes[0][1] - systolic_time)*1000)
sheet['AI'+str(linePatient)] = (systolic_time/(headerTimes[0][1] - systolic_time))
sheet['AJ'+str(linePatient)] = outGLS[0] #Saves the caculated GLS in the sheet
sheet['AK'+str(linePatient)] = outMD[0]	#Saves the caculated MD in the sheet
"""
wb.save("Patients_DB.xlsx")		#Parameters are saved in the xl file
