# -*- coding: utf-8 -*-

# A package created for the D-Station (https://gpdsifpb.github.io/D-Station/)
# containing the functions used to calculate its parameters

"""Put these outputs in a bullseye
	Colocar nomes significativos"""

import pandas as pd			# Package used to work with the raw data files (Used in GLS_calc, MD_calc, IVA_calc)
import numpy as np			# Used in the mean and standard deviance calculation (GLS_calc and MD_calc)
import openpyxl				# Used in the moreInfo function
import string				# Used in the moreInfo function

#Calculates the Global Longitudinal Strain of from the LV Strain curves = mean of the peak systolic strain of all curves
def GLS_calc(txt1, txt2, txt3, op, test_op, prmt, LM_Time, ES_Time, AVCvalues1, tcolunas1, tcolunas2, tcolunas3):

																			#If it's a real patient
	txt1_s = txt1[(txt1.index >= LM_Time[0]) & (txt1.index <= ES_Time[0])]		#From the LM_Time until the AVC from the raw data files
	txt2_s = txt2[(txt2.index >= LM_Time[1]) & (txt2.index <= ES_Time[1])]
	txt3_s = txt3[(txt3.index >= LM_Time[2]) & (txt3.index <= ES_Time[2])]

	if prmt == '1':																	#Shows detailed info about the GLS
		print("\n\nPeak negative systolic strain:\n")
	gls = []																		#List that stores the peak systolic points
	colours=list(txt2_s)
	for colour_it in range(0,tcolunas2-2):
		if prmt == '1':
			print("2CH:", colours[colour_it],":",round(txt2_s[colours[colour_it]].min(),2),"%","\t","Time:",txt2_s[colours[colour_it]].idxmin(),"s")
		gls.append(txt2_s[colours[colour_it]].min())								#Peak systolic points in 2CH are appended to list

	if prmt == '1':
		print("\n")
	colours=list(txt1_s)
	for colour_it in range(0,tcolunas1-2):
		if prmt == '1':
			print("4CH:", colours[colour_it],":",round(txt1_s[colours[colour_it]].min(),2),"%","\t","Time:",txt1_s[colours[colour_it]].idxmin(),"s")
		gls.append(txt1_s[colours[colour_it]].min())								#Peak systolic points in 4CH are appended to list

	if prmt == '1':
		print("\n")
	colours=list(txt3_s)
	for colour_it in range(0,tcolunas3-2):
		if prmt == '1':
			print("APLAX:", colours[colour_it],":",round(txt3_s[colours[colour_it]].min(),2),"%","\t","Time:",txt3_s[colours[colour_it]].idxmin(),"s")
		gls.append(txt3_s[colours[colour_it]].min())								#Peak systolic points in APLAX(3CH) are appended to list

	gls=round(np.mean(gls),1)					#GLS is calculated as the mean of all the peak systolic strain values

	if prmt == '1':
		print("\n")
	print("\nGlobal Longitudinal Strain: ", gls,"%")

	txt2_s.index = txt2_s.index-(LM_Time[1]-LM_Time[0])		#syncs the points used in GLS calculation
	txt3_s.index = txt3_s.index-(LM_Time[2]-LM_Time[0])		# ''

	#Returns the GLS value and the peak systolic points (txt1_s - 4CH, txt2_s - 2CH and txt3_s - APLAX) to be plotted later
	return gls, txt1_s, txt2_s, txt3_s


