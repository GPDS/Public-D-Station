# -*- coding: utf-8 -*-
#Cálculo dos parâmetros com a quantidade de segmentos e marcação dos pontos em todas as curvas
#Saber quais segmentos existem - talvez usando txt.iloc
#Switchs para parâmetros depois das 18 curvas

#http://onlinelibrary.wiley.com/doi/10.1111/echo.13547/full
#Ver se os pontos estão corretos

import pandas as pd                     #Package usado no trabalho com os arquivos .txt
import numpy as np
import matplotlib.pyplot as plt
import re                               #Package padrão - Para extrair números da string
import openpyxl                         #Package para trabalhar com os arquivos .xlsx
import scipy

#Constantes a serem definidas
it = 4   #Iterador para a marcação na planilha (Depende da linha inicial nela, nesse caso os valores estão a partir da linha 4)

height_line = 1.025 #Tamanho que a linha das fases ultrapassa o gráfico

#Declaração de variaveis
xcoord = []
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
IVRTvalues = []
Evalues = []
Diastasisvalues = []
Avalues = []

#Função para ler apenas as P colunas do dataframe - INÍCIO
def front(self, n):
    return self.iloc[:, :n]

pd.DataFrame.front = front
#Função para ler apenas as P colunas do dataframe - FIM

#Função para marcação dos pontos no ECG - INÍCIO
def onclick(event):
    #print ("\nValue: Time = %f milliseconds"%(event.xdata*1000))
    xcoord.append(event.xdata*1000)
#Função para marcação dos pontos no ECG - FIM

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
    plt.plot(txt.iloc[:,tcolunas-2], 'k.')                  #Correspondentes ao segmento Global
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
    plt.ylabel('Strain - LV\n(%)')
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
    colorPlot(strain_rate_lv,tcolunas_strain_rate_lv)
    plt.ylabel('Strain Rate - LV\n(1/s)')
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
    plt.xlabel('Time (ms)')
    plt.ylabel('ECG\nVoltage (mV)')
    plt.grid()
    #Fim das definições dos subplots
    #Marcacao dos pontos no gráfico - INÍCIO
    cid = fig.canvas.mpl_connect('button_press_event', onclick)
    #Marcacao dos pontos no gráfico - FIM
    plt.tight_layout()
    plt.show()
    fig.canvas.mpl_disconnect(cid)
    #Processo de plotagem - FIM
#Funcao para plotagem das curvas de deformacao e marcação no ECG -  FIM

