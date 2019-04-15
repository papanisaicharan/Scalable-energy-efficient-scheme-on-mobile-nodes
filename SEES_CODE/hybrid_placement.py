""" 

This is a hybrid placement algorithm(offline mode)
"""

from sympy.solvers import solve
from sympy import Symbol
#this is testing plot
from matplotlib import pyplot as plt
from matplotlib.ticker import MultipleLocator
import numpy as np
import math
import random
import Node as nd
import EH_relay as relay_nd
import LBS as L_B_S
import Zone as zone
import Network as nw

def getpoints(startx,starty,endx,endy,id):
    rangeX = (startx,endx)
    rangeY = (starty,endy)
    randPoints = []
    excluded = set()
    i = 0
    while i<D:
        x = random.randrange(*rangeX)
        y = random.randrange(*rangeY)
        if (x,y) in excluded: continue
        randPoints.append((x,y))
        i += 1
        excluded.update((x, y))
        
    secure_random = random.SystemRandom()
    nodeswithenergy = []#(x,y),energy,id
    for j in range(len(nodesinlevel)):
        for i in range(nodesinlevel[j]):
            list1 = []
            list1.append(secure_random.choice(randPoints))
            randPoints.remove(list1[0])
            list1.append(Et[j])
            list1.append(id)
            list1.append(j+1)
            id = id+1
            nodeswithenergy.append(list1)
    return(nodeswithenergy)

def get_rand_uniform_points_LBS(x1,x2,y1,y2):
    final_list = []
    t1 = []
    t2 = []
    t1.append(random.randint(x1,x2))
    t2.append(random.randint(y1,y2))
    for i in range(no_lbs_on_each_side-1):
        p1 = random.randint(x1,x2)
        p2 = random.randint(y1,y2)
        while check_validation(t1,t2,p1,p2):
            p1 = random.randint(x1,x2)
            p2 = random.randint(y1,y2)
        t1.append(p1)
        t2.append(p2)
    final_list.append(t1)
    final_list.append(t2)
    return final_list

def euclidean_distance(x1,y1,x2,y2):
    distance = math.sqrt(math.pow(x2 - x1, 2) +  math.pow(y2 - y1, 2) ) 
    return distance

def check_validation(t1,t2,p1,p2):
    all_distances = []
    for i in range(len(t1)):
        all_distances.append(euclidean_distance(p1,p2,t1[i],t2[i]))
    for i in all_distances:
        if i < distance_btw_lbs:
            return True
    return False

#taking inputs,parameters setting
N = 2000#int(input("Enter N( the total number of HN nodes) : "))
Fs = 20#int(input("Enter Fs() : "))
L = 200#int(input("Enter L(length of area) : "))
B = 12#int(input("Enter B(LBS) : "))
n = 2#int(input("Enter n(number of heterogeneity level) : "))

#taking constants
alpha = 2#float(input("Enter alpha : "))#singh has taken this as 0.5
#beta = input("Enter beta")
gamma = 0.4#float(input("Enter gamma : "))#intial gamma will be given
theta = 0.025#float(input("Enter theta : "))#should validate a equation

Einti = 0.5#float(input("Enter E1(initial energy) : "))

