# -*- coding: utf-8 -*-
#testeasds
import pandas as pd                     #Package usado no trabalho com os arquivos .txt
import numpy as np
import matplotlib.pyplot as plt
import re                               #Package padrão - Para extrair números da string
import openpyxl                         #Package para trabalhar com os arquivos .xlsx
import scipy
#import mplcursors
#import peakutils

#Constantes a serem definidas
N = 80   #CASO A INTERPOLAÇÃO ESTEJA ATIVADA(Ainda não está) - É definido aqui o número de frames desejados no arquivo final
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

#Função para deixar os arquivos com o mesmo numero de amostras - INÍCIO
def nsamples(exame, txt, N):
    tcolunas=int(((txt.size/len(txt.index))))
    if(len(txt.index))>N:                           #Caso o numero de linhas seja > N
        txt=txt.head(N)

    if(len(txt.index))<N:                           #Caso seja o numero de linhas seja < N
        a = np.full(tcolunas, float('nan'))         #Cria uma linha de tcolunas NaN
        indices = list(txt.index.values)#Rotina para a alteração do índice da lista de forma que os novos indíces sejam o último índice
        var_t_med = indices[len(txt)-1]/len(txt)    #Nativos da lista incrementados
        for it in range(1,N+1-len(txt)):
            if N<100:
                txt.loc[2*it*(var_t_med)] = a
            elif N<150:
                txt.loc[0.8*it*(var_t_med)] = a
            elif N<175:
                txt.loc[0.6*it*(var_t_med)] = a
            elif N<200:
                txt.loc[0.4*it*(var_t_med)] = a
            else:
                txt.loc[0.2*it*(var_t_med)] = a
        txt = txt.sort_index()
        txt = txt.interpolate(method = 'cubic')
    #ALTERAÇÃO PARA O MESMO NÚMERO DE LINHAS - FIM

    #Impressões dos dados do arquivo de texto no terminal - INÍCIO
    print("\n\n")
    print(exame)
    print("\n")
    print(txt)
    #Impressões dos dados do arquivo de texto no terminal - FIM
#Função para deixar os arquivos com o mesmo numero de amostras - FIM

#Função para marcação dos pontos no ECG - INÍCIO
def onclick(event):
    #print ("\nValue: Time = %f milliseconds"%(event.xdata*1000))
    xcoord.append(event.xdata*1000)
#Função para marcação dos pontos no ECG - FIM