#Plotagem dos gráficos de saída final - INÍCIO
def Parameters_Plot():
    fig = plt.figure(figsize=(16, 8))               #Definição do tamanho da figura
    #Definição do subplot das curvas (gráfico do meio)
    ax0 = plt.subplot2grid((16,1),(1,0), rowspan = 6, colspan = 1)
    plt.xlim(0, END_Time1)
    colorPlot(txt1,tcolunas1)
    colorPlot(txt2,tcolunas2)
    colorPlot(txt3,tcolunas3)

    #Marcações dos pontos usados para os parâmetros
    if prmt == "1":
        colours=list(txt1_s)
        for colour_it in range(0,tcolunas1-2):
            plt.plot(txt1_s[colours[colour_it]].idxmin(), txt1_s[colours[colour_it]].min(), 'kx')

        colours=list(txt2_s)
        for colour_it in range(0,tcolunas2-2):
            plt.plot(txt2_s[colours[colour_it]].idxmin(), txt2_s[colours[colour_it]].min(), 'k*')

        colours=list(txt3_s)
        for colour_it in range(0,tcolunas3-2):
            plt.plot(txt3_s[colours[colour_it]].idxmin(), txt3_s[colours[colour_it]].min(), 'k+')

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
    plt.ylabel('\nStrain - LV\n(%)')
    plt.setp(ax0.get_xticklabels(), visible=False)
    #

    plt.text(MVOvalues1[it-4]+x_inc, txt_height_1, "MVO" , rotation=0, verticalalignment='center')
    plt.text(MVOvalues2[it-4]+x_inc, txt_height_1, "MVO" , rotation=0, verticalalignment='center')
    plt.text(MVCvalues1[it-4]+x_inc, txt_height_1, "MVC" , rotation=0, verticalalignment='center')
    plt.text(MVCvalues2[it-4]+x_inc, txt_height_1, "MVC" , rotation=0, verticalalignment='center')
    plt.text(AVOvalues1[it-4]+x_inc, txt_height_1, "AVO" , rotation=0, verticalalignment='center')
    plt.text(AVOvalues2[it-4]+x_inc, txt_height_1, "AVO" , rotation=0, verticalalignment='center')
    plt.text(AVCvalues1[it-4]+x_inc, txt_height_1, "AVC" , rotation=0, verticalalignment='center')
    plt.text(AVCvalues2[it-4]+x_inc, txt_height_1, "AVC" , rotation=0, verticalalignment='center')
    plt.text(EMCvalues1[it-4]+x_inc, txt_height_2, "EMC" , rotation=0, verticalalignment='center')
    plt.text(EMCvalues2[it-4]+x_inc, txt_height_2, "EMC" , rotation=0, verticalalignment='center')
    plt.text(IVCvalues1[it-4]+x_inc, txt_height_2, "IVC" , rotation=0, verticalalignment='center')
    plt.text(IVCvalues2[it-4]+x_inc, txt_height_2, "IVC" , rotation=0, verticalalignment='center')
    plt.text(EjectionTimevalues1[it-4]+x_inc, txt_height_2, "Ejec" , rotation=0, verticalalignment='center')
    plt.text(EjectionTimevalues2[it-4]+x_inc, txt_height_2, "Ejec" , rotation=0, verticalalignment='center')
    plt.text(IVRTvalues[it-4]+x_inc, txt_height_2, "IVRT" , rotation=0, verticalalignment='center')
    plt.text(Evalues[it-4]+x_inc, txt_height_2, "E" , rotation=0, verticalalignment='center')
    plt.text(Diastasisvalues[it-4]+x_inc, txt_height_2, "D" , rotation=0, verticalalignment='center')
    plt.text(Avalues[it-4]+x_inc, txt_height_2, "A" , rotation=0, verticalalignment='center')

    #Definição do subplot das curvas (gráfico do meio)
    ax1 = plt.subplot2grid((16,1),(7,0), rowspan = 6, colspan = 1)
    plt.xlim(0, END_Time1)
    colorPlot(txt_mid,tcolunas_mid)
    plt.grid()
    tick_locs = np.arange(0.0,END_Time1,0.2)
    tick_lbls = np.arange(0, int(END_Time1*1000), 200)
    plt.xticks(tick_locs, tick_lbls)

    if op == "1" or op == "5":
        plt.ylabel('Strain Rate - LV\n(1/s)')
    if op == "2":
        plt.ylabel('Strain - LA\n(%)')
    if op == "3":
        plt.ylabel('Strain Rate - LA\n(1/s)')
    if op == "4":
        plt.ylabel('Strain - RV\n(%)')
    plt.setp(ax1.get_xticklabels(), visible=False)

    #Definição do subplot do gráfico do ECG (gráfico de baixo)
    ax2 = plt.subplot2grid((16, 1), (13, 0), rowspan = 4, colspan = 1)
    plt.plot(txt1.loc[:,'ECG : '])
    plt.xlim(0, END_Time1)
    tick_locs = np.arange(0.0,END_Time1,0.2)
    tick_lbls = np.arange(0, int(END_Time1*1000), 200)
    plt.xticks(tick_locs, tick_lbls)
    plt.xlabel('Time (ms)')
    plt.ylabel('ECG\nVoltage (mV)')
    plt.grid()

    #Plotagem das linhas entre os subplots - INÍCIO
    ax0.axvline(x=MVOvalues1[it-4], c="k",ymin=-0.1,ymax= height_line+0.1, linewidth=1, linestyle = ':', zorder=0, clip_on=False)
    ax0.axvline(x=MVOvalues2[it-4], c="k",ymin=-0.1,ymax= height_line+0.1, linewidth=1, linestyle = ':', zorder=0, clip_on=False)
    ax0.axvline(x=MVCvalues1[it-4], c="k",ymin=-0.1,ymax= height_line+0.1, linewidth=1, linestyle = ':', zorder=0, clip_on=False)
    ax0.axvline(x=MVCvalues2[it-4], c="k",ymin=-0.1,ymax= height_line+0.1, linewidth=1, linestyle = ':', zorder=0, clip_on=False)
    ax0.axvline(x=AVOvalues1[it-4], c="k",ymin=-0.1,ymax= height_line+0.1, linewidth=1, linestyle = ':', zorder=0, clip_on=False)
    ax0.axvline(x=AVOvalues2[it-4], c="k",ymin=-0.1,ymax= height_line+0.1, linewidth=1, linestyle = ':', zorder=0, clip_on=False)
    ax0.axvline(x=AVCvalues1[it-4], c="g",ymin=-0.1,ymax= height_line+0.1, linewidth=1.5, zorder=0, clip_on=False)
    ax0.axvline(x=AVCvalues2[it-4], c="k",ymin=-0.1,ymax= height_line+0.1, linewidth=1, linestyle = ':', zorder=0, clip_on=False)
    ax0.axvline(x=EMCvalues1[it-4], c="y",ymin=-0.1,ymax= height_line, linewidth=1.5, zorder=0, clip_on=False)
    ax0.axvline(x=EMCvalues2[it-4], c="y",ymin=-0.1,ymax= height_line, linewidth=1.5, zorder=0, clip_on=False)
    ax0.axvline(x=IVCvalues1[it-4], c="k",ymin=-0.1,ymax= height_line, linewidth=1, linestyle = ':', zorder=0, clip_on=False)
    ax0.axvline(x=IVCvalues2[it-4], c="k",ymin=-0.1,ymax= height_line, linewidth=1, linestyle = ':', zorder=0, clip_on=False)
    ax0.axvline(x=EjectionTimevalues1[it-4], c="k",ymin=-0.1,ymax= height_line, linewidth=1, linestyle = ':', zorder=0, clip_on=False)
    ax0.axvline(x=EjectionTimevalues2[it-4], c="k",ymin=-0.1,ymax= height_line, linewidth=1, linestyle = ':', zorder=0, clip_on=False)
    ax0.axvline(x=IVRTvalues[it-4], c="k",ymin=-0.1,ymax= height_line, linewidth=1, linestyle = ':', zorder=0, clip_on=False)
    ax0.axvline(x=Evalues[it-4], c="k",ymin=-0.1,ymax= height_line, linewidth=1, linestyle = ':', zorder=0, clip_on=False)
    ax0.axvline(x=Diastasisvalues[it-4], c="k",ymin=-0.1,ymax= height_line, linewidth=1, linestyle = ':', zorder=0, clip_on=False)
    ax0.axvline(x=Avalues[it-4], c="k",ymin=-0.1,ymax= height_line, linewidth=1, linestyle = ':', zorder=0, clip_on=False)

    ax1.axvline(x=MVOvalues1[it-4], c="k",ymin=-0.1,ymax= height_line+0.1, linewidth=1, linestyle = ':', zorder=0, clip_on=False)
    ax1.axvline(x=MVOvalues2[it-4], c="k",ymin=-0.1,ymax= height_line+0.1, linewidth=1, linestyle = ':', zorder=0, clip_on=False)
    ax1.axvline(x=MVCvalues1[it-4], c="k",ymin=-0.1,ymax= height_line+0.1, linewidth=1, linestyle = ':', zorder=0, clip_on=False)
    ax1.axvline(x=MVCvalues2[it-4], c="k",ymin=-0.1,ymax= height_line+0.1, linewidth=1, linestyle = ':', zorder=0, clip_on=False)
    ax1.axvline(x=AVOvalues1[it-4], c="k",ymin=-0.1,ymax= height_line+0.1, linewidth=1, linestyle = ':', zorder=0, clip_on=False)
    ax1.axvline(x=AVOvalues2[it-4], c="k",ymin=-0.1,ymax= height_line+0.1, linewidth=1, linestyle = ':', zorder=0, clip_on=False)
    ax1.axvline(x=AVCvalues1[it-4], c="g",ymin=-0.1,ymax= height_line+0.1, linewidth=1.5, zorder=0, clip_on=False)
    ax1.axvline(x=AVCvalues2[it-4], c="k",ymin=-0.1,ymax= height_line+0.1, linewidth=1, linestyle = ':', zorder=0, clip_on=False)
    ax1.axvline(x=EMCvalues1[it-4], c="y",ymin=-0.1,ymax= height_line, linewidth=1.5, zorder=0, clip_on=False)
    ax1.axvline(x=EMCvalues2[it-4], c="y",ymin=-0.1,ymax= height_line, linewidth=1.5, zorder=0, clip_on=False)
    ax1.axvline(x=IVCvalues1[it-4], c="k",ymin=-0.1,ymax= height_line, linewidth=1, linestyle = ':', zorder=0, clip_on=False)
    ax1.axvline(x=IVCvalues2[it-4], c="k",ymin=-0.1,ymax= height_line, linewidth=1, linestyle = ':', zorder=0, clip_on=False)
    ax1.axvline(x=EjectionTimevalues1[it-4], c="k",ymin=-0.1,ymax= height_line, linewidth=1, linestyle = ':', zorder=0, clip_on=False)
    ax1.axvline(x=EjectionTimevalues2[it-4], c="k",ymin=-0.1,ymax= height_line, linewidth=1, linestyle = ':', zorder=0, clip_on=False)
    ax1.axvline(x=IVRTvalues[it-4], c="k",ymin=-0.1,ymax= height_line, linewidth=1, linestyle = ':', zorder=0, clip_on=False)
    ax1.axvline(x=Evalues[it-4], c="k",ymin=-0.1,ymax= height_line, linewidth=1, linestyle = ':', zorder=0, clip_on=False)
    ax1.axvline(x=Diastasisvalues[it-4], c="k",ymin=-0.1,ymax= height_line, linewidth=1, linestyle = ':', zorder=0, clip_on=False)
    ax1.axvline(x=Avalues[it-4], c="k",ymin=-0.1,ymax= height_line, linewidth=1, linestyle = ':', zorder=0, clip_on=False)

    ax2.axvline(x=MVOvalues1[it-4], c="k",ymin=0,ymax=1, linewidth=1, linestyle = ':', zorder=0, clip_on=False)
    ax2.axvline(x=MVOvalues2[it-4], c="k",ymin=0,ymax=1, linewidth=1, linestyle = ':', zorder=0, clip_on=False)
    ax2.axvline(x=MVCvalues1[it-4], c="k",ymin=-0,ymax=1, linewidth=1, linestyle = ':', zorder=0, clip_on=False)
    ax2.axvline(x=MVCvalues2[it-4], c="k",ymin=-0,ymax=1, linewidth=1, linestyle = ':', zorder=0, clip_on=False)
    ax2.axvline(x=AVOvalues1[it-4], c="k",ymin=-0,ymax=1, linewidth=1, linestyle = ':', zorder=0, clip_on=False)
    ax2.axvline(x=AVOvalues2[it-4], c="k",ymin=-0,ymax=1, linewidth=1, linestyle = ':', zorder=0, clip_on=False)
    ax2.axvline(x=AVCvalues1[it-4], c="g",ymin=0,ymax=1, linewidth=1.5, zorder=0, clip_on=False)
    ax2.axvline(x=AVCvalues2[it-4], c="k",ymin=0,ymax=1, linewidth=1, linestyle = ':', zorder=0, clip_on=False)
    ax2.axvline(x=EMCvalues1[it-4], c="y",ymin=0,ymax=1, linewidth=1.5, zorder=0, clip_on=False)
    ax2.axvline(x=EMCvalues2[it-4], c="y",ymin=0,ymax=1, linewidth=1.5, zorder=0, clip_on=False)
    ax2.axvline(x=IVCvalues1[it-4], c="k",ymin=-0,ymax=1, linewidth=1, linestyle = ':', zorder=0, clip_on=False)
    ax2.axvline(x=IVCvalues2[it-4], c="k",ymin=-0,ymax=1, linewidth=1, linestyle = ':', zorder=0, clip_on=False)
    ax2.axvline(x=EjectionTimevalues1[it-4], c="k",ymin=-0,ymax=1, linewidth=1, linestyle = ':', zorder=0, clip_on=False)
    ax2.axvline(x=EjectionTimevalues2[it-4], c="k",ymin=-0,ymax=1, linewidth=1, linestyle = ':', zorder=0, clip_on=False)
    ax2.axvline(x=IVRTvalues[it-4], c="k",ymin=0,ymax=1, linewidth=1, linestyle = ':', zorder=0, clip_on=False)
    ax2.axvline(x=Evalues[it-4], c="k",ymin=0,ymax=1, linewidth=1, linestyle = ':', zorder=0, clip_on=False)
    ax2.axvline(x=Diastasisvalues[it-4], c="k",ymin=0,ymax=1, linewidth=1, linestyle = ':', zorder=0, clip_on=False)
    ax2.axvline(x=Avalues[it-4], c="k",ymin=-0,ymax=1, linewidth=1, linestyle = ':', zorder=0, clip_on=False)
    #Plotagem das linhas entre os subplots - FIM

    plt.tight_layout()
    plt.show()
