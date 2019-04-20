# -*- coding: utf-8 -*-

"""
O que fazer:

Substituir a planilha
Ordenar os events e fazer a nova separacao
Verificar ordem dos eventos e fazer a separação de fases
Picos sistolicos
Verificar sincronia das curvas agora - com os txts
Adicionar a variação do Strain e SR em cada fase
Falar o segmento por nome
Taxa de amostragem (pegar do txt) -> Relacionar com HR
Retirar essas variáveis globais e modularizar o código - fica melhor ate para editar funcoes e o main ao mesmo tempo

Para o IVA:

Plotar 1 segmento por vez e marcar (iterar por eles, por paciente)
Marcar os pontos em cada um deles
Armazenar valores marcados na memória
Colocar em 18 colunas

Criar um vetor com todas as opcoes, nao so test_op
"""

#Importing packages...
import pandas as pd              # Package used to work with the raw data files
import numpy as np
import matplotlib as mpl		 # Used in the plots
import matplotlib.pyplot as plt	 # Also used in the plots
import re                        # Used to obtain the LM, RM and ES Times in the raw data files
import openpyxl                  # Package to work with .xlsx - See documentation when working with a big amount of data
from os import listdir			 # Used to obtain the files in their directories
from os.path import isfile, join # Also used to do file operations

#
#Packages that i (https://github.com/rafaelds9) created
import front
from dstationplotlib import *
from dstationcalc import *
#


#Defining constants
height_line = 1.025 # Constant to define the height of the lines that separate the phases
test_op = '6'		# Defines the number of the option that will use the simulated strain curves
SizeFont = 11		# Defines the font size in the plots
SizePhaseFont = 11  # Defines the font size of the phases' legends
SizeLabelFont = 11  # Defines the font size of the labels in the plots' axis
#


#Initializing variables
it = 4   #Defines the first row in the xl file that has values
prmt = '0' #Defines the prmt value in the first run to 0 - Change with caution
#


#Declaring variables and arrays
#Lists used to store relevant time values for the phase calculations
Dif_LM_OnsetQRS1 = []
MVOvalues1 = []			# Mitral Valve opening time in the first cycle
MVOvalues2 = []			#	'''						 second '''
MVCvalues1 = []			#	'''		   closing        '''
MVCvalues2 = []
AVOvalues1 = []			# Aortic '''
AVOvalues2 = []
AVCvalues1 = []
AVCvalues2 = []
EMCvalues1 = []			#Time values of the beginning of each phase
EMCvalues2 = []
IVCvalues1 = []
IVCvalues2 = []
EjectionTimevalues1 = []
EjectionTimevalues2 = []
IVRvalues = []
Evalues = []
Diastasisvalues = []
Avalues = []


