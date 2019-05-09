""" 
CODED BY : PAPANI SAICHARAN
"""
import pandas as pd
import matplotlib.pyplot as plt

f = pd.read_csv('node_energies2001(2).csv')
print(f.shape)

columns_of_f = list(f)

f1 = pd.read_csv('node_static.csv')
print(f1.shape)

columns_of_f1 = list(f1)

for i in range(1,len(columns_of_f)):
	x = f[columns_of_f[0]].values.tolist()
	y = f[columns_of_f[i]].values.tolist()
	plt.xlabel(columns_of_f[0])
	plt.ylabel(columns_of_f[i])
	plt.plot(x, y,color = 'b')
	x1 = f[columns_of_f1[0]].values.tolist()
	y1= f[columns_of_f1[i]].values.tolist()
	plt.plot(x1, y1,color = 'r')
	plt.show()