#Plotagem dos gráficos de saída final - FIM


#print("\033c") #Caso queira limpar o terminal
#Início da abertura da planilha
wb = openpyxl.load_workbook('Event_Timing.xlsx')
sheet = wb.get_sheet_by_name('Sheet1')
#Fim da abertura da planilha

#Início da abertura dos .txt
print("\nPatient:", sheet['A'+str(it)].value)
print("Options:\n\t1. Strain LV, Strain Rate LV and ECG\n\t2. Strain LV, Strain LA and ECG")
print("\t3. Strain LV, Strain Rate LA and ECG\n\t4. Strain LV, Strain RV and ECG")
print("\t5. TESTE")
op = input("Option: ")
if op == "1":
    arq = open('main_option', 'r')

elif op == "2":
    arq = open('alt_option1', 'r')

elif op == "3":
    arq = open('alt_option2', 'r')

elif op == "4":
    arq = open('alt_option3', 'r')

elif op == "5":
    arq = open('test_option', 'r')

else:
    arq = open('main_option', 'r')

arq_sr_lv = open('exam_sr_LV', 'r')
exame1 = arq.readline()
exame1 = exame1[:len(exame1)-1]    #Retira o \n
exame_mid = arq.readline()
exame_mid = exame_mid[:len(exame_mid)-1]    #Retira o \n
exame2 = arq.readline()
exame2 = exame2[:len(exame2)-1]    #Retira o \n
exame3 = arq.readline()
exame3 = exame3[:len(exame3)-1]    #Retira o \n
exame_sr_LV = arq_sr_lv.readline()
exame_sr_LV = exame_sr_LV[:len(exame_sr_LV)-1]    #Retira o \n
print("\n\nUsing files: ")
print("\t",exame1)
print("\t",exame2)
print("\t",exame3)
print("\t",exame_mid)
if (exame1 == exame2 or exame1 == exame3 or exame2 == exame3):
    input("\n\n\n\n\n\n\n\n\n\n\n\nWARNING: Some files are duplicated. To find out which ones are equal check their names above.\n\nPress enter to continue.")
