from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import positionsDB as pdb
import time

class HandPlot():
    def __init__(self):
        self.get_user_input()

    def get_user_input(self):
        user_position_choice = int(input("Enter position number: "))
        self.get_values_from_db(user_position_choice)
    
    def get_values_from_db(self, position_number):
        if (position_number == 1):
            desired_position = pdb.position1
        elif (position_number == 2):
            desired_position = pdb.position2
        elif (position_number == 3):
            desired_position = pdb.position3
        else:
            print("Invalid. Try another number.")
            self.get_user_input()
        self.get_sensor_data(desired_position)
        return

    def get_sensor_data(self, desired_position):
        # Thumb
        self.thumbA_x = desired_position['thumbA'][0]
        self.thumbA_y = desired_position['thumbA'][1]
        self.thumbA_z = desired_position['thumbA'][2]
        self.thumbB_x = desired_position['thumbB'][0]
        self.thumbB_y = desired_position['thumbB'][1]
        self.thumbB_z = desired_position['thumbB'][2]
        self.thumbC_x = desired_position['thumbC'][0]
        self.thumbC_y = desired_position['thumbC'][1]
        self.thumbC_z = desired_position['thumbC'][2]

        # Index
        self.indexA_x = desired_position['indexA'][0]
        self.indexA_y = desired_position['indexA'][1]
        self.indexA_z = desired_position['indexA'][2]
        self.indexB_x = desired_position['indexB'][0]
        self.indexB_y = desired_position['indexB'][1]
        self.indexB_z = desired_position['indexB'][2]
        self.indexC_x = desired_position['indexC'][0]
        self.indexC_y = desired_position['indexC'][1]
        self.indexC_z = desired_position['indexC'][2]

        # Middle
        self.middleA_x = desired_position['middleA'][0]
        self.middleA_y = desired_position['middleA'][1]
        self.middleA_z = desired_position['middleA'][2]
        self.middleB_x = desired_position['middleB'][0]
        self.middleB_y = desired_position['middleB'][1]
        self.middleB_z = desired_position['middleB'][2]
        self.middleC_x = desired_position['middleC'][0]
        self.middleC_y = desired_position['middleC'][1]
        self.middleC_z = desired_position['middleC'][2]

        # Ring
        self.ringA_x = desired_position['ringA'][0]
        self.ringA_y = desired_position['ringA'][1]
        self.ringA_z = desired_position['ringA'][2]
        self.ringB_x = desired_position['ringB'][0]
        self.ringB_y = desired_position['ringB'][1]
        self.ringB_z = desired_position['ringB'][2]
        self.ringC_x = desired_position['ringC'][0]
        self.ringC_y = desired_position['ringC'][1]
        self.ringC_z = desired_position['ringC'][2]

        # Pinky
        self.pinkyA_x = desired_position['pinkyA'][0]
        self.pinkyA_y = desired_position['pinkyA'][1]
        self.pinkyA_z = desired_position['pinkyA'][2]
        self.pinkyB_x = desired_position['pinkyB'][0]
        self.pinkyB_y = desired_position['pinkyB'][1]
        self.pinkyB_z = desired_position['pinkyB'][2]
        self.pinkyC_x = desired_position['pinkyC'][0]
        self.pinkyC_y = desired_position['pinkyC'][1]
        self.pinkyC_z = desired_position['pinkyC'][2]

        # Wrist
        self.wristA_x = desired_position['wristA'][0]
        self.wristA_y = desired_position['wristA'][1]
        self.wristA_z = desired_position['wristA'][2]
        self.wristB_x = desired_position['wristB'][0]
        self.wristB_y = desired_position['wristB'][1]
        self.wristB_z = desired_position['wristB'][2]
        self.wristC_x = desired_position['wristC'][0]
        self.wristC_y = desired_position['wristC'][1]
        self.wristC_z = desired_position['wristC'][2]
        self.wristD_x = desired_position['wristD'][0]
        self.wristD_y = desired_position['wristD'][1]
        self.wristD_z = desired_position['wristD'][2]
        self.wristE_x = desired_position['wristE'][0]
        self.wristE_y = desired_position['wristE'][1]
        self.wristE_z = desired_position['wristE'][2]

        self.format_data_for_plot()
        return

    def format_data_for_plot(self):
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

        self.plot_data()
        return

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
        self.get_user_input()

    def update_plot(self):
        pass



if __name__ == "__main__":
    hp = HandPlot()