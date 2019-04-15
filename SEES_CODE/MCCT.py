"""
this is a MCCT procedure 
"""
import math
import time

def nearest_za(node,zas):
	distance=[]
	for i in zas:
		euclidean_distance = math.sqrt((i.getlocation()[0]-node.getlocation()[0])**2 +(i.getlocation()[1]-node.getlocation()[1])**2)
		distance.append((i,euclidean_distance))
	distance = sorted(distance,key=lambda x: x[1])
	# print(distance)
	return distance[0]

def MCCT(node,zas):
	# find nearest relay node and it's distance
	dmin = node.distanceToNearestRelay()
	nxt_hop = (node.nearestrelayobject(),dmin)
	# check whether this node is zone aggregator or not
	if node.get_iszas():
		# print("it is a zone aggregator")
		# if it is a zone aggregator then register for tdma in EH
		nxt_hop[0].register_for_tdma(node)
		# print("registered for relay ",nxt_hop[0],nxt_hop[0].get_registered_nodes_for_tdma())
	else:
		# find nearest zone aggregator node
		my_za = nearest_za(node,zas)
		# form my_za, find nearest relay node
		za_relay = my_za[0].nearestrelayobject()
		# their respective distances
		dza = my_za[1]
		drn = my_za[0].distanceToNearestRelay()
		# checking for next hop condition 
		indicator = 0 
		if ((dza**2 + drn**2) < dmin**2):
			# print("multipath is better so registering for za")
			indicator = 1
			nxt_hop = my_za
			dmin = dza
		# this is the registers for Tdma in my_za
		nxt_hop[0].register_for_tdma(node)
		# if(indicator == 1):
		# 	print("registered for za",nxt_hop[0],nxt_hop[0].get_nodes_for_tdma())
		# else:
		# 	print("registered for relay",nxt_hop[0],nxt_hop[0].get_registered_nodes_for_tdma())
		
	












