# -*- coding: utf-8 -*-

"Separar as funcoes de plot para cada parâmetro mesmo, ficam menos confusas"

# A package created for the D-Station (https://gpdsifpb.github.io/D-Station/)
# to plot strain or strain rate curves and calculate its parameters



import matplotlib as mpl		 # Used in the plots
import matplotlib.pyplot as plt	 # Also used in the plots
import numpy as np				 # Ditto


# Declaring variables and arrays
xcoord = []	# List where the time values of the selected points are stored


# Function to select the points of interest in the ECG curve
def onclick(event):
	#print ("\nValue: Time = %f milliseconds"%(event.xdata*1000)) # Shows the time value of the clicked point
	xcoord.append(event.xdata*1000) # Appends the points to an array


# This function below may be used in the future
def onclick_iva(event):
	#print ("\nValue: Time = %f milliseconds"%(event.xdata*1000))
	if prmt != "8":
		xcoord.append(event.xdata*1000)
	else:
		times_IVA.append(event.xdata)


# Function to plot the curves with the colors that they have in the raw data file
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
	#plt.plot(txt.iloc[:,tcolunas-2], 'k.')                  # Global segment, uncomment this to show it


#Plots the ECG curve so the user may see in the red lines the OnsetQRS1, OnsetP and OnsetQRS2 and verify if the values stored in the spreadsheet are correct
def ecgVerification(txt1, LM_Time, ES_Time, RM_Time, END_Time0, SizeFont, OnsetQRS1, OnsetP, OnsetQRS2):

	ax0 = plt.subplot2grid((12,1),(0,0), rowspan = 12, colspan = 1)
	plt.xlim(0, END_Time0)
	ax0.axvline(LM_Time, color='y')
	ax0.axvline(ES_Time, color='g')
	ax0.axvline(RM_Time, color='y')

	ax0.axvline(OnsetQRS1,color = 'r')
	ax0.axvline(OnsetP,color = 'r')
	ax0.axvline(OnsetQRS2,color = 'r')

	tick_locs = np.arange(0.0,END_Time0,0.2)
	tick_lbls = np.arange(0, int(END_Time0*1000), 200)
	plt.xticks(tick_locs, tick_lbls)
	plt.plot(txt1.loc[:,'ECG : '])

	print("\nStored Values:\n\tOnset QRS 1: ", OnsetQRS1*1000,"ms\n\tOnset P: ", OnsetP*1000, "ms\n\tOnset QRS 2: ", OnsetQRS2*1000,"ms")

	"""
	ymin, ymax = plt.ylim()
	txt_height_1 = ymax+0.15*(ymax-ymin) #Valve events text height

	plt.text(OnsetQRS1+0.002, txt_height_1, "OnsetQRS1" , rotation=0, verticalalignment='center')
	plt.text(OnsetP+0.002, 0.1, txt_height_1, "OnsetP" , rotation=0, verticalalignment='center')
	plt.text(OnsetQRS2+0.002, 0.1, txt_height_1, "OnsetQRS2" , rotation=0, verticalalignment='center')
	"""

	plt.xlabel('Time (ms)', fontsize=SizeFont)
	plt.ylabel('ECG\nVoltage (mV)', fontsize=SizeFont)
	plt.grid()
	plt.show()

