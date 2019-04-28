# -*- coding: utf-8 -*-

"""
O que fazer:

Ordenar os events e fazer a nova separacao
Verificar ordem dos eventos e fazer a separação de fases
Picos sistolicos
Verificar sincronia das curvas agora - com os txts
Adicionar a variação do Strain e SR em cada fase
Falar o segmento por nome
Taxa de amostragem (pegar do txt) -> Relacionar com HR
Retirar essas variáveis globais e modularizar o código

Criar um vetor com todas as opcoes, nao so test_op

Futuramente: Razão E/e’Sr
"""

#Importing packages...
import pandas as pd              # Package used to work with the raw data files
import numpy as np
import openpyxl                  # Package to work with .xlsx - See documentation when working with a big amount of data


#
#Packages that i (https://github.com/rafaelds9) created
import front
from dstationplotlib import *
from dstationparameters import *
from rawdatafiles import *
#


#Defining constants
height_line = 1.025 # Constant to define the height of the lines that separate the phases
test_op = '6'		# Defines the number of the option that will use the simulated strain curves
SizeFont = 11		# Defines the font size in the plots
SizePhaseFont = 11  # Defines the font size of the phases' legends
SizeLabelFont = 11  # Defines the font size of the labels in the plots' axis
#


#Initializing variables
it = 3   #Defines the first row in the xl file that has values
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



#MAIN
print("\033c", end='') # Clears the terminal


#idPatient = input('Patient ID: ')
print("Options:\n\t1. Strain LV, Strain Rate LV and ECG\n\t2. Strain LV, Strain LA and ECG")
print("\t3. Strain LV, Strain Rate LA and ECG\n\t4. Strain LV, Strain RV and ECG")
print("\t5. Strain LV, Strain Rate LV and ECG (without SR files)\n\t"+test_op+". Test Option")
op = input("Option: ")

idPatient = 'Aristoteles'	# Used to debug
#op = '5'					# Used to debug

if op != test_op:
	exams_path = ('Patients/'+idPatient)
else:
	exams_path = ('Simulations/'+idPatient)


txt1, txt2, txt3, txt_mid, strain_rate_lv4ch, LM_Time, RM_Time, ES_Time = openfiles(exams_path, op, test_op)


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


# Sheet is open
wb = openpyxl.load_workbook('Patients_DB.xlsx')
sheet = wb['Sheet1']
#Determinar a linha correspondente ao paciente:
for cell in sheet['A']:
	if(cell.value is not None): #We need to check that the cell is not empty.
		if idPatient == cell.value: #Check if the value of the cell contains the idPatient
			it = format(cell.row)

#Points are marked in the ECG curve
if op != test_op:
	#Gravação dos valores marcados na planilha do excel - INÍCIO
	print("\n\nMarcacao do Onset QRS 1, onset P, onset QRS 2")
	xcoord = PlotClick(txt1, tcolunas1, LM_Time[0], ES_Time[0], RM_Time[0], END_Time0, SizeFont, op, test_op, strain_rate_lv4ch,tcolunas_strain_rate_lv4ch, prmt)
	sheet['U'+str(it)] = round(xcoord[0],0) #Houve um arredondamento do tempo em ms - ONSET QRS 1
	#sheet['Q'+str(it)] = round(xcoord[1],0) #Houve um arredondamento do tempo em ms - Ponto de Diástase
	sheet['V'+str(it)] = round(xcoord[1],0) #Houve um arredondamento do tempo em ms - ONSET P
	sheet['W'+str(it)] = round(xcoord[2],0) #Houve um arredondamento do tempo em ms - #ONSET QRS 2
	#Gravação dos valores marcados na planilha do excel - FIM



