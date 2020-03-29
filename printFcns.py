import numpy as np

def printValveTimes(valveTimes):
    
    auxPrintValves = np.array(['MVO', 'MVC', 'AVO', 'AVC'])
    print("\n\nValve Event Times:\n")
    for it1 in range(2):
        for it2 in range(4):
            print("\t", auxPrintValves[it2]+str(it1+1),": ", valveTimes[it1][it2]*1000, " ms", sep='')
#


def printPhaseTimes(phasesTimes):
    
    print("\n\nLeft Ventricle Phase Times:\n")
    auxPrintPhases = np.array(['EMC', 'IVC', 'Ejection Time', 'IVR', 'E', 'A'])
    for it in range(9):
        if it < 6:
            print("\t", auxPrintPhases[it],": ", phasesTimes[it]*1000, " ms", sep='')
        else:
            print("\t", auxPrintPhases[it-6]+'2',": ", phasesTimes[it]*1000, " ms", sep='')
#


def printLAPhaseTimes(LAphasesTimes):    
	auxPrintLAPhases = np.array(['Reservoir', 'Conduit', 'Atrial Contraction'])
	print("\n\nLeft Atrium Phase Times:\n")
	for it in range(3):
		print("\t", auxPrintLAPhases[it],": ", LAphasesTimes[it]*1000, " ms", sep='')
#