#Calculates the Mechanical Dispersion (std.deviance from all the peak strain time values in a cycle)
def MD_calc(txt1, txt2, txt3, txt2_mod, txt3_mod, op, test_op, prmt, LM_Time, RM_Time, AVCvalues1, tcolunas1, tcolunas2, tcolunas3):

	txt1_sliced_onsets = txt1[(txt1.index >= LM_Time[0]) & (txt1.index < RM_Time[0])] #slices the DF to one that has points from LM to RM time
	txt2_sliced_onsets = txt2[(txt2.index >= LM_Time[1]) & (txt2.index < RM_Time[1])]
	txt3_sliced_onsets = txt3[(txt3.index >= LM_Time[2]) & (txt3.index < RM_Time[2])]

	global_minima_times = [] #List that will store the peak strain points

	if prmt == '2':
		print("\n\nTimes of peak negative strain:\n")

	if prmt == '2':
		print("\n")
	colours=list(txt2_sliced_onsets)
	for colour_it in range(0,tcolunas2-2):
		if prmt == '2':
			print("2CH:", colours[colour_it],":",txt2_sliced_onsets[colours[colour_it]].idxmin(),"ms") #Selects the peak strain points - 2CH
		global_minima_times.append(txt2_sliced_onsets[colours[colour_it]].idxmin())			#Peak Strain poins are appended to global_minima_times

	if prmt == '2':
		print("\n")
	colours=list(txt1_sliced_onsets)
	for colour_it in range(0,tcolunas1-2):
		if prmt == '2':
			print("4CH:", colours[colour_it],":",txt1_sliced_onsets[colours[colour_it]].idxmin(),"ms") #Selects the peak strain points - 4CH
		global_minima_times.append(txt1_sliced_onsets[colours[colour_it]].idxmin())			#Peak Strain poins are appended to global_minima_times

	if prmt == '2':
		print("\n")
	colours=list(txt3_sliced_onsets)
	for colour_it in range(0,tcolunas3-2):
		if prmt == '2':
			print("APLAX:", colours[colour_it],":",txt3_sliced_onsets[colours[colour_it]].idxmin(),"ms") #Selects the peak strain points - APLAX
		global_minima_times.append(txt3_sliced_onsets[colours[colour_it]].idxmin())			#Peak Strain poins are appended to global_minima_times

	if prmt == '2':
		print("\n")
	md = round(np.std(global_minima_times,dtype=np.float64,ddof=1)*1000, 1)	#MD is calculated as the std.dev from the sample(ddof=1) of all the peak strain times
	print("Mechanical Dispersion: ", md, "ms")

	#Returns the MD value and the peak strain points (txt1_sliced_onsets - 4CH, txt2_sliced_onsets - 2CH and txt3_sliced_onsets - APLAX) to be plotted later
	return md, txt1_sliced_onsets, txt2_sliced_onsets, txt3_sliced_onsets


#Calculates the global strain variation in each phase
def avgPhaseStrainVar(txt1, txt2, txt3, op, test_op, EMCvalues1, IVCvalues1, EjectionTimevalues1, IVRvalues, Evalues, Avalues, EMCvalues2, IVCvalues2, EjectionTimevalues2):

	#line below: calculates the average longitudinal strain from all the LV segments
	averageLongStrain =  (pd.concat([txt1.iloc[:,0:-2], txt2.iloc[:,0:-2], txt3.iloc[:,0:-2]], axis=1, sort = False)).mean(axis=1)

	#Adds the time points where the phase changes and interpolates in case they don't exist in the DF
	a = float('NaN')
	averageLongStrain.loc[EMCvalues1[0]] = a
	averageLongStrain.loc[IVCvalues1[0]] = a
	averageLongStrain.loc[EjectionTimevalues1[0]] = a
	averageLongStrain.loc[IVRvalues[0]] = a
	averageLongStrain.loc[Evalues[0]] = a
	averageLongStrain.loc[Avalues[0]] = a
	averageLongStrain.loc[EMCvalues2[0]] = a
	averageLongStrain.loc[IVCvalues2[0]] = a
	averageLongStrain.loc[EjectionTimevalues2[0]] = a
	averageLongStrain = averageLongStrain.sort_index()
	averageLongStrain = averageLongStrain.interpolate(method = 'quadratic')
	#

	#Prints the average strain values
	print("\nAverage longitudinal strain variation between:")
	print("\tElectrical Mechanical Coupling (EMC) 2 and Isovolumic Contraction (IVC) Phase 1: ", round(averageLongStrain.loc[IVCvalues1[0]]-averageLongStrain.loc[EMCvalues1[0]],2), "%")
	print("\tIsovolumic contraction (IVC) Phase 1 and Ejection Phase (Ejec) 1: ", round(averageLongStrain.loc[EjectionTimevalues1[0]]-averageLongStrain.loc[IVCvalues1[0]],2), "%")
	print("\tEjection (Ejec) Phase 1 and Isovolumic Relaxation (IVR) Phase: ", round(averageLongStrain.loc[IVRvalues[0]]-averageLongStrain.loc[EjectionTimevalues1[0]],2), "%")
	print("\tIsovolumic Relaxation (IVR) Phase and Rapid Inflow (E) Phase: ", round(averageLongStrain.loc[Evalues[0]]-averageLongStrain.loc[IVRvalues[0]],2), "%")
	print("\tRapid Inflow (E) Phase and Atrial (A) Contraction Phase: ", round(averageLongStrain.loc[Avalues[0]]-averageLongStrain.loc[Evalues[0]],2), "%")
	print("\tAtrial Contraction (A) Phase and Electrical Mechanical (EMC) Coupling 2: ", round(averageLongStrain.loc[EMCvalues2[0]]-averageLongStrain.loc[Avalues[0]],2), "%")

	#maybe i should return them in an array to later save in the spreadsheet
	return averageLongStrain


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
#=====================================================
#Below here: to be implemented

