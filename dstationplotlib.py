# -*- coding: utf-8 -*-

# A set of packages used by the D-Station (https://gpdsifpb.github.io/D-Station/)
# to plot strain or strain rate curves and post process ThirdDiastoleTime


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
"""
def onclick(event):

	#print ("\nValue: Time = %f milliseconds"%(event.xdata*1000))
	if prmt != "8":
		xcoord.append(event.xdata*1000)
	else:
		times_IVA.append(event.xdata)
#Função para marcação dos pontos no ECG - FIM
"""


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
