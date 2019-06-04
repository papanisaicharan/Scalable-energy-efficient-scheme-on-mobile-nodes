""" 

This is a hybrid placement algorithm(offline mode)
"""

from sympy.solvers import solve
from sympy import Symbol
#this is testing plot
from matplotlib import pyplot as plt
from matplotlib.ticker import MultipleLocator
import math
import random
import Node as nd
import EH_relay as relay_nd
import LBS as L_B_S
import Zone as zone
import Network as nw
import math
PI = math.pi
import MSWE as mswe
import MCCT as mcct
import time
from random import randint
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np


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

# --------------------------------------------- inputs  ----------------------------------------------------#
# taking inputs,parameters setting
N = 2000#int(input("Enter N( the total number of HN nodes) : "))
Fs = 20#int(input("Enter Fs() : "))
L = 200#int(input("Enter L(length of area) : "))
B = 12#int(input("Enter B(LBS) : "))
n = int(input("Enter n(number of heterogeneity level) : "))

#taking constants
alpha = 2#float(input("Enter alpha : "))#singh has taken this as 0.5
#beta = input("Enter beta")
gamma = 0.4#float(input("Enter gamma : "))#intial gamma will be given
theta = 0.025#float(input("Enter theta : "))#should validate a equation

Einti = 0.5#float(input("Enter E1(initial energy) : "))
# --------------------------------------------- end  ----------------------------------------------------#