if exame_mid != exame_sr_LV:
    print("\t",exame_sr_LV)
txt1=pd.read_csv(exame1, sep='\t', engine='python', skiprows=3, index_col=0) #Parte do índice arrumada
txt2=pd.read_csv(exame2, sep='\t', engine='python', skiprows=3, index_col=0) #Parte do índice arrumada
txt3=pd.read_csv(exame3, sep='\t', engine='python', skiprows=3, index_col=0) #Parte do índice arrumada
txt_mid=pd.read_csv(exame_mid, sep='\t', engine='python', skiprows=3, index_col=0)
strain_rate_lv=pd.read_csv(exame_sr_LV, sep='\t', engine='python', skiprows=3, index_col=0)
#Fim da abertura dos .txt

txt_original = open(exame1, 'r')
numbers = re.findall("\d+\.\d+", txt_original.readlines()[2]) #Numeros extraidos da linha 3 do txt - LM_Time, ES_Time e RM_Time
txt_original.close()

txt1.drop('Unnamed: 1', axis=1, inplace=True) #Retira a coluna inútil que é lida (devido à tabulação exagerada do arquivo exportado)
txt2.drop('Unnamed: 1', axis=1, inplace=True)
txt3.drop('Unnamed: 1', axis=1, inplace=True)
txt_mid.drop('Unnamed: 1', axis=1, inplace=True)
strain_rate_lv.drop('Unnamed: 1', axis=1, inplace=True)