def DI_calc():            #Diastolic Index Calculation - To be implemented

	global ThirdDiastoleTime
	global txt1_dr
	global txt2_dr
	global txt3_dr

	if op == test_op:
		ThirdDiastoleTime = AVCvalues1[0]+(RM_Time-systolic_time)/3 #Tempo de AVC + tempo de diastole/3
	else:
		ThirdDiastoleTime = AVCvalues1[0]+((EMCvalues2[0]+Dif_LM_OnsetQRS1[0])-AVCvalues1[0])/3 #EMC2+Diferença do Pico R1 e o onset QRS1-AVC1
	#Criação das células com os valores de AVC e de 1/3 da diástole - Início
	a = np.full(tcolunas1, float('nan'))         #Cria uma linha de tcolunas NaN
	txt1_dr = txt1
	indices = list(txt1_dr.index.values)#Rotina para a alteração do índice da lista de forma que os novos indíces sejam o último índice
	var_t_med = indices[len(txt1_dr)-1]/len(txt1_dr)    #Nativos da lista incrementados
	txt1_dr.loc[AVCvalues1[0]] = a
	txt1_dr.loc[ThirdDiastoleTime] = a
	txt1_dr = txt1_dr.sort_index()
	txt1_dr = txt1_dr.interpolate(method = 'linear') #Antes era cubic

	a = np.full(tcolunas2, float('nan'))         #Cria uma linha de tcolunas NaN
	txt2_dr = txt2
	indices = list(txt2_dr.index.values)#Rotina para a alteração do índice da lista de forma que os novos indíces sejam o último índice
	var_t_med = indices[len(txt2_dr)-1]/len(txt2_dr)    #Nativos da lista incrementados
	txt2_dr.loc[AVCvalues1[0]] = a
	txt2_dr.loc[ThirdDiastoleTime] = a
	txt2_dr = txt2_dr.sort_index()
	txt2_dr = txt2_dr.interpolate(method = 'linear')

	a = np.full(tcolunas3, float('nan'))         #Cria uma linha de tcolunas NaN
	txt3_dr = txt3
	indices = list(txt3_dr.index.values)#Rotina para a alteração do índice da lista de forma que os novos indíces sejam o último índice
	var_t_med = indices[len(txt3_dr)-1]/len(txt3_dr)    #Nativos da lista incrementados
	txt3_dr.loc[AVCvalues1[0]] = a
	txt3_dr.loc[ThirdDiastoleTime] = a
	txt3_dr = txt3_dr.sort_index()
	txt3_dr = txt3_dr.interpolate(method = 'linear')
	#Criação das células com os valores de AVC e de 1/3 da diástole - Fim

	if prmt == '3':
		print("\n\nFirst third of diastole time: ",ThirdDiastoleTime*1000,"ms")

	DI_2CH = []
	colours=list(txt2_dr)
	if prmt == '3':
		print("\nDiastolic Recovery\n\n2CH:")
	for colour_it in range(0,tcolunas2-2):
		DI_2CH.append((txt2_dr.at[AVCvalues1[0],colours[colour_it]] - txt2_dr.at[ThirdDiastoleTime,colours[colour_it]])/txt2_dr.at[AVCvalues1[0],colours[colour_it]])
		if prmt == '3':
			print(colours[colour_it],":", DI_2CH[colour_it]*100,"%")

	DI_4CH = []
	colours=list(txt1_dr)
	if prmt == '3':
		print("\n4CH:")
	for colour_it in range(0,tcolunas1-2):
		DI_4CH.append((txt1_dr.at[AVCvalues1[0],colours[colour_it]] - txt1_dr.at[ThirdDiastoleTime,colours[colour_it]])/txt1_dr.at[AVCvalues1[0],colours[colour_it]])
		if prmt == '3':
			print(colours[colour_it],":", DI_4CH[colour_it]*100,"%")

	DI_APLAX = []
	colours=list(txt3_dr)
	if prmt == '3':
		print("\nAPLAX:")
	for colour_it in range(0,tcolunas3-2):
		DI_APLAX.append((txt3_dr.at[AVCvalues1[0],colours[colour_it]] - txt3_dr.at[ThirdDiastoleTime,colours[colour_it]])/txt3_dr.at[AVCvalues1[0],colours[colour_it]])
		if prmt == '3':
			print(colours[colour_it],":", DI_APLAX[colour_it]*100,"%")
	if prmt == '3':
		print("\n")
	ALL_DI = [DI_2CH, DI_4CH, DI_APLAX]
	ALL_DI100 = np.array(ALL_DI)*100

	if op != test_op:

		global BullseyeAux

		BullseyeAux = [ALL_DI100[0][0], ALL_DI100[2][5], ALL_DI100[1][5], ALL_DI100[0][5], ALL_DI100[2][0], ALL_DI100[1][0], ALL_DI100[0][1], ALL_DI100[2][4], ALL_DI100[1][4], ALL_DI100[0][4],ALL_DI100[2][1], ALL_DI100[1][1], ALL_DI100[0][2], ALL_DI100[2][3], ALL_DI100[1][3], ALL_DI100[0][3], ALL_DI100[2][2], ALL_DI100[1][2]]
		#O vetor APLAX está na ordem inversa.
		if prmt == '3':
			print("Segmentos Bullseye:\n")
			for i in range(18):
				print("Segmento ",i+1,"- Valor: ", BullseyeAux[i])

		if prmt == '3':
			print("\n\n")
			print("ATENCAO: REVISAR ESSE VALOR -> Diastolic Index: ", np.std(ALL_DI))
	else:
		DI_op5 = []
		DI_op5.extend(DI_2CH)
		DI_op5.extend(DI_4CH)
		DI_op5.extend(DI_APLAX)
		if prmt == '3':
			print("\n\n")
		print("Diastolic Index: ", np.std(DI_op5))
	if prmt != '0':
		Parameters_Plot()