MVOvalues1.append((int(sheet['Q'+str(it)].value)/1000)+LM_Time[0])#Valor do MVO à esquerda: Valor de MVO da planilha(em ms)/1000 + LM_Time(em s)
MVCvalues1.append((int(sheet['R'+str(it)].value)/1000)+LM_Time[0])#Valor do MVC à esquerda: Valor de MVC da planilha(em ms)/1000 + LM_Time(em s)
AVOvalues1.append((int(sheet['S'+str(it)].value)/1000)+LM_Time[0])#Valor do AVO à esquerda: Valor de AVO da planilha(em ms)/1000 + LM_Time(em s)
AVCvalues1.append((int(sheet['T'+str(it)].value)/1000)+LM_Time[0])#Valor do AVC à esquerda: Valor de AVC da planilha(em ms)/1000 + LM_Time(em s)
MVOvalues2.append((int(sheet['Q'+str(it)].value)/1000)+RM_Time[0])#Valor do MVO à esquerda: Valor de MVO da planilha(em ms)/1000 + RM_Time(em s)
MVCvalues2.append((int(sheet['R'+str(it)].value)/1000)+RM_Time[0])#Valor do MVC à esquerda: Valor de MVC da planilha(em ms)/1000 + RM_Time(em s)
AVOvalues2.append((int(sheet['S'+str(it)].value)/1000)+RM_Time[0])#Valor do AVO à esquerda: Valor de AVO da planilha(em ms)/1000 + RM_Time(em s)
AVCvalues2.append((int(sheet['T'+str(it)].value)/1000)+RM_Time[0])#Valor do AVC à esquerda: Valor de AVC da planilha(em ms)/1000 + RM_Time(em s)
if op != test_op:
	Dif_LM_OnsetQRS1.append(LM_Time[0] - (int(sheet['U'+str(it)].value)/1000)) #Diferença entre o Onset QRS 1 e o LM_Time

#Recomputação devido à limitações do package para pegar valores da planilha - Não é preciso adicionar LM_Time aos valores marcados no programa
if op != test_op:
	EMCvalues1.append((int(sheet['U'+str(it)].value)/1000))                 #Início de EMC1 = Onset QRS 1(em ms)/1000
	EMCvalues2.append((int(sheet['W'+str(it)].value)/1000))                 #Início de EMC2 = Onset QRS 2(em ms)/1000
IVCvalues1.append((int(sheet['R'+str(it)].value)/1000+LM_Time[0]))             #Início de IVC1 = MVC(em ms)/1000 + LM_Time
IVCvalues2.append((int(sheet['R'+str(it)].value)/1000+RM_Time[0]))             #Início de IVC2 = MVC(em ms)/1000 + RM_Time
EjectionTimevalues1.append((int(sheet['S'+str(it)].value)/1000+LM_Time[0]))    #Início de EjectionTime1 = AVO(em ms)/1000 + LM_Time
EjectionTimevalues2.append((int(sheet['S'+str(it)].value)/1000+RM_Time[0]))    #Início de EjectionTime2 = AVO(em ms)/1000 + RM_Time
IVRvalues.append((int(sheet['T'+str(it)].value)/1000+LM_Time[0]))             #Início de IVR = AVC(em ms)/1000 + LM_Time
Evalues.append((int(sheet['Q'+str(it)].value)/1000+LM_Time[0]))                #Início de E = MVO(em ms)/1000 + LM_Time
if op != test_op:
	#Diastasisvalues.append((int(sheet['Q'+str(it)].value)/1000))            #Início da Diastase = D point/1000
	Avalues.append((int(sheet['V'+str(it)].value)/1000))                    #Início de A = Onset P(em ms)/1000

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
	sheet['X'+str(it)] = round(EMCvalues1[0]*1000)
	print("EMC2: ",EMCvalues2[0]*1000, "ms")
	sheet['AD'+str(it)] = round(EMCvalues2[0]*1000)
print("IVC1: ",IVCvalues1[0]*1000, "ms")
sheet['Y'+str(it)] = round(IVCvalues1[0]*1000)
print("IVC2: ",IVCvalues2[0]*1000, "ms")
sheet['AE'+str(it)] = round(IVCvalues2[0]*1000)
print("Ejection Time1: ",EjectionTimevalues1[0]*1000, "ms")
sheet['Z'+str(it)] = round(EjectionTimevalues1[0]*1000)
print("Ejection Time2: ",EjectionTimevalues2[0]*1000, "ms")
sheet['AF'+str(it)] = round(EjectionTimevalues2[0]*1000)
print("IVR: ",IVRvalues[0]*1000, "ms")
sheet['AA'+str(it)] = round(IVRvalues[0]*1000)
print("E: ",Evalues[0]*1000, "ms")
sheet['AB'+str(it)] = round(Evalues[0]*1000)

if op != test_op:
	#print("Diastasis: ",Diastasisvalues[0]*1000, "ms")
	print("Atrial Systole: ",Avalues[0]*1000, "ms")
	sheet['AC'+str(it)] = round(Avalues[0]*1000)

systolic_time = (AVCvalues1[0]-MVCvalues1[0])
print("Systolic Time: ", systolic_time*1000)
sheet['AG'+str(it)] = (systolic_time*1000)
print("Diastolic Time: ", (RM_Time[0] - systolic_time)*1000)
sheet['AH'+str(it)] = ((RM_Time[0] - systolic_time)*1000)
print("Ratio: Systolic Time/Diastolic Time: ",(systolic_time/(RM_Time[0] - systolic_time)))
sheet['AI'+str(it)] = (systolic_time/(RM_Time[0] - systolic_time))
print("\n")

outGLS = GLS_calc(txt1, txt2, txt3, op, test_op, prmt, LM_Time, ES_Time, AVCvalues1, tcolunas1, tcolunas2, tcolunas3)
sheet['AJ'+str(it)] = outGLS[0]

outMD = MD_calc(txt1, txt2, txt3, txt2_mod, txt3_mod, op, test_op, prmt, LM_Time, RM_Time, AVCvalues1, tcolunas1, tcolunas2, tcolunas3)
sheet['AK'+str(it)] = outMD[0]

#DI_calc()
print("\n\n")

calculated_IVA = 0	#Currently not used

while True:
	print("\n\nParameters:\n\t1. Global Longitudinal Strain\n\t2. Mechanical Dispersion")
	#print("\t3. Diastolic Recovery")
	print("\t4. Show plot w/o any parameters\n\t0. Terminate program")
	prmt = input("Parameter: ")
	#prmt="8"

	if prmt == "1":                                                             #Obtenção do Global Longitudinal Strain
		outGLS = GLS_calc(txt1, txt2, txt3, op, test_op, prmt, LM_Time, ES_Time, AVCvalues1, tcolunas1, tcolunas2, tcolunas3)
		Parameters_Plot(txt1, txt2_mod, txt3_mod, txt_mid, strain_rate_lv4ch, strain_rate_lv2ch, strain_rate_lv3ch, tcolunas1, tcolunas2, tcolunas3, tcolunas_mid, prmt,
		 				op, test_op, END_Time1, SizeFont, SizePhaseFont, MVOvalues1, MVCvalues1, AVOvalues1, AVCvalues1, MVOvalues2, MVCvalues2, AVOvalues2, AVCvalues2,
						EMCvalues1, EMCvalues2, IVCvalues1, IVCvalues2, EjectionTimevalues1, EjectionTimevalues2, IVRvalues, Evalues, Avalues, height_line, outGLS[1], outGLS[2], outGLS[3])
		sheet['AJ'+str(it)] = outGLS[0]

	elif prmt == "2":
		outMD = MD_calc(txt1, txt2, txt3, txt2_mod, txt3_mod, op, test_op, prmt, LM_Time, RM_Time, AVCvalues1, tcolunas1, tcolunas2, tcolunas3)
		Parameters_Plot(txt1, txt2_mod, txt3_mod, txt_mid, strain_rate_lv4ch, strain_rate_lv2ch, strain_rate_lv3ch, tcolunas1, tcolunas2, tcolunas3, tcolunas_mid, prmt,
						op, test_op, END_Time1, SizeFont, SizePhaseFont, MVOvalues1, MVCvalues1, AVOvalues1, AVCvalues1, MVOvalues2, MVCvalues2, AVOvalues2, AVCvalues2,
						EMCvalues1, EMCvalues2, IVCvalues1, IVCvalues2, EjectionTimevalues1, EjectionTimevalues2, IVRvalues, Evalues, Avalues, height_line, outMD[1], outMD[2], outMD[3])
		sheet['AK'+str(it)] = outMD[0]


	#elif prmt == "3": #DI - Not working right now/to be implemented later
	#    DI_calc()
	#    DR_bullseye(BullseyeAux)
		#Ver a barra

	elif prmt == "4":
		print("\nPlot w/o any parameters")
		Parameters_Plot(txt1, txt2_mod, txt3_mod, txt_mid, strain_rate_lv4ch, strain_rate_lv2ch, strain_rate_lv3ch, tcolunas1, tcolunas2, tcolunas3, tcolunas_mid, prmt, op, test_op, END_Time1, SizeFont, SizePhaseFont, MVOvalues1, MVCvalues1,
		 				AVOvalues1, AVCvalues1, MVOvalues2, MVCvalues2, AVOvalues2, AVCvalues2, EMCvalues1, EMCvalues2, IVCvalues1, IVCvalues2, EjectionTimevalues1,
						EjectionTimevalues2, IVRvalues, Evalues, Avalues, height_line, None, None, None)

	#elif prmt == "8":		#IVA - Not working right now/to be implemented later
		#IVA_calc()
		#break

	elif prmt == "0":
		break

	else:
		print("\n\nInvalid option\n\n\n")
		continue
	print("\n")

wb.save("Patients_DB.xlsx")		#mudar para a nova - criar uma etapa só para trabalhar com a planilha
