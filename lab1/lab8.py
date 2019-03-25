from pyCreate2 import create2
import lab8_map
import math
import odometry
import partical_filter as partf

class Run:
    def __init__(self, factory):
        """Constructor.

        Args:
            factory (factory.FactoryCreate)
        """
        self.create = factory.create_create()
        self.time = factory.create_time_helper()
        self.servo = factory.create_servo()
        self.sonar = factory.create_sonar()
        # Add the IP-address of your computer here if you run on the robot
        self.virtual_create = factory.create_virtual_create()
        self.map = lab8_map.Map("lab8_map.json")
        self.pf = partf.ParticleFilter()
        self.create = factory.create_create()
        self.odometry = odometry.Odometry()

    def run(self):
        self.create.start()
        self.create.safe()

        # request sensors
        self.create.start_stream([
            create2.Sensor.LeftEncoderCounts,
            create2.Sensor.RightEncoderCounts,
        ])

        # This is an example on how to visualize the pose of our estimated position
        # where our estimate is that the robot is at (x,y,z)=(0.5,0.5,0.1) with heading pi
        self.virtual_create.set_pose((0.5, 0.5, 0.1), 0)

        # This is an example on how to show particles
        # the format is x,y,z,theta,x,y,z,theta,...
        data = [0.5, 0.5, 0.1, math.pi/2, 1.5, 1, 0.1, 0]
        # self.virtual_create.set_point_cloud(data)
        self.virtual_create.set_point_cloud(self.pf.p_List)

        # This is an example on how to estimate the distance to a wall for the given
        # map, assuming the robot is at (0, 0) and has heading math.pi
        # print(self.map.closest_distance((0.5,0.5), 0))

        # This is an example on how to detect that a button was pressed in V-REP

        while True:
            state = self.create.update()
            if state is not None:
                self.odometry.update(state.leftEncoderCounts, state.rightEncoderCounts)
            b = self.virtual_create.get_last_button()
            if b == self.virtual_create.Button.MoveForward:
                print("Forward pressed!")
                self.create.drive_direct(100, 100)
                self.time.sleep(1.08)
                self.create.drive_direct(0, 0)
                self.time.sleep(.01)
                self.pf.Movement("Move Foward")
                self.virtual_create.set_point_cloud(self.pf.p_List)
            elif b == self.virtual_create.Button.TurnLeft:
                print("Turn Left pressed!")
                self.create.drive_direct(100, -100)
                self.time.sleep(1)
                self.create.drive_direct(0, 0)
                self.time.sleep(.01)
                print(self.odometry.theta)
                self.pf.Movement("Turn Left")
                self.virtual_create.set_point_cloud(self.pf.p_List)
            elif b == self.virtual_create.Button.TurnRight:
                print("Turn Right pressed!")
                self.create.drive_direct(-100, 100)
                self.time.sleep(1)
                self.create.drive_direct(0, 0)
                self.time.sleep(.01)
                print(self.odometry.theta)
                self.pf.Movement("Turn Right")
                self.virtual_create.set_point_cloud(self.pf.p_List)
            elif b == self.virtual_create.Button.Sense:
                print("Sense pressed!")
                distance = self.sonar.get_distance()
                self.pf.Sensing(distance)
                self.virtual_create.set_point_cloud(self.pf.p_List)

            self.time.sleep(0.01)
