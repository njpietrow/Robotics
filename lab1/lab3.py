"""
Sample Code for Lab3
Use "run.py [--sim] lab3" to execute
"""

from pyCreate2 import create2
import time
import math

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
        # leftRev = self.leftEncoderCount/508.8
        # rightRev = self.rightEncoderCount/508.8
        # leftD = leftRev*226.1946 #deltaL
        # rightD = rightRev*226.1946 #deltaR
        # totalD = (leftD + rightD)/2 #D
        # self.theta = (rightD - leftD)/235 #theta
        # self.x = totalD*math.cos(self.theta)
        # self.y = totalD*math.sin(self.theta)
        self.x =0
        self.y =0
        self.theta =0

        self.xstart=0
        self.ystart =0
        self.thetastart =0

    def initialCheck(self):
        state = self.create.update()

    def checkTime(self):
        state = self.create.update()
        if state is not None:
            leftE = state.leftEncoderCounts - self.leftEncoderCount
            rightE = state.rightEncoderCounts - self.rightEncoderCount
            if(abs(leftE)>2000):
                leftE += pow(2,16)
            if(abs(rightE)>2000):
                rightE += pow(2,16)
            leftRev = leftE/508.8
            rightRev = rightE/508.8
            leftD = leftRev*226.1946 #deltaL
            rightD = rightRev*226.1946 #deltaR
            totalD = (leftD + rightD)/2 #D
            theta = (rightD - leftD)/235 #theta
            xDist = totalD*math.cos(self.theta)
            yDist = totalD*math.sin(self.theta)
            self.x += xDist
            self.y += yDist
            self.theta += theta
            print(str(self.x) + ", " + str(self.y) + ", " + str(self.theta))

            self.leftEncoderCount = state.leftEncoderCounts
            self.rightEncoderCount = state.rightEncoderCounts



    def run(self):

        # check = time.time() + 10    
        # self.create.drive_direct(100,100)
        # while (time.time() < check):
        #     self.checkTime()

        # check = time.time() + 1.5  
        # self.create.drive_direct(-100,100)
        # while (time.time() < check):
        #     self.checkTime()

        # check = time.time() + 10  
        # self.create.drive_direct(100,100)
        # while (time.time() < check):
        #     self.checkTime()

        # check = time.time() + 1.5    
        # self.create.drive_direct(-100,100)
        # while (time.time() < check):
        #     self.checkTime()

        # check = time.time() + 10  
        # self.create.drive_direct(100,100)
        # while (time.time() < check):
        #     self.checkTime()

        # check = time.time() + 1.5  
        # self.create.drive_direct(-100,100)
        # while (time.time() < check):
        #     self.checkTime()

        # check = time.time() + 10  
        # self.create.drive_direct(100,100)
        # while (time.time() < check):
        #     self.checkTime()

        # check = time.time() + 1.5  
        # self.create.drive_direct(-100,100)
        # while (time.time() < check):
        #     self.checkTime()

        self.create.drive_direct(200,200)
        while (self.x < self.xstart + 998):
            self.checkTime()

        self.create.drive_direct(-200,200)
        while (self.theta > self.thetastart -1.5708):
            self.checkTime()

        self.create.drive_direct(200,200)
        while (self.y > self.ystart -998):
            self.checkTime()

        self.create.drive_direct(-200,200)
        while (self.theta > self.thetastart -2*1.5708):
            self.checkTime()

        self.create.drive_direct(200,200)
        while (self.x > self.xstart):
            self.checkTime()

        self.create.drive_direct(-200,200)
        while (self.theta > self.thetastart -3*1.5708):
            self.checkTime()

        self.create.drive_direct(200,200)
        while (self.y < self.ystart):
            self.checkTime()


     




