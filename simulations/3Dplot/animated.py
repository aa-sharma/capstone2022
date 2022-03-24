import matplotlib
from matplotlib import pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import positionsDB as pdb
import time
import numpy as np
import matplotlib.animation as animation

class AnimatedHand():
    def __init__(self):
        self.get_sensor_data()

    def get_sensor_data(self):
        # Thumb
        self.thumbA_x = pdb.position1['thumbA'][0]
        self.thumbA_y = pdb.position1['thumbA'][1]
        self.thumbA_z = pdb.position1['thumbA'][2]
        self.thumbB_x = pdb.position1['thumbB'][0]
        self.thumbB_y = pdb.position1['thumbB'][1]
        self.thumbB_z = pdb.position1['thumbB'][2]
        self.thumbC_x = pdb.position1['thumbC'][0]
        self.thumbC_y = pdb.position1['thumbC'][1]
        self.thumbC_z = pdb.position1['thumbC'][2]

        # Index
        self.indexA_x = pdb.position1['indexA'][0]
        self.indexA_y = pdb.position1['indexA'][1]
        self.indexA_z = pdb.position1['indexA'][2]
        self.indexB_x = pdb.position1['indexB'][0]
        self.indexB_y = pdb.position1['indexB'][1]
        self.indexB_z = pdb.position1['indexB'][2]
        self.indexC_x = pdb.position1['indexC'][0]
        self.indexC_y = pdb.position1['indexC'][1]
        self.indexC_z = pdb.position1['indexC'][2]

        # Middle
        self.middleA_x = pdb.position1['middleA'][0]
        self.middleA_y = pdb.position1['middleA'][1]
        self.middleA_z = pdb.position1['middleA'][2]
        self.middleB_x = pdb.position1['middleB'][0]
        self.middleB_y = pdb.position1['middleB'][1]
        self.middleB_z = pdb.position1['middleB'][2]
        self.middleC_x = pdb.position1['middleC'][0]
        self.middleC_y = pdb.position1['middleC'][1]
        self.middleC_z = pdb.position1['middleC'][2]

        # Ring
        self.ringA_x = pdb.position1['ringA'][0]
        self.ringA_y = pdb.position1['ringA'][1]
        self.ringA_z = pdb.position1['ringA'][2]
        self.ringB_x = pdb.position1['ringB'][0]
        self.ringB_y = pdb.position1['ringB'][1]
        self.ringB_z = pdb.position1['ringB'][2]
        self.ringC_x = pdb.position1['ringC'][0]
        self.ringC_y = pdb.position1['ringC'][1]
        self.ringC_z = pdb.position1['ringC'][2]

        # Pinky
        self.pinkyA_x = pdb.position1['pinkyA'][0]
        self.pinkyA_y = pdb.position1['pinkyA'][1]
        self.pinkyA_z = pdb.position1['pinkyA'][2]
        self.pinkyB_x = pdb.position1['pinkyB'][0]
        self.pinkyB_y = pdb.position1['pinkyB'][1]
        self.pinkyB_z = pdb.position1['pinkyB'][2]
        self.pinkyC_x = pdb.position1['pinkyC'][0]
        self.pinkyC_y = pdb.position1['pinkyC'][1]
        self.pinkyC_z = pdb.position1['pinkyC'][2]

        # Wrist
        self.wristA_x = pdb.position1['wristA'][0]
        self.wristA_y = pdb.position1['wristA'][1]
        self.wristA_z = pdb.position1['wristA'][2]
        self.wristB_x = pdb.position1['wristB'][0]
        self.wristB_y = pdb.position1['wristB'][1]
        self.wristB_z = pdb.position1['wristB'][2]
        self.wristC_x = pdb.position1['wristC'][0]
        self.wristC_y = pdb.position1['wristC'][1]
        self.wristC_z = pdb.position1['wristC'][2]
        self.wristD_x = pdb.position1['wristD'][0]
        self.wristD_y = pdb.position1['wristD'][1]
        self.wristD_z = pdb.position1['wristD'][2]
        self.wristE_x = pdb.position1['wristE'][0]
        self.wristE_y = pdb.position1['wristE'][1]
        self.wristE_z = pdb.position1['wristE'][2]

        list_data = self.generate_data_format()
        self.plot_data(list_data)

    def generate_data_format(self, iterations=10, N=18):
        """
        Generate the data in proper format to animate.
        Args:
            iterations (int) : Number of iterations data needs to be moved
            N (int): number of elements (or points) that will move
        Returns:
            list of positions of elements
        """

        # Inital starting segments
        
        self.x_thumb = [self.thumbA_x, self.thumbB_x, self.thumbC_x]
        self.y_thumb = [self.thumbA_y, self.thumbB_y, self.thumbC_y]
        self.z_thumb = [self.thumbA_z, self.thumbB_z, self.thumbC_z]

        self.x_index = [self.wristC_x, self.indexA_x, self.indexB_x, self.indexC_x]
        self.y_index = [self.wristC_y, self.indexA_y, self.indexB_y, self.indexC_y]
        self.z_index = [self.wristC_z, self.indexA_z, self.indexB_z, self.indexC_z]

        self.x_middle = [self.ringA_x, self.middleA_x, self.middleB_x, self.middleC_x]
        self.y_middle = [self.ringA_y, self.middleA_y, self.middleB_y, self.middleC_y]
        self.z_middle = [self.ringA_z, self.middleA_z, self.middleB_z, self.middleC_z]

        self.x_ring = [self.pinkyA_x, self.ringA_x, self.ringB_x, self.ringC_x]
        self.y_ring = [self.pinkyA_y, self.ringA_y, self.ringB_y, self.ringC_y]
        self.z_ring = [self.pinkyA_z, self.ringA_z, self.ringB_z, self.ringC_z]

        self.x_pinky = [self.wristB_x, self.pinkyA_x, self.pinkyB_x, self.pinkyC_x]
        self.y_pinky = [self.wristB_y, self.pinkyA_y, self.pinkyB_y, self.pinkyC_y]
        self.z_pinky = [self.wristB_z, self.pinkyA_z, self.pinkyB_z, self.pinkyC_z]

        self.x_wrist = [self.wristB_x, self.wristA_x, self.wristC_x, self.wristE_x, self.wristD_x, self.wristB_x]
        self.y_wrist = [self.wristB_y, self.wristA_y, self.wristC_y, self.wristE_y, self.wristD_y, self.wristB_y]
        self.z_wrist = [self.wristB_z, self.wristA_z, self.wristC_z, self.wristE_z, self.wristD_z, self.wristB_z]

        self.middle_index_join_x = [self.middleA_x, self.indexA_x]
        self.middle_index_join_y = [self.middleA_y, self.indexA_y]
        self.middle_index_join_z = [self.middleA_z, self.indexA_z]
        
        # Initial starting positions

        start_thumbA = [self.thumbA_x, self.thumbA_y, self.thumbA_z]
        start_thumbB = [self.thumbB_x, self.thumbB_y, self.thumbB_z]
        start_thumbC = [self.thumbC_x, self.thumbC_y, self.thumbC_z]

        start_indexA = [self.indexA_x, self.indexA_y, self.indexA_z]
        start_indexB = [self.indexB_x, self.indexB_y, self.indexB_z]
        start_indexC = [self.indexC_x, self.indexC_y, self.indexC_z]

        start_middleA = [self.middleA_x, self.middleA_y, self.middleA_z]
        start_middleB = [self.middleB_x, self.middleB_y, self.middleB_z]
        start_middleC = [self.middleC_x, self.middleC_y, self.middleC_z]

        start_ringA = [self.ringA_x, self.ringA_y, self.ringA_z]
        start_ringB = [self.ringB_x, self.ringB_y, self.ringB_z]
        start_ringC = [self.ringC_x, self.ringC_y, self.ringC_z]

        start_pinkyA = [self.pinkyA_x, self.pinkyA_y, self.pinkyA_z]
        start_pinkyB = [self.pinkyB_x, self.pinkyB_y, self.pinkyB_z]
        start_pinkyC = [self.pinkyC_x, self.pinkyC_y, self.pinkyC_z]

        start_wristA = [self.wristA_x, self.wristA_y, self.wristA_z]
        start_wristB = [self.wristB_x, self.wristB_y, self.wristB_z]
        start_wristC = [self.wristC_x, self.wristC_y, self.wristC_z]
        start_wristD = [self.wristD_x, self.wristD_y, self.wristD_z]
        start_wristE = [self.wristE_x, self.wristE_y, self.wristE_z]

        start_positions = np.array([start_thumbA, start_thumbB, start_thumbC, start_indexA, start_indexB, start_indexC,
                            start_middleA, start_middleB, start_middleC, start_ringA, start_ringB, start_ringC,
                            start_pinkyA, start_pinkyB, start_pinkyC, start_wristA, start_wristB, start_wristC,
                            start_wristD, start_wristE])

        print(start_positions)
        # displacement characteristics
        movement = [0, 0.1, -0.8]           # used for segment C
        movement_small = [0, 0.1, 0.04]     # used for segment B
        no_movement = [0, 0, 0]             # used for segment A
        
        # Move three fingers (middle, ring, pinky only B and C)
        start_displacement = np.array([no_movement, no_movement, no_movement, no_movement, no_movement, no_movement, 
                                no_movement, movement_small, movement, no_movement, movement_small, movement,
                                no_movement, movement_small, movement, no_movement, no_movement, no_movement,
                                no_movement, no_movement])
        data = [start_positions]
        for iteration in range(iterations):
            prev_positions = data[-1]
            new_positions = prev_positions + start_displacement
            data.append(new_positions)

        print (data)
        return data

    def animate_scatters(self, iteration, data, scatters):
        """
        Animate plot with generated data
        Args:
            iteration (int) - current iteration of animation
            data (list) - list of data positions of each iteration
            scatters (list) - list of all scatters (1/element)

        Returns:
            list - list of scatter with new coordinates
        """
        for i in range(data[0].shape[0]):
            scatters[i]._offsets3d = (data[iteration][i,0:1], data[iteration][i,1:2], data[iteration][i,2:])
            
            if(i==7):
                x_middleB = data[iteration][i,0:1]
                y_middleB = data[iteration][i,1:2]
                z_middleB = data[iteration][i,2:]
            elif(i==8):
                x_middleC = data[iteration][i,0:1]
                y_middleC = data[iteration][i,1:2]
                z_middleC = data[iteration][i,2:]   

                x_middle_segment = [self.middleA_x, x_middleB, x_middleC]
                y_middle_segment = [self.middleA_y, y_middleB, y_middleC]
                z_middle_segment = [self.middleA_z, z_middleB, z_middleC]
                plt.plot(x_middle_segment, y_middle_segment, z_middle_segment, color='bisque', linestyle='dashed')          #middle 

            elif(i==10):
                x_ringB = data[iteration][i,0:1]
                y_ringB = data[iteration][i,1:2]
                z_ringB = data[iteration][i,2:]
            elif(i==11):
                x_ringC = data[iteration][i,0:1]
                y_ringC = data[iteration][i,1:2]
                z_ringC = data[iteration][i,2:]   

                x_ring_segment = [self.ringA_x, x_ringB, x_ringC]
                y_ring_segment = [self.ringA_y, y_ringB, y_ringC]
                z_ring_segment = [self.ringA_z, z_ringB, z_ringC]
                plt.plot(x_ring_segment, y_ring_segment, z_ring_segment, color='bisque', linestyle='dashed')          #ring          
            elif(i==13):
                x_pinkyB = data[iteration][i,0:1]
                y_pinkyB = data[iteration][i,1:2]
                z_pinkyB = data[iteration][i,2:]
            elif(i==14):
                x_pinkyC = data[iteration][i,0:1]
                y_pinkyC = data[iteration][i,1:2]
                z_pinkyC = data[iteration][i,2:]

                x_pinky_segment = [self.pinkyA_x, x_pinkyB, x_pinkyC]
                y_pinky_segment = [self.pinkyA_y, y_pinkyB, y_pinkyC]
                z_pinky_segment = [self.pinkyA_z, z_pinkyB, z_pinkyC]
                plt.plot(x_pinky_segment, y_pinky_segment, z_pinky_segment, color='bisque', linestyle='dashed')          #pinky 
            else:
                pass

        return scatters
    
    def plot_data(self, data):
        matplotlib.use("TkAgg")         # Mac animation dependency issue
        fig = plt.figure()
        ax = p3.Axes3D(fig)

        # Initialize scatters
        scatters = [ ax.scatter(data[0][i,0:1], data[0][i,1:2], data[0][i,2:], c='skyblue', s=60) for i in range(data[0].shape[0])]

        # stationary segments
        plt.plot(self.x_thumb,self.y_thumb,self.z_thumb, color='orange')          #thumb 
        plt.plot(self.x_index, self.y_index, self.z_index, color='orange')          #index

        self.x_palm_segment = [self.wristB_x, self.pinkyA_x, self.ringA_x, self.middleA_x]  #palm
        self.y_palm_segment = [self.wristB_y, self.pinkyA_y, self.ringA_y, self.middleA_y]
        self.z_palm_segment = [self.wristB_z, self.pinkyA_z, self.ringA_z, self.middleA_z]
        plt.plot(self.x_palm_segment, self.y_palm_segment, self.z_palm_segment, color='orange')          #palm

        plt.plot(self.x_wrist, self.y_wrist, self.z_wrist, color='orange')                   #wrist
        plt.plot(self.middle_index_join_x, self.middle_index_join_y, self.middle_index_join_z, color='orange')

        plt.plot(self.x_middle, self.y_middle, self.z_middle, color='orange')          #lines between points
        plt.plot(self.x_ring, self.y_ring, self.z_ring, color='orange')          #lines between points
        plt.plot(self.x_pinky, self.y_pinky, self.z_pinky, color='orange')          #lines between points

        # Number of iterations
        iterations = len(data)

        # Axis limits
        ax.set_xlim(-10, 5)
        ax.set_ylim(-10, 18)
        ax.set_zlim(-10, 12)

        # Labels
        plt.title('Finger Position Simulation')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')

        # Starting angle
        ax.view_init(25, 10)
        
        ani = animation.FuncAnimation(plt.gcf(), self.animate_scatters, iterations, fargs=(data, scatters),
                                       interval=1, blit=False, repeat=True)   

        plt.show()     




if __name__ == "__main__":
    ah = AnimatedHand()