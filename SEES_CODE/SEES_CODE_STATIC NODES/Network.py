"""
 This is a class of Network where class information is stored 
 in it.

"""
class Network():
	def __init__(self,zone_object_in_it,EH,lbs):
		self.dead = 0
		self.zone_object_in_it = zone_object_in_it
		self.EH_relay_node = EH
		self.lbs = lbs

	def get_zones_in_network(self):
		return self.zone_object_in_it

	def get_EH_relay_nodes(self):
		return self.EH_relay_node

	def get_lbs_for_network(self):
		return self.lbs

	def network_is_alive(self):
		alivezones = []
		for i in self.zone_object_in_it:
			if i.is_zone_alive():
				alivezones.append(i)
		self.zone_object_in_it = alivezones[:]
		return [int(len(alivezones)),alivezones]

	def is_Network_alive(self):
		self.dead = 1
		for i in self.zone_object_in_it:
			if i.is_zone_alive():
				self.dead = 0
				break
		p = self.network_is_alive()
		if self.dead == 0:
			return True
		else:
			return False

