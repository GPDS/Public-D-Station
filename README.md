# Software for Post-Processing Analysis of Strain Curves: The D-Station


The D-Station is a custom and free application, developed using the Python 3 programming language and directed to the offline post processing of the heart strain curves.

The application’s inputs are: 

1) the opening and closing times of the aortic and mitral valves; 

2) the raw data files containing the Strain or Strain Rate curves; 

3) the Patient ID;

4) the option of visualization selected by the user.

#

In the current version of the software, six output options are available to the users:

* Strain - LV (Left Ventricle), Strain Rate - LV and ECG;

* Strain - LV, Strain - LA (Left Atrium) and ECG; 

* Strain - LV, Strain Rate - LA and ECG; 

* Strain - LV, Strain - RV (Right Ventricle) and ECG; 

* Strain - LV, Strain Rate - LV and ECG, in which the Strain Rate is obtained from the Strain curves;

* Test Option (to use with CircAdapt): Strain - LV and Strain Rate - LV.



### Packages

In order to run the application you will need the following packages for Python 3 (tested in Python 3.8.3 64-bit):

 - [Pandas](https://pandas.pydata.org/) 
 - [numpy](http://www.numpy.org/)
 - [matplotlib](https://matplotlib.org/)
 - [openpyxl](https://pypi.org/project/openpyxl/)
 - [numpy](http://www.numpy.org/)


### Usage 


To run the application the following criteria need to be met:

* The text files containing the strain/strain rate curves of at least the LV (2CH, 4CH and APLAX/3CH) should be in the directory Patients, if they are from real patients or, or Simulations, if they are CircAdapt simulations.

* The valve event times (Mitral Valve Opening, Mitral Valve Closing, Aortic Valve Opening and Aortic Valve Closing) should be in the spreadsheet (Patients_DB.xlsx), where the IdPatient must have the same name as the directory in which the text files are stored.

To help new users, a few examples are already available in this repository. Use the instructions above to register new patients.


### Running the application

When you run the D-Station, the application starts asking the user to type the Patient ID, that is, the name of the directory containing the text files with the curves. After that, the user must input one of the output options presented in the description section and in the console of the application. It is important to emphasise that **simulations only work with the test option**. After selecting the option, if it is not a simulation, the user must select in the ECG plot the **Onset of the QRS complex 1, Onset of the P-Wave and the Onset of the QRS complex 2**. The parameters will all be calculated and printed in the console. The user can then select an option to view more details about those parameters. 


### Parameters

* Global Longitudinal Strain **(validated considering peak systolic strain as the most negative points during systole)**:  Mean value of the peak systolic strain. 

* Mechanical Dispersion **(to be validated)**: Standard deviation of the time values of the peak strain points, considering the peak as the most negative points in the whole cycle.



### Authors

 - Rafael D. de Sousa
	 - Student/Reseacher/Developer
	 - IFPB - Campus João Pessoa 

 - Ittalo S. Silva 
	 - Student/Reseacher/Developer
	 - IFPB - Campus João Pessoa 

 - José Raimundo Barbosa
	 - Student/Reseacher/Developer
	 - IFPB - Campus João Pessoa 
	 
 - Carlos Danilo M. Regis
	 - Professor Advisor
	 - IFPB - Campus João Pessoa 
	 
 - Paulo Szewierenko 
	 - Statistical Consultant
	 
 - Renato A. Hortegal
	 - Cardiologist/Advisor
	 - Beneficência Portuguesa Hospital of São Paulo/Dante Pazzanese Institute of Cardiology




### Main References

For more references check the related paper: https://doi.org/10.36660/abc.20180403  

1.  D’hooge J, Bijnens B, Thoen J, Van de Werf F, Sutherland GR and Suetens P.
Echocardiographic Strain and Strain-Rate Imaging: A New Tool to Study Regional Myocardial Function. IEEE Trans Med Imaging. 2002 Sep;21(9):1022–30.

2.  Voigt JU, Pedrizzetti G, Lysyansky P, Marwick TH, Houle H, Baumann R, et al. Definitions for a common standard for 2D speckle tracking echocardiography: consensus document of the EACVI/ASE/Industry Task Force to standardize deformation imaging. Eur Heart J Cardiovasc Imaging. 2015 Jan; 16(1):1–11.

3.  Walmsley J, Arts T, Derval N, Bordachar P, Cochet H, Ploux S, et al. Fast Simulation of Mechanical Heterogeneity in the Electrically Asynchronous Heart Using the MultiPatch Module.PLoS Comput Biol. 2015 Jul; 11(7): e1004284.
