"""
Sample Code for Lab3
Use "run.py [--sim] lab3" to execute
"""

from pyCreate2 import create2
import math
import numpy as np

# if on the robot, don't use X backend
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle


class Run:
    def __init__(self, factory):
        """Constructor.

        Args:
            factory (factory.FactoryCreate)
        """
        self.create = factory.create_create()
        self.time = factory.create_time_helper()
        self.create.start()
        self.create.safe()

        # request sensors
        self.create.start_stream([
            create2.Sensor.LeftEncoderCounts,
            create2.Sensor.RightEncoderCounts,
        ])
        state = self.create.update()
        self.leftEncoderCount = state.leftEncoderCounts
        self.rightEncoderCount = state.rightEncoderCounts

        self.x = 0
        self.y = 0
        self.theta = 0
        self.result = np.empty((0, 5))

    def checkTime(self):
        state = self.create.update()
        if state is not None:
            leftE = state.leftEncoderCounts - self.leftEncoderCount
            rightE = state.rightEncoderCounts - self.rightEncoderCount
            if (abs(leftE) > 2000):
                leftE += pow(2, 16)
            if (abs(rightE) > 2000):
                rightE += pow(2, 16)
            leftRev = leftE / 508.8
            rightRev = rightE / 508.8
            leftD = leftRev * 226.1946  # deltaL
            rightD = rightRev * 226.1946  # deltaR
            totalD = (leftD + rightD) / 2  # D
            theta = (rightD - leftD) / 235  # theta
            xDist = totalD * math.cos(self.theta)
            yDist = totalD * math.sin(self.theta)

            # update odometry coordinates
            self.x += xDist
            self.y += yDist
            self.theta += theta
            print(str(self.x) + ", " + str(self.y) + ", " + str(self.theta))

            # udpate actual ground truth coordinates
            ground_truth = self.create.sim_get_position()
            new_row = [self.time.time(), self.x/1000, self.y/1000, ground_truth[0], ground_truth[1]]
            self.result = np.vstack([self.result, new_row])

            # update encoder counts for the time period
            self.leftEncoderCount = state.leftEncoderCounts
            self.rightEncoderCount = state.rightEncoderCounts

    def run(self):

        self.create.drive_direct(300, 300)
        while (self.x <  998):
            self.checkTime()

        self.create.drive_direct(-300, 300)
        while (self.theta >  -math.pi/2):
            self.checkTime()

        self.create.drive_direct(300, 300)
        while (self.y > -498):
            self.checkTime()

        self.create.drive_direct(-300, 300)
        while (self.theta > -math.pi):
            self.checkTime()

        self.create.drive_direct(300, 300)
        while (self.x > 0):
            self.checkTime()

        self.create.drive_direct(-300, 300)
        while (self.theta >  -1.5*math.pi):
            self.checkTime()

        self.create.drive_direct(300, 300)
        while (self.y < 0):
            self.checkTime()

        # plot the odometry and ground truth measurements
        plt.title("position")
        plt.plot(self.result[:,1], self.result[:,2], label="odometry")
        plt.plot(self.result[:,3], self.result[:,4], label="ground truth")
        plt.grid()
        plt.legend()
        plt.savefig("Hmwrk2_positions_300.png") # make sure to not overwrite plots