def IVA_calc():			 #Isovolumic Aceleration by segment Calculation - To be implemented
	global segment
	global segment_IVC
	global calculated_IVA

	IVA_aux = strain_rate_lv4ch
	IVA_aux = pd.concat([IVA_aux.iloc[:,0:-2], strain_rate_lv2ch.iloc[:,0:-2], strain_rate_lv3ch.iloc[:,0:-2]], axis=1, sort = False) #Junta todas as curvas de SR
	IVA_aux = IVA_aux.interpolate(method ='quadratic')

	#for segment_number in range(IVA_aux.shape[1]): #Cada segmento sera plotado para marcacao
	for segment_number in range(7):#range(IVA_aux.shape[1]): #Cada segmento sera plotado para marcacao
		calculated_IVA = 0
		segment = IVA_aux.iloc[:,segment_number]
		a = float('NaN')
		segment.loc[IVCvalues1[0]] = a
		segment.loc[EjectionTimevalues1[0]] = a
		segment = segment.sort_index()
		segment = segment.interpolate(method = 'quadratic')
		segment_IVC = segment[(segment.index >= IVCvalues1[0]) & (segment.index <= EjectionTimevalues1[0])] #Usou para pegar o ponto mais proximo - fazer algo semelhante para um segmento
		Parameters_Plot()
		#Colocar algo pro caso da lista ser vazia(sem iva possível)
		if (not times_IVA):
			print("\n\nIVA could not be calculated. No points were marked.\n")

		else: #Vai para os pontos mais proximos aos marcados no dataframe
			print("\n\nTime Values(s): ",segment_IVC.index[segment_IVC.index.get_loc(times_IVA[0], method = 'nearest')], segment_IVC.index[segment_IVC.index.get_loc(times_IVA[1], method = 'nearest')],"\nSR Values (1/s): ", segment_IVC.iloc[segment_IVC.index.get_loc(times_IVA[0], method = 'nearest')], segment_IVC.iloc[segment_IVC.index.get_loc(times_IVA[1], method = 'nearest')])
			T_initvar = segment_IVC.index[segment_IVC.index.get_loc(times_IVA[0], method = 'nearest')]
			T_endvar =  segment_IVC.index[segment_IVC.index.get_loc(times_IVA[1], method = 'nearest')]	#Fiz assim por uma questão de saúde mental
			SR_initvar = segment_IVC.iloc[segment_IVC.index.get_loc(times_IVA[0], method = 'nearest')]
			SR_endvar = segment_IVC.iloc[segment_IVC.index.get_loc(times_IVA[1], method = 'nearest')]
			IVA = (SR_endvar-SR_initvar)/(T_endvar-T_initvar)

			print("IVA = ",IVA,"m/s²\n")
			calculated_IVA = 1
			cells = ['Y', 'Z', 'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'AG', 'AH', 'AI', 'AJ', 'AK', 'AL', 'AM', 'AN', 'AO', 'AP']
			sheet[cells[segment_number]+str(it)] = IVA
			#Parameters_Plot()


def old_IVA_calc(): 	#Isovolumic Aceleration using the average SR Calculation - To be implemented
	global avg_SR_LV
	global avg_SR_LV_IVC
	global calculated_IVA

	#calcula a média
	#Possivelmente altero aqui abaixo para calcular por segmento
	IVA_aux = strain_rate_lv4ch
	IVA_aux = pd.concat([IVA_aux.iloc[:,0:-2], strain_rate_lv2ch.iloc[:,0:-2], strain_rate_lv3ch.iloc[:,0:-2]], axis=1, sort = False)
	IVA_aux = IVA_aux.interpolate(method ='quadratic')
	#print(IVA_aux)
	avg_SR_LV = IVA_aux.mean(axis=1)
	#Adiciona valores aos pontos de inicio e fim da IVC
	a = float('NaN')
	avg_SR_LV.loc[IVCvalues1[0]] = a
	avg_SR_LV.loc[EjectionTimevalues1[0]] = a
	avg_SR_LV = avg_SR_LV.sort_index()
	avg_SR_LV = avg_SR_LV.interpolate(method = 'quadratic')
	avg_SR_LV_IVC = avg_SR_LV[(avg_SR_LV.index >= IVCvalues1[0]) & (avg_SR_LV.index <= EjectionTimevalues1[0])] #Usou para pegar o ponto mais proximo - fazer algo semelhante para um segmento
	Parameters_Plot()
	#Colocar algo pro caso da lista ser vazia(sem iva possível)
	if (not times_IVA):
		print("\n\nIVA could not be calculated. No points were marked.\n")

	else: #Vai para os pontos mais proximos aos marcados no dataframe
		print("\n\nTime Values(s): ",avg_SR_LV_IVC.index[avg_SR_LV_IVC.index.get_loc(times_IVA[0], method = 'nearest')], avg_SR_LV_IVC.index[avg_SR_LV_IVC.index.get_loc(times_IVA[1], method = 'nearest')],"\nSR Values (1/s): ", avg_SR_LV_IVC.iloc[avg_SR_LV_IVC.index.get_loc(times_IVA[0], method = 'nearest')], avg_SR_LV_IVC.iloc[avg_SR_LV_IVC.index.get_loc(times_IVA[1], method = 'nearest')])
		T_initvar = avg_SR_LV_IVC.index[avg_SR_LV_IVC.index.get_loc(times_IVA[0], method = 'nearest')]
		T_endvar =  avg_SR_LV_IVC.index[avg_SR_LV_IVC.index.get_loc(times_IVA[1], method = 'nearest')]	#Fiz assim por uma questão de saúde mental
		SR_initvar = avg_SR_LV_IVC.iloc[avg_SR_LV_IVC.index.get_loc(times_IVA[0], method = 'nearest')]
		SR_endvar = avg_SR_LV_IVC.iloc[avg_SR_LV_IVC.index.get_loc(times_IVA[1], method = 'nearest')]
		IVA = (SR_endvar-SR_initvar)/(T_endvar-T_initvar)

		print("IVA = ",IVA,"m/s²\n")
		calculated_IVA = 1
		#Indice por segmento em bullseye
		sheet['Y'+str(it)] = IVA
		#Parameters_Plot()
