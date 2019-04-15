# import Node as nd
# import time
# node1 = nd.Node(10,12,1,1,1,1)
# print(node1.get_sensed_data())
# time.sleep(3)
# print(node1.get_sensed_data())
# time.sleep(3)
# print(node1.get_sensed_data())

# import time, threading
# def foo():
#     print(time.ctime())
#     threading.Timer(10, foo).start()

# foo()

# import math,random

# def getpoints(startx,starty,endx,endy,id):
#     rangeX = (startx,endx)
#     rangeY = (starty,endy)
#     randPoints = []
#     excluded = set()
#     i = 0
#     while i<20:
#         x = random.randrange(*rangeX)
#         y = random.randrange(*rangeY)
#         if (x,y) in excluded: continue
#         randPoints.append((x,y))
#         i += 1
#         excluded.update((x, y))
        
#     secure_random = random.SystemRandom()
#     nodeswithenergy = []#(x,y),energy,id
#     for j in range(len(nodesinlevel)):
#         for i in range(nodesinlevel[j]):
#             list1 = []
#             list1.append(secure_random.choice(randPoints))
#             randPoints.remove(list1[0])
#             list1.append(Et[j])
#             list1.append(id)
#             id = id+1
#             nodeswithenergy.append(list1)
#     return(nodeswithenergy)

# Z=10
# node_objects = []
# for i in range(0,int(math.sqrt(int(Z)))):#for y axis
# 	for j in range(0,int(math.sqrt(int(Z)))):#for x axis
# 	    for k in getpoints(j*20,i*20,(j+1)*20,(i+1)*20,j*20+1+200*i):
# 	    	node_objects.append(k[0][0],k[0][1],k[1],k[2])

# for i in node_objects:
# 	print(i.get_node_id(),end=" ")
# L = 200
# R=121
# import EH_relay as relay_nd

# EH = []
# count = 1
# for i in range(0,L+1,20):
# 	for j in range(0,L+1,20):
# 		print(i,j)
# 		if count <= R: 
# 			EH.append(relay_nd.EH_relay(i,j,count))
# 			count+=1
# print(len(EH))
# EHx = []
# EHy = []
# for j in EH:
# 	EHx.append(j.getlocation()[0])
# 	EHy.append(j.getlocation()[1])
# print(EHx,EHy)

p = [1,2,3,4,5]
q = p[:]
print(p,q)
q[0] =10
q[4] = 30
p = q[:]
print(p,q)
# f = open("node_energies.txt", "a")
# h = 0
# # hp.network.is_Network_alive()
# while(h < 10):
#     f.write("round :"+str(h+1)+"\n")
#     h +=1

# print(h)

# f.close()