# --------------------   we need to validate theta and gamma values and find beta constant --------------#
if((gamma /  (2*(n-1)) ) > theta):
	print("validated theta and gamma values")
	# finding gamma values
	# --------------------------------------------- gamma values  ----------------------------------------#
	gammavalues = [gamma]
	# getting gamma values,this is done according to singh model
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
	# --------------------------------------------- finished  -------------------------------------------#

	# --------------------------------------------- solving for beta  -----------------------------------#
	beta = Symbol('x',positive=True)
	f =1
	for i in range(n-1,-1,-1):
	    f = f*(beta-gammavalues[i])
	    f= f+1

	f = f-2
	print("equation used for solving beta: ",f)
	beta = solve(f, beta)
	print("positive beta value: ",beta)
	# --------------------------------------------- finished  -----------------------------------#

	# --------------------------------------------- finding cardinality,energy   ------------------------#
	Nt = [] #indicate cardinality of n categories
	Et = [] #indicate Energy of n categories

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

	Nt1 = [round(Nt[i],1) for i in range(len(Nt))]
	for i in range(len(Nt1)):
	    if (Nt1[i]-int(Nt1[i])) >= 0.5:
	        Nt1[i] = math.ceil(Nt1[i])
	    else:
	        Nt1[i] = math.floor(Nt1[i])
	        
	# print("rounded total number of HN nodes in each level : ",Nt1)
	Nt[:] = Nt1[:]
	for i in range(len(Nt1)):
	    print("Nodes in level - ",i+1," = ",Nt[i] ," , Energy = ",Et[i])
	# -----------------------------------------    finished    -----------------------------------------#
	# print("rounded total number of HN nodes in each level : ",Nt)
	#checking
	# ----------------------------------------      checking   -----------------------------------------#
	sum1 = 0
	for i in Nt:
	    sum1=sum1+i
	if N == sum1:
	    print("sum of nodes in all the level is equal to N ")
	else:
	    print("sum of nodes in all the level is not equal to N,Something went wrong ")
	#for sake of solving
	# print(Nt)
	# ----------------------------------------      finished     -----------------------------------------#
	# ----------------------------------------      rounding     -----------------------------------------#
	for i in range(len(Nt)):
	    Nt[i] = float(Nt[i]/100)
	    #print(Nt[i])
	    if (Nt[i] - int(Nt[i])) >= 0.5:
	        Nt[i] = math.ceil(Nt[i])*100
	    else:
	        Nt[i] = math.floor(Nt[i])*100
	print("rounded total number of HN nodes in each level : ",Nt)

	# ----------------------------------------      finished      -----------------------------------------#
	# ----------------------------------------      total energy    -----------------------------------------#
	total_energy_of_all_nodes = 0.0
	for i in range(len(Nt)):
		total_energy_of_all_nodes += Nt[i]*Et[i]
	# ----------------------------------------        finished    -----------------------------------------#
	# -----------------------------    number of nodes in a zone,count of zones -------------------------------#
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
	# --------------------------- -------------   finished    ----------------------------------------------#

	# ---------------------------  node sensing and communication ranges  -----------------------------------#

	rsmax = []#node sensing
	rcmax = []#communication ranges

	for i in range(0,int(Z)):
	    rsmax.append(  (L/math.sqrt(int(Z)  ))  *     math.sqrt(2)      )
	    rcmax.append( (L/math.sqrt(int(Z)))*math.sqrt(2)*2)

	# print("sensing range",rsmax,"             communication range   ",rcmax)
	# ------------------------------------------ finished --------------------------------------------------#

	# --------------------- number of relay nodesand length of zone square  -------------------------------#
	R = int(math.pow( math.sqrt(int(Z))+1 , 2 ))
	print("number of relay nodes : ",R)
	D = int(L/math.sqrt(Z))
	print("length of working area : ",D)

	# ---------------- end of number of relay nodesand length of zone square  -------------------------------#

	nodesinlevel = []
	for i in range(len(Nt)):
	    nodesinlevel.append(int(Nt[i]/int(Z)))

	# --------------------------- -------------creating zones and nodes    ------------------------------------#
	zones_objects = [] # all nodes objects
	object_of_zones = [] # each element in this represent a zone object
	for i in range(0,int(math.sqrt(int(Z)))):
		for j in range(0,int(math.sqrt(int(Z)))):
			np = []
			for p in getpoints(j*D,i*D,(j+1)*D,(i+1)*D,j*D+1+D*int(math.sqrt(int(Z)))*i):
				np.append(nd.Node(p[0][0],p[0][1],p[1],p[2],p[3],i*int(math.sqrt(int(Z)))+j+1))
			zones_objects.extend(np)
			object_of_zones.append(zone.Zone(i*int(math.sqrt(int(Z)))+j+1,np,(j*D,i*D)))
	# --------------------------- -------------   finished    ----------------------------------------------#
	# --------------------------- -------------   EH node    ----------------------------------------------#
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
	# --------------------------- -------------   finished    ----------------------------------------------#
	# print(EHx,EHy)

	# --------------------------- get coordinates of nodes of each level    ---------------------------------#
	x = [[] for i in range(len(Et))]
	y = [[] for i in range(len(Et))]

	for i in zones_objects:
	    for k in range(len(Et)):
	        if Et[k] == i.get_e_initial():
	            x[k].append(i.getlocation()[0])
	            y[k].append(i.getlocation()[1])

	# --------------------------- -------------   finished    ----------------------------------------------#

	# --------------------------- -------------   LBS and their coordinates   ------------------------------#

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

	# --------------------------- -------------   finished    ----------------------------------------------#

	# --------------------------- -------------   Network formation   --------------------------------------#

	# network formation
	network = nw.Network(object_of_zones,EH,local_bs)

	# --------------------------- -------------   finished    ----------------------------------------------#

	# --------------------------- ------ initial plotting    ----------------------------------------------#
	fig = plt.figure()#defining size
	fig.set_size_inches(100,100)
	ax1 = fig.add_subplot(1,1,1)#adding a plot to figure

	spacing = D # This can be your user specified spacing. 
	minorLocator = MultipleLocator(spacing)
	# jet = plt.get_cmap('jet')
	# colors = iter(jet(np.linspace(0,1,10)))
	# --------------------------- --   plotting nodes   ----------------------------------------------#
	colors = ['g','r','c','m','y','k','b']
	for i in range(0,len(x),1):
	    ax1.plot(x[i],y[i], 'o',color = colors[i])
	
	HN_ids = []
	for i in zones_objects:
		HN_ids.append(i.get_node_id())

	for i, txt in enumerate(HN_ids):
		ax1.annotate(txt, (zones_objects[i].getlocation()[0],zones_objects[i].getlocation()[1]))
	# --------------------------- ----  plotting finished    ----------------------------------------------#

	# --------------------------- ----  plotting relays    ----------------------------------------------#
	ax1.plot(EHx,EHy, 'D',color = colors[len(colors)-1],markersize=12)

	EH_ids = []
	for i in EH:
		EH_ids.append(i.get_node_id())
	# print(EH_ids)

	for i, txt in enumerate(EH_ids):
		ax1.annotate(txt, (EH[i].getlocation()[0],EH[i].getlocation()[1]))
	# --------------------------- ----  plotting finished    ----------------------------------------------#
	# --------------------------- ----  plotting LBS area and lbs  ----------------------------------------#
	x11 = [-50, -50, -20, -20]
	y11 = [-50, L+50, L+50, -50]
	ax1.fill(x11,y11,'y')
	x22 = [ -20,L+50,L+50 ,-20]
	y22 = [ L+50,L+50,L+20 ,L+20]
	ax1.fill(x22,y22,'y')
	x33 = [ L+50,L+50,L+20 ,L+20]
	y33 = [ L+50,-50 ,-50,L+50]
	ax1.fill(x33,y33,'y')
	x44 = [ -20,-20,L+20 ,L+20]
	y44 = [ -50,-20 ,-20,-50]
	ax1.fill(x44,y44,'y')
	for i in local_bs:
		# print(i.get_node_id())
		ax1.plot(i.getlocation()[0],i.getlocation()[1], 'D',color = colors[1],markersize=20)

	LB_ids = []
	for i in local_bs:
		LB_ids.append(i.get_node_id())
	# print(LB_ids)

	for i, txt in enumerate(LB_ids):
		ax1.annotate(txt, (local_bs[i].getlocation()[0],local_bs[i].getlocation()[1]))
	# --------------------------- ----  plotting finished    ----------------------------------------------#


	# Set minor tick locations.
	ax1.yaxis.set_minor_locator(minorLocator)
	ax1.xaxis.set_minor_locator(minorLocator)

	plt.axis([-60, L+60, -60, L+60])#defining axix x and y
	# Set grid to use minor tick locations. 

	ax1.grid(which = 'minor')#only major works fine

	plt.show()
	# --------------------------- ----  plotting finished    ----------------------------------------------#