#we need to validate theta and gamma values and find beta constant
if((gamma /  (2*(n-1)) ) > theta):
	print("validated theta and gamma values")
	# finding gamma values
	gammavalues = [gamma]
	#getting gamma values,this is done according to singh model
	for i in range(1,n+1):
	    #gammai = gammai-1 - 2*theta
	    gammavalues.append(round(gammavalues[i-1] - 2*theta,3))
	    
	print("gamma-values : ",gammavalues)
	#number of nodes in each level
	beta = gammavalues[len(gammavalues)-1]
	lastgamma = beta
	gammavalues[:] = gammavalues[:len(gammavalues)-1]

	print("gamma-values : ",gammavalues)
	#https://docs.sympy.org/latest/modules/solvers/solvers.html#systems-of-polynomial-equations
	beta = Symbol('x',positive=True)
	f =1
	for i in range(n-1,-1,-1):
	    f = f*(beta-gammavalues[i])
	    f= f+1

	f = f-2
	print("equation used for solving beta: ",f)
	beta = solve(f, beta)
	print("positive beta value: ",beta)
	Nt = [] #indicate cardinality of n categories
	Et = [] #indicate Energy of n categories
	EnergySinghTotal = []

	for i in range(1,n+1):
	    # we compute Nit and Eit and append them to Nt and Et,formulea are shown below
	    #(Einti * (1 + ((i − 1) * alpha)))
	    et = i-1
	    et = et*alpha
	    et = et+1
	    et = et*Einti
	    Et.append(et)
	    #Nit = N × (beta − gamma1) × (beta − gamma2) × (beta − gamma3)×⋯× (beta − gammai)
	    nt = N
	    for j in range(0,i):
	        nt = nt *(beta[0] - gammavalues[j])
	    Nt.append(nt)

	# print("enregy of each HN type : ",Et)
	# print("total number of HN nodes in each level : ",Nt)

	Nt1 = [round(Nt[i],1) for i in range(len(Nt))]
	for i in range(len(Nt1)):
	    if (Nt1[i]-int(Nt1[i])) >= 0.5:
	        Nt1[i] = math.ceil(Nt1[i])
	    else:
	        Nt1[i] = math.floor(Nt1[i])
	        
	# print("rounded total number of HN nodes in each level : ",Nt1)
	total_energy_of_all_nodes = 0.0
	Nt[:] = Nt1[:]
	for i in range(len(Nt1)):
	    print("Nodes in level - ",i+1," = ",Nt[i] ," , Energy = ",Et[i])
	    total_energy_of_all_nodes +=Nt[i]*Et[i]
	# print("rounded total number of HN nodes in each level : ",Nt)
	#checking
	sum1 = 0
	for i in Nt:
	    sum1=sum1+i
	if N == sum1:
	    print("sum of nodes in all the level is equal to N ")
	else:
	    print("sum of nodes in all the level is not equal to N,Something went wrong ")
	#for sake of solving
	# print(Nt)
	for i in range(len(Nt)):
	    Nt[i] = float(Nt[i]/100)
	    #print(Nt[i])
	    if (Nt[i] - int(Nt[i])) >= 0.5:
	        Nt[i] = math.ceil(Nt[i])*100
	    else:
	        Nt[i] = math.floor(Nt[i])*100
	        
	print("rounded total number of HN nodes in each level : ",Nt)
	Z = math.pow(math.ceil(math.sqrt(N)/math.sqrt(Fs)),2)
	print("number of zones : ",Z)#number of zones
	Nz = []
	for z in range(1,int(Z)+1):
	    if z==1:
	        Nz.append(math.ceil(N/Z))
	    else:
	        k = 0
	        for i in Nz:
	            k = k + i
	            
	        Nz.append(math.ceil((N - k)/(Z - z + 1)))
	        
	print("number of nodes in each zones : ",Nz)

	rsmax = []#node sensing
	rcmax = []#communication ranges

	for i in range(0,int(Z)):
	    rsmax.append(  (L/math.sqrt(int(Z)  ))  *     math.sqrt(2)      )
	    rcmax.append( (L/math.sqrt(int(Z)))*math.sqrt(2)*2)

	# print("sensing range",rsmax,"             communication range   ",rcmax)
	R = int(math.pow( math.sqrt(int(Z))+1 , 2 ))
	print("number of relay nodes : ",R)
	D = int(L/math.sqrt(Z))
	print("length of working area : ",D)

	nodesinlevel = []
	for i in range(len(Nt)):
	    nodesinlevel.append(int(Nt[i]/int(Z)))

	zones_objects = [] # all nodes objects
	object_of_zones = [] # each element in this represent a zone object
	for i in range(0,int(math.sqrt(int(Z)))):
		for j in range(0,int(math.sqrt(int(Z)))):
			np = []
			for p in getpoints(j*20,i*20,(j+1)*20,(i+1)*20,j*20+1+200*i):
				np.append(nd.Node(p[0][0],p[0][1],p[1],p[2],p[3],i*10+j+1))
			zones_objects.extend(np)
			object_of_zones.append(zone.Zone(i*10+j+1,np))
	

	# for i in zones_objects:
	# 	print(i.getlocation(),i.get_node_id(),i.get_e_initial())
	#for each corner place a EH node
	EH = []
	count = 1
	for i in range(0,L+1,20):
		for j in range(0,L+1,20):
		    if count <= R: 
		    	EH.append(relay_nd.EH_relay(i,j,count))
		    	count+=1

	EHx = []
	EHy = []
	for j in EH:
	    EHx.append(j.getlocation()[0])
	    EHy.append(j.getlocation()[1])
	# print(EHx,EHy)

	x = [[] for i in range(len(Et))]
	y = [[] for i in range(len(Et))]

	for i in zones_objects:
	    for k in range(len(Et)):
	        if Et[k] == i.get_e_initial():
	            x[k].append(i.getlocation()[0])
	            y[k].append(i.getlocation()[1])

	# we will definately start plotting form (0,0), so
	# we can place base stations from 20 to 50 distance from working area uniformly so as to cover all the nodes
	dist_lbs = int(input("Enter the distance of LBS from working area : "))
	perimneter_lbs = (L+2*dist_lbs)*4
	distance_btw_lbs = int(perimneter_lbs/B)

	left = [(-dist_lbs, i) for i in range(-dist_lbs, L+2*dist_lbs+1,distance_btw_lbs )]
	top = [(i,L+dist_lbs ) for i in range(-dist_lbs+distance_btw_lbs,L+2*dist_lbs+1, distance_btw_lbs)]
	right = [(L+dist_lbs, i) for i in range(L+dist_lbs-distance_btw_lbs, -dist_lbs-1, -distance_btw_lbs)]
	bottom = [(i, -dist_lbs) for i in range(L+dist_lbs-distance_btw_lbs, -dist_lbs, -distance_btw_lbs)]
	idx = left+top+right+bottom
	#local base station objects
	local_bs = []
	count = 1
	for i in idx:
		local_bs.append(L_B_S.LBS(i[0],i[1],count))
		count+=1

	# network formation
	network = nw.Network(object_of_zones,EH,local_bs)

	#print(x,y)
	fig = plt.figure()#defining size
	fig.set_size_inches(100,100)
	ax1 = fig.add_subplot(1,1,1)#adding a plot to figure

	spacing = D # This can be your user specified spacing. 
	minorLocator = MultipleLocator(spacing)
	# jet = plt.get_cmap('jet')
	# colors = iter(jet(np.linspace(0,1,10)))
	colors = ['g','r','c','m','y','k','b']
	for i in range(0,len(x),1):
	    ax1.plot(x[i],y[i], 'o',color = colors[i])

	HN_ids = []
	for i in zones_objects:
		HN_ids.append(i.get_node_id())
	# print(HN_ids)

	for i, txt in enumerate(HN_ids):
		ax1.annotate(txt, (zones_objects[i].getlocation()[0],zones_objects[i].getlocation()[1]))

	ax1.plot(EHx,EHy, 'D',color = colors[len(colors)-1],markersize=12)

	EH_ids = []
	for i in EH:
		EH_ids.append(i.get_node_id())
	# print(EH_ids)

	for i, txt in enumerate(EH_ids):
		ax1.annotate(txt, (EH[i].getlocation()[0],EH[i].getlocation()[1]))

	x = [-50, -50, -20, -20]
	y = [-50, L+50, L+50, -50]
	ax1.fill(x,y,'y')
	x = [ -20,L+50,L+50 ,-20]
	y = [ L+50,L+50,L+20 ,L+20]
	ax1.fill(x,y,'y')
	x = [ L+50,L+50,L+20 ,L+20]
	y = [ L+50,-50 ,-50,L+50]
	ax1.fill(x,y,'y')
	x = [ -20,-20,L+20 ,L+20]
	y = [ -50,-20 ,-20,-50]
	ax1.fill(x,y,'y')
	for i in local_bs:
		# print(i.get_node_id())
		ax1.plot(i.getlocation()[0],i.getlocation()[1], 'D',color = colors[1],markersize=20)

	LB_ids = []
	for i in local_bs:
		LB_ids.append(i.get_node_id())
	# print(LB_ids)

	for i, txt in enumerate(LB_ids):
		ax1.annotate(txt, (local_bs[i].getlocation()[0],local_bs[i].getlocation()[1]))


	# Set minor tick locations.
	ax1.yaxis.set_minor_locator(minorLocator)
	ax1.xaxis.set_minor_locator(minorLocator)

	plt.axis([-60, L+60, -60, L+60])#defining axix x and y
	# Set grid to use minor tick locations. 

	ax1.grid(which = 'minor')#only major works fine

	plt.show()
	
else:
    print("error in input values")