#Plotagem com as cores correspondentes ao arquivo - INÍCIO
def ColorPlot(txt):
    colors=list(txt)                                                    #Alterar o fundo, caso faça o resto
    #print("=============== SEPARADOR ==============")
    for it in range(0,6):
        #print(colors[it]+'teste')                                      #Só para saber a string certa do header
        if(colors[it] == '      RED    '):
            plt.plot(txt.iloc[:,it], 'r')
        elif(colors[it] == '     BLUE    '):
            plt.plot(txt.iloc[:,it], 'b')
        elif(colors[it] == '  MAGENTA    '):
            plt.plot(txt.iloc[:,it], 'm')
        elif(colors[it] == '    GREEN    '):
            plt.plot(txt.iloc[:,it], 'g')
        elif(colors[it] == '     CYAN    '):
            plt.plot(txt.iloc[:,it], 'c')
        elif(colors[it] == '   YELLOW    '):
            plt.plot(txt.iloc[:,it], 'y')
        else:
            plt.plot(txt.iloc[:,it], 'k')
    plt.plot(txt.iloc[:,6], 'k.')                                       #Caso altere o fundo, mudar para branco para ficar como no echopac
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
    ColorPlot(txt)
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
    ColorPlot(strain_la)
    plt.ylabel('Strain - LA\n(%)')
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
    plt.plot(txt.loc[:,'ECG : '])
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
    ColorPlot(txt)

    #Marcações dos pontos usados para os parâmetros
    if prmt == "1":
        plt.plot(txt_s['      RED    '].idxmin(),txt_s['      RED    '].min(), 'kx')
        plt.plot(txt_s['     BLUE    '].idxmin(),txt_s['     BLUE    '].min(), 'kx')
        plt.plot(txt_s['  MAGENTA    '].idxmin(),txt_s['  MAGENTA    '].min(), 'kx')
        plt.plot(txt_s['    GREEN    '].idxmin(),txt_s['    GREEN    '].min(), 'kx')
        plt.plot(txt_s['     CYAN    '].idxmin(),txt_s['     CYAN    '].min(), 'kx')
        plt.plot(txt_s['   YELLOW    '].idxmin(),txt_s['   YELLOW    '].min(), 'kx')

    if prmt == "2":
        plt.plot(txt_sliced_onsets['      RED    '].idxmin(),txt_sliced_onsets['      RED    '].min(), 'kx')
        plt.plot(txt_sliced_onsets['     BLUE    '].idxmin(),txt_sliced_onsets['     BLUE    '].min(), 'kx')
        plt.plot(txt_sliced_onsets['  MAGENTA    '].idxmin(),txt_sliced_onsets['  MAGENTA    '].min(), 'kx')
        plt.plot(txt_sliced_onsets['    GREEN    '].idxmin(),txt_sliced_onsets['    GREEN    '].min(), 'kx')
        plt.plot(txt_sliced_onsets['     CYAN    '].idxmin(),txt_sliced_onsets['     CYAN    '].min(), 'kx')
        plt.plot(txt_sliced_onsets['   YELLOW    '].idxmin(),txt_sliced_onsets['   YELLOW    '].min(), 'kx')

    if prmt == "3":
        plt.plot(ThirdDiastoleTime,txt_dr.at[ThirdDiastoleTime,'      RED    '], 'kx')
        plt.plot(ThirdDiastoleTime,txt_dr.at[ThirdDiastoleTime,'     BLUE    '], 'kx')
        plt.plot(ThirdDiastoleTime,txt_dr.at[ThirdDiastoleTime,'  MAGENTA    '], 'kx')
        plt.plot(ThirdDiastoleTime,txt_dr.at[ThirdDiastoleTime,'    GREEN    '], 'kx')
        plt.plot(ThirdDiastoleTime,txt_dr.at[ThirdDiastoleTime,'     CYAN    '], 'kx')
        plt.plot(ThirdDiastoleTime,txt_dr.at[ThirdDiastoleTime,'   YELLOW    '], 'kx')

    if prmt == "4":
        plt.plot(txt_s['      RED    '].idxmin(),txt_s['      RED    '].min(), 'k+')
        plt.plot(txt_s['     BLUE    '].idxmin(),txt_s['     BLUE    '].min(), 'k+')
        plt.plot(txt_s['  MAGENTA    '].idxmin(),txt_s['  MAGENTA    '].min(), 'k+')
        plt.plot(txt_s['    GREEN    '].idxmin(),txt_s['    GREEN    '].min(), 'k+')
        plt.plot(txt_s['     CYAN    '].idxmin(),txt_s['     CYAN    '].min(), 'k+')
        plt.plot(txt_s['   YELLOW    '].idxmin(),txt_s['   YELLOW    '].min(), 'k+')

        plt.plot(txt_sliced_onsets['      RED    '].idxmin(),txt_sliced_onsets['      RED    '].min(), 'kx')
        plt.plot(txt_sliced_onsets['     BLUE    '].idxmin(),txt_sliced_onsets['     BLUE    '].min(), 'kx')
        plt.plot(txt_sliced_onsets['  MAGENTA    '].idxmin(),txt_sliced_onsets['  MAGENTA    '].min(), 'kx')
        plt.plot(txt_sliced_onsets['    GREEN    '].idxmin(),txt_sliced_onsets['    GREEN    '].min(), 'kx')
        plt.plot(txt_sliced_onsets['     CYAN    '].idxmin(),txt_sliced_onsets['     CYAN    '].min(), 'kx')
        plt.plot(txt_sliced_onsets['   YELLOW    '].idxmin(),txt_sliced_onsets['   YELLOW    '].min(), 'kx')

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
    ColorPlot(txt_mid)
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
    plt.plot(txt.loc[:,'ECG : '])
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
    #mplcursors.cursor(hover='True') #Ver como selecionar todas de uma vez e como mostrar ao passar o mouse sobre
    plt.show()
