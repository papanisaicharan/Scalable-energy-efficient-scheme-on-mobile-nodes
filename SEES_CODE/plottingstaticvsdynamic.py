""" 
CODED BY : PAPANI SAICHARAN
"""
import pandas as pd
import matplotlib.pyplot as plt

f = pd.read_csv('HN2.csv')
print(f.shape)

columns_of_f = list(f)

f1 = pd.read_csv('HNmobile2.csv')
print(f1.shape)

columns_of_f1 = list(f1)


for i in range(1,len(columns_of_f1)):
	x = f[columns_of_f1[0]].values.tolist()
	y = f[columns_of_f1[i]].values.tolist()
	x1 = f1[columns_of_f1[0]].values.tolist()
	y1= f1[columns_of_f1[i]].values.tolist()
	plt.plot(y1,label="static nodes")
	plt.plot(y,label="mobile nodes")
	plt.xlabel(columns_of_f1[0], fontsize=10)
	plt.ylabel(columns_of_f1[i], fontsize=10)
	plt.legend()
	plt.show()