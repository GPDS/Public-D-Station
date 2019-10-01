# Software - Análise Curvas de Deformação Cardíaca

### Descrição

A análise da deformação cardíaca pela técnica de Speckle Tracking[1] tem se mostrado de grande aplicabilidade em diversos cenários, tanto da prática cardiológica[1]  quanto no âmbito da pesquisa clínica[2], uma vez que torna possível avaliar em detalhe a mecânica das câmaras do coração a níveis regional e global. Porém, o emprego de ferramentas para processamento offline dos sinais fornecidos pelo Speckle Tracking tornaram-se imprescindíveis para aplicações mais amplas desta tecnologia no âmbito da pesquisa clínica. Enquanto o acesso às estações de pós processamento, no entanto, é limitado à certas regiões em função das dimensões do país e pelo seu alto custo. Ademais, fabricantes desses equipamentos impõem padrões específicos de análise para suas workstations, gerando limitações de análise, bem como discrepâncias na mensuração dos diferentes parâmetros.

É comum que, centros internacionais de referência no estudo da deformação cardíaca, tenham softwares livres customizados para a realização do processamento offline sem as limitações impostas pelos fabricantes, permitindo que sejam adaptados com base nas necessidades de suas pesquisas. No Brasil, entretanto, não há registro na literatura de centros que possuem tais softwares livres.

O presente trabalho visa apresentar e pré-validar um novo software, para uso livre, que denominamos D-station, para análise das curvas de deformação cardíaca fornecidas por qualquer software proprietário de análise offline. Para isso, a solução proposta torna possível apresentar e validar o D-station para avaliação de curvas de deformação cardíaca que, a partir destes sinais, possibilite o cálculo de parâmetros de diferentes softwares de processamento offline de curvas de deformação, com a vantagem de ser gratuito e ter código livre. Sua validação será feita por comparação entre parâmetros obtidos com o D-station e o software EchoPAC(GE).


### Dependências

Para o funcionamento correto do software são necessárias a instalações das seguintes ferramentas:


 - [Python 3](https://www.python.org/downloads/)
 - [Panda](https://pandas.pydata.org/) 
 - [numpy](http://www.numpy.org/)
 - [matplotlib](https://matplotlib.org/)
 - [openpyxl](https://pypi.org/project/openpyxl/)
 - [numpy](http://www.numpy.org/)


### Instruções de uso

  
Para o funcionamento do programa são necessárias as seguintes condições:

Os arquivos .txt devem estar numa pasta contida na pasta Patients, caso sejam de pacientes reais, ou numa pasta contida em Simulations, caso sejam simulações provenientes do CircAdapt, de forma semelhante aos arquivos de exemplo.

Os tempos de abertura e fechamento das valvas devem estar no arquivo Event_Timing.

Executando o arquivo D-Station, o programa inicia-se pedindo para que seja inserido o Patient ID, isto é, o nome da pasta que contém os exames (e.g. Aristoteles). O usuário deve então escolher uma das opções de visualização oferecidas (simulações funcionam apenas com a Test Option) e marcar os seguintes pontos: QRS 1 Onset, P Onset, QRS 2 Onset e serão exibidos então os tempos de início de cada fase, caso seja um paciente real. Por fim o usuário pode escolher o parâmetro que deseja visualizar.


### Publicações 




### Autores

 - Rafael D. de Sousa
	 - IFPB - João Pessoa 
	 - Aluno: pesquisador e desenvolvedor

 - Ittalo S. Silva 
	  - IFPB - João Pessoa 
	 - Aluno: pesquisador e desenvolvedor
	 
 - Carlos Danilo M. Regis
	 - Professor Orientador
	 - IFPB - João Pessoa 
	 
 - Paulo Szewierenko 
	 - Professor Orientador
	 - Instituto Tecnológico de Aeronáutica - São José dos Campos - SP
	 
 - Renato A. Hortegal
	 - Professor Orientador
	 - Instituto Dante Pazzanese de Cardiologia - SP

 - José Raimundo Barbosa
	 -	IFPB - João Pessoa 
	 - Aluno: desenvolvedor suporte.


### Referências

1.  Almeida ALC, Gjesdal O, Newton N, Choi EY, Tura-Teixido G, Yoneyama K, et al. Speckle-Tracking pela ecocardiografia bidimensional: aplicações clínicas. Rev bras ecocardiogr imagem cardiovasc. 2013 Jan-Mar;26(1):38-49.
    
2.  Haugaa KH, Grenne BL, Eek CH, Ersbøll M, Valeur Nana, Svendsen JH, et al. Strain Echocardiography Improves Risk Prediction of Ventricular Arrhythmias After Myocardial Infarction. JACC Cardiovasc Imaging. 2013 Aug, 6(8):841-50.
    
3.  Mentz RJ, Khouri MG. Longitudinal Strain in Heart Failure With Preserved  
    Ejection Fraction: Is There a Role for Prognostication? Circulation. 2015 Aug  
    4;132(5):368-70.
