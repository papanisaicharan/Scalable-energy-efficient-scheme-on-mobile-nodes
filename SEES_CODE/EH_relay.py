""" 
CODED BY : PAPANI SAICHARAN
 This is a class of EH_relay node where class information is stored 
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


class EH_relay():
	def __init__(self,x,y,id1):
		self.xcoord = x
		self.ycoord = y
		self.nodeid = id1
		self.nearest_nodes = []
		self.data = 0
		self.joins_list = []
		self.joins_list_na = []

	def getlocation(self):
		return (self.xcoord,self.ycoord)

	def get_data(self):
		return self.data

	def get_node_id(self):
		return self.nodeid

	def register_near_node(self,node_object,dist_to_Hn):
		self.nearest_nodes.append((node_object,dist_to_Hn))

	def get_nearest_nodes(self):
		return self.nearest_nodes

	def get_info_bs(self,bs_object,dist_to_bs):
		self.nearest_bs_object = bs_object
		self.dist_to_bs= dist_to_bs

	def register_for_tdma(self,node):
		if node.get_iszas():
			self.joins_list.append(node)
		else:
			self.joins_list_na.append(node)

	def discard_nodes_of_tdma(self):
		self.joins_list = []
		self.joins_list_na = []

	def get_registered_nodes_for_tdma(self):
		return [self.joins_list,self.joins_list_na]

	def add_data_from_sender(self,d0):
		self.data = self.data + d0

	def get_energy_desipated_dut_to_reci(self,d0):
		return float(d0)*(ERx_elec*(len(self.joins_list)+len(self.joins_list_na))+Eda*len(self.joins_list_na))

	def transfer_data_to_lbs(self,reciver):
		d0 = self.data
		self.data = 0
		dra = math.sqrt((reciver.getlocation()[0]-self.xcoord)**2 + (reciver.getlocation()[1]-self.ycoord)**2 )
		return d0*(ETx_elec+Efs*dra**2)