tcolunas1=int(((txt1.size/len(txt1.index))))
tcolunas2=int(((txt2.size/len(txt2.index))))
tcolunas3=int(((txt2.size/len(txt2.index))))
tcolunas_mid=int(((txt_mid.size/len(txt_mid.index))))
tcolunas_strain_rate_lv = int(((strain_rate_lv.size/len(strain_rate_lv.index))))

LM_Time = float(numbers[0])
RM_Time = float(numbers[1])
ES_Time = float(numbers[2])                    #AVC - Aortic Valve Closure

#Determinação do tempo máximo para o gráfico de marcação - Início
if txt1.index[len(txt1.index)-1] < strain_rate_lv.index[len(strain_rate_lv.index)-1]:#Determinar o arquivo de texto com menor tempo
    END_Time0 = txt1.index[len(txt1.index)-1]                              #para que um gráfico não fique sobrando
else:
    END_Time0 = strain_rate_lv.index[len(strain_rate_lv.index)-1]
#Para o gráfico de marcação - FIM

#Para o gráfico dos parâmetros - Início
#achar o menor entre os strains e comparar com o do meio
if txt1.index[len(txt1.index)-1] < txt2.index[len(txt2.index)-1]:#Determinar o arquivo de texto com menor tempo
    if txt1.index[len(txt1.index)-1] < txt3.index[len(txt3.index)-1]:
        strain_end_time = txt1.index[len(txt1.index)-1]
    else:
        strain_end_time = txt3.index[len(txt3.index)-1]
else:
    if txt2.index[len(txt2.index)-1] < txt3.index[len(txt3.index)-1]:
        strain_end_time = txt2.index[len(txt2.index)-1]
    else:
        strain_end_time = txt3.index[len(txt3.index)-1]

if strain_end_time < txt_mid.index[len(txt_mid.index)-1]:#Determinar o arquivo de texto com menor tempo
    END_Time1 = strain_end_time                          #para que um gráfico não fique sobrando
else:
    END_Time1 = txt_mid.index[len(txt_mid.index)-1]
#Para o gráfico dos parâmetros - Fim