def GLS_calc():             #Função para calculo do GLS

	#Sincronizar os tempos da plotagem dos pontos do GLS
	#Diferença nos valores médios de uma visualização
	#Talvez o ES_Time não corresponda ao AVC para aquele arquivo

	if op == test_op:
		txt1_s = txt1[(txt1.index >= MVCvalues1[0]) & (txt1.index < AVCvalues1[0])] #Valores até o AVC - Durante a sístole
		txt2_s = txt2[(txt2.index >= MVCvalues1[0]) & (txt2.index < AVCvalues1[0])]
		txt3_s = txt3[(txt3.index >= MVCvalues1[0]) & (txt3.index < AVCvalues1[0])]
	else:
		#Valores até o AVC - Durante a sístole
		txt1_s = txt1[(txt1.index >= LM_Time[0]) & (txt1.index <= ES_Time[0])]
		txt2_s = txt2[(txt2.index >= LM_Time[1]) & (txt2.index <= ES_Time[1])]
		txt3_s = txt3[(txt3.index >= LM_Time[2]) & (txt3.index <= ES_Time[2])]
	#Terei que arrumar os tempos para as marcações

	#print((tcolunas1-2)+(tcolunas2-2)+(tcolunas3-2)) #quantidade total de segmentos
	#print(list(txt2_s))                              #lista os nomes dos segmentos
	#print (colours[:-2])
	if prmt == '1':
		print("\n\nPeak negative systolic strain:\n")
	gls = []
	colours=list(txt2_s)
	for colour_it in range(0,tcolunas2-2):
		if prmt == '1':
			print("2CH:", colours[colour_it],":",round(txt2_s[colours[colour_it]].min(),1),"%","\t","Time:",txt2_s[colours[colour_it]].idxmin(),"s")
		gls.append(txt2_s[colours[colour_it]].min())
	if prmt == '1':
		print("\n")
	colours=list(txt1_s)
	for colour_it in range(0,tcolunas1-2):
		if prmt == '1':
			print("4CH:", colours[colour_it],":",round(txt1_s[colours[colour_it]].min(),1),"%","\t","Time:",txt1_s[colours[colour_it]].idxmin(),"s")
		gls.append(txt1_s[colours[colour_it]].min())
	if prmt == '1':
		print("\n")
	colours=list(txt3_s)
	for colour_it in range(0,tcolunas3-2):
		if prmt == '1':
			print("APLAX:", colours[colour_it],":",round(txt3_s[colours[colour_it]].min(),1),"%","\t","Time:",txt3_s[colours[colour_it]].idxmin(),"s")
		gls.append(txt3_s[colours[colour_it]].min())
	gls=np.mean(gls)

	if prmt == '1':
		print("\n\n")
	print("Global Longitudinal Strain: ", gls,"%\n")
	if prmt != '0':
		Parameters_Plot(txt1, txt2_mod, txt3_mod, strain_rate_lv4ch, strain_rate_lv2ch, strain_rate_lv3ch, txt_mid, tcolunas1, tcolunas2, tcolunas3, tcolunas_mid, prmt, op, test_op, END_Time1, SizeFont, SizePhaseFont, MVOvalues1, MVCvalues1,
		 				AVOvalues1, AVCvalues1, MVOvalues2, MVCvalues2, AVOvalues2, AVCvalues2, EMCvalues1, EMCvalues2, IVCvalues1, IVCvalues2, EjectionTimevalues1,
						EjectionTimevalues2, IVRvalues, Evalues, Avalues, height_line, txt1_s, txt2_s, txt3_s)
	sheet['V'+str(it)] = round(gls, 2)


def MD_calc():             #Função para calculo do MD

	if op == test_op:
		txt1_sliced_onsets = txt1[(txt1.index >= LM_Time) & (txt1.index < RM_Time)] #Obtenção da Mechanical Dispersion
		txt2_sliced_onsets = txt2[(txt2.index >= LM_Time) & (txt2.index < RM_Time)]
		txt3_sliced_onsets = txt3[(txt3.index >= LM_Time) & (txt3.index < RM_Time)]
	else:
		txt1_sliced_onsets = txt1[(txt1.index >= LM_Time[0]) & (txt1.index < RM_Time[0])]#Obtenção da Mechanical Dispersion
		txt2_sliced_onsets = txt2_mod[(txt2_mod.index >= (LM_Time[1]+LM_Time[0])) & (txt2_mod.index < (RM_Time[1]-LM_Time[0]))]
		txt3_sliced_onsets = txt3_mod[(txt3_mod.index >= (LM_Time[2]+LM_Time[0])) & (txt3_mod.index < (RM_Time[2]-LM_Time[0]))]
	global_minima_times = []
	if prmt == '2':
		print("\n\nTimes of peak negative strain:\n")

	colours=list(txt2_sliced_onsets)
	for colour_it in range(0,tcolunas2-2):
		if prmt == '2':
			if op == test_op:
				print("2CH:", colours[colour_it],":",txt2_sliced_onsets[colours[colour_it]].idxmin(),"ms")
			else:
				print("2CH:", colours[colour_it],":",txt2_sliced_onsets[colours[colour_it]].idxmin(),"ms")
		global_minima_times.append(txt2_sliced_onsets[colours[colour_it]].idxmin())
	if prmt == '2':
		print("\n")

	colours=list(txt1_sliced_onsets)
	for colour_it in range(0,tcolunas1-2):
		if prmt == '2':
			if op == test_op:
				print("4CH:", colours[colour_it],":",txt1_sliced_onsets[colours[colour_it]].idxmin(),"ms")
			else:
				print("4CH:", colours[colour_it],":",txt1_sliced_onsets[colours[colour_it]].idxmin(),"ms")
		global_minima_times.append(txt1_sliced_onsets[colours[colour_it]].idxmin())
	if prmt == '2':
		print("\n")

	colours=list(txt3_sliced_onsets)
	for colour_it in range(0,tcolunas3-2):
		if prmt == '2':
			if op == test_op:
				print("APLAX:", colours[colour_it],":",txt3_sliced_onsets[colours[colour_it]].idxmin(),"ms")
			else:
				print("APLAX:", colours[colour_it],":",txt3_sliced_onsets[colours[colour_it]].idxmin(),"ms")
		global_minima_times.append(txt3_sliced_onsets[colours[colour_it]].idxmin())

	if prmt == '2':
		print("\n\n")
	print("Mechanical Dispersion: ",round(np.std(global_minima_times,dtype=np.float64,ddof=1)*1000, 2), "ms") #IMPORTANTE: CALCULA A STD DA POPULAÇÃO

	if prmt != '0':
		Parameters_Plot(txt1, txt2_mod, txt3_mod, txt_mid, strain_rate_lv4ch, strain_rate_lv2ch, strain_rate_lv3ch, tcolunas1, tcolunas2, tcolunas3, tcolunas_mid, prmt, op, test_op, END_Time1, SizeFont, SizePhaseFont, MVOvalues1, MVCvalues1,
		 				AVOvalues1, AVCvalues1, MVOvalues2, MVCvalues2, AVOvalues2, AVCvalues2, EMCvalues1, EMCvalues2, IVCvalues1, IVCvalues2, EjectionTimevalues1,
						EjectionTimevalues2, IVRvalues, Evalues, Avalues, height_line, txt1_sliced_onsets, txt2_sliced_onsets, txt3_sliced_onsets)

	sheet['W'+str(it)] = round(np.std(global_minima_times,dtype=np.float64,ddof=1)*1000, 2) #IMPORTANTE: CALCULA A STD DA POPULAÇÃO


