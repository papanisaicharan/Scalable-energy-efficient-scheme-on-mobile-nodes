"""
doubt: 
The nodes in all the zones broadcast an “INFO” messages containing its ID , its type, and its location, to the
nearest relaying layer.
EH nodes nearby the zones receive these messages,add their own information (i.e. ID , and location), and
then re-broadcast to the LBSs layer.
The LBSs receive these messages, keep the information for the future use, and forward the messages to the MBS .
Once MBS receives “INFO” messages, it sends a “SET” message, to the deployed LBSs ,that contains information 
on which zones are served by which LBSs.
Each LBS then send “INIT” message, through the EHs , to the nodes in the concerned zones, which provides
the nodes with all necessary information that describes the main functionality of a node, operation parameters,
and transmission policies.
"""

import hybrid_placement as hp
import math
import MSWE as mswe
import MCCT as mcct
import time

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

# for i in hp.zones_objects:
# 	print(i.send_info(),end=" /")

𝜇 = 0.8#float(input("Enter the 𝜇 value"))
m = 3#int(input("Enter m value"))# number of stages
cutofZag = 0.7#float(input("Enter the cut of Zag =  "))


for i in hp.zones_objects:
	nearest_relay = distanceToNearestRelay(hp.EH,i) #(relay_object,distance_to_nearest_relay)
	i.get_info_relay(nearest_relay[0],nearest_relay[1])
	nearest_relay[0].register_near_node(i,nearest_relay[1])

# sum1 = 0
# for i in hp.EH:
# 	print(i.get_nearest_nodes(),len(i.get_nearest_nodes()))
# 	sum1 += len(i.get_nearest_nodes())
# print(sum1)

for i in hp.EH:
	nearest_bs = distanceToNearestRelay(hp.local_bs,i)
	i.get_info_bs(nearest_bs[0],nearest_bs[1])
	nearest_bs[0].register_near_relay(i,nearest_bs[1])

sum1 = 0
for i in hp.local_bs:
	print(i.get_nearest_relays(),len(i.get_nearest_relays()))
	sum1 += len(i.get_nearest_relays())
# print(sum1)

# list1 = []
zones_in_each_lbs = []
for i in hp.local_bs:
    relay_object_lbs = []
    for j in i.get_nearest_relays():
        relay_object_lbs.append(j[0])
    zonesid_in_lbs = []
    for j in relay_object_lbs:
        for k in j.get_nearest_nodes():
            zonesid_in_lbs.append(k[0].get_zone_ID())
    # list1.append(zonesid_in_lbs)
    # zones_in_each_lbs.append(list(set(zonesid_in_lbs)))
    i.register_zone_ids(list(set(zonesid_in_lbs)))


# print(list1)
# print(zones_in_each_lbs)
 # checking code
# c= 0
# for i in list1:
#     c = c+ len(i)
# print(c)

"""
DATA TRANSMISSION PHASE STARTS
"""

#finding initial weight
sum = 0
for i in range(0,m):
    sum =sum + math.pow(𝜇,i)
    
w1 = 1/sum

print(sum,w1)

weights = [w1]

#for remaining weight

for i in range(1,m):
    weights.append(𝜇*weights[i-1])
    
# print(weights)#these weigths are used in every stage of ZAG election without any change in their value


weights[:] = [round(weights[i],2) for i in range(len(weights))]
# print(weights)
#testing condition ,mah.fsum is used for computing sum of float values
if (math.fsum(weights) == 1):
    print("No Error in weights")
else:
    print("Error in weights")


