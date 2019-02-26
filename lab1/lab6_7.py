from pyCreate2 import create2
import math
import numpy as np

# if on the robot, don't use X backend
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import odometry
import pd_controller
import pid_controller


class Run:
    def __init__(self, factory):
        self.create = factory.create_create()
        self.time = factory.create_time_helper()
        self.sonar = factory.create_sonar()
        self.servo = factory.create_servo()
        self.odometry = odometry.Odometry()
        self.pdTheta = pd_controller.PDController(500, 100, -200, 200)
        # self.pd_controller = pd_controller.PDController(1000, 100, -75, 75)
        self.pidTheta = pid_controller.PIDController(500, 100, 50, -200, 200, -100, 100)
        # self.pidVelocity = pid_controller.PIDController(500, 100, 100, -50, 50, -50, 50)

    def run(self):
        self.create.start()
        self.create.safe()

        # request sensors
        self.create.start_stream([
            create2.Sensor.LeftEncoderCounts,
            create2.Sensor.RightEncoderCounts,
        ])

        # goal_theta = -math.pi/2
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

        # rotate robot to theta and update x,y as moving
        # goal theta is dependent on current xy and goal xy

        # change result plot for the #4 has 5 data points, not 3
        result = np.empty((0,5))
        end_time = self.time.time() + 200
        avoid_time = self.time.time()
        while self.time.time() < end_time:
            state = self.create.update()
            if state is not None:
                # update odometry and sonar
                self.odometry.update(state.leftEncoderCounts, state.rightEncoderCounts)
                goal_theta = math.atan2(goal_y-self.odometry.y, goal_x-self.odometry.x)
                distance = self.sonar.get_distance()
                print(distance)

                # check to see if the robot is at its goal
                check = (abs(goal_y)-abs(self.odometry.y) + abs(goal_x)-abs(self.odometry.x))
                if abs(check) < .005:
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
                if distance < 0.5 or avoid_time > self.time.time():
                    # need to avoid the robot for extra time since sensor straight forward
                    avoid_time = self.time.time() + 2
                    # output is based on the distance from the obstacle, could make a controller
                    output = 50/distance
                else:
                    # call controller's update function
                    output = self.pidTheta.update(self.odometry.theta, goal_theta, self.time.time())

                # call the self.create.drive_direct(left, right) here
                self.create.drive_direct(int(base_speed + output), int(base_speed - output))




        # plotting for go-to-angle goal_theta:
        # plt.title("Angle")
        # plt.plot(result[:,0], result[:,1], label="odometry")
        # plt.plot(result[:,0], result[:,2], label="goal")
        # plt.grid()
        # plt.legend()
        # plt.savefig("lab6_angle.png") # make s ure to not overwrite plots

        # plotting for go-to-goal (goal_x, goal_x):
        plt.figure()
        f, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
        ax1.set_title("Angle")
        ax1.plot(result[:,0], result[:,1], label="odometry")
        ax1.plot(result[:,0], result[:,2], label="goal")
        ax1.grid()
        ax1.legend()

        ax2.set_title("Position")
        ax2.plot(result[:,3], result[:,4], label="odometry")
        ax2.scatter([2], [0], color="r", s=40, label="goal1")
        ax2.scatter([3], [2], color="r", s=40, label="goal2")
        ax2.scatter([2.5], [2], color="r", s=40, label="goal3")
        ax2.scatter([0], [1.5], color="r", s=40, label="goal4")
        ax2.scatter([0], [0], color="r", s=40, label="goal5")
        ax2.axis("equal")
        ax2.grid()
        ax2.legend()
        plt.savefig("lab6_position_avoid.png")