def DI_calc():             #Função para calculo do DI

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


def IVA_calc():
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
			#Colocar tudo num bullseye depois

def old_IVA_calc(): #Calculo do IVA usando a media das curvas de SR
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

print("\033c", end='') #Caso queira limpar o terminal

#Início da abertura dos .txt

#idPatient = input('Patient ID: ')

print("Options:\n\t1. Strain LV, Strain Rate LV and ECG\n\t2. Strain LV, Strain LA and ECG")
print("\t3. Strain LV, Strain Rate LA and ECG\n\t4. Strain LV, Strain RV and ECG")
print("\t5. Strain LV, Strain Rate LV and ECG (without SR files)\n\t"+test_op+". Test Option")
op = input("Option: ")


idPatient = 'Aristoteles'
#op = '5'

if op != test_op:
	exams_path = ('Patients/'+idPatient)
else:
	exams_path = ('Simulations/'+idPatient)

list_txtfiles = [f for f in listdir(exams_path) if isfile(join(exams_path, f))]

if op == "1":
	for f in list_txtfiles:
		if ('4CH_SL_TRACE' in f) or ('4CH_SL4CH STRAIN_TRACE' in f) or ('4CH_Peak dose_SL_TRACE' in f):
			txt1=pd.read_csv(exams_path+'/'+f, sep='\t', engine='python', skiprows=3, index_col=0) #Parte do índice arrumada
		if ('4CH_SrL' in f) or ('4CH_SrL4CH SR LV_TRACE' in f) or ('4CH_SrL4CH SR_TRACE' in f) or ('4CH_Peak dose_SrL_TRACE' in f):
			txt_mid=pd.read_csv(exams_path+'/'+f, sep='\t', engine='python', skiprows=3, index_col=0)
			strain_rate_lv4ch = txt_mid
		if ('2CH_SL_TRACE' in f) or ('2CH_SL2CH STRAIN_TRACE' in f) or ('2CH_Low dose_SL_TRACE' in f):
			txt2=pd.read_csv(exams_path+'/'+f, sep='\t', engine='python', skiprows=3, index_col=0)
		if ('APLAX_SL_TRACE' in f) or ('APLAX_SL3CH STRAIN_TRACE' in f) or ('APLAX_Low dose_SL_TRACE' in f):
			txt3=pd.read_csv(exams_path+'/'+f, sep='\t', engine='python', skiprows=3, index_col=0)

