from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


# Dictonaries of hand positions
# Each contains 21 keys (xyz for 5 fingers, palm and wrist) where the values are lists of coordinates
horizontal_ok = {
    'x_thumb' : [0, 0, 0, 0],
    'y_thumb' : [6, 9, 5, 0],
    'z_thumb' : [3, -1, -2, -1],

    'x_index' : [-2, -2, -2],
    'y_index' : [5, 9, 11],
    'z_index' : [4, 8, 10],
    
    'x_middle' : [-4, -4, -4],
    'y_middle' : [5, 9, 11],
    'z_middle' : [4, 8, 10],

    'x_ring' : [-6, -6, -6],
    'y_ring' : [5, 9, 11],
    'z_ring' : [4, 8, 10],

    'x_pinky' : [],
    'y_pinky' : [],
    'z_pinky' : [],

    'x_palm' : [-6, -6, -4, -2, 0, 0],
    'y_palm' : [0, 5, 5, 5, 6, 0],
    'z_palm' : [-1, 4, 4, 4, 3, -1],

    'x_wrist' : [-6, 0, 0, -6, -6],    #order matters for connecting points properly
    'y_wrist' : [-5, -5, 0, 0, -5],
    'z_wrist' : [-1, -1, -1, -1, -1]
}

peace = {
    'x_thumb' : [],
    'y_thumb' : [],
    'z_thumb' : [],

    'x_index' : [],
    'y_index' : [],
    'z_index' : [],
    
    'x_middle' : [],
    'y_middle' : [],
    'z_middle' : [],

    'x_ring' : [],
    'y_ring' : [],
    'z_ring' : [],

    'x_pinky' : [],
    'y_pinky' : [],
    'z_pinky' : [],

    'x_palm' : [],
    'y_palm' : [],
    'z_palm' : [],

    'x_wrist' : [],    #order matters for connecting points properly
    'y_wrist' : [],
    'z_wrist' : []
}


#List that contain all gesture dictionaries so that it can be called and randomized
all_positions = [horizontal_ok, peace]


# Data points
x_thumb = [0, 0, 0, 0]
y_thumb = [6, 9, 5, 0]
z_thumb = [3, -1, -2, -1]

x_index = [-2, -2, -2]
y_index = [5, 9, 11]
z_index = [4, 8, 10]

x_middle = [-4, -4, -4]
y_middle = [5, 9, 11]
z_middle = [4, 8, 10]

x_ring = [-6, -6, -6]
y_ring = [5, 9, 11]
z_ring = [4, 8, 10]

x_pinky = []
y_pinky = []
z_pinky = []

x_palm = [-6, -6, -4, -2, 0, 0]
y_palm = [0, 5, 5, 5, 6, 0]
z_palm = [-1, 4, 4, 4, 3, -1]

x_wrist = [-6, 0, 0, -6, -6]    #order matters for connecting points properly
y_wrist = [-5, -5, 0, 0, -5]
z_wrist = [-1, -1, -1, -1, -1]


#3D Plot
fig3d = plt.figure()
ax = fig3d.add_subplot(1,1,1, projection='3d')
ax.set_xlim(-10, 5)
ax.set_ylim(-10, 15)
ax.set_zlim(-10, 12)

ax.scatter(x_thumb,y_thumb,z_thumb, c='r',s=100, label='True Position')      #points
plt.plot(x_thumb,y_thumb,z_thumb, color='r')          #lines between points

ax.scatter(x_wrist,y_wrist,z_wrist, c='r',s=100)      #points
plt.plot(x_wrist,y_wrist,z_wrist, color='r')          #lines between points

ax.scatter(x_palm,y_palm,z_palm, c='r',s=100)      #points
plt.plot(x_palm,y_palm,z_palm, color='r')          #lines between points

ax.scatter(x_index, y_index, z_index, color='r', s=100)     #points
plt.plot(x_index,y_index,z_index, color='r')          #lines between points

ax.scatter(x_middle, y_middle, z_middle, color='r', s=100)     #points
plt.plot(x_middle,y_middle,z_middle, color='r')          #lines between points

ax.scatter(x_ring, y_ring, z_ring, color='r', s=100)     #points
plt.plot(x_ring,y_ring,z_ring, color='r')          #lines between points


plt.title('Finger Position Simulation')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
plt.show()