#Gravação dos valores marcados na planilha do excel - INÍCIO
print("\n\nMarcacao do Onset QRS 1, ponto de diástase, onset P, pico P, onset QRS 2")
PlotClick(LM_Time, ES_Time, RM_Time, END_Time0)
sheet['G'+str(it)] = round(xcoord[0],0) #Houve um arredondamento do tempo em ms
sheet['Q'+str(it)] = round(xcoord[1],0) #Houve um arredondamento do tempo em ms
sheet['I'+str(it)] = round(xcoord[2],0) #Houve um arredondamento do tempo em ms
sheet['J'+str(it)] = round(xcoord[3],0) #Houve um arredondamento do tempo em ms
sheet['H'+str(it)] = round(xcoord[4],0) #Houve um arredondamento do tempo em ms
wb.save("Event_Timing.xlsx")
#Gravação dos valores marcados na planilha do excel - FIM

MVOvalues1.append((int(sheet['C'+str(it)].value)/1000)+LM_Time)#Valor do MVO à esquerda: Valor de MVO da planilha(em ms)/1000 + LM_Time(em s)
MVCvalues1.append((int(sheet['D'+str(it)].value)/1000)+LM_Time)#Valor do MVC à esquerda: Valor de MVC da planilha(em ms)/1000 + LM_Time(em s)
AVOvalues1.append((int(sheet['E'+str(it)].value)/1000)+LM_Time)#Valor do AVO à esquerda: Valor de AVO da planilha(em ms)/1000 + LM_Time(em s)
AVCvalues1.append((int(sheet['F'+str(it)].value)/1000)+LM_Time)#Valor do AVC à esquerda: Valor de AVC da planilha(em ms)/1000 + LM_Time(em s)
MVOvalues2.append((int(sheet['C'+str(it)].value)/1000)+RM_Time)#Valor do MVO à esquerda: Valor de MVO da planilha(em ms)/1000 + RM_Time(em s)
MVCvalues2.append((int(sheet['D'+str(it)].value)/1000)+RM_Time)#Valor do MVC à esquerda: Valor de MVC da planilha(em ms)/1000 + RM_Time(em s)
AVOvalues2.append((int(sheet['E'+str(it)].value)/1000)+RM_Time)#Valor do AVO à esquerda: Valor de AVO da planilha(em ms)/1000 + RM_Time(em s)
AVCvalues2.append((int(sheet['F'+str(it)].value)/1000)+RM_Time)#Valor do AVC à esquerda: Valor de AVC da planilha(em ms)/1000 + RM_Time(em s)
Dif_LM_OnsetQRS1.append(LM_Time - (int(sheet['G'+str(it)].value)/1000)) #Diferença entre o Onset QRS 1 e o LM_Time

#Recomputação devido à limitações do package para pegar valores da planilha - Não é preciso adicionar LM_Time aos valores marcados no programa
EMCvalues1.append((int(sheet['G'+str(it)].value)/1000))                 #Início de EMC1 = Onset QRS 1(em ms)/1000
EMCvalues2.append((int(sheet['H'+str(it)].value)/1000))                 #Início de EMC2 = Onset QRS 2(em ms)/1000
IVCvalues1.append((int(sheet['D'+str(it)].value)/1000+LM_Time))         #Início de IVC1 = MVC(em ms)/1000 + LM_Time
IVCvalues2.append((int(sheet['D'+str(it)].value)/1000+RM_Time))         #Início de IVC2 = MVC(em ms)/1000 + RM_Time
EjectionTimevalues1.append((int(sheet['E'+str(it)].value)/1000+LM_Time))#Início de EjectionTime1 = AVO(em ms)/1000 + LM_Time
EjectionTimevalues2.append((int(sheet['E'+str(it)].value)/1000+RM_Time))#Início de EjectionTime2 = AVO(em ms)/1000 + RM_Time
IVRTvalues.append((int(sheet['F'+str(it)].value)/1000+LM_Time))         #Início de IVRT = AVC(em ms)/1000 + LM_Time
Evalues.append((int(sheet['C'+str(it)].value)/1000+LM_Time))            #Início de E = MVO(em ms)/1000 + LM_Time
Diastasisvalues.append((int(sheet['Q'+str(it)].value)/1000))            #Início da Diastase = D point/1000
Avalues.append((int(sheet['I'+str(it)].value)/1000))                    #Início de A = Onset P(em ms)/1000
Avalues.append((int(sheet['I'+str(it)].value)/1000))                    #Início de A = Onset P(em ms)/1000
#Os valores acima são usados na separação das fases

#Impressão dos valores trabalhados no terminal
print("\nLM_Time: ",LM_Time*1000, "ms")
print("RM_Time: ",RM_Time)
print("Difference between LM_Time and Onset QRS1:", Dif_LM_OnsetQRS1[it-4]*1000, "ms")
print("\nMVO1: ",MVOvalues1[it-4]*1000, "ms")
print("MVO2: ",MVOvalues2[it-4]*1000, "ms")
print("MVC1: ",MVCvalues1[it-4]*1000, "ms")
print("MVC2: ",MVCvalues2[it-4]*1000, "ms")
print("AVO1: ",AVOvalues1[it-4]*1000, "ms")
print("AVO2: ",AVOvalues2[it-4]*1000, "ms")
print("AVC1: ",AVCvalues1[it-4]*1000, "ms")
print("AVC2: ",AVCvalues2[it-4]*1000, "ms")
print("\nEMC1: ",EMCvalues1[it-4]*1000, "ms")
print("EMC2: ",EMCvalues2[it-4]*1000, "ms")
print("IVC1: ",IVCvalues1[it-4]*1000, "ms")
print("IVC2: ",IVCvalues2[it-4]*1000, "ms")
print("Ejection Time1: ",EjectionTimevalues1[it-4]*1000, "ms")
print("Ejection Time2: ",EjectionTimevalues2[it-4]*1000, "ms")
print("IVRT: ",IVRTvalues[it-4]*1000, "ms")
print("E: ",Evalues[it-4]*1000, "ms")
print("Diastasis: ",Diastasisvalues[it-4]*1000, "ms")
print("Atrial Systole: ",Avalues[it-4]*1000, "ms")
print("\n\n")
#Trabalho com Excel - FIM