elif op == "2":
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

elif op == "3":
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

elif op == "4":
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

elif op == "5":
	for f in list_txtfiles:
		if ('4CH_SL_TRACE' in f) or ('4CH_SL4CH STRAIN_TRACE' in f) or ('4CH_Peak dose_SL_TRACE' in f):
			txt1=pd.read_csv(exams_path+'/'+f, sep='\t', engine='python', skiprows=3, index_col=0) #Parte do índice arrumada
		if ('2CH_SL_TRACE' in f) or ('2CH_SL2CH STRAIN_TRACE' in f) or ('2CH_Low dose_SL_TRACE' in f):
			txt2=pd.read_csv(exams_path+'/'+f, sep='\t', engine='python', skiprows=3, index_col=0)
		if ('APLAX_SL_TRACE' in f) or ('APLAX_SL3CH STRAIN_TRACE' in f) or ('APLAX_Low dose_SL_TRACE' in f):
			txt3=pd.read_csv(exams_path+'/'+f, sep='\t', engine='python', skiprows=3, index_col=0)

elif op == test_op:
	for f in list_txtfiles:
		if '4CH_teste' in f:
			txt1=pd.read_csv(exams_path+'/'+f, sep='\t', engine='python', skiprows=3, index_col=0)
			txt_mid=txt1.diff()
		if '2CH_teste' in f:
			txt2=pd.read_csv(exams_path+'/'+f, sep='\t', engine='python', skiprows=3, index_col=0)
		if 'APLAX_teste' in f:
			txt3=pd.read_csv(exams_path+'/'+f, sep='\t', engine='python', skiprows=3, index_col=0)

else:
	for f in list_txtfiles:
		if '4CH_SL_TRACE' in f:
			txt1=pd.read_csv(exams_path+'/'+f, sep='\t', engine='python', skiprows=3, index_col=0) #Parte do índice arrumada
		if '4CH_SrL4CH SR LV_TRACE' in f:
			txt_mid=pd.read_csv(exams_path+'/'+f, sep='\t', engine='python', skiprows=3, index_col=0)
			strain_rate_lv4ch = txt_mid
		if '2CH_SL_TRACE' in f:
			txt2=pd.read_csv(exams_path+'/'+f, sep='\t', engine='python', skiprows=3, index_col=0)
		if 'APLAX_SL_TRACE' in f:
			txt3=pd.read_csv(exams_path+'/'+f, sep='\t', engine='python', skiprows=3, index_col=0)


LM_Time = []
RM_Time = []
ES_Time = []

for f in list_txtfiles:
	if ('4CH_SL_TRACE' in f) or ('4CH_SL4CH STRAIN_TRACE' in f) or ('4CH_Peak dose_SL_TRACE' in f):
		txt_original = open(exams_path+'/'+f, 'r')
		numbers = re.findall("\d+\.\d+", txt_original.readlines()[2]) #Numeros extraidos da linha 3 do txt - LM_Time, ES_Time e RM_Time
		txt_original.close()
		LM_Time.append(float(numbers[0]))
		RM_Time.append(float(numbers[1]))
		ES_Time.append(float(numbers[2]))

for f in list_txtfiles:
	if ('2CH_SL_TRACE' in f) or ('2CH_SL2CH STRAIN_TRACE' in f) or ('2CH_Low dose_SL_TRACE' in f):
		txt_original = open(exams_path+'/'+f, 'r')
		numbers = re.findall("\d+\.\d+", txt_original.readlines()[2]) #Numeros extraidos da linha 3 do txt - LM_Time, ES_Time e RM_Time
		txt_original.close()
		LM_Time.append(float(numbers[0]))
		RM_Time.append(float(numbers[1]))
		ES_Time.append(float(numbers[2]))

for f in list_txtfiles:
	if ('APLAX_SL_TRACE' in f) or ('APLAX_SL3CH STRAIN_TRACE' in f) or ('APLAX_Low dose_SL_TRACE' in f):
		txt_original = open(exams_path+'/'+f, 'r')
		numbers = re.findall("\d+\.\d+", txt_original.readlines()[2]) #Numeros extraidos da linha 3 do txt - LM_Time, ES_Time e RM_Time
		txt_original.close()
		LM_Time.append(float(numbers[0]))
		RM_Time.append(float(numbers[1]))
		ES_Time.append(float(numbers[2]))
