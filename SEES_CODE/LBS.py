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

class LBS():
	def __init__(self,x,y,id1):
		self.xcoord = x
		self.ycoord = y
		self.lbsId = id1
		self.nearest_relays = []

	def getlocation(self):
		return (self.xcoord,self.ycoord)

	def get_node_id(self):
		return self.lbsId

	def register_near_relay(self,relay_object,dist_to_relay):
		self.nearest_relays.append((relay_object,dist_to_relay))

	def get_nearest_relays(self):
		return self.nearest_relays

	def register_zone_ids(self,zoneids):
		self.nearest_zone_ids = zoneids

	def get_zone_ids(self):
		return self.nearest_zone_ids 


		