while True:
    print("\n\nParameters:\n\t1. Global Longitudinal Strain\n\t2. Mechanical Dispersion")
    print("\t3. Diastolic Recovery")
    print("\t4. Show plot w/o any parameters\n\t0. Terminate program")
    prmt = input("Parameter: ")

    if prmt == "1":                                                             #Obtenção do Global Longitudinal Strain
        txt1_s = txt1[(txt1.index >= EMCvalues1[it-4]) & (txt1.index < AVCvalues1[it-4])] #Valores até o AVC - Durante a sístole
        txt2_s = txt2[(txt2.index >= EMCvalues1[it-4]) & (txt2.index < AVCvalues1[it-4])]
        txt3_s = txt3[(txt3.index >= EMCvalues1[it-4]) & (txt3.index < AVCvalues1[it-4])]
        #print((tcolunas1-2)+(tcolunas2-2)+(tcolunas3-2)) #quantidade total de segmentos
        #print(list(txt2_s))                              #lista os nomes dos segmentos
        #print (colours[:-2])
        print("\n\nPeak negative systolic strain:\n")
        gls = []
        colours=list(txt2_s)
        for colour_it in range(0,tcolunas2-2):
            print("2CH:", colours[colour_it],":",txt2_s[colours[colour_it]].min(),"%")
            gls.append(txt2_s[colours[colour_it]].min())
        print("\n")
        colours=list(txt1_s)
        for colour_it in range(0,tcolunas1-2):
            print("4CH:", colours[colour_it],":",txt1_s[colours[colour_it]].min(),"%")
            gls.append(txt1_s[colours[colour_it]].min())
        print("\n")
        colours=list(txt3_s)
        for colour_it in range(0,tcolunas3-2):
            print("APLAX:", colours[colour_it],":",txt3_s[colours[colour_it]].min(),"%")
            gls.append(txt3_s[colours[colour_it]].min())
        gls=np.mean(gls)
        print("\n\nGlobal Longitudinal Strain: ", gls,"%")

    elif prmt == "2":
        txt1_sliced_onsets = txt1[(txt1.index >= EMCvalues1[it-4]) & (txt1.index < EMCvalues2[it-4])]#Obtenção da Mechanical Dispersion
        txt2_sliced_onsets = txt2[(txt2.index >= EMCvalues1[it-4]) & (txt2.index < EMCvalues2[it-4])]
        txt3_sliced_onsets = txt3[(txt3.index >= EMCvalues1[it-4]) & (txt3.index < EMCvalues2[it-4])]
        global_minima_times = []
        print("\n\nTimes of peak negative strain:\n")

        colours=list(txt2_sliced_onsets)
        for colour_it in range(0,tcolunas2-2):
            print("2CH:", colours[colour_it],":",txt2_sliced_onsets[colours[colour_it]].idxmin()-EMCvalues1[it-4],"ms")
            global_minima_times.append(txt2_sliced_onsets[colours[colour_it]].idxmin())
        print("\n")

        colours=list(txt1_sliced_onsets)
        for colour_it in range(0,tcolunas1-2):
            print("4CH:", colours[colour_it],":",txt1_sliced_onsets[colours[colour_it]].idxmin()-EMCvalues1[it-4],"ms")
            global_minima_times.append(txt1_sliced_onsets[colours[colour_it]].idxmin())
        print("\n")

        colours=list(txt3_sliced_onsets)
        for colour_it in range(0,tcolunas3-2):
            print("APLAX:", colours[colour_it],":",txt3_sliced_onsets[colours[colour_it]].idxmin()-EMCvalues1[it-4],"ms")
            global_minima_times.append(txt3_sliced_onsets[colours[colour_it]].idxmin())

        print("\n\nMechanical Dispersion: ",np.std(global_minima_times)*1000, "ms")

    elif prmt == "3":
        ThirdDiastoleTime=AVCvalues1[it-4]+((EMCvalues2[it-4]+Dif_LM_OnsetQRS1[it-4])-AVCvalues1[it-4])/3 #EMC2+Diferença do Pico R1 e o onset QRS1-AVC1
        #Criação das células com os valores de AVC e de 1/3 da diástole - Início
        a = np.full(tcolunas1, float('nan'))         #Cria uma linha de tcolunas NaN
        txt1_dr = txt1
        indices = list(txt1_dr.index.values)#Rotina para a alteração do índice da lista de forma que os novos indíces sejam o último índice
        var_t_med = indices[len(txt1_dr)-1]/len(txt1_dr)    #Nativos da lista incrementados
        txt1_dr.loc[AVCvalues1[it-4]] = a
        txt1_dr.loc[ThirdDiastoleTime] = a
        txt1_dr = txt1_dr.sort_index()
        txt1_dr = txt1_dr.interpolate(method = 'cubic')

        a = np.full(tcolunas2, float('nan'))         #Cria uma linha de tcolunas NaN
        txt2_dr = txt2
        indices = list(txt2_dr.index.values)#Rotina para a alteração do índice da lista de forma que os novos indíces sejam o último índice
        var_t_med = indices[len(txt2_dr)-1]/len(txt2_dr)    #Nativos da lista incrementados
        txt2_dr.loc[AVCvalues1[it-4]] = a
        txt2_dr.loc[ThirdDiastoleTime] = a
        txt2_dr = txt1_dr.sort_index()
        txt2_dr = txt2_dr.interpolate(method = 'cubic')

        a = np.full(tcolunas3, float('nan'))         #Cria uma linha de tcolunas NaN
        txt3_dr = txt3
        indices = list(txt3_dr.index.values)#Rotina para a alteração do índice da lista de forma que os novos indíces sejam o último índice
        var_t_med = indices[len(txt3_dr)-1]/len(txt3_dr)    #Nativos da lista incrementados
        txt3_dr.loc[AVCvalues1[it-4]] = a
        txt3_dr.loc[ThirdDiastoleTime] = a
        txt3_dr = txt3_dr.sort_index()
        txt3_dr = txt3_dr.interpolate(method = 'cubic')
        #Criação das células com os valores de AVC e de 1/3 da diástole - Fim

        print("\n\nFirst third of diastole time: ",ThirdDiastoleTime*1000,"ms")

        DI_2CH = []
        colours=list(txt2_dr)
        print("\nDiastolic Index\n\n2CH:")
        for colour_it in range(0,tcolunas2-2):
            DI_2CH.append((txt2_dr.at[AVCvalues1[it-4],colours[colour_it]] - txt2_dr.at[ThirdDiastoleTime,colours[colour_it]])/txt2_dr.at[AVCvalues1[it-4],colours[colour_it]])
            print(colours[colour_it],":", DI_2CH[colour_it]*100,"%")
        print("\n")

        DI_4CH = []
        colours=list(txt1_dr)
        print("\n4CH:")
        for colour_it in range(0,tcolunas1-2):
            DI_4CH.append((txt1_dr.at[AVCvalues1[it-4],colours[colour_it]] - txt1_dr.at[ThirdDiastoleTime,colours[colour_it]])/txt1_dr.at[AVCvalues1[it-4],colours[colour_it]])
            print(colours[colour_it],":", DI_4CH[colour_it]*100,"%")
        print("\n")

        DI_APLAX = []
        colours=list(txt3_dr)
        print("\nAPLAX:")
        for colour_it in range(0,tcolunas3-2):
            DI_APLAX.append((txt3_dr.at[AVCvalues1[it-4],colours[colour_it]] - txt3_dr.at[ThirdDiastoleTime,colours[colour_it]])/txt3_dr.at[AVCvalues1[it-4],colours[colour_it]])
            print(colours[colour_it],":", DI_APLAX[colour_it]*100,"%")
        print("\n")

    elif prmt == "4":
        print("\nPlot w/o any parameters")


    elif prmt == "0":
        break

    else:
        print("\n\nInvalid option\n\n\n")
        continue
    Parameters_Plot()
    print("\n")

arq.close()
arq_sr_lv.close()