#Fim da abertura dos .txt

txt1.drop('Unnamed: 1', axis=1, inplace=True) #Retira a coluna inútil que é lida (devido à tabulação exagerada do arquivo exportado)
txt2.drop('Unnamed: 1', axis=1, inplace=True)
txt3.drop('Unnamed: 1', axis=1, inplace=True)
if op != "5" and op != test_op:
	txt_mid.drop('Unnamed: 1', axis=1, inplace=True)
#strain_rate_lv4ch.drop('Unnamed: 1', axis=1, inplace=True)

txt2_mod=txt2.copy(deep=True)  		#Se deep for false é uma shallow copy, index e data são compartilhados
txt2_mod.index = txt2_mod.index-(LM_Time[1]-LM_Time[0])
txt3_mod=txt3.copy(deep=True)
txt3_mod.index = txt3_mod.index-(LM_Time[2]-LM_Time[0])

if op == "5" or op == test_op:
	txt_mid=txt1.diff()
	strain_rate_lv4ch = txt_mid.truediv(txt1.index.to_series().diff(), axis = 0)/100
strain_rate_lv2ch = txt2_mod.diff().truediv(txt2_mod.index.to_series().diff(), axis = 0)/100
strain_rate_lv3ch = txt3_mod.diff().truediv(txt3_mod.index.to_series().diff(), axis = 0)/100

tcolunas1=int(((txt1.size/len(txt1.index))))
tcolunas2=int(((txt2.size/len(txt2.index))))
tcolunas3=int(((txt3.size/len(txt3.index))))
tcolunas_mid=int(((txt_mid.size/len(txt_mid.index))))
tcolunas_strain_rate_lv4ch = int(((strain_rate_lv4ch.size/len(strain_rate_lv4ch.index))))

#Sort para detectar o menor index -  #para que um gráfico não fique sobrando

END_Time0 = sorted([txt1.index[len(txt1.index)-1], txt2.index[len(txt2.index)-1], txt3.index[len(txt3.index)-1], strain_rate_lv4ch.index[len(strain_rate_lv4ch.index)-1]])[3]

#Para o gráfico dos parâmetros - Início
#achar o menor entre os strains e comparar com o do meio
END_Time1 = sorted([txt1.index[len(txt1.index)-1], txt2.index[len(txt2.index)-1], txt3.index[len(txt3.index)-1], txt_mid.index[len(txt_mid.index)-1]])[3]
#Para o gráfico dos parâmetros - Fim

#Início da abertura da planilha
wb = openpyxl.load_workbook('Event_Timing.xlsx')
sheet = wb['Sheet1']
#Determinar a linha correspondente ao paciente:
for cell in sheet['A']:
	if(cell.value is not None): #We need to check that the cell is not empty.
		if idPatient == cell.value: #Check if the value of the cell contains the idPatient
			it = format(cell.row)
#Fim da abertura da planilha

if op != test_op:
	#Gravação dos valores marcados na planilha do excel - INÍCIO
	print("\n\nMarcacao do Onset QRS 1, onset P, onset QRS 2")
	xcoord = PlotClick(txt1, tcolunas1, LM_Time[0], ES_Time[0], RM_Time[0], END_Time0, SizeFont, op, test_op, strain_rate_lv4ch,tcolunas_strain_rate_lv4ch, prmt)
	sheet['G'+str(it)] = round(xcoord[0],0) #Houve um arredondamento do tempo em ms - ONSET QRS 1
	#sheet['Q'+str(it)] = round(xcoord[1],0) #Houve um arredondamento do tempo em ms - Ponto de Diástase
	sheet['I'+str(it)] = round(xcoord[1],0) #Houve um arredondamento do tempo em ms - ONSET P
	sheet['H'+str(it)] = round(xcoord[2],0) #Houve um arredondamento do tempo em ms - #ONSET QRS 2
	#Gravação dos valores marcados na planilha do excel - FIM


