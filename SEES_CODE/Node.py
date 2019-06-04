""" 
CODED BY : PAPANI SAICHARAN
 This is a class of node where class information is stored 
 in it.

"""


import time, threading
import math

# units nJ/bit --> J/bit
ETx_elec = 50*math.pow(10,-9)
ERx_elec = 50*math.pow(10,-9)
# units nJ/bit/signal --> J/bit/signal
Eda = 5 *math.pow(10,-9)
# units pJ/bit/m2 --> J/bit/m2
Efs = 10*math.pow(10,-12)
# units pJ/bit/m4 --> --> J/bit/m4


Emp = 0.0013*math.pow(10,-12)
class Node():
	
	def __init__(self,x,y,e_initial,id1,type1,zoneid):
		self.xcoord = x
		self.ycoord = y
		self.e_initial = e_initial
		self.e_residual = e_initial
		self.nodeid = id1
		self.dead = 0
		self.type= type1
		self.iszag = False
		self.iszas = False
		self.zoneid = zoneid
		# if we want to consider energy consumption while moving intilize this with Ed value according to requirement
		self.Ed_energy = 10*math.pow(10,-10)
		self.data = 4000
		#threading.Timer(0.2, self.start_generate_data).start()
		
	def start_generate_data(self):
		#print(self.data)
		# self.data = self.data + 2000
		self.data = self.data + 4000

	def get_sensed_data(self):
		return self.data

	def getlocation(self):
		return (self.xcoord,self.ycoord)

	def set_location(self,xcord,ycord):
		self.xcoord = xcord
		self.ycoord = ycord

	def get_zone_ID(self):
		return self.zoneid

	def get_node_id(self):
		return self.nodeid

	def get_e_initial(self):
		return self.e_initial
		
	def get_e_residual(self):
		return self.e_residual

	def energyformoving(self):
		if (self.e_residual >= self.Ed_energy):
			self.e_residual = self.e_residual - self.Ed_energy
			return False
		else:
			return True

	def get_info_relay(self,relay_object,dist_to_relay):
		self.nearest_relay_object = relay_object
		self.dist_to_relay = dist_to_relay

	def is_node_alive(self):
		if self.e_residual <= 0:
			self.dead = 1
			return False
		else:
			return True

	def discard_zag(self):
		self.iszag = False

	def set_as_zag(self):
		self.iszag = True

	def get_iszag(self):
		return self.iszag

	def discard_zas(self):
		self.iszas = False

	def set_as_zas(self):
		self.joins_list = []
		self.iszas = True

	def get_iszas(self):
		return self.iszas

	def centrality(self,points):
		distance=[]
		for i in points:
			euclidean_distance = math.sqrt((self.xcoord-i.getlocation()[0])**2 +(self.ycoord-i.getlocation()[1])**2)
			distance.append(euclidean_distance)
		sumofdistances = 0
		for i in distance:
			sumofdistances = sumofdistances+i
		if sumofdistances == 0:
			return 1
		return((len(points)-1)/sumofdistances)

	def distanceToNearestRelay(self):
		return self.dist_to_relay

	def nearestrelayobject(self):
		return self.nearest_relay_object

	def register_for_tdma(self,nodes):
		if self.iszas:
			self.joins_list.append(nodes)

	def get_nodes_for_tdma(self):
		return self.joins_list

	def get_energy_desipated_na(self,d0,dza):
		e = float(d0)*(ETx_elec + Efs*(dza**2))
		# print("at na sending : ",e)
		p = self.e_residual
		self.e_residual = self.e_residual - e
		if self.e_residual <= 0:
			self.dead =1
			return p
		return e

	def get_energy_desipated_due_receiving(self,d0,numberofna):
		e = float(d0)*(ERx_elec*float(numberofna) + Eda*float((numberofna+1)))
		# print("at zas receiving",e)
		p = self.e_residual
		self.e_residual = self.e_residual - e
		if self.e_residual <= 0:
			self.dead = 1
			return p
		return e

	def get_energy_desipated_at_za_due_tran(self,d0,drn):
		eenergy = float(d0)*(ETx_elec+Efs*float((drn**2)))
		# print("energy due to tran to rn : ",eenergy)
		p = self.e_residual
		self.e_residual = self.e_residual - eenergy
		if self.e_residual <= 0:
			self.dead = 1
			return p
		return eenergy

	def add_data_from_sender(self,d):
		if self.iszas:
			self.data = self.data + d

	def transfer_data(self,reciver,numberofna):
		d0 = self.data
		self.data = 0
		# adding the data to za or relay
		reciver.add_data_from_sender(d0)
		dza = math.sqrt((reciver.getlocation()[0]-self.xcoord)**2 + (reciver.getlocation()[1]-self.ycoord)**2 )
		return self.get_energy_desipated_na(d0,dza) + reciver.get_energy_desipated_due_receiving(d0,numberofna)

	def transfer_data_to_rn(self,reciver,nodesatza_na):
		d0 = self.data
		self.data = 0
		# adding the data to za or relay
		reciver.add_data_from_sender(d0)
		drn = math.sqrt((reciver.getlocation()[0]-self.xcoord)**2 + (reciver.getlocation()[1]-self.ycoord)**2 )
		return (self.get_energy_desipated_at_za_due_tran(d0,drn),reciver.get_energy_desipated_dut_to_reci(d0))