#Plotagem dos gráficos de saída final - FIM



#print("\033c") Caso queira limpar o terminal
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

arq_la = open('exam_la', 'r')
exame = arq.readline()
exame = exame[:len(exame)-1]    #Retira o \n
exame_mid = arq.readline()
exame_mid = exame_mid[:len(exame_mid)-1]    #Retira o \n
exame_la = arq_la.readline()
exame_la = exame_la[:len(exame_la)-1]    #Retira o \n
print("\n\nUsing files: ")
print("\t",exame)
print("\t",exame_mid)
if exame_mid != exame_la:
    print("\t",exame_la)
txt=pd.read_csv(exame, sep='\t', engine='python', skiprows=3, index_col=0) #Parte do índice arrumada
txt_mid=pd.read_csv(exame_mid, sep='\t', engine='python', skiprows=3, index_col=0)
strain_la=pd.read_csv(exame_la, sep='\t', engine='python', skiprows=3, index_col=0)
#Fim da abertura dos .txt

"""
#Criação do arquivo de saída com o cabeçalho - INÍCIO
new_w_file = open("novo"+exame+".txt", 'w')
txt_original = open(exame+".txt", 'r')

cont = 0
for line in txt_original:
    if ((cont < 3) and (cont != 1)):
        new_w_file.write(line)
        cont = cont+1
    if cont == 1:
        new_w_file.write("Number of Frames ")
        new_w_file.write(str(N))
        new_w_file.write(" - Previous ")
        cont = cont + 1
txt_original.close()
new_w_file.close()
#Criação do arquivo de saída com o cabeçalho - FIM
"""

txt_original = open(exame, 'r')
numbers = re.findall("\d+\.\d+", txt_original.readlines()[2]) #Numeros extraidos da linha 3 do txt - LM_Time, ES_Time e RM_Time
txt_original.close()

txt.drop('Unnamed: 1', axis=1, inplace=True) #Retira a coluna inútil que é lida (devido à tabulação exagerada do arquivo exportado)
txt_mid.drop('Unnamed: 1', axis=1, inplace=True) #Retira a coluna inútil que é lida (devido à tabulação exagerada do arquivo exportado)
strain_la.drop('Unnamed: 1', axis=1, inplace=True) #Retira a coluna inútil que é lida (devido à tabulação exagerada do arquivo exportado)
#nsamples(exame, txt, N) #Função para colocar o mesmo numero de amostras

tcolunas=int(((txt.size/len(txt.index))))
LM_Time = float(numbers[0])
RM_Time = float(numbers[1])
ES_Time = float(numbers[2])                    #AVC - Aortic Valve Closure



if txt.index[len(txt.index)-1] < strain_la.index[len(strain_la.index)-1]:#Determinar o arquivo de texto com menor tempo
    END_Time0 = txt.index[len(txt.index)-1]                     #para que um gráfico não fique sobrando
else:
    END_Time0 = strain_la.index[len(strain_la.index)-1]

if txt.index[len(txt.index)-1] < txt_mid.index[len(txt_mid.index)-1]:#Determinar o arquivo de texto com menor tempo
    END_Time1 = txt.index[len(txt.index)-1]                     #para que um gráfico não fique sobrando
else:
    END_Time1 = txt_mid.index[len(txt_mid.index)-1]

###################################################################################   A parte alterada nessa etapa foi a parte abaixo