MVOvalues1.append((int(sheet['C'+str(it)].value)/1000)+LM_Time[0])#Valor do MVO à esquerda: Valor de MVO da planilha(em ms)/1000 + LM_Time(em s)
MVCvalues1.append((int(sheet['D'+str(it)].value)/1000)+LM_Time[0])#Valor do MVC à esquerda: Valor de MVC da planilha(em ms)/1000 + LM_Time(em s)
AVOvalues1.append((int(sheet['E'+str(it)].value)/1000)+LM_Time[0])#Valor do AVO à esquerda: Valor de AVO da planilha(em ms)/1000 + LM_Time(em s)
AVCvalues1.append((int(sheet['F'+str(it)].value)/1000)+LM_Time[0])#Valor do AVC à esquerda: Valor de AVC da planilha(em ms)/1000 + LM_Time(em s)
MVOvalues2.append((int(sheet['C'+str(it)].value)/1000)+RM_Time[0])#Valor do MVO à esquerda: Valor de MVO da planilha(em ms)/1000 + RM_Time(em s)
MVCvalues2.append((int(sheet['D'+str(it)].value)/1000)+RM_Time[0])#Valor do MVC à esquerda: Valor de MVC da planilha(em ms)/1000 + RM_Time(em s)
AVOvalues2.append((int(sheet['E'+str(it)].value)/1000)+RM_Time[0])#Valor do AVO à esquerda: Valor de AVO da planilha(em ms)/1000 + RM_Time(em s)
AVCvalues2.append((int(sheet['F'+str(it)].value)/1000)+RM_Time[0])#Valor do AVC à esquerda: Valor de AVC da planilha(em ms)/1000 + RM_Time(em s)
if op != test_op:
	Dif_LM_OnsetQRS1.append(LM_Time[0] - (int(sheet['G'+str(it)].value)/1000)) #Diferença entre o Onset QRS 1 e o LM_Time

#Recomputação devido à limitações do package para pegar valores da planilha - Não é preciso adicionar LM_Time aos valores marcados no programa
if op != test_op:
	EMCvalues1.append((int(sheet['G'+str(it)].value)/1000))                 #Início de EMC1 = Onset QRS 1(em ms)/1000
	EMCvalues2.append((int(sheet['H'+str(it)].value)/1000))                 #Início de EMC2 = Onset QRS 2(em ms)/1000
IVCvalues1.append((int(sheet['D'+str(it)].value)/1000+LM_Time[0]))             #Início de IVC1 = MVC(em ms)/1000 + LM_Time
IVCvalues2.append((int(sheet['D'+str(it)].value)/1000+RM_Time[0]))             #Início de IVC2 = MVC(em ms)/1000 + RM_Time
EjectionTimevalues1.append((int(sheet['E'+str(it)].value)/1000+LM_Time[0]))    #Início de EjectionTime1 = AVO(em ms)/1000 + LM_Time
EjectionTimevalues2.append((int(sheet['E'+str(it)].value)/1000+RM_Time[0]))    #Início de EjectionTime2 = AVO(em ms)/1000 + RM_Time
IVRvalues.append((int(sheet['F'+str(it)].value)/1000+LM_Time[0]))             #Início de IVR = AVC(em ms)/1000 + LM_Time
Evalues.append((int(sheet['C'+str(it)].value)/1000+LM_Time[0]))                #Início de E = MVO(em ms)/1000 + LM_Time
if op != test_op:
	#Diastasisvalues.append((int(sheet['Q'+str(it)].value)/1000))            #Início da Diastase = D point/1000
	Avalues.append((int(sheet['I'+str(it)].value)/1000))                    #Início de A = Onset P(em ms)/1000

#Os valores acima são usados na separação das fases

#Impressão dos valores trabalhados no terminal
print("\nLM_Time: ",LM_Time[0]*1000, "ms")
print("RM_Time: ",RM_Time[0]*1000, "ms")
if op != test_op:
	print("Difference between LM_Time and Onset QRS1:", Dif_LM_OnsetQRS1[0]*1000, "ms")
