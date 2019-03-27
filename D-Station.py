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
Retirar essas variáveis globais e modularizar o código - fica melhor ate para editar funcoes e o main ao mesmo tempo


Para o IVA:

Plotar 1 segmento por vez e marcar (iterar por eles, por paciente)
Marcar os pontos em cada um deles
Armazenar valores marcados na memória
Colocar em 18 colunas


Ideia: Ir retirando funcoes aos poucos e reimplementando para evitar a dependencia entre elas
e aos poucos reorganizar o codigo para divulga-lo
"""

import pandas as pd              #Package usado no trabalho com os arquivos .txt
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import re                        #Package padrão - Para extrair números da string
import openpyxl                  #Package para trabalhar com os arquivos .xlsx - Para trabalhar com grandes quantidades deve-se ver a documentação
from os import listdir
from os.path import isfile, join


#Constantes a serem definidas
height_line = 1.025 #Tamanho que a linha das fases ultrapassa o gráfico
test_op = '6'		#Defines that the option in which the simulated strain curves are used
SizeFont = 11		#Defines the font size in the plots
SizePhaseFont = 11  #Defines the font size of the phases' legends
SizeLabelFont = 11  #Defines the font size of the labels in the plots' axis

#Declaração de variaveis
xcoord = []			#List where the selected xvalues in the first plot are stored

Dif_LM_OnsetQRS1 = []
MVOvalues1 = []
MVOvalues2 = []
MVCvalues1 = []
MVCvalues2 = []
AVOvalues1 = []
AVOvalues2 = []
AVCvalues1 = []
AVCvalues2 = []
EMCvalues1 = []
EMCvalues2 = []
IVCvalues1 = []
IVCvalues2 = []
EjectionTimevalues1 = []
EjectionTimevalues2 = []
IVRvalues = []
Evalues = []
Diastasisvalues = []
Avalues = []

#Inicialiazação de Variáveis:
it = 4   #Iterador para a marcação na planilha (Depende da linha inicial nela, nesse caso os valores estão a partir da linha 4)
prmt = '0'

#Função para ler apenas as P colunas do dataframe - INÍCIO
def front(self, n):
	return self.iloc[:, :n]

pd.DataFrame.front = front
#Função para ler apenas as P colunas do dataframe - FIM

#Função para marcação dos pontos no ECG - INÍCIO
def onclick(event):
	#print ("\nValue: Time = %f milliseconds"%(event.xdata*1000))
	if prmt != "8":
		xcoord.append(event.xdata*1000)
	else:
		times_IVA.append(event.xdata)
#Função para marcação dos pontos no ECG - FM

#Plotagem com as cores correspondentes ao arquivo - INÍCIO
def colorPlot(txt,tcolunas):
	colours=list(txt)
	for it in range(0,tcolunas-2):
		if(colours[it] == '      RED    '):
			plt.plot(txt.iloc[:,it], 'r')
		elif(colours[it] == '     BLUE    '):
			plt.plot(txt.iloc[:,it], 'b')
		elif(colours[it] == '  MAGENTA    '):
			plt.plot(txt.iloc[:,it], 'm')
		elif(colours[it] == '    GREEN    '):
			plt.plot(txt.iloc[:,it], 'g')
		elif(colours[it] == '     CYAN    '):
			plt.plot(txt.iloc[:,it], 'c')
		elif(colours[it] == '   YELLOW    '):
			plt.plot(txt.iloc[:,it], 'y')
		else:
			plt.plot(txt.iloc[:,it], 'k')
	#plt.plot(txt.iloc[:,tcolunas-2], 'k.')                  #Correspondentes ao segmento Global
#Plotagem com as cores correspondentes ao arquivo - FIM

#Funcao para plotagem das curvas de deformacao e marcação no ECG -  INÍCIO
def PlotClick(LM_Time, ES_Time, RM_Time, END_Time0):
	#Processo de plotagem -  INÍCIO
	fig = plt.figure(figsize=(12, 8))               #Definição do tamanho da figura
	#Definição do subplot das curvas (gráfico de cima)
	ax0 = plt.subplot2grid((12,1),(0,0), rowspan = 4, colspan = 1)
	plt.xlim(0, END_Time0)
	ax0.axvline(LM_Time, color='y')
	ax0.axvline(ES_Time, color='g')
	ax0.axvline(RM_Time, color='y')
	tick_locs = np.arange(0.0,END_Time0,0.2)
	tick_lbls = np.arange(0, int(END_Time0*1000), 200)
	plt.xticks(tick_locs, tick_lbls)
	colorPlot(txt1,tcolunas1)
	#colorPlot(txt2_mod,tcolunas2)
	#colorPlot(txt3_mod,tcolunas3)
	plt.ylabel('Strain - LV\n(%)', fontsize=SizeFont)
	plt.grid()
	plt.setp(ax0.get_xticklabels(), visible=False)

	#Definição do subplot das curvas de strain LA (gráfico do meio)
	ax1 = plt.subplot2grid((12,1),(4,0), rowspan = 4, colspan = 1)
	plt.xlim(0, END_Time0)
	ax1.axvline(LM_Time, color='y')
	ax1.axvline(ES_Time, color='g')
	ax1.axvline(RM_Time, color='y')
	tick_locs = np.arange(0.0,END_Time0,0.2)
	tick_lbls = np.arange(0, int(END_Time0*1000), 200)
	plt.xticks(tick_locs, tick_lbls)
	if op != test_op:
		colorPlot(strain_rate_lv4ch,tcolunas_strain_rate_lv4ch)
	else:
		colorPlot(txt1.diff(),tcolunas1)
		#colorPlot(txt2_mod.diff(),tcolunas2)
		#colorPlot(txt3_mod.diff(),tcolunas3)
	plt.ylabel('Strain Rate - LV\n(1/s)', fontsize=SizeFont)
	plt.grid()
	plt.setp(ax1.get_xticklabels(), visible=False)

	#Definição do subplot do gráfico do ECG (gráfico de baixo)
	ax2 = plt.subplot2grid((12, 1), (8, 0), rowspan = 4, colspan = 1)
	plt.xlim(0, END_Time0)
	ax2.axvline(LM_Time, color='y')
	ax2.axvline(ES_Time, color='g')
	ax2.axvline(RM_Time, color='y')
	tick_locs = np.arange(0.0,END_Time0,0.2)
	tick_lbls = np.arange(0, int(END_Time0*1000), 200)
	plt.xticks(tick_locs, tick_lbls)
	plt.plot(txt1.loc[:,'ECG : '])
	plt.xlabel('Time (ms)', fontsize=SizeFont)
	plt.ylabel('ECG\nVoltage (mV)', fontsize=SizeFont)
	plt.grid()
	#Fim das definições dos subplots
	#Marcacao dos pontos no gráfico - INÍCIO
	cid = fig.canvas.mpl_connect('button_press_event', onclick)
	#Marcacao dos pontos no gráfico - FIM
	#plt.tight_layout()
	plt.show()
	fig.canvas.mpl_disconnect(cid)
	#Processo de plotagem - FIM
#Funcao para plotagem das curvas de deformacao e marcação no ECG -  FIM

#Plotagem dos gráficos de saída final - INÍCIO
def Parameters_Plot():
	global times_IVA
	times_IVA = []

	fig = plt.figure(figsize=(16, 8))               #Definição do tamanho da figura
	#Definição do subplot das curvas (gráfico do meio)
	if prmt != "8" or calculated_IVA:
		ax0 = plt.subplot2grid((16,1),(1,0), rowspan = 6, colspan = 1)
	else:
		ax0 = plt.subplot2grid((16,1),(0,0), rowspan = 8, colspan = 1)
	plt.xlim(0, END_Time1)
	if prmt != "8":
		colorPlot(txt1,tcolunas1)
		colorPlot(txt2_mod,tcolunas2)
		colorPlot(txt3_mod,tcolunas3)
	else: #Parte relativa ao IVA, colocar de forma que plote uma curva de cada vez
		plt.plot(segment, 'r')
		plt.plot(segment_IVC, 'k')
	#Marcações dos pontos usados para os parâmetros
	if prmt == "1":

		colours=list(txt1_s)
		for colour_it in range(0,tcolunas1-2):
			plt.plot(txt1_s[colours[colour_it]].idxmin(), txt1_s[colours[colour_it]].min(), 'kx')
		"""
		colours=list(txt2_s)
		for colour_it in range(0,tcolunas2-2):
			plt.plot(txt2_s[colours[colour_it]].idxmin(), txt2_s[colours[colour_it]].min(), 'k*')

		colours=list(txt3_s)
		for colour_it in range(0,tcolunas3-2):
			plt.plot(txt3_s[colours[colour_it]].idxmin(), txt3_s[colours[colour_it]].min(), 'k+')
		"""
	if prmt == "2":
		colours=list(txt1_sliced_onsets)
		for colour_it in range(0,tcolunas1-2):
			plt.plot(txt1_sliced_onsets[colours[colour_it]].idxmin(), txt1_sliced_onsets[colours[colour_it]].min(), 'kx')

		colours=list(txt2_sliced_onsets)
		for colour_it in range(0,tcolunas2-2):
			plt.plot(txt2_sliced_onsets[colours[colour_it]].idxmin(), txt2_sliced_onsets[colours[colour_it]].min(), 'kx')

		colours=list(txt3_sliced_onsets)
		for colour_it in range(0,tcolunas3-2):
			plt.plot(txt3_sliced_onsets[colours[colour_it]].idxmin(), txt3_sliced_onsets[colours[colour_it]].min(), 'kx')

	if prmt == "3":
		ax0.axvline(ThirdDiastoleTime, color='k')

	#Diferenciação Entre eventos das valvas e das fases (altura da linha)/ Disposição do texto
	ymin, ymax = plt.ylim()
	txt_height_1 = ymax+0.15*(ymax-ymin)
	txt_height_2 = ymax+0.05*(ymax-ymin)
	x_inc=0.002
	plt.grid()
	tick_locs = np.arange(0.0,END_Time1,0.2)
	tick_lbls = np.arange(0, int(END_Time1*1000), 200)
	plt.xticks(tick_locs, tick_lbls)
	if prmt != "8":
		plt.ylabel('\nStrain - LV\n(%)', fontsize=SizeFont)

	else:
		plt.ylabel('\nSegmental Strain Rate - LV\n(1/s)', fontsize=SizeFont)
		ax0.tick_params(axis="y", labelsize=SizeLabelFont)

		if(calculated_IVA == 0):
			cid = fig.canvas.mpl_connect('button_press_event', onclick)

	plt.setp(ax0.get_xticklabels(), visible=False)
	#

	plt.text(MVOvalues1[0]+x_inc, txt_height_1, "MVO" , rotation=0, verticalalignment='center', fontsize=SizePhaseFont)
	plt.text(MVCvalues1[0]+x_inc, txt_height_1, "MVC" , rotation=0, verticalalignment='center', fontsize=SizePhaseFont)
	plt.text(AVOvalues1[0]+x_inc, txt_height_1, "AVO" , rotation=0, verticalalignment='center', fontsize=SizePhaseFont)
	plt.text(AVCvalues1[0]+x_inc, txt_height_1, "AVC" , rotation=0, verticalalignment='center', fontsize=SizePhaseFont)
	if op != test_op:
		plt.text(EMCvalues1[0]+x_inc, txt_height_2, "EMC" , rotation=0, verticalalignment='center', fontsize=SizePhaseFont)
	plt.text(IVCvalues1[0]+x_inc, txt_height_2, "IVC" , rotation=0, verticalalignment='center', fontsize=SizePhaseFont)
	plt.text(EjectionTimevalues1[0]+x_inc, txt_height_2, "Ejec" , rotation=0, verticalalignment='center', fontsize=SizePhaseFont)
	plt.text(IVRvalues[0]+x_inc, txt_height_2, "IVR" , rotation=0, verticalalignment='center', fontsize=SizePhaseFont)
	plt.text(Evalues[0]+x_inc, txt_height_2, "E" , rotation=0, verticalalignment='center', fontsize=SizePhaseFont)
	if op != test_op:
		#plt.text(Diastasisvalues[0]+x_inc, txt_height_2, "D" , rotation=0, verticalalignment='center')
		plt.text(Avalues[0]+x_inc, txt_height_2, "A" , rotation=0, verticalalignment='center', fontsize=SizePhaseFont)

	#ifs para definir o que aparecerá na figura com base no final dela
	if MVOvalues2[0]<END_Time1:
		plt.text(MVOvalues2[0]+x_inc, txt_height_1, "MVO" , rotation=0, verticalalignment='center', fontsize=SizePhaseFont)
		ax0.axvline(x=MVOvalues2[0], c="k",ymin=-0.1,ymax= height_line+0.1, linewidth=1, linestyle = ':', zorder=0, clip_on=False)
	if MVCvalues2[0]<END_Time1:
		plt.text(MVCvalues2[0]+x_inc, txt_height_1, "MVC" , rotation=0, verticalalignment='center', fontsize=SizePhaseFont)
		ax0.axvline(x=MVCvalues2[0], c="k",ymin=-0.1,ymax= height_line+0.1, linewidth=1, linestyle = ':', zorder=0, clip_on=False)
	if AVOvalues2[0]<END_Time1:
		plt.text(AVOvalues2[0]+x_inc, txt_height_1, "AVO" , rotation=0, verticalalignment='center', fontsize=SizePhaseFont)
		ax0.axvline(x=AVOvalues2[0], c="k",ymin=-0.1,ymax= height_line+0.1, linewidth=1, linestyle = ':', zorder=0, clip_on=False)
	if AVCvalues2[0]<END_Time1:
		plt.text(AVCvalues2[0]+x_inc, txt_height_1, "AVC" , rotation=0, verticalalignment='center', fontsize=SizePhaseFont)
		ax0.axvline(x=AVCvalues2[0], c="k",ymin=-0.1,ymax= height_line+0.1, linewidth=1, linestyle = ':', zorder=0, clip_on=False)
	if op != test_op and EMCvalues2 < END_Time1:
		plt.text(EMCvalues2[0]+x_inc, txt_height_2, "EMC" , rotation=0, verticalalignment='center', fontsize=SizePhaseFont)
		ax0.axvline(x=EMCvalues2[0], c="y",ymin=-0.1,ymax= height_line, linewidth=1.5, zorder=0, clip_on=False)
	if IVCvalues2[0]<END_Time1:
		plt.text(IVCvalues2[0]+x_inc, txt_height_2, "IVC" , rotation=0, verticalalignment='center', fontsize=SizePhaseFont)
		ax0.axvline(x=IVCvalues2[0], c="k",ymin=-0.1,ymax= height_line, linewidth=1, linestyle = ':', zorder=0, clip_on=False)
	if EjectionTimevalues2[0]<END_Time1:
		plt.text(EjectionTimevalues2[0]+x_inc, txt_height_2, "Ejec" , rotation=0, verticalalignment='center', fontsize=SizePhaseFont)
		ax0.axvline(x=EjectionTimevalues2[0], c="k",ymin=-0.1,ymax= height_line, linewidth=1, linestyle = ':', zorder=0, clip_on=False)

	#Definição do subplot das curvas (gráfico do meio)
	if prmt != "8" or calculated_IVA:
		ax1 = plt.subplot2grid((16,1),(7,0), rowspan = 6, colspan = 1)
	else:
		ax1 = plt.subplot2grid((16,1),(8,0), rowspan = 8, colspan = 1)
		plt.xlabel('Time (ms)', fontsize=SizeFont)
		ax1.tick_params(axis="x", labelsize=SizeLabelFont)
		ax1.tick_params(axis="y", labelsize=SizeLabelFont)


	plt.xlim(0, END_Time1)
	if op != test_op and op != '5':
		colorPlot(txt_mid,tcolunas_mid)
	elif op == '5' or op == test_op:
		colorPlot(strain_rate_lv4ch,tcolunas1)
		colorPlot(strain_rate_lv2ch,tcolunas2)
		colorPlot(strain_rate_lv3ch,tcolunas3)
	plt.grid()
	tick_locs = np.arange(0.0,END_Time1,0.2)
	tick_lbls = np.arange(0, int(END_Time1*1000), 200)
	plt.xticks(tick_locs, tick_lbls)

	if op == "1" or op == "5" or op == test_op:
		plt.ylabel('Strain Rate - LV\n(1/s)', fontsize=SizeFont)
	if op == "2":
		plt.ylabel('Strain - LA\n(%)', fontsize=SizeFont)
	if op == "3":
		plt.ylabel('Strain Rate - LA\n(1/s)', fontsize=SizeFont)
	if op == "4":
		plt.ylabel('Strain - RV\n(%)', fontsize=SizeFont)

	if prmt != "8" or calculated_IVA:
		plt.setp(ax1.get_xticklabels(), visible=False)

	#Definição do subplot do gráfico do ECG (gráfico de baixo)
	if prmt != "8" or calculated_IVA:
		ax2 = plt.subplot2grid((16, 1), (13, 0), rowspan = 4, colspan = 1)
	#else:
		#ax2 = plt.subplot2grid((16, 1), (15, 0), rowspan = 2, colspan = 1)
		plt.plot(txt1.loc[:,'ECG : '])
		plt.xlim(0, END_Time1)
		tick_locs = np.arange(0.0,END_Time1,0.2)
		tick_lbls = np.arange(0, int(END_Time1*1000), 200)
		plt.xticks(tick_locs, tick_lbls)
		plt.xlabel('Time (ms)', fontsize=SizeFont)
		plt.ylabel('ECG\nVoltage\n(mV)', fontsize=SizeFont)
		plt.grid()

	#Plotagem das linhas entre os subplots - INÍCIO
	ax0.axvline(x=MVOvalues1[0], c="k",ymin=-0.1,ymax= height_line+0.1, linewidth=1, linestyle = ':', zorder=0, clip_on=False)
	ax0.axvline(x=MVCvalues1[0], c="k",ymin=-0.1,ymax= height_line+0.1, linewidth=1, linestyle = ':', zorder=0, clip_on=False)
	ax0.axvline(x=AVOvalues1[0], c="k",ymin=-0.1,ymax= height_line+0.1, linewidth=1, linestyle = ':', zorder=0, clip_on=False)
	ax0.axvline(x=AVCvalues1[0], c="g",ymin=-0.1,ymax= height_line+0.1, linewidth=1.5, zorder=0, clip_on=False)
	if op != test_op:
		ax0.axvline(x=EMCvalues1[0], c="y",ymin=-0.1,ymax= height_line, linewidth=1.5, zorder=0, clip_on=False)
	ax0.axvline(x=IVCvalues1[0], c="k",ymin=-0.1,ymax= height_line, linewidth=1, linestyle = ':', zorder=0, clip_on=False)
	ax0.axvline(x=EjectionTimevalues1[0], c="k",ymin=-0.1,ymax= height_line, linewidth=1, linestyle = ':', zorder=0, clip_on=False)
	ax0.axvline(x=IVRvalues[0], c="k",ymin=-0.1,ymax= height_line, linewidth=1, linestyle = ':', zorder=0, clip_on=False)
	ax0.axvline(x=Evalues[0], c="k",ymin=-0.1,ymax= height_line, linewidth=1, linestyle = ':', zorder=0, clip_on=False)
	if op != test_op:
		#ax0.axvline(x=Diastasisvalues[0], c="k",ymin=-0.1,ymax= height_line, linewidth=1, linestyle = ':', zorder=0, clip_on=False)
		ax0.axvline(x=Avalues[0], c="k",ymin=-0.1,ymax= height_line, linewidth=1, linestyle = ':', zorder=0, clip_on=False)

	ax1.axvline(x=MVOvalues1[0], c="k",ymin=-0.1,ymax= height_line+0.1, linewidth=1, linestyle = ':', zorder=0, clip_on=False)
	ax1.axvline(x=MVCvalues1[0], c="k",ymin=-0.1,ymax= height_line+0.1, linewidth=1, linestyle = ':', zorder=0, clip_on=False)
	ax1.axvline(x=AVOvalues1[0], c="k",ymin=-0.1,ymax= height_line+0.1, linewidth=1, linestyle = ':', zorder=0, clip_on=False)
	ax1.axvline(x=AVCvalues1[0], c="g",ymin=-0.1,ymax= height_line+0.1, linewidth=1.5, zorder=0, clip_on=False)
	if op != test_op:
		ax1.axvline(x=EMCvalues1[0], c="y",ymin=-0.1,ymax= height_line, linewidth=1.5, zorder=0, clip_on=False)
	ax1.axvline(x=IVCvalues1[0], c="k",ymin=-0.1,ymax= height_line, linewidth=1, linestyle = ':', zorder=0, clip_on=False)
	ax1.axvline(x=EjectionTimevalues1[0], c="k",ymin=-0.1,ymax= height_line, linewidth=1, linestyle = ':', zorder=0, clip_on=False)
	ax1.axvline(x=IVRvalues[0], c="k",ymin=-0.1,ymax= height_line, linewidth=1, linestyle = ':', zorder=0, clip_on=False)
	ax1.axvline(x=Evalues[0], c="k",ymin=-0.1,ymax= height_line, linewidth=1, linestyle = ':', zorder=0, clip_on=False)
	if op != test_op:
		#ax1.axvline(x=Diastasisvalues[0], c="k",ymin=-0.1,ymax= height_line, linewidth=1, linestyle = ':', zorder=0, clip_on=False)
		ax1.axvline(x=Avalues[0], c="k",ymin=-0.1,ymax= height_line, linewidth=1, linestyle = ':', zorder=0, clip_on=False)

	#ifs para definir o que aparecerá na figura com base no final dela
	if MVOvalues2[0]<END_Time1:
		ax1.axvline(x=MVOvalues2[0], c="k",ymin=-0.1,ymax= height_line+0.1, linewidth=1, linestyle = ':', zorder=0, clip_on=False)
	if MVCvalues2[0]<END_Time1:
		ax1.axvline(x=MVCvalues2[0], c="k",ymin=-0.1,ymax= height_line+0.1, linewidth=1, linestyle = ':', zorder=0, clip_on=False)
	if AVOvalues2[0]<END_Time1:
		ax1.axvline(x=AVOvalues2[0], c="k",ymin=-0.1,ymax= height_line+0.1, linewidth=1, linestyle = ':', zorder=0, clip_on=False)
	if AVCvalues2[0]<END_Time1:
		ax1.axvline(x=AVCvalues2[0], c="k",ymin=-0.1,ymax= height_line+0.1, linewidth=1, linestyle = ':', zorder=0, clip_on=False)
	if op != test_op and EMCvalues2 < END_Time1:
		ax1.axvline(x=EMCvalues2[0], c="y",ymin=-0.1,ymax= height_line, linewidth=1.5, zorder=0, clip_on=False)
	if IVCvalues2[0]<END_Time1:
		ax1.axvline(x=IVCvalues2[0], c="k",ymin=-0.1,ymax= height_line, linewidth=1, linestyle = ':', zorder=0, clip_on=False)
	if EjectionTimevalues2[0]<END_Time1:
		ax1.axvline(x=EjectionTimevalues2[0], c="k",ymin=-0.1,ymax= height_line, linewidth=1, linestyle = ':', zorder=0, clip_on=False)

	if prmt != "8" or calculated_IVA:
		ax2.axvline(x=MVOvalues1[0], c="k",ymin=0,ymax=1, linewidth=1, linestyle = ':', zorder=0, clip_on=False)
		ax2.axvline(x=MVCvalues1[0], c="k",ymin=-0,ymax=1, linewidth=1, linestyle = ':', zorder=0, clip_on=False)
		ax2.axvline(x=AVOvalues1[0], c="k",ymin=-0,ymax=1, linewidth=1, linestyle = ':', zorder=0, clip_on=False)
		ax2.axvline(x=AVCvalues1[0], c="g",ymin=0,ymax=1, linewidth=1.5, zorder=0, clip_on=False)
		if op != test_op:
			ax2.axvline(x=EMCvalues1[0], c="y",ymin=0,ymax=1, linewidth=1.5, zorder=0, clip_on=False)
		ax2.axvline(x=IVCvalues1[0], c="k",ymin=-0,ymax=1, linewidth=1, linestyle = ':', zorder=0, clip_on=False)
		ax2.axvline(x=EjectionTimevalues1[0], c="k",ymin=-0,ymax=1, linewidth=1, linestyle = ':', zorder=0, clip_on=False)
		ax2.axvline(x=IVRvalues[0], c="k",ymin=0,ymax=1, linewidth=1, linestyle = ':', zorder=0, clip_on=False)
		ax2.axvline(x=Evalues[0], c="k",ymin=0,ymax=1, linewidth=1, linestyle = ':', zorder=0, clip_on=False)
		if op != test_op:
			#ax2.axvline(x=Diastasisvalues[0], c="k",ymin=0,ymax=1, linewidth=1, linestyle = ':', zorder=0, clip_on=False)
			ax2.axvline(x=Avalues[0], c="k",ymin=-0,ymax=1, linewidth=1, linestyle = ':', zorder=0, clip_on=False)

		#ifs para definir o que aparecerá na figura com base no final dela
		if MVOvalues2[0]<END_Time1:
			ax2.axvline(x=MVOvalues2[0], c="k",ymin=-0.1,ymax= height_line+0.1, linewidth=1, linestyle = ':', zorder=0, clip_on=False)
		if MVCvalues2[0]<END_Time1:
			ax2.axvline(x=MVCvalues2[0], c="k",ymin=-0.1,ymax= height_line+0.1, linewidth=1, linestyle = ':', zorder=0, clip_on=False)
		if AVOvalues2[0]<END_Time1:
			ax2.axvline(x=AVOvalues2[0], c="k",ymin=-0.1,ymax= height_line+0.1, linewidth=1, linestyle = ':', zorder=0, clip_on=False)
		if AVCvalues2[0]<END_Time1:
			ax2.axvline(x=AVCvalues2[0], c="k",ymin=-0.1,ymax= height_line+0.1, linewidth=1, linestyle = ':', zorder=0, clip_on=False)
		if op != test_op and EMCvalues2 < END_Time1:
			ax2.axvline(x=EMCvalues2[0], c="y",ymin=-0.1,ymax= height_line, linewidth=1.5, zorder=0, clip_on=False)
		if IVCvalues2[0]<END_Time1:
			ax2.axvline(x=IVCvalues2[0], c="k",ymin=-0.1,ymax= height_line, linewidth=1, linestyle = ':', zorder=0, clip_on=False)
		if EjectionTimevalues2[0]<END_Time1:
			ax2.axvline(x=EjectionTimevalues2[0], c="k",ymin=-0.1,ymax= height_line, linewidth=1, linestyle = ':', zorder=0, clip_on=False)

	#Plotagem das linhas entre os subplots - FIM

	#plt.tight_layout()
	plt.show()
	if prmt == "8" and calculated_IVA == 0:
		fig.canvas.mpl_disconnect(cid)

#Plotagem dos gráficos de saída final - FIM

#INÍCIO DO BULLSEYE DE 17 SEGMENTOS
"""
This example demonstrates how to create the 17 segment model for the left
ventricle recommended by the American Heart Association (AHA).
"""
def bullseye_seventeenSEG_plot(ax, data, segBold=None, cmap=None, norm=None):
	"""
	Bullseye representation for the left ventricle.

	Parameters
	----------
	ax : axes
	data : list of int and float
		The intensity values for each of the 17 segments
	segBold: list of int, optional
		A list with the segments to highlight
	cmap : ColorMap or None, optional
		Optional argument to set the desired colormap
	norm : Normalize or None, optional
		Optional argument to normalize data into the [0.0, 1.0] range


	Notes
	-----
	This function create the 17 segment model for the left ventricle according
	to the American Heart Association (AHA) [1]_

	References
	----------
	.. [1] M. D. Cerqueira, N. J. Weissman, V. Dilsizian, A. K. Jacobs,
		S. Kaul, W. K. Laskey, D. J. Pennell, J. A. Rumberger, T. Ryan,
		and M. S. Verani, "Standardized myocardial segmentation and
		nomenclature for tomographic imaging of the heart",
		Circulation, vol. 105, no. 4, pp. 539-542, 2002.
	"""
	if segBold is None:
		segBold = []

	linewidth = 2
	data = np.array(data).ravel()
	print(data)

	if cmap is None:
		cmap = plt.cm.viridis

	if norm is None:
		norm = mpl.colors.Normalize(vmin=data.min(), vmax=data.max())

	theta = np.linspace(0, 2*np.pi, 768)
	r = np.linspace(0.2, 1, 4)

	# Create the bound for the segment 17
	for i in range(r.shape[0]):
		ax.plot(theta, np.repeat(r[i], theta.shape), '-k', lw=linewidth)

	# Create the bounds for the segments  1-12
	for i in range(6):
		theta_i = i*60*np.pi/180
		ax.plot([theta_i, theta_i], [r[1], 1], '-k', lw=linewidth)

	# Create the bounds for the segments 13-16
	for i in range(4):
		theta_i = i*90*np.pi/180 - 45*np.pi/180
		ax.plot([theta_i, theta_i], [r[0], r[1]], '-k', lw=linewidth)

	# Fill the segments 1-6
	r0 = r[2:4]
	r0 = np.repeat(r0[:, np.newaxis], 128, axis=1).T
	for i in range(6):
		# First segment start at 60 degrees
		theta0 = theta[i*128:i*128+128] + 60*np.pi/180
		theta0 = np.repeat(theta0[:, np.newaxis], 2, axis=1)
		z = np.ones((128, 2))*data[i]
		ax.pcolormesh(theta0, r0, z, cmap=cmap, norm=norm)
		if i+1 in segBold:
			ax.plot(theta0, r0, '-k', lw=linewidth+2)
			ax.plot(theta0[0], [r[2], r[3]], '-k', lw=linewidth+1)
			ax.plot(theta0[-1], [r[2], r[3]], '-k', lw=linewidth+1)

	# Fill the segments 7-12
	r0 = r[1:3]
	r0 = np.repeat(r0[:, np.newaxis], 128, axis=1).T
	for i in range(6):
		# First segment start at 60 degrees
		theta0 = theta[i*128:i*128+128] + 60*np.pi/180
		theta0 = np.repeat(theta0[:, np.newaxis], 2, axis=1)
		z = np.ones((128, 2))*data[i+6]
		ax.pcolormesh(theta0, r0, z, cmap=cmap, norm=norm)
		if i+7 in segBold:
			ax.plot(theta0, r0, '-k', lw=linewidth+2)
			ax.plot(theta0[0], [r[1], r[2]], '-k', lw=linewidth+1)
			ax.plot(theta0[-1], [r[1], r[2]], '-k', lw=linewidth+1)

	# Fill the segments 13-16
	r0 = r[0:2]
	r0 = np.repeat(r0[:, np.newaxis], 192, axis=1).T
	for i in range(4):
		# First segment start at 45 degrees
		theta0 = theta[i*192:i*192+192] + 45*np.pi/180
		theta0 = np.repeat(theta0[:, np.newaxis], 2, axis=1)
		z = np.ones((192, 2))*data[i+12]
		ax.pcolormesh(theta0, r0, z, cmap=cmap, norm=norm)
		if i+13 in segBold:
			ax.plot(theta0, r0, '-k', lw=linewidth+2)
			ax.plot(theta0[0], [r[0], r[1]], '-k', lw=linewidth+1)
			ax.plot(theta0[-1], [r[0], r[1]], '-k', lw=linewidth+1)

	# Fill the segments 17
	if data.size == 17:
		r0 = np.array([0, r[0]])
		r0 = np.repeat(r0[:, np.newaxis], theta.size, axis=1).T
		theta0 = np.repeat(theta[:, np.newaxis], 2, axis=1)
		z = np.ones((theta.size, 2))*data[16]
		ax.pcolormesh(theta0, r0, z, cmap=cmap, norm=norm)
		if 17 in segBold:
			ax.plot(theta0, r0, '-k', lw=linewidth+2)

	ax.set_ylim([0, 1])
	ax.set_yticklabels([])
	ax.set_xticklabels([])
##FIM DO BULLSEYE DE 17 SEGMENTOS

#INÍCIO DO BULLSEYE DE 18 SEGMENTOS
def bullseye_eighteenSEG_plot(ax, data, segBold=None, cmap=None, norm=None):
	"""
	Bullseye representation for the left ventricle.

	Parameters
	----------
	ax : axes
	data : list of int and float
		The intensity values for each of the 17 segments
	segBold: list of int, optional
		A list with the segments to highlight
	cmap : ColorMap or None, optional
		Optional argument to set the desired colormap
	norm : Normalize or None, optional
		Optional argument to normalize data into the [0.0, 1.0] range


	Notes
	-----
	This function create the 17 segment model for the left ventricle according
	to the American Heart Association (AHA) [1]

	ALTERAR ACIMA, CITAR A FUNÇÃO NA QUAL ME BASEEI.
	"""
	if segBold is None:
		segBold = []

	linewidth = 2
	data = np.array(data).ravel()

	if cmap is None:
		cmap = plt.cm.viridis

	if norm is None:
		norm = mpl.colors.Normalize(vmin=data.min(), vmax=data.max())

	theta = np.linspace(0, 2*np.pi, 768)
	r = np.linspace(0, 1, 4)

	# Create the bounds for the segments  1-18
	for i in range(6):
		theta_i = i*60*np.pi/180
		ax.plot([theta_i, theta_i], [r[0], 1], '-k', lw=linewidth)

	# Fill the segments 1-6
	r0 = r[2:4]
	r0 = np.repeat(r0[:, np.newaxis], 128, axis=1).T
	for i in range(6):
		# First segment start at 60 degrees
		theta0 = theta[i*128:i*128+128] + 60*np.pi/180
		theta0 = np.repeat(theta0[:, np.newaxis], 2, axis=1)
		z = np.ones((128, 2))*data[i]
		ax.pcolormesh(theta0, r0, z, cmap=cmap, norm=norm)
		if i+1 in segBold:
			ax.plot(theta0, r0, '-k', lw=linewidth+2)
			ax.plot(theta0[0], [r[2], r[3]], '-k', lw=linewidth+1)
			ax.plot(theta0[-1], [r[2], r[3]], '-k', lw=linewidth+1)
		else:
			ax.plot(theta0, r0, '-k', lw=linewidth)

	# Fill the segments 7-12
	r0 = r[1:3]
	r0 = np.repeat(r0[:, np.newaxis], 128, axis=1).T
	for i in range(6):
		# First segment start at 60 degrees
		theta0 = theta[i*128:i*128+128] + 60*np.pi/180
		theta0 = np.repeat(theta0[:, np.newaxis], 2, axis=1)
		z = np.ones((128, 2))*data[i+6]
		ax.pcolormesh(theta0, r0, z, cmap=cmap, norm=norm)
		if i+7 in segBold:
			ax.plot(theta0, r0, '-k', lw=linewidth+2)
			ax.plot(theta0[0], [r[1], r[2]], '-k', lw=linewidth+1)
			ax.plot(theta0[-1], [r[1], r[2]], '-k', lw=linewidth+1)
		else:
			ax.plot(theta0, r0, '-k', lw=linewidth)

	# Fill the segments 13-18
	r0 = r[0:2]
	r0 = np.repeat(r0[:, np.newaxis], 128, axis=1).T
	for i in range(6):
		# First segment start at 60 degrees
		theta0 = theta[i*128:i*128+128] + 60*np.pi/180
		theta0 = np.repeat(theta0[:, np.newaxis], 2, axis=1)
		z = np.ones((128, 2))*data[i+12]
		ax.pcolormesh(theta0, r0, z, cmap=cmap, norm=norm)
		if i+13 in segBold:
			ax.plot(theta0, r0, '-k', lw=linewidth+2)
			ax.plot(theta0[0], [r[0], r[1]], '-k', lw=linewidth+1)
			ax.plot(theta0[-1], [r[0], r[1]], '-k', lw=linewidth+1)
		else:
			ax.plot(theta0, r0, '-k', lw=linewidth)

	ax.set_ylim([0, 1])
	ax.set_yticklabels([])
	ax.set_xticklabels([])
#FIM DO BULLSEYE DE 18 SEGMENTOS

#Inserção dos dados no bullseye
def DR_bullseye(data):
	# Make a figure and axes with dimensions as desired.
	fig, ax = plt.subplots(figsize=(8, 6), nrows=1, ncols=1,
						   subplot_kw=dict(projection='polar'))
	fig.canvas.set_window_title('Diastolic Recovery Bulls Eye')

	# Create the axis for the colorbars
	axl = fig.add_axes([0.75, 0.1, 0.2, 0.05])	#Orientação

	# Set the colormap and norm to correspond to the data for which
	# the colorbar will be used.
	cmap = mpl.cm.viridis

	norm = mpl.colors.Normalize(vmin=np.amin(BullseyeAux)-10, vmax=np.amax(BullseyeAux)+10) #Valores para normalização

	# ColorbarBase derives from ScalarMappable and puts a colorbar
	# in a specified axes, so it has everything needed for a
	# standalone colorbar.  There are many more kwargs, but the
	# following gives a basic continuous colorbar with ticks
	# and labels.
	cb1 = mpl.colorbar.ColorbarBase(axl, cmap=cmap, norm=norm,
									orientation='horizontal')
	cb1.set_label('Diastolic Recovery (%)')

	# Create the 17 segment model
	bullseye_eighteenSEG_plot(ax, data, cmap=None, norm=None)
	ax.set_title('Diastolic Recovery Bulls Eye')

	plt.show()
	#Fim da função do Bullseye

def GLS_calc():             #Função para calculo do GLS

	#Sincronizar os tempos da plotagem dos pontos do GLS
	#Diferença nos valores médios de uma visualização
	#Talvez o ES_Time não corresponda ao AVC para aquele arquivo
	global txt1_s
	global txt2_s
	global txt3_s

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
		Parameters_Plot()
	sheet['V'+str(it)] = round(gls, 2)


def MD_calc():             #Função para calculo do MD

	global txt1_sliced_onsets
	global txt2_sliced_onsets
	global txt3_sliced_onsets

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
		Parameters_Plot()

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

	for segment_number in range(IVA_aux.shape[1]): #Cada segmento sera plotado para marcacao
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
"""
print("Options:\n\t1. Strain LV, Strain Rate LV and ECG\n\t2. Strain LV, Strain LA and ECG")
print("\t3. Strain LV, Strain Rate LA and ECG\n\t4. Strain LV, Strain RV and ECG")
print("\t5. Strain LV, Strain Rate LV and ECG (without SR files)\n\t"+test_op+". Test Option")
op = input("Option: ")
"""

idPatient = 'Aristoteles'
op = '5'

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
	PlotClick(LM_Time[0], ES_Time[0], RM_Time[0], END_Time0)
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
	#prmt = input("Parameter: ")
	prmt="8"

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
		Parameters_Plot()
	elif prmt == "8":
		IVA_calc()
		break
	elif prmt == "0":
		break

	else:
		print("\n\nInvalid option\n\n\n")
		continue
	print("\n")

wb.save("Event_Timing.xlsx")