# print(len(hp.object_of_zones),len(hp.object_of_zones[0].get_nodes_in_zone()))
# print(len(hp.network.get_zones_in_network()))

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
starttime = time.time()
zp = hp.total_energy_of_all_nodes
dp =0
# file that takes 
f = open("node_energies.csv", "a")
h = 0
f.write("round,total disipated energy for hetergeneous nodes,residual energy ,number of nodes alive,Total Energy consumed at each round,TotalEnergyconsumed till this round,throughput\n")
# hp.network.is_Network_alive()
while(hp.network.is_Network_alive()):
    print("round : ",h+1)
    energy_in_this_round = 0
    heterogenius_energy = 0
    data_in_this_round = 0
    # f.write("round :"+str(h+1)+"\n")
    l = 0
    for i in hp.network.get_zones_in_network():
        l+=1
        # f.write("\tzone:"+str(l)+"\n")
        # for each zone register start time
        # starttimeofzone = time.time()
        # all nones which are alive
        t = i.zone_is_alive()
        # cardinality of nodes in a zone
        Nalive = t[0]
        # set of alive nodes
        HNsalive = t[1]
        # find zone aggregator group and zone aggregator selectors
        # those nodes which are ZAG we will enable the varaiable in respective class
        # tthose nodes which are ZAs we will enable the varaiable in respective class
        # we will be getting zas as output
        # f.write("\tnodes :"+str([s.get_node_id() for s in HNsalive])+"\n")
        thzg = 0
        for o in HNsalive:
            thzg = thzg + o.get_e_residual()
        thzg =  thzg/Nalive
        # f.write("\tthreshold energy :"+str(thzg)+"\n")
        Zoneaggregators = mswe.MSWE(Nalive,HNsalive,m,p,weights,cutofZag,k,per2,thzg)
        # now MCCT algo for finding nearest hop 
        # in this we will as give the time slot for nodes at zone aggregator and also find energy
        # desipated in za as well as na and collect all data za 
        # f.write("\tZoneaggregators :"+str([s.get_node_id() for s in Zoneaggregators])+"\n")
        # now MCCT algo for finding nearest hop 
        # in this we will as give the time slot for nodes at zone aggregator and also find energy
        # desipated in za as well as na and collect all data za 
        for j in HNsalive:
            mcct.MCCT(j,Zoneaggregators)
            # f.write("\tnode is : "+str(j.get_node_id())+" with residual energy :"+str(j.get_e_residual())+"\n")
        # now provide time slots at zas for registered nodes
        for y in Zoneaggregators:
            # get all registered nodes
            nodesatza = y.get_nodes_for_tdma()
            # f.write("\tnode registerd for tdma : "+str([s.get_node_id() for s in nodesatza])+"\n")
            # period of za for tdma
            for q in nodesatza:
                energy_in_this_round = energy_in_this_round + q.transfer_data(y,len(nodesatza))
                # f.write("\tnode is() : "+str(q.get_node_id())+" with residual energy :"+str(q.get_e_residual())+"\n")
    # now run a loop at Hn_relay and give time slot registered for tdma and colect data
    l =0
    heterogenius_energy +=energy_in_this_round
    for i in hp.network.get_EH_relay_nodes():
        l+=1
        # f.write("\trelay node :"+str(i.get_node_id())+"\n")
        # starttimeofzone = time.time()
        # give time slots to all registered nodes for tdma ,collect data and aggregate it
        # find the total amount of energy desipated overall
        # get all registered nodes
        nodesatzana = i.get_registered_nodes_for_tdma()
        nodesatza_na = nodesatzana[0]+nodesatzana[1]
        # f.write("\t\tall nodes registered for this relay :"+str([s.get_node_id() for s in nodesatza_na])+"\n")
        for q in nodesatza_na:
            w = q.transfer_data_to_rn(i,nodesatza_na)
            heterogenius_energy += w[0]
            energy_in_this_round = energy_in_this_round + w[0] + w[1]
        data_in_this_round = i.get_data()

            # f.write("\t\tnode is(registered for relay) : "+str(q.get_node_id())+" with residual energy :"+str(q.get_e_residual())+"\n")
    numberofnodescountalive = 0
    for i in hp.network.get_zones_in_network():
        t = i.zone_is_alive()
        # cardinality of nodes in a zone
        Nalive = t[0]
        numberofnodescountalive += Nalive
        # set of alive nodes
        HNsalive = t[1]
        # f.write("before : "+str([s.get_sensed_data() for s in HNsalive]))
        for j in HNsalive:
            j.start_generate_data()
        # f.write("after : "+str([s.get_sensed_data() for s in HNsalive]))
    for i in hp.network.get_lbs_for_network():
        realys = i.get_nearest_relays()
        for j in realys:
            energy_in_this_round = energy_in_this_round + j[0].transfer_data_to_lbs(i)
    h +=1
    TotalEnergyconsumed +=energy_in_this_round
    f.write(str(h)+",")
    f.write(str(heterogenius_energy)+",")
    zp = zp - heterogenius_energy
    f.write(str(zp)+",")
    f.write(str(numberofnodescountalive)+",")
    f.write(str(energy_in_this_round)+",")
    f.write(str(TotalEnergyconsumed)+",")
    dp = dp +data_in_this_round
    f.write(str(dp)+"\n")
    # print(" TotalEnergyconsumed till round:",h," energy:",TotalEnergyconsumed)
f.close()
# zas1 = mswe.MSWE(hp.network.get_zones_in_network()[0].zone_is_alive()[0],hp.network.get_zones_in_network()[0].zone_is_alive()[1],m,p,weights,cutofZag,k,per2,thzg)
# print(zas1)
# list23= []
# for i in hp.network.get_zones_in_network()[0].zone_is_alive()[1]:
#     list23.append((i.get_iszag(),i.get_iszas()))
# print(list23)

# mcct.MCCT(hp.network.get_zones_in_network()[0].zone_is_alive()[1][0],zas1)



## checking doubt


# p = hp.zones_objects[:2]

# p[0].set_as_za()

# print(p,hp.zones_objects[0],hp.zones_objects[1])

# print(p[0].get_isza(),hp.zones_objects[0].get_isza())
