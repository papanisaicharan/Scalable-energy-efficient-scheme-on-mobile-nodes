import pandas as pd
import matplotlib.pyplot as plt

f = pd.read_csv('node_energies.csv')
print(f.shape)

columns_of_f = list(f)

for i in range(1,len(columns_of_f)):
	x = f[columns_of_f[0]].values.tolist()
	y = f[columns_of_f[i]].values.tolist()
	plt.xlabel(columns_of_f[0])
	plt.ylabel(columns_of_f[i])
	plt.plot(x, y)
	plt.show()