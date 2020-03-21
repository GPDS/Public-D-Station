# -*- coding: utf-8 -*-

import pandas as pd              # Package used to work with the raw data files
import re                        # Used to obtain the LM, RM and ES Times in the raw data files
from os import listdir			 # Used to obtain the files in their directories
from os.path import isfile, join # Also used to do file operations
import openpyxl


def openRawData(exams_path, heartChamber, strainType, visualization):


	#Ainda não está certo, não entra no except caso o arquivo não apareça

	
	try:
		#Lists the txt files in the directory pointed by exams_path
		list_txtfiles = [f for f in listdir(exams_path+'/'+heartChamber) if isfile(join(exams_path+'/'+heartChamber, f))] 
		for f in list_txtfiles:
			if(visualization in f and strainType in f):
				print(f)
				input('')
				txt=pd.read_csv(exams_path+'/'+heartChamber+'/'+f, sep='\t', engine='python', skiprows=3, index_col=0)
				return txt

	except FileNotFoundError:
		print(heartChamber, " ", visualization," file not found in the ", exams_path,"/", heartChamber,"/\' directory.", sep='')



def openRawDataFiles(idPatient, op, test_op): # Abrir todos os arquivos disponíveis para um paciente aqui
	#Getting all the files in the new folder	
	#Colocar mensagens de erro caso não consiga abrir
	
	if op != test_op:							#Checks if the file will be on the simulation directory or in the patients one
		exams_path = ('Patients/'+idPatient)
	else:
		exams_path = ('Simulations/'+idPatient)

	#LV
	txt1 = openRawData(exams_path, 'LV', 'SL', '4CH')
	txt2 = openRawData(exams_path, 'LV', 'SL', '2CH')
	txt3 = openRawData(exams_path, 'LV', 'SL', 'APLAX')



	input('RODOU\n\n\n\n')
	#Fazer um para cada câmara 
	#Podia fazer uma função para isso (camara como string)




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
