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

# p = [1,2,3,4,5]
# q = p[:]
# print(p,q)
# q[0] =10
# q[4] = 30
# p = q[:]
# print(p,q)
# f = open("node_energies.txt", "a")
# h = 0
# # hp.network.is_Network_alive()
# while(h < 10):
#     f.write("round :"+str(h+1)+"\n")
#     h +=1

# print(h)

# f.close()

# (a,b) = (1,2)
# print(a,b)
# m = 12
# d =  3
# import numpy as np
# import matplotlib.pyplot as plt
# import matplotlib.patches as patches
# from matplotlib import animation

# x = [0, 1, 2]
# y = [0, 1, 2]
# yaw = [0.0, 0.5, 1.3]
# fig = plt.figure()
# plt.axis('equal')
# plt.grid()
# ax = fig.add_subplot(111)
# ax.set_xlim(-10, 10)
# ax.set_ylim(-10, 10)

# patch = patches.Rectangle((0, 0), 0, 0, fc='y')

# def init():
#     ax.add_patch(patch)
#     return patch,

# def animate(i):
#     patch.set_width(1.2)
#     patch.set_height(1.0)
#     patch.set_xy([x[i], y[i]])
#     patch._angle = -np.rad2deg(yaw[i])
#     return patch,

# anim = animation.FuncAnimation(fig, animate,
#                                init_func=init,
#                                frames=len(x),
#                                interval=500,
#                                blit=True)
# plt.show()

# import numpy as np
# import matplotlib.pyplot as plt
# import mpl_toolkits.mplot3d.axes3d as p3
# import matplotlib.animation as animation

# # Fixing random state for reproducibility
# np.random.seed(19680801)


# def Gen_RandLine(length, dims=2):
#     """
#     Create a line using a random walk algorithm

#     length is the number of points for the line.
#     dims is the number of dimensions the line has.
#     """
#     lineData = np.empty((dims, length))
#     lineData[:, 0] = np.random.rand(dims)
#     for index in range(1, length):
#         # scaling the random numbers by 0.1 so
#         # movement is small compared to position.
#         # subtraction by 0.5 is to change the range to [-0.5, 0.5]
#         # to allow a line to move backwards.
#         step = ((np.random.rand(dims) - 0.5) * 0.1)
#         lineData[:, index] = lineData[:, index - 1] + step

#     return lineData


# def update_lines(num, dataLines, lines):
#     for line, data in zip(lines, dataLines):
#         # NOTE: there is no .set_data() for 3 dim data...
#         line.set_data(data[0:2, :num])
#         line.set_3d_properties(data[2, :num])
#     return lines

# # Attaching 3D axis to the figure
# fig = plt.figure()
# ax = p3.Axes3D(fig)

# # Fifty lines of random 3-D lines
# data = [Gen_RandLine(25, 3) for index in range(50)]

# # Creating fifty line objects.
# # NOTE: Can't pass empty arrays into 3d version of plot()
# lines = [ax.plot(dat[0, 0:1], dat[1, 0:1], dat[2, 0:1])[0] for dat in data]

# # Setting the axes properties
# ax.set_xlim3d([0.0, 1.0])
# ax.set_xlabel('X')

# ax.set_ylim3d([0.0, 1.0])
# ax.set_ylabel('Y')

# ax.set_zlim3d([0.0, 1.0])
# ax.set_zlabel('Z')

# ax.set_title('3D Test')

# # Creating the Animation object
# line_ani = animation.FuncAnimation(fig, update_lines, 25, fargs=(data, lines),
#                                    interval=50, blit=False)

# plt.show()

# t = [1,2,3]
# t = []
# print(t)

import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np

fig = plt.figure()

def updatefig(i):
    fig.clear()
    p = plt.plot(np.random.random(100))
    p1 = plt.plot(np.random.random(100))
    plt.draw()

anim = animation.FuncAnimation(fig, updatefig, 100)



plt.show()