else:
    print("error in input values")
    exit()

# --------------------------------  distanceToNearestRelay   ----------------------------------------------#
def distanceToNearestRelay(points,p):
    distance=[] 
    for i in points:
        #calculate the euclidean distance of p from training points  
        euclidean_distance = math.sqrt((i.getlocation()[0]-p.getlocation()[0])**2 +(i.getlocation()[1]-p.getlocation()[1])**2) 
  
        # Add a touple of form (distance,group) in the distance list 
        distance.append((i,euclidean_distance)) 
    # sort the distance list in ascending order 
    # and select first k distances 
    distance = sorted(distance,key=lambda x: x[1]) 
    # print(distance)
    return(distance[0])

# --------------------------------        inputs         ----------------------------------------------#
𝜇 = 0.8#float(input("Enter the 𝜇 value"))
m = 3#int(input("Enter m value"))# number of stages
cutofZag = 0.7#float(input("Enter the cut of Zag =  "))
# --------------------------------  end of inputs         ----------------------------------------------#

# -----------------------------   finding  nearest relay nodes   --------------------------------------#
for i in zones_objects:
	nearest_relay = distanceToNearestRelay(EH,i) #(relay_object,distance_to_nearest_relay)
	i.get_info_relay(nearest_relay[0],nearest_relay[1])
	nearest_relay[0].register_near_node(i,nearest_relay[1])
# --------------------------------      finished  ------------------------------------#
# --------------------------------      finding  nearest lbs nodes  ------------------------------------#
for i in EH:
	nearest_bs = distanceToNearestRelay(local_bs,i)
	i.get_info_bs(nearest_bs[0],nearest_bs[1])
	nearest_bs[0].register_near_relay(i,nearest_bs[1])
# --------------------------------      finished  ------------------------------------#

# --------------------------------nodes under each lbs registration  ------------------------------------#
zones_in_each_lbs = []
for i in local_bs:
    relay_object_lbs = []
    for j in i.get_nearest_relays():
        relay_object_lbs.append(j[0])
    zonesid_in_lbs = []
    for j in relay_object_lbs:
        for k in j.get_nearest_nodes():
            zonesid_in_lbs.append(k[0].get_zone_ID())
    i.register_zone_ids(list(set(zonesid_in_lbs)))
# --------------------------------      finished  ------------------------------------#