# Funcao to plot the Strain and ECG curves to select 3 points of interest on the latter
def PlotClick(txt1, tcolunas1, LM_Time, ES_Time, RM_Time, END_Time0, SizeFont, op, test_op, strain_rate_lv4ch,tcolunas_strain_rate_lv4ch, prmt):
	fig = plt.figure(figsize=(12, 8))

	# Subplot 1 (Top Plot - LV Strain)
	ax0 = plt.subplot2grid((12,1),(0,0), rowspan = 4, colspan = 1)
	plt.xlim(0, END_Time0)
	ax0.axvline(LM_Time, color='y')
	ax0.axvline(ES_Time, color='g')
	ax0.axvline(RM_Time, color='y')
	tick_locs = np.arange(0.0,END_Time0,0.2)
	tick_lbls = np.arange(0, int(END_Time0*1000), 200)
	plt.xticks(tick_locs, tick_lbls)
	colorPlot(txt1,tcolunas1)			# Right now only the 4CH is plotted in this stage
	#colorPlot(txt2_mod,tcolunas2)		# To plot the others uncomment this and the line below and add the parameters txt2_mod and txt3_mod in PlotClick
	#colorPlot(txt3_mod,tcolunas3)
	plt.ylabel('Strain - LV\n(%)', fontsize=SizeFont)
	plt.grid()
	plt.setp(ax0.get_xticklabels(), visible=False)		# The time label isn't shown in this subplot

	# Subplot 2 (Mid Plot - LV Strain Rate)
	ax1 = plt.subplot2grid((12,1),(4,0), rowspan = 4, colspan = 1)
	plt.xlim(0, END_Time0)
	ax1.axvline(LM_Time, color='y')			# Plots the LM_Time line from the raw data file
	ax1.axvline(ES_Time, color='g')			# 		   ES_Time
	ax1.axvline(RM_Time, color='y')			# 		   RM_Time
	tick_locs = np.arange(0.0,END_Time0,0.2)
	tick_lbls = np.arange(0, int(END_Time0*1000), 200)
	plt.xticks(tick_locs, tick_lbls)		# Uses the ticks and ticklabels created above
	if op != test_op:
		colorPlot(strain_rate_lv4ch,tcolunas_strain_rate_lv4ch)		#S train Rate 4ch is shown if it is not a simulation
	else:
		colorPlot(txt_mid.truediv(txt1.index.to_series().diff(), axis = 0)/100, tcolunas1)
		# If it is a simulation then the strain rate 4ch is calculated from the simulated strain curves
		#colorPlot(txt2_mod.diff(),tcolunas2)
		#colorPlot(txt3_mod.diff(),tcolunas3)
	plt.ylabel('Strain Rate - LV\n(1/s)', fontsize=SizeFont)
	plt.grid()
	plt.setp(ax1.get_xticklabels(), visible=False)		# The time label isn't shown in this subplot

	# Subplot 3 (Bottom plot - ECG)
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

	cid = fig.canvas.mpl_connect('button_press_event', onclick) # Allowing to store the time values of the clicked points

	# Plotting everything to be clicked
	#plt.tight_layout()
	plt.show()

	fig.canvas.mpl_disconnect(cid)	# After the points selection the function to store them will finish

	return xcoord


#Plots the points of interest in the GLS, MD and DI calculation
def POIPlot(txt1, txt2_mod, txt3_mod, txt_mid, strain_rate_lv4ch, strain_rate_lv2ch, strain_rate_lv3ch, tcolunas1, tcolunas2, tcolunas3, tcolunas_mid, prmt, op, test_op,
END_Time1, SizeFont, SizePhaseFont, MVOvalues1, MVCvalues1, AVOvalues1, AVCvalues1, MVOvalues2, MVCvalues2, AVOvalues2, AVCvalues2, EMCvalues1, EMCvalues2, IVCvalues1,
IVCvalues2, EjectionTimevalues1, EjectionTimevalues2, IVRvalues, Evalues, Avalues, height_line, txt1_par, txt2_par, txt3_par):

	fig = plt.figure(figsize=(16, 8))

	#Top plot
	ax0 = plt.subplot2grid((16,1),(1,0), rowspan = 6, colspan = 1)
	plt.xlim(0, END_Time1)
	colorPlot(txt1,tcolunas1)
	colorPlot(txt2_mod,tcolunas2)
	colorPlot(txt3_mod,tcolunas3)

	# Below: The points used in the parameters calculations are shown
	if prmt == "1":		#Points used for GLS

		colours=list(txt1_par)
		for colour_it in range(0,tcolunas1-2):
			plt.plot(txt1_par[colours[colour_it]].idxmin(), txt1_par[colours[colour_it]].min(), 'kx')

		colours=list(txt2_par)
		for colour_it in range(0,tcolunas2-2):
			plt.plot(txt2_par[colours[colour_it]].idxmin(), txt2_par[colours[colour_it]].min(), 'k*')

		colours=list(txt3_par)
		for colour_it in range(0,tcolunas3-2):
			plt.plot(txt3_par[colours[colour_it]].idxmin(), txt3_par[colours[colour_it]].min(), 'k+')

	if prmt == "2":		#Points used for MD

		colours=list(txt1_par)

		for colour_it in range(0,tcolunas1-2):
			plt.plot(txt1_par[colours[colour_it]].idxmin(), txt1_par[colours[colour_it]].min(), 'kx')

		colours=list(txt2_par)

		for colour_it in range(0,tcolunas2-2):
			plt.plot(txt2_par[colours[colour_it]].idxmin(), txt2_par[colours[colour_it]].min(), 'kx')

		colours=list(txt3_par)

		for colour_it in range(0,tcolunas3-2):
			plt.plot(txt3_par[colours[colour_it]].idxmin(), txt3_par[colours[colour_it]].min(), 'kx')

	#if prmt == "3": 		#Points used for DI - Diastolic Index
		#ax0.axvline(ThirdDiastoleTime, color='k')

	#Diferenciação Entre eventos das valvas e das fases (altura da linha)/ Disposição do texto
	ymin, ymax = plt.ylim()
	txt_height_1 = ymax+0.15*(ymax-ymin) #Valve events text height
	txt_height_2 = ymax+0.05*(ymax-ymin) #Phase names text height
	x_inc=0.002
	plt.grid()
	tick_locs = np.arange(0.0,END_Time1,0.2)
	tick_lbls = np.arange(0, int(END_Time1*1000), 200)
	plt.xticks(tick_locs, tick_lbls)

	plt.ylabel('\nStrain - LV\n(%)', fontsize=SizeFont)


	plt.setp(ax0.get_xticklabels(), visible=False)		#Time labels in the top subplot won't be shown

	#Below: Valve events and phases names are written in the plot
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

	#These if are to determine which name will be the last written on the plot
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

	#Subplot 2 (mid)
	ax1 = plt.subplot2grid((16,1),(7,0), rowspan = 6, colspan = 1)

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

	plt.setp(ax1.get_xticklabels(), visible=False)

	#ECG plot (bottom)
	ax2 = plt.subplot2grid((16, 1), (13, 0), rowspan = 4, colspan = 1)
	plt.plot(txt1.loc[:,'ECG : '])
	plt.xlim(0, END_Time1)
	tick_locs = np.arange(0.0,END_Time1,0.2)
	tick_lbls = np.arange(0, int(END_Time1*1000), 200)
	plt.xticks(tick_locs, tick_lbls)
	plt.xlabel('Time (ms)', fontsize=SizeFont)
	plt.ylabel('ECG\nVoltage\n(mV)', fontsize=SizeFont)
	plt.grid()

	#Lines between subplots - May be deleted later
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

	#ifs to find which event will be last shown in the plot
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

	#ifs to find which event will be last shown in the plot
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

	#plt.tight_layout()
	plt.show()


