from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import positionsDB as pdb
import time

class HandPlot():
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

        self.format_data_for_plot()

    def format_data_for_plot(self):
        self.x_thumb = [self.thumbA_x, self.thumbB_x, self.thumbC_x]
        print(self.x_thumb)
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

        self.plot_data()

    def plot_data(self):
        fig3d = plt.figure()
        ax = fig3d.add_subplot(1,1,1, projection='3d')

        ax.set_xlim(-10, 5)
        ax.set_ylim(-10, 18)
        ax.set_zlim(-10, 12)

        ax.scatter(self.x_thumb,self.y_thumb,self.z_thumb, c='r',s=100, label='True Position')      #points
        plt.plot(self.x_thumb,self.y_thumb,self.z_thumb, color='r')          #lines between points

        ax.scatter(self.x_index, self.y_index, self.z_index, color='r', s=100)     #points
        plt.plot(self.x_index, self.y_index, self.z_index, color='r')          #lines between points

        ax.scatter(self.x_middle, self.y_middle, self.z_middle, color='r', s=100)     #points
        plt.plot(self.x_middle, self.y_middle, self.z_middle, color='r')          #lines between points

        ax.scatter(self.x_ring, self.y_ring, self.z_ring, color='r', s=100)     #points
        plt.plot(self.x_ring, self.y_ring, self.z_ring, color='r')          #lines between points

        ax.scatter(self.x_pinky, self.y_pinky, self.z_pinky, color='r', s=100)     #points
        plt.plot(self.x_pinky, self.y_pinky, self.z_pinky, color='r')          #lines between points

        ax.scatter(self.x_wrist, self.y_wrist, self.z_wrist, color='r', s=100)     #points
        plt.plot(self.x_wrist, self.y_wrist, self.z_wrist, color='r')          #lines between points

        plt.plot(self.middle_index_join_x, self.middle_index_join_y, self.middle_index_join_z, color='r')

        plt.title('Finger Position Simulation')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        #self.update_plot()

        #ani = plt.animation.FuncAnimation(plt.gcf(), self.update_plot, 19, 
        #                       interval=500, blit=False)


        plt.show()

    def update_plot(self):
        pass



if __name__ == "__main__":
    hp = HandPlot()