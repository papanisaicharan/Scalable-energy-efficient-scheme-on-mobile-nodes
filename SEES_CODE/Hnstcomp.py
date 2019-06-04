""" 
CODED BY : PAPANI SAICHARAN
this is can be done by looping also
"""
import pandas as pd
import matplotlib.pyplot as plt

f = pd.read_csv('HN2.csv')
print(f.shape)

columns_of_f = list(f)

f1 = pd.read_csv('HN3.csv')
print(f1.shape)

columns_of_f1 = list(f1)

f2 = pd.read_csv('HN4.csv')
print(f2.shape)

columns_of_f2 = list(f2)

f3 = pd.read_csv('HN1.csv')
print(f3.shape)

columns_of_f3 = list(f3)

f_ = pd.read_csv('HNmobile2.csv')
print(f_.shape)

columns_of_f_ = list(f_)

f_1 = pd.read_csv('HNmobile3.csv')
print(f_1.shape)

columns_of_f_1 = list(f_1)

f_3 = pd.read_csv('HNmobile1.csv')
print(f_3.shape)

columns_of_f_3 = list(f_3)

f_2 = pd.read_csv('HNmobile4.csv')
print(f_2.shape)

columns_of_f_2 = list(f_2)


for i in range(1,len(columns_of_f1)):
	x = f[columns_of_f1[0]].values.tolist()
	y = f[columns_of_f1[i]].values.tolist()
	x1 = f1[columns_of_f1[0]].values.tolist()
	y1= f1[columns_of_f1[i]].values.tolist()
	x2 = f2[columns_of_f1[0]].values.tolist()
	y2= f2[columns_of_f1[i]].values.tolist()
	plt.plot(y1,label="HN level 3")
	plt.plot(y,label="HN level 2")
	plt.plot(y2,label="HN level 4")
	x = f_[columns_of_f1[0]].values.tolist()
	y = f_[columns_of_f1[i]].values.tolist()
	x1 = f_1[columns_of_f1[0]].values.tolist()
	y1= f_1[columns_of_f1[i]].values.tolist()
	plt.plot(y1,label="HNmobile level 3")
	plt.plot(y,label="HNmobile level 2")
	x1 = f_2[columns_of_f1[0]].values.tolist()
	y1= f_2[columns_of_f1[i]].values.tolist()
	plt.plot(y1,label="HNmobile level 4")
	x = f3[columns_of_f1[0]].values.tolist()
	y = f3[columns_of_f1[i]].values.tolist()
	x1 = f_3[columns_of_f1[0]].values.tolist()
	y1= f_3[columns_of_f1[i]].values.tolist()
	plt.plot(y1,label="HNmobile level 1")
	plt.plot(y,label="HN level 1")	
	plt.xlabel(columns_of_f1[0], fontsize=10)
	plt.ylabel(columns_of_f1[i], fontsize=10)
	plt.legend()
	plt.show()