# Plots the figures containing the results of the operations
def avgPhaseStrainVarPlot(txt1, txt2, txt3, averageLongStrain, tcolunas1, tcolunas2, tcolunas3, END_Time1, SizeFont, SizePhaseFont, MVOvalues1, MVCvalues1,
 					AVOvalues1, AVCvalues1, MVOvalues2, MVCvalues2, AVOvalues2, AVCvalues2, EMCvalues1, EMCvalues2, IVCvalues1, IVCvalues2, EjectionTimevalues1,
					EjectionTimevalues2, IVRvalues, Evalues, Avalues, height_line):

	fig = plt.figure(figsize=(16, 8))
	ax0 = plt.subplot2grid((16,1),(0,0), rowspan = 8, colspan = 1)
	plt.xlim(0, END_Time1)
	plt.plot(averageLongStrain, '.k')

	#Diferenciação Entre eventos das valvas e das fases (altura da linha)/ Disposição do texto
	ymin, ymax = plt.ylim()
	txt_height_1 = ymax+0.15*(ymax-ymin) #Valve events text height
	txt_height_2 = ymax+0.05*(ymax-ymin) #Phase names text height
	x_inc=0.002
	plt.grid()
	tick_locs = np.arange(0.0,END_Time1,0.2)
	tick_lbls = np.arange(0, int(END_Time1*1000), 200)
	plt.xticks(tick_locs, tick_lbls)
	plt.ylabel('\nAverage LV\nStrain (%)', fontsize=SizeFont)
	plt.setp(ax0.get_xticklabels(), visible=False)		#Time labels in the top subplot won't be shown

	#Below: Valve events and phases names are written in the plot
	plt.text(MVOvalues1[0]+x_inc, txt_height_1, "MVO" , rotation=0, verticalalignment='center', fontsize=SizePhaseFont)
	plt.text(MVCvalues1[0]+x_inc, txt_height_1, "MVC" , rotation=0, verticalalignment='center', fontsize=SizePhaseFont)
	plt.text(AVOvalues1[0]+x_inc, txt_height_1, "AVO" , rotation=0, verticalalignment='center', fontsize=SizePhaseFont)
	plt.text(AVCvalues1[0]+x_inc, txt_height_1, "AVC" , rotation=0, verticalalignment='center', fontsize=SizePhaseFont)
	plt.text(EMCvalues1[0]+x_inc, txt_height_2, "EMC" , rotation=0, verticalalignment='center', fontsize=SizePhaseFont)
	plt.text(IVCvalues1[0]+x_inc, txt_height_2, "IVC" , rotation=0, verticalalignment='center', fontsize=SizePhaseFont)
	plt.text(EjectionTimevalues1[0]+x_inc, txt_height_2, "Ejec" , rotation=0, verticalalignment='center', fontsize=SizePhaseFont)
	plt.text(IVRvalues[0]+x_inc, txt_height_2, "IVR" , rotation=0, verticalalignment='center', fontsize=SizePhaseFont)
	plt.text(Evalues[0]+x_inc, txt_height_2, "E" , rotation=0, verticalalignment='center', fontsize=SizePhaseFont)
	#plt.text(Diastasisvalues[0]+x_inc, txt_height_2, "D" , rotation=0, verticalalignment='center')
	plt.text(Avalues[0]+x_inc, txt_height_2, "A" , rotation=0, verticalalignment='center', fontsize=SizePhaseFont)

	#These if are to determine which name will be the last written on the plot
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
	if EMCvalues2 < END_Time1:
		plt.text(EMCvalues2[0]+x_inc, txt_height_2, "EMC" , rotation=0, verticalalignment='center', fontsize=SizePhaseFont)
		ax0.axvline(x=EMCvalues2[0], c="y",ymin=-0.1,ymax= height_line, linewidth=1.5, zorder=0, clip_on=False)
	if IVCvalues2[0]<END_Time1:
		plt.text(IVCvalues2[0]+x_inc, txt_height_2, "IVC" , rotation=0, verticalalignment='center', fontsize=SizePhaseFont)
		ax0.axvline(x=IVCvalues2[0], c="k",ymin=-0.1,ymax= height_line, linewidth=1, linestyle = ':', zorder=0, clip_on=False)
	if EjectionTimevalues2[0]<END_Time1:
		plt.text(EjectionTimevalues2[0]+x_inc, txt_height_2, "Ejec" , rotation=0, verticalalignment='center', fontsize=SizePhaseFont)
		ax0.axvline(x=EjectionTimevalues2[0], c="k",ymin=-0.1,ymax= height_line, linewidth=1, linestyle = ':', zorder=0, clip_on=False)

	#Subplot 2 (LV Strain Curves)
	ax1 = plt.subplot2grid((16,1),(8,0), rowspan = 8, colspan = 1)
	plt.xlim(0, END_Time1)
	colorPlot(txt1,tcolunas1)
	colorPlot(txt2,tcolunas2)
	colorPlot(txt3,tcolunas3)
	plt.grid()
	tick_locs = np.arange(0.0,END_Time1,0.2)
	tick_lbls = np.arange(0, int(END_Time1*1000), 200)
	plt.xticks(tick_locs, tick_lbls)
	plt.xlabel('Time (ms)', fontsize=SizeFont)
	plt.ylabel('\nStrain - LV\n(%)', fontsize=SizeFont)


	#Lines between subplots - May be deleted later
	ax0.axvline(x=MVOvalues1[0], c="k",ymin=-0.1,ymax= height_line+0.1, linewidth=1, linestyle = ':', zorder=0, clip_on=False)
	ax0.axvline(x=MVCvalues1[0], c="k",ymin=-0.1,ymax= height_line+0.1, linewidth=1, linestyle = ':', zorder=0, clip_on=False)
	ax0.axvline(x=AVOvalues1[0], c="k",ymin=-0.1,ymax= height_line+0.1, linewidth=1, linestyle = ':', zorder=0, clip_on=False)
	ax0.axvline(x=AVCvalues1[0], c="g",ymin=-0.1,ymax= height_line+0.1, linewidth=1.5, zorder=0, clip_on=False)
	ax0.axvline(x=EMCvalues1[0], c="y",ymin=-0.1,ymax= height_line, linewidth=1.5, zorder=0, clip_on=False)
	ax0.axvline(x=IVCvalues1[0], c="k",ymin=-0.1,ymax= height_line, linewidth=1, linestyle = ':', zorder=0, clip_on=False)
	ax0.axvline(x=EjectionTimevalues1[0], c="k",ymin=-0.1,ymax= height_line, linewidth=1, linestyle = ':', zorder=0, clip_on=False)
	ax0.axvline(x=IVRvalues[0], c="k",ymin=-0.1,ymax= height_line, linewidth=1, linestyle = ':', zorder=0, clip_on=False)
	ax0.axvline(x=Evalues[0], c="k",ymin=-0.1,ymax= height_line, linewidth=1, linestyle = ':', zorder=0, clip_on=False)
	#ax0.axvline(x=Diastasisvalues[0], c="k",ymin=-0.1,ymax= height_line, linewidth=1, linestyle = ':', zorder=0, clip_on=False)
	ax0.axvline(x=Avalues[0], c="k",ymin=-0.1,ymax= height_line, linewidth=1, linestyle = ':', zorder=0, clip_on=False)

	ax1.axvline(x=MVOvalues1[0], c="k",ymin=-0.1,ymax= height_line+0.1, linewidth=1, linestyle = ':', zorder=0, clip_on=False)
	ax1.axvline(x=MVCvalues1[0], c="k",ymin=-0.1,ymax= height_line+0.1, linewidth=1, linestyle = ':', zorder=0, clip_on=False)
	ax1.axvline(x=AVOvalues1[0], c="k",ymin=-0.1,ymax= height_line+0.1, linewidth=1, linestyle = ':', zorder=0, clip_on=False)
	ax1.axvline(x=AVCvalues1[0], c="g",ymin=-0.1,ymax= height_line+0.1, linewidth=1.5, zorder=0, clip_on=False)
	ax1.axvline(x=EMCvalues1[0], c="y",ymin=-0.1,ymax= height_line, linewidth=1.5, zorder=0, clip_on=False)
	ax1.axvline(x=IVCvalues1[0], c="k",ymin=-0.1,ymax= height_line, linewidth=1, linestyle = ':', zorder=0, clip_on=False)
	ax1.axvline(x=EjectionTimevalues1[0], c="k",ymin=-0.1,ymax= height_line, linewidth=1, linestyle = ':', zorder=0, clip_on=False)
	ax1.axvline(x=IVRvalues[0], c="k",ymin=-0.1,ymax= height_line, linewidth=1, linestyle = ':', zorder=0, clip_on=False)
	ax1.axvline(x=Evalues[0], c="k",ymin=-0.1,ymax= height_line, linewidth=1, linestyle = ':', zorder=0, clip_on=False)
	#ax1.axvline(x=Diastasisvalues[0], c="k",ymin=-0.1,ymax= height_line, linewidth=1, linestyle = ':', zorder=0, clip_on=False)
	ax1.axvline(x=Avalues[0], c="k",ymin=-0.1,ymax= height_line, linewidth=1, linestyle = ':', zorder=0, clip_on=False)

	#ifs to find which event will be last shown in the plot
	if MVOvalues2[0]<END_Time1:
		ax1.axvline(x=MVOvalues2[0], c="k",ymin=-0.1,ymax= height_line+0.1, linewidth=1, linestyle = ':', zorder=0, clip_on=False)
	if MVCvalues2[0]<END_Time1:
		ax1.axvline(x=MVCvalues2[0], c="k",ymin=-0.1,ymax= height_line+0.1, linewidth=1, linestyle = ':', zorder=0, clip_on=False)
	if AVOvalues2[0]<END_Time1:
		ax1.axvline(x=AVOvalues2[0], c="k",ymin=-0.1,ymax= height_line+0.1, linewidth=1, linestyle = ':', zorder=0, clip_on=False)
	if AVCvalues2[0]<END_Time1:
		ax1.axvline(x=AVCvalues2[0], c="k",ymin=-0.1,ymax= height_line+0.1, linewidth=1, linestyle = ':', zorder=0, clip_on=False)
	if EMCvalues2 < END_Time1:
		ax1.axvline(x=EMCvalues2[0], c="y",ymin=-0.1,ymax= height_line, linewidth=1.5, zorder=0, clip_on=False)
	if IVCvalues2[0]<END_Time1:
		ax1.axvline(x=IVCvalues2[0], c="k",ymin=-0.1,ymax= height_line, linewidth=1, linestyle = ':', zorder=0, clip_on=False)
	if EjectionTimevalues2[0]<END_Time1:
		ax1.axvline(x=EjectionTimevalues2[0], c="k",ymin=-0.1,ymax= height_line, linewidth=1, linestyle = ':', zorder=0, clip_on=False)

	#plt.tight_layout()
	plt.show()


#Below: To be implemented later
#===============================================

# Plots 17 segment bullseye
def bullseye_seventeenSEG_plot(ax, data, segBold=None, cmap=None, norm=None):
	"""
	This example demonstrates how to create the 17 segment model for the left
	ventricle recommended by the American Heart Association (AHA).
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


# Plots 18 segment bullseye
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
	This function creats the 18 segment model for the left ventricle according
	to the American Heart Association (AHA) [1]
	Based on the function developed by
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


# Inserts the data in the bullseye - Add GLS and MD here
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
