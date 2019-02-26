from pyCreate2 import create2
import math
import numpy as np

# if on the robot, don't use X backend
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import odometry
import pd_controller2
import pid_controller


class Run:
    def __init__(self, factory):
        self.create = factory.create_create()
        self.time = factory.create_time_helper()
        self.sonar = factory.create_sonar()
        self.servo = factory.create_servo()
        self.odometry = odometry.Odometry()
        self.pdTheta = pd_controller2.PDController(500, 100, -200, 200)
        self.pd_controller = pd_controller2.PDController(1000, 100, -85, 85, is_angle=True)
        self.pidTheta = pid_controller.PIDController(300, 5, 50, [-10, 10], [-200, 200], is_angle=True)
        self.pidDistance = pid_controller.PIDController(1000, 0, 50, [0, 0], [-200, 200], is_angle=False)

    def run(self):
        self.create.start()
        self.create.safe()

        # request sensors
        self.create.start_stream([
            create2.Sensor.LeftEncoderCounts,
            create2.Sensor.RightEncoderCounts,
        ])
        # self.servo.go_to(70)
        goal_distance = 0.5
        base_speed = 200

        waypoints = [
            [2.0, 0.0],
            [3.0, 2.0],
            [2.5, 2.0],
            [0.0, 1.5],
            [0.0, 0.0]
        ]
        index = 0

        goal_x = waypoints[index][0]
        goal_y = waypoints[index][1]
        previous_distance = .5
        cont = 0

        # rotate robot to theta and update x,y as moving
        # goal theta is dependent on current xy and goal xy

        # change result plot for the #4 has 5 data points, not 3
        result = np.empty((0,5))
        end_time = self.time.time() + 300
        avoid_time = self.time.time()
        while self.time.time() < end_time:
            state = self.create.update()
            if state is not None:
                # update odometry and sonar
                self.odometry.update(state.leftEncoderCounts, state.rightEncoderCounts)
                goal_theta = math.atan2(goal_y-self.odometry.y, goal_x-self.odometry.x)
                distance = self.sonar.get_distance()

                # check to see if the robot is at its goal
                check = (abs(goal_y)-abs(self.odometry.y) + abs(goal_x)-abs(self.odometry.x))
                if abs(check) < .075:
                    index += 1
                    if index == 4:
                        break
                    # update the robots new goal
                    goal_x = waypoints[index][0]
                    goal_y = waypoints[index][1]
                    print(goal_x)
                    print(goal_y)

                print("[%.6f, %.6f, %.6f]" % (self.odometry.x, self.odometry.y, math.degrees(self.odometry.theta)))
                new_row = [self.time.time(), math.degrees(self.odometry.theta), math.degrees(goal_theta),
                            self.odometry.x, self.odometry.y]
                result = np.vstack([result, new_row])
                # print(goal_theta)
                # print(self.odometry.theta)

                # determine how to control the robot based on obstacle presence
                if distance < .5:
                    avoid_time = self.time.time() + 3

                    self.servo.go_to(77)
                    output = self.pd_controller.update(distance, goal_distance, self.time.time())
                    self.create.drive_direct(int(base_speed - output), int(base_speed + output))

                elif avoid_time > self.time.time() and math.degrees(self.odometry.theta) - math.degrees(goal_theta) < 60:

                    output = self.pd_controller.update(distance, goal_distance, self.time.time())
                    self.create.drive_direct(int(base_speed - output), int(base_speed + output))
                    self.servo.go_to(77)

                else:
                    # call controller's update function
                    self.servo.go_to(-10)
                    output = self.pidTheta.update(self.odometry.theta, goal_theta, self.time.time())
                    # self.create.drive_direct(int(base_speed + output), int(base_speed - output))
                    distance = math.sqrt(math.pow(goal_x - self.odometry.x, 2) + math.pow(goal_y - self.odometry.y, 2))
                    output_distance = self.pidDistance.update(0, distance, self.time.time())
                    self.create.drive_direct(int(output + output_distance), int(-output + output_distance))

                # call the self.create.drive_direct(left, right) here





        # plotting for go-to-angle goal_theta:
        # plt.title("Angle")
        # plt.plot(result[:,0], result[:,1], label="odometry")
        # plt.plot(result[:,0], result[:,2], label="goal")
        # plt.grid()
        # plt.legend()
        # plt.savefig("lab6_angle.png") # make s ure to not overwrite plots

        # plotting for go-to-goal (goal_x, goal_x):
        plt.figure()
        plt.plot(result[:, 3], result[:, 4])
        plt.scatter([2], [0], color="r", s=40, label="goal1")
        plt.scatter([3], [2], color="r", s=40, label="goal2")
        plt.scatter([2.5], [2], color="r", s=40, label="goal3")
        plt.scatter([0], [1.5], color="r", s=40, label="goal4")
        plt.scatter([0], [0], color="r", s=40, label="goal5")
        plt.savefig("lab7_avoid.png")