#Gravação dos valores marcados na planilha do excel - INÍCIO

#print("\nMarcacao %d\n" %(it - 3))
print("\n\nMarcacao do Onset QRS 1, ponto de diástase, onset P, pico P, onset QRS 2")
PlotClick(LM_Time, ES_Time, RM_Time, END_Time0)
sheet['G'+str(it)] = round(xcoord[0],0) #Houve um arredondamento do tempo em ms
sheet['Q'+str(it)] = round(xcoord[1],0) #Houve um arredondamento do tempo em ms
sheet['I'+str(it)] = round(xcoord[2],0) #Houve um arredondamento do tempo em ms
sheet['J'+str(it)] = round(xcoord[3],0) #Houve um arredondamento do tempo em ms
sheet['H'+str(it)] = round(xcoord[4],0) #Houve um arredondamento do tempo em ms
#VER COMO MELHORAR O ALGORITMO DA MARCACAO

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
    print("\t3. Diastolic Recovery\n\t4. Global Longitudinal Strain and Mechanical Dispersion")
    print("\t5. Show plot w/o any parameters\n\t0. Terminate program")
    prmt = input("Parameter: ")

    if prmt == "1":                                                             #Obtenção do Global Longitudinal Strain
        txt_s = txt[(txt.index >= EMCvalues1[it-4]) & (txt.index < AVCvalues1[it-4])] #Valores até o AVC - Durante a sístole
        gls = (txt_s['      RED    '].min() + txt_s['     BLUE    '].min() + txt_s['  MAGENTA    '].min() + txt_s['    GREEN    '].min()
        + txt_s['     CYAN    '].min() + txt_s['   YELLOW    '].min())/6
        print("\n\nGlobal Longitudinal Strain: ", gls)
        #print(tcolunas-2) #Imprime o número de curvas

    elif prmt == "2":
        txt_sliced_onsets = txt[(txt.index >= EMCvalues1[it-4]) & (txt.index < EMCvalues2[it-4])]#Obtenção da Mechanical Dispersion
        global_minima_times = np.array([txt_sliced_onsets['      RED    '].idxmin(),
        txt_sliced_onsets['     BLUE    '].idxmin(), txt_sliced_onsets['  MAGENTA    '].idxmin(),
        txt_sliced_onsets['    GREEN    '].idxmin(), txt_sliced_onsets['     CYAN    '].idxmin(),
        txt_sliced_onsets['   YELLOW    '].idxmin()])
        print("\n\nMechanical Dispersion: ",np.std(global_minima_times)*1000, "ms")

    elif prmt == "3":
        #print("\nDiastolic Recovery: Currently not available")
        ThirdDiastoleTime=AVCvalues1[it-4]+((EMCvalues2[it-4]+Dif_LM_OnsetQRS1[it-4])-AVCvalues1[it-4])/3 #EMC2+Diferença do Pico R1 e o onset QRS1-AVC1
        #Criação das células com os valores de AVC e de 1/3 da diástole - Início
        a = np.full(tcolunas, float('nan'))         #Cria uma linha de tcolunas NaN
        txt_dr = txt
        indices = list(txt_dr.index.values)#Rotina para a alteração do índice da lista de forma que os novos indíces sejam o último índice
        var_t_med = indices[len(txt_dr)-1]/len(txt_dr)    #Nativos da lista incrementados
        txt_dr.loc[AVCvalues1[it-4]] = a
        txt_dr.loc[ThirdDiastoleTime] = a
        txt_dr = txt_dr.sort_index()
        txt_dr = txt_dr.interpolate(method = 'cubic')
        #Criação das células com os valores de AVC e de 1/3 da diástole - Fim

        #print(txt_dr.at[AVCvalues1[it-4],'      RED    '])
        print("\nFirst third of diastole time ",ThirdDiastoleTime*1000,"ms")

        DI_R= (txt_dr.at[AVCvalues1[it-4],'      RED    '] - txt_dr.at[ThirdDiastoleTime,'      RED    '])/txt_dr.at[AVCvalues1[it-4],'      RED    ']
        DI_B= (txt_dr.at[AVCvalues1[it-4],'     BLUE    '] - txt_dr.at[ThirdDiastoleTime,'     BLUE    '])/txt_dr.at[AVCvalues1[it-4],'     BLUE    ']
        DI_M= (txt_dr.at[AVCvalues1[it-4],'  MAGENTA    '] - txt_dr.at[ThirdDiastoleTime,'  MAGENTA    '])/txt_dr.at[AVCvalues1[it-4],'  MAGENTA    ']
        DI_G= (txt_dr.at[AVCvalues1[it-4],'    GREEN    '] - txt_dr.at[ThirdDiastoleTime,'    GREEN    '])/txt_dr.at[AVCvalues1[it-4],'    GREEN    ']
        DI_C= (txt_dr.at[AVCvalues1[it-4],'     CYAN    '] - txt_dr.at[ThirdDiastoleTime,'     CYAN    '])/txt_dr.at[AVCvalues1[it-4],'     CYAN    ']
        DI_Y= (txt_dr.at[AVCvalues1[it-4],'   YELLOW    '] - txt_dr.at[ThirdDiastoleTime,'   YELLOW    '])/txt_dr.at[AVCvalues1[it-4],'   YELLOW    ']
        print("\nDiastolic Index - RED: ",DI_R*100,"%")
        print("Diastolic Index - BLUE: ",DI_B*100,"%")
        print("Diastolic Index - MAGENTA: ",DI_M*100,"%")
        print("Diastolic Index - CYAN: ",DI_G*100,"%")
        print("Diastolic Index - GREEN: ",DI_C*100,"%")
        print("Diastolic Index - YELLOW: ",DI_Y*100,"%")

    elif prmt == "4":
        txt_s = txt[(txt.index >= EMCvalues1[it-4]) & (txt.index < AVCvalues1[it-4])] #Valores até o AVC - Durante a sístole
        gls = (txt_s['      RED    '].min() + txt_s['     BLUE    '].min() + txt_s['  MAGENTA    '].min() + txt_s['    GREEN    '].min()
        + txt_s['     CYAN    '].min() + txt_s['   YELLOW    '].min())/6
        print("\n\nGlobal Longitudinal Strain: ", gls)
        txt_sliced_onsets = txt[(txt.index >= EMCvalues1[it-4]) & (txt.index < EMCvalues2[it-4])]#Obtenção da Mechanical Dispersion
        global_minima_times = np.array([txt_sliced_onsets['      RED    '].idxmin(),
        txt_sliced_onsets['     BLUE    '].idxmin(), txt_sliced_onsets['  MAGENTA    '].idxmin(),
        txt_sliced_onsets['    GREEN    '].idxmin(), txt_sliced_onsets['     CYAN    '].idxmin(),
        txt_sliced_onsets['   YELLOW    '].idxmin()])
        print("\n\nMechanical Dispersion: ",np.std(global_minima_times)*1000, "ms")

    elif prmt == "5":
        print("\nPlot w/o any parameters")

    elif prmt == "0":
        break

    else:
        print("\n\nInvalid option\n\n\n")
        continue
    Parameters_Plot()
    print("\n")
#Geração do novo arquivo .txt após a interpolação
"""
txt = txt.reset_index() #Passa os índices, que antes eram o tempo, para uma coluna (assim o tempo é transferido para o novo arquivo)
txt.to_csv("novo"+exame+".txt", sep='\t', index = None, float_format='%.6f', mode='a') #Gera novo arquivo com o prefixo "novo"

it=it+1     #Iterador que funciona para "definir a linha a ser lida no excel", ou seja, para ler a linha seguinte
"""
arq.close()
arq_la.close()
