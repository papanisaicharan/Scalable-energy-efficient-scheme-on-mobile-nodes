"""
 This is a class of Zone where class information is stored 
 in it.

"""
class Zone():
	def __init__(self,zoneid,node_object_in_it,init_coord):
		self.dead = 0
		self.zoneid = zoneid
		self.node_object_in_it = node_object_in_it
		self.zone_startcoord = init_coord

	def get_zone_ID(self):
		return self.zoneid

	def get_init_coord(self):
		return self.zone_startcoord

	def get_nodes_in_zone(self):
		return self.node_object_in_it

	def zone_is_alive(self):
		alivenodes = []
		for i in self.node_object_in_it:
			if i.is_node_alive():
				alivenodes.append(i)
		self.node_object_in_it = alivenodes[:]
		return [int(len(alivenodes)),alivenodes]


	def is_zone_alive(self):
		self.dead = 1
		for i in self.node_object_in_it:
			if i.is_node_alive():
				self.dead = 0
				break
		p = self.zone_is_alive()
		if self.dead == 0:
			return True
		else:
			return False

