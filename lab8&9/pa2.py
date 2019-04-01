"""
Code for PA2
Use "run.py [--sim] pa2" to execute
"""
import math
import random

class Run:
    def __init__(self, factory):
        """Constructor.

        Args:
            factory (factory.FactorySimulation)
        """
        self.arm = factory.create_kuka_lbr4p()
        self.time = factory.create_time_helper()
        self.x = 0
        self.y = 1.168
        self.l1 = .2
        self.l2 = .2

    # joint2 for forward kinematics is the origin [0,0,0]
    # distance between all joints is 0.2M

    def run(self):
        self.arm.go_to(4, -math.pi/2)
        self.arm.go_to(5, math.pi/2)
        self.time.sleep(2)

        # # forward kinematics
        # self.forward_kinematics()
        #
        # # inverse kinematics at same points as forward kinematics
        # pos_array = [(0, .28), (-.2, .2), (0, .4), (-.3414,.1414)]
        # self.inverse_kinematics(pos_array, self.l1, self.l2)
        #
        # # go to corners of rectangle
        # pos_array = [(-.25, .2), (.25, .2), (.25, .3), (-.25, .3)]
        # self.rectangle_attempt1(pos_array, self.l1, self.l2)
        #
        # # create a better rectangle with straight lines
        # pos_array = [(-.25, .2), (.25, .2), (.25, .3), (-.25, .3)]
        # self.rectangle_attempt2(pos_array, self.l1, self.l2)

        # create a triangle
        pos_array = [(-.25, .2), (.25, .2), (0, .4)]
        self.triangle(pos_array, self.l1, self.l2)

    def angle_math(self, t1, t2):
        z = self.l1 * math.cos(t1) + self.l2 * math.cos(t1+t2)
        x = self.l1 * math.sin(t1) + self.l2 * math.sin(t1+t2)
        return -x, z

    def paint(self):
        self.arm.set_color(random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1))
        self.arm.enable_painting()
        self.time.sleep(2)
        self.arm.disable_painting()

    def forward_kinematics(self):

        print("Using joint 2 ( range -120 to 240 degrees )")
        print("Using joint 4 ( range -120 to 240 degrees )")

        x, z = self.angle_math(math.radians(45), math.radians(-90))
        print("Go to 45, -90 deg, FK: [%.4f, 0, %.4f]" % (x, z))
        self.arm.go_to(1, math.radians(45))
        self.arm.go_to(3, math.radians(-90))
        self.time.sleep(4)
        self.paint()

        x, z = self.angle_math(math.radians(0), math.radians(90))
        print("Go to -45, 90 deg, FK: [%.4f, 0, %.4f]" % (x, z))
        self.arm.go_to(1, math.radians(0))
        self.arm.go_to(3, math.radians(90))
        self.time.sleep(4)
        self.paint()

        x, z = self.angle_math(math.radians(0), math.radians(0))
        print("Go to 0, 0 deg, FK: [%.4f, 0, %.4f]" % (x, z))
        self.arm.go_to(1, math.radians(0))
        self.arm.go_to(3, math.radians(0))
        self.time.sleep(4)
        self.paint()

        x, z = self.angle_math(math.radians(45), math.radians(45))
        print("Go to 45, 0 deg, FK: [%.4f, 0, %.4f]" % (x, z))
        self.arm.go_to(1, math.radians(45))
        self.arm.go_to(3, math.radians(45))
        self.time.sleep(4)
        self.paint()

        self.time.sleep(10)

    def inverse_kinematics(self, position_array, l1, l2):
        for pos in position_array:
            r = pow(pos[0], 2) + pow(pos[1], 2)
            alpha = math.acos((pow(l1, 2) + pow(l2, 2) - r) / (2 * l1 * l2))
            beta = math.acos((r + pow(l1, 2) - pow(l2, 2)) / (2 * l1 * math.sqrt(r)))
            theta1 = math.atan2(pos[1], pos[0]) + beta
            theta2 = math.pi - alpha
            print("Go to[%.2f, %.2f], IK: [%.4f, 0, %.4f]" % (pos[0], pos[1], theta1, theta2))
            self.arm.go_to(1, theta1 - math.pi/2)
            self.arm.go_to(3, -theta2)
            self.time.sleep(5)
            self.paint()

    def go_to(self, position_array, l1, l2):
        for pos in position_array:
            r = pow(pos[0], 2) + pow(pos[1], 2)
            alpha = math.acos((pow(l1, 2) + pow(l2, 2) - r) / (2 * l1 * l2))
            beta = math.acos((r + pow(l1, 2) - pow(l2, 2)) / (2 * l1 * math.sqrt(r)))
            theta1 = math.atan2(pos[1], pos[0]) + beta
            theta2 = math.pi - alpha
            # print(math.degrees(theta1), math.degrees(theta2))
            self.arm.go_to(1, theta1 - math.pi/2)
            self.arm.go_to(3, -theta2)
            self.time.sleep(2)

    def rectangle_attempt1(self, position_array, l1, l2):
        self.arm.enable_painting()
        for pos in position_array:
            r = pow(pos[0], 2) + pow(pos[1], 2)
            alpha = math.acos((pow(l1, 2) + pow(l2, 2) - r) / (2 * l1 * l2))
            beta = math.acos((r + pow(l1, 2) - pow(l2, 2)) / (2 * l1 * math.sqrt(r)))
            theta1 = math.atan2(pos[1], pos[0]) + beta
            theta2 = math.pi - alpha
            # print(math.degrees(theta1), math.degrees(theta2))
            self.arm.go_to(1, theta1 - math.pi/2)
            self.arm.go_to(3, -theta2)
            self.arm.enable_painting()
            self.time.sleep(5)

    def rectangle_attempt2(self, position_array, l1, l2):
        array = []
        array.append(position_array[0])
        self.go_to(array, l1, l2)
        x = 0
        j = 1
        for pos in position_array:
            if x == 3:
                j= -3

            xgap = (position_array[x+j][0] - position_array[x][0])/20
            ygap = (position_array[x+j][1] - position_array[x][1])/20
            self.arm.set_color(random.uniform(0,1), random.uniform(0,1), random.uniform(0,1))
            for i in range(20):
                xpos = pos[0] + i*xgap
                ypos = pos[1] + i*ygap
                r = pow(xpos, 2) + pow(ypos, 2)

                alpha = math.acos((pow(l1, 2) + pow(l2, 2) - r) / (2 * l1 * l2))
                beta = math.acos((r + pow(l1, 2) - pow(l2, 2)) / (2 * l1 * math.sqrt(r)))
                theta1 = math.atan2(ypos, xpos) + beta
                theta2 = math.pi - alpha
                # print(math.degrees(theta1), math.degrees(theta2))
                self.arm.go_to(1, theta1 - math.pi/2)
                self.arm.go_to(3, -theta2)
                self.time.sleep(.5)
                self.arm.enable_painting()
            x +=1

    def triangle(self, position_array, l1, l2):
        array = []
        array.append(position_array[0])
        self.go_to(array,l1,l2)
        x = 0
        j = 1
        for pos in position_array:
            if x == 2:
                j =-2

            xgap = (position_array[x + j][0] - position_array[x][0]) / 20
            ygap = (position_array[x + j][1] - position_array[x][1]) / 20
            self.arm.set_color(random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1))
            for i in range(20):
                xpos = pos[0] + i * xgap
                ypos = pos[1] + i * ygap
                r = pow(xpos, 2) + pow(ypos, 2)

                alpha = math.acos((pow(l1, 2) + pow(l2, 2) - r) / (2 * l1 * l2))
                beta = math.acos((r + pow(l1, 2) - pow(l2, 2)) / (2 * l1 * math.sqrt(r)))
                theta1 = math.atan2(ypos, xpos) + beta
                theta2 = math.pi - alpha
                # print(math.degrees(theta1), math.degrees(theta2))
                self.arm.go_to(1, theta1 - math.pi / 2)
                self.arm.go_to(3, -theta2)
                self.time.sleep(.5)
                self.arm.enable_painting()
            x += 1


