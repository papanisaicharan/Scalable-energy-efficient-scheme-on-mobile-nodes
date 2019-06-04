"""
this is the implementation of MSWE
"""
import copy
import math

def ZAS_selection(per1,Nalive,HNsalive):
	#print(pr1,Nalive,HNsalive)
	for_sort_on_Er = []
	for i in HNsalive:
		if i.get_iszag():
			for_sort_on_Er.append((i,i.get_e_residual()))
	for_sort_on_Er = sorted(for_sort_on_Er,key=lambda x: x[1],reverse=True)
	#print(per1 * Nalive)
	Nza = math.ceil(per1*Nalive)
	updated_nza = []
	for i in for_sort_on_Er:
		updated_nza.append(i[0])
	selected_zas = updated_nza[:Nza]
	# print("selected_zas : ",len(selected_zas))
	for i in selected_zas:
		i.set_as_zas()
	return selected_zas
	# list23= []
	# for i in HNsalive:
	#     list23.append((i.get_iszag(),i.get_iszas()))
	# print(list23)

def MSWE(Nalive,HNsalive,m,p,w,par1,k,per2,thzg):
	# print(k)
	""" Nalive,HNsalive,m,p,w,0.7,0.1,0.2,thzg
	Nalive : number of nodes alive in each zone
	HNsalive : list of laive node object in a zone
	m : number of parments considered for calculating scor of a noded
	p : set of paraments
	g : significances of parameters
	w : weights set
	par1 : it is percentage of Nalive
	per1 : percentage of ZAs selection
	per2 : percentage for ZAG election
	thzg : average of all alive nodes
	"""
	#print(per2 * Nalive)
	Nzg = 0
	for i in HNsalive:
		if i.get_iszag():
			Nzg = Nzg+1

	for i in HNsalive:
		if i.get_iszag():
			if i.get_e_residual() <= thzg:
				i.discard_zag()
				Nzg = Nzg-1

	if Nzg >= per2 * Nalive:
		return ZAS_selection(k,Nalive,HNsalive)

	for i in HNsalive:
		if i.get_iszag():
			i.discard_zag()

	# NEW ZAG ELECTION
	Hns1 = HNsalive[:]
	for r in range(0,m):
		Scj = []
		g = r
		while g>0:
			w[g],w[g-1] = w[g-1],w[g]
			g = g-1
		w = w[:m]+w[m:]
		for i in Hns1:
			parameterswithweights = 0
			parameterswithweights = parameterswithweights + (i.get_e_residual()*w[0])
			parameterswithweights = parameterswithweights +(i.centrality(HNsalive)*w[1])
			parameterswithweights = parameterswithweights +(i.distanceToNearestRelay()*w[2])
			Scj.append((i,parameterswithweights))
		Scj = sorted(Scj,key=lambda x: x[1],reverse=True)
		totalnodestonextround = math.ceil((len(Scj)*par1))
		updated_HNs = []
		for i in Scj:
			updated_HNs.append(i[0])
		Hns1 = updated_HNs[:totalnodestonextround]
		# print("(zone)next level : ",len(Hns1))
	for i in Hns1:
		i.set_as_zag()
	return ZAS_selection(k,Nalive,HNsalive)