print("\nMVO1: ",MVOvalues1[0]*1000, "ms")
print("MVO2: ",MVOvalues2[0]*1000, "ms")
print("MVC1: ",MVCvalues1[0]*1000, "ms")
print("MVC2: ",MVCvalues2[0]*1000, "ms")
print("AVO1: ",AVOvalues1[0]*1000, "ms")
print("AVO2: ",AVOvalues2[0]*1000, "ms")
print("AVC1: ",AVCvalues1[0]*1000, "ms")
print("AVC2: ",AVCvalues2[0]*1000, "ms")
if op != test_op:
	print("\nEMC1: ",EMCvalues1[0]*1000, "ms")
	sheet['J'+str(it)] = round(EMCvalues1[0]*1000)
	print("EMC2: ",EMCvalues2[0]*1000, "ms")
	sheet['P'+str(it)] = round(EMCvalues2[0]*1000)
print("IVC1: ",IVCvalues1[0]*1000, "ms")
sheet['K'+str(it)] = round(IVCvalues1[0]*1000)
print("IVC2: ",IVCvalues2[0]*1000, "ms")
sheet['Q'+str(it)] = round(IVCvalues2[0]*1000)
print("Ejection Time1: ",EjectionTimevalues1[0]*1000, "ms")
sheet['L'+str(it)] = round(EjectionTimevalues1[0]*1000)
print("Ejection Time2: ",EjectionTimevalues2[0]*1000, "ms")
sheet['R'+str(it)] = round(EjectionTimevalues2[0]*1000)
print("IVR: ",IVRvalues[0]*1000, "ms")
sheet['M'+str(it)] = round(IVRvalues[0]*1000)
print("E: ",Evalues[0]*1000, "ms")
sheet['N'+str(it)] = round(Evalues[0]*1000)
if op != test_op:
	#print("Diastasis: ",Diastasisvalues[0]*1000, "ms")
	print("Atrial Systole: ",Avalues[0]*1000, "ms")
	sheet['O'+str(it)] = round(Avalues[0]*1000)
else:
	systolic_time = (AVCvalues1[0]-MVCvalues1[0])
	print("Systolic Time: ", systolic_time*1000)
	sheet['S'+str(it)] = (systolic_time*1000)
	print("Diastolic Time: ", (RM_Time[0] - systolic_time)*1000)
	sheet['T'+str(it)] = ((RM_Time[0] - systolic_time)*1000)
	print("Ratio: Systolic Time/Diastolic Time: ",(systolic_time/(RM_Time[0] - systolic_time)))
	sheet['U'+str(it)] = (systolic_time/(RM_Time[0] - systolic_time))


print("\n")
GLS_calc()
MD_calc()
#DI_calc()
print("\n\n")

calculated_IVA = 0

while True:
	print("\n\nParameters:\n\t1. Global Longitudinal Strain\n\t2. Mechanical Dispersion")
	#print("\t3. Diastolic Recovery")
	print("\t4. Show plot w/o any parameters\n\t0. Terminate program")
	prmt = input("Parameter: ")
	#prmt="8"

	if prmt == "1":                                                             #Obtenção do Global Longitudinal Strain
		GLS_calc()

	elif prmt == "2":
		MD_calc()

	#elif prmt == "3":
	#    DI_calc()
	#    DR_bullseye(BullseyeAux)
		#Ver a barra

	elif prmt == "4":
		print("\nPlot w/o any parameters")
		Parameters_Plot(txt1, txt2_mod, txt3_mod, txt_mid, strain_rate_lv4ch, strain_rate_lv2ch, strain_rate_lv3ch, tcolunas1, tcolunas2, tcolunas3, tcolunas_mid, prmt, op, test_op, END_Time1, SizeFont, SizePhaseFont, MVOvalues1, MVCvalues1,
		 				AVOvalues1, AVCvalues1, MVOvalues2, MVCvalues2, AVOvalues2, AVCvalues2, EMCvalues1, EMCvalues2, IVCvalues1, IVCvalues2, EjectionTimevalues1,
						EjectionTimevalues2, IVRvalues, Evalues, Avalues, height_line, None, None, None)

	#elif prmt == "8":		#IVA - Not working right now
		#IVA_calc()
		#break
	elif prmt == "0":
		break

	else:
		print("\n\nInvalid option\n\n\n")
		continue
	print("\n")

wb.save("Event_Timing.xlsx")
