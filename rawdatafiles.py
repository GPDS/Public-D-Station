# -*- coding: utf-8 -*-

import pandas as pd              # Package used to work with the raw data files
import re                        # Used to obtain the LM, RM and ES Times in the raw data files
from os import listdir			 # Used to obtain the files in their directories
from os.path import isfile, join # Also used to do file operations



def openfiles(exams_path, op, test_op):     #Script to open the raw data files exported from proprietary software

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
    	if ('4CH_SL_TRACE' in f) or ('4CH_SL4CH STRAIN_TRACE' in f) or ('4CH_Peak dose_SL_TRACE' in f):
    		txt_original = open(exams_path+'/'+f, 'r')
    		numbers = re.findall("\d+\.\d+", txt_original.readlines()[2]) #Values are extracted from the line 3 of the txt file - LM_Time, ES_Time e RM_Time
    		txt_original.close()
    		LM_Time.append(float(numbers[0]))
    		RM_Time.append(float(numbers[1]))
    		ES_Time.append(float(numbers[2]))

    for f in list_txtfiles:
    	if ('2CH_SL_TRACE' in f) or ('2CH_SL2CH STRAIN_TRACE' in f) or ('2CH_Low dose_SL_TRACE' in f):
    		txt_original = open(exams_path+'/'+f, 'r')
    		numbers = re.findall("\d+\.\d+", txt_original.readlines()[2]) #Values are extracted from the line 3 of the txt file - LM_Time, ES_Time e RM_Time
    		txt_original.close()
    		LM_Time.append(float(numbers[0]))
    		RM_Time.append(float(numbers[1]))
    		ES_Time.append(float(numbers[2]))

    for f in list_txtfiles:
    	if ('APLAX_SL_TRACE' in f) or ('APLAX_SL3CH STRAIN_TRACE' in f) or ('APLAX_Low dose_SL_TRACE' in f):
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

    return txt1, txt2, txt3, txt_mid, strain_rate_lv4ch, LM_Time, RM_Time, ES_Time
