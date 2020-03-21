# -*- coding: utf-8 -*-

import pandas as pd
from os import listdir			 # Used to obtain the files in their directories
from os.path import isfile, join # Also used to do file operations

#Function to read only the first N columns of a dataframe
def front(self, n):
	return self.iloc[:, :n]

pd.DataFrame.front = front


#
def segmentName(segmentColor, chamber):

	if chamber == '2CH':

		if 'RED' in segmentColor:
			return "Red - Basal Anterior"

		elif 'BLUE' in segmentColor:
			return "Blue - Medium Anterior"

		elif 'MAGENTA' in segmentColor:
			return "Magenta - Apical Anterior"

		elif 'GREEN' in segmentColor:
			return "Green - Apical Inferior"

		elif 'CYAN' in segmentColor:
			return "Cyan - Medium Inferior"

		elif 'YELLOW' in segmentColor:
			return "Yellow - Basal Inferior"

		else:
			return "\nERROR - Color could not be identified\n"

	elif chamber == '4CH':

		if 'RED' in segmentColor:
			return "Red - Basal Anterolateral"

		elif 'BLUE' in segmentColor:
			return "Blue - Medium Anterolateral"

		elif 'MAGENTA' in segmentColor:
			return "Magenta - Apical Anterolateral"

		elif 'GREEN' in segmentColor:
			return "Green -Apical Inferoseptal"

		elif 'CYAN' in segmentColor:
			return "Cyan - Medium Inferoseptal"

		elif 'YELLOW' in segmentColor:
			return "Yellow - Basal Inferoseptal"

		else:
			return "\nERROR - Color could not be identified\n"

	elif chamber == 'APLAX':

		if 'RED' in segmentColor:
			return "Red - Basal Anteroseptal"

		elif 'BLUE' in segmentColor:
			return "Blue - Medium Anteroseptal"

		elif 'MAGENTA' in segmentColor:
			return "Magenta - Apical Anteroseptal"

		elif 'GREEN' in segmentColor:
			return "Green - Apical Inferolateral"

		elif 'CYAN' in segmentColor:
			return "Cyan - Medium Inferolateral"

		elif 'YELLOW' in segmentColor:
			return "Yellow - Basal Inferolateral"

		else:
			return "\nERROR - Color could not be identified\n"

	else:
		return "\nERROR - Vision could not be identified\n"



def openRawData(exams_path, heartChamber, strainType, visualization):

	
	exam = '_not_found_'
	try:
		#Lists the txt files in the directory pointed by exams_path
		list_txtfiles = [f for f in listdir(exams_path+'/'+heartChamber) if isfile(join(exams_path+'/'+heartChamber, f))] 
		for f in list_txtfiles:
			if(visualization in f and strainType in f):
				exam = f
			
		txt=pd.read_csv(exams_path+'/'+heartChamber+'/'+exam, sep='\t', engine='python', skiprows=3, index_col=0)
		return txt

	except FileNotFoundError:
		print(heartChamber, " ", visualization," file not found in the ", exams_path,"/", heartChamber,"/\' directory.", sep='')