#--------------------       DATA TRANSMISSION PHASE STARTS ---------------------------#

#-----------------------finding initial weight        ----------------------------------------#
sum = 0
for i in range(0,m):
    sum =sum + math.pow(𝜇,i)
w1 = 1/sum
weights = [w1]
#for remaining weight

for i in range(1,m):
    weights.append(𝜇*weights[i-1])
    

weights[:] = [round(weights[i],2) for i in range(len(weights))]
# print(weights)
#testing condition ,mah.fsum is used for computing sum of float values
if (math.fsum(weights) == 1):
    print("No Error in weights")
else:
    print("Error in weights")
# --------------------------------      finished  ------------------------------------#


#--------------------------------------defining constants ------------------------------#
Efs = 10# float(input("Enter energy of free space : "))# in pj/bit/m2
Emp = 0.0013 # float(input("Enter energy of multipath model : ")) pj/bit/m4

d0 = math.sqrt(Efs/Emp)
thzg = 0
p =3
k = 0.1 
per2 = 0.2
# we will run through all the zones and find the time taken by them separately and find maximum time
# total network lifetime is taken as sum all max time in each round till all nodes are dead

# network life time
networklifetime = 0
TotalEnergyconsumed = 0 
# until all the nodes in the network is dead we will repeat this
dount = 0
zp = total_energy_of_all_nodes
dp = 0
# file that takes output
f = open("HN1.csv", "a")
h = 0 # for counting nimber of rounds
f.write("round,total disipated energy for hetergeneous nodes,residual energy ,number of nodes alive,Total Energy consumed at each round,TotalEnergyconsumed till this round,throughput\n")
print(zp)
fig = plt.figure()
fig.set_size_inches(100,100)
# --------------------------------      finished  ------------------------------------#
# --------------------------------      animation function  ------------------------------------#
def updatefig(i):
	# --------------------------------declaring globals----------------------------#
    global zp
    global h
    global TotalEnergyconsumed
    global p
    global weights
    global HN_ids
    krp = 0
    global dp
    p =3
    k = 0.1 
    per2 = 0.2
    print("round : ",h+1)
    energy_in_this_round = 0
    heterogenius_energy = 0
    data_in_this_round = 0
    l = 0
    if (not(network.is_Network_alive())):
    	if(int(input("press 0 to exit all nodes are dead:")) == 0):
    		exit()
    	else:
    		exit()
    else:
    	pass
    #------------------------------------finished -----------------------------------------------#
    #----------------data transmission from heterogeneous node to zone aggregator--------#
    for i in network.get_zones_in_network():
        l+=1
        # all nones which are alive
        t = i.zone_is_alive()
        # cardinality of nodes in a zone
        Nalive = t[0]
        # set of alive nodes
        HNsalive = t[1]

        # finding zone aggregator group and zone aggregator selectors
        # those nodes which belong to ZAG will have a varaiable enabled in respective class
        # those nodes which belong to ZAS will have a varaiable enabled in respective class

        # finding average threshold residual eneregy
        thzg = 0
        for o in HNsalive:
            thzg = thzg + o.get_e_residual()
        thzg =  thzg/Nalive
        #------------------------------------MSWE-----------------------------------------------#
        Zoneaggregators = mswe.MSWE(Nalive,HNsalive,m,p,weights,cutofZag,k,per2,thzg)
        #------------------------------------finished-----------------------------------------------#
        # now MCCT algo for finding nearest hop 
        #------------------------------------MSWE-----------------------------------------------#
        for j in HNsalive:
            mcct.MCCT(j,Zoneaggregators)
        #------------------------------------finished-----------------------------------------------#
        #----------------------------transfering data,energy desipation------------------------------#
        for y in Zoneaggregators:
            # get all registered nodes
            nodesatza = y.get_nodes_for_tdma()
            # period of za for tdma
            for q in nodesatza:
                energy_in_this_round = energy_in_this_round + q.transfer_data(y,len(nodesatza))
        #------------------------------------finished-----------------------------------------------#
    #------------------------------------finished-----------------------------------------------#
    #----------------data transmission from heterogeneous nodes to relay nodes --------------#
    l = 0
    heterogenius_energy += energy_in_this_round
    for i in network.get_EH_relay_nodes():
        l+=1
        # starttimeofzone = time.time()
        # get all registered nodes
        nodesatzana = i.get_registered_nodes_for_tdma()
        nodesatza_na = nodesatzana[0]+nodesatzana[1]
        for q in nodesatza_na:
            w = q.transfer_data_to_rn(i,nodesatza_na)
            heterogenius_energy += w[0]
            energy_in_this_round = energy_in_this_round + w[0] + w[1]
        data_in_this_round = i.get_data()
        i.discard_nodes_of_tdma()
    #------------------------------------finished-----------------------------------------------#
    #----------------data transmission from relay nodes to LBS -----------------------------#
    for i in network.get_lbs_for_network():
        realys = i.get_nearest_relays()
        for j in realys:
            energy_in_this_round = energy_in_this_round + j[0].transfer_data_to_lbs(i)
    #------------------------------------finished-----------------------------------------------#
    #-----------------------regenerating data periodically-----------------------------------------------#
    numberofnodescountalive = 0
    x_hn = [[] for i in range(n+1)]
    y_hn = [[] for i in range(n+1)]
    x_za = []
    y_za = []
    x_hn_dead = []
    y_hn_dead = []
    for i in network.get_zones_in_network():
        t = i.zone_is_alive()
        # cardinality of nodes in a zone
        Nalive = t[0]
        numberofnodescountalive += Nalive
        # set of alive nodes
        HNsalive = t[1]
        for j in HNsalive:
        	if j.get_iszas():
        		x_za.append(j.getlocation()[0])
        		y_za.append(j.getlocation()[1])
	        	j.discard_zas()
	        	j.start_generate_data()	
        		continue
        	for e in range(n):
        		if j.get_e_residual() <= 0:
        			x_hn_dead.append(j.getlocation()[0])
        			y_hn_dead.append(j.getlocation()[1])
        			break
        		elif j.get_e_residual() <= Et[e]:
        			x_hn[e].append(j.getlocation()[0])
        			y_hn[e].append(j.getlocation()[1])
        			break
        		else:
        			pass
        	j.start_generate_data()
        	j.discard_zas()
    #------------------------------------finished-----------------------------------------------#
    #-------------------------writing into file  -----------------------------------------------#
    h +=1
    TotalEnergyconsumed += energy_in_this_round
    f.write(str(h)+",")
    f.write(str(heterogenius_energy)+",")
    krp = krp+heterogenius_energy
    zp = zp - heterogenius_energy
    f.write(str(zp)+",")
    f.write(str(numberofnodescountalive)+",")
    f.write(str(energy_in_this_round)+",")
    f.write(str(TotalEnergyconsumed)+",")
    dp = dp + data_in_this_round
    f.write(str(dp)+"\n")
    #------------------------------------finished-----------------------------------------------#
    #------------------------------------plotting-----------------------------------------------#
    fig.clear()
    spacing = D # This can be your user specified spacing.
    minorLocator = MultipleLocator(spacing)
    colors = ['g','r','c','m','y','k','b']
    for j in range(len(x_hn)):
        plt.plot(x_hn[j],y_hn[j], 'o',color = colors[j])
    plt.plot(x_za,y_za, 'D',color = colors[len(colors)-2],markersize=6)
    global EHx,EHy,EH_ids
    plt.plot(EHx,EHy, 'D',color = colors[len(colors)-1],markersize=12)
    global x11,y11,x22,y22,x33,y33,x44,y44
    plt.fill(x11,y11,'y')
    plt.fill(x22,y22,'y')
    plt.fill(x33,y33,'y')
    plt.fill(x44,y44,'y')
    global local_bs
    for q in local_bs:
    	plt.plot(q.getlocation()[0],q.getlocation()[1], 'D',color = colors[1],markersize=20)
    LB_ids = []
    for q in local_bs:
    	LB_ids.append(q.get_node_id())
    for q, txt in enumerate(LB_ids):
    	plt.annotate(txt, (local_bs[q].getlocation()[0],local_bs[q].getlocation()[1]))
    plt.axis([-60, L+60, -60, L+60])#defining axix x and y
    plt.grid(which = 'minor')#only major works fine
    plt.draw()

anim = animation.FuncAnimation(fig, updatefig, 1)

plt.show()

f.close()
