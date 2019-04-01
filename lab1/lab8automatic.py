from pyCreate2 import create2
import lab8_map
import math
import odometry
import partical_filter as partf


class Run:
    BASE_TIME = 1
    BASE_SPEED = 100

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
        self.virtual_create = factory.create_virtual_create("128.125.148.61")
        self.map = lab8_map.Map("lab8_map.json")
        self.pf = partf.ParticleFilter()
        self.create = factory.create_create()
        self.odometry = odometry.Odometry()

    def left(self):
        old_theta = self.odometry.theta
        self.create.drive_direct(self.BASE_SPEED, -self.BASE_SPEED)
        end_time = self.time.time() + self.BASE_TIME
        while self.time.time() < end_time:
            state = self.create.update()
            if state is not None:
                self.odometry.update(state.leftEncoderCounts, state.rightEncoderCounts)
        self.create.drive_direct(0, 0)
        self.pf.Movement(0, self.odometry.theta - old_theta, True)

    def right(self):
        old_theta = self.odometry.theta
        self.create.drive_direct(-self.BASE_SPEED, self.BASE_SPEED)
        end_time = self.time.time() + self.BASE_TIME
        while self.time.time() < end_time:
            state = self.create.update()
            if state is not None:
                self.odometry.update(state.leftEncoderCounts, state.rightEncoderCounts)
        self.create.drive_direct(0, 0)
        self.pf.Movement(0, self.odometry.theta - old_theta, True)

    def forward(self):
        self.create.drive_direct(self.BASE_SPEED, self.BASE_SPEED)
        end_time = self.time.time() + self.BASE_TIME
        while self.time.time() < end_time:
            state = self.create.update()
            if state is not None:
                self.odometry.update(state.leftEncoderCounts, state.rightEncoderCounts)
        self.create.drive_direct(0, 0)
        self.pf.Movement(self.BASE_SPEED * self.BASE_TIME / 1000, self.odometry.theta, False)

    def update_particles(self):
        p_List = []
        for x in range(self.pf.num_particles):
            p_List.append(self.pf.Particle_List[x].x)
            p_List.append(self.pf.Particle_List[x].y)
            p_List.append(0)
            p_List.append(self.pf.Particle_List[x].theta)
        return p_List

    def run(self):
        self.create.start()
        self.create.safe()

        self.odometry.theta = 0
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
            self.virtual_create.set_point_cloud(self.update_particles())

            b = self.virtual_create.get_last_button()
            if b == self.virtual_create.Button.MoveForward:
                self.forward()
            elif b == self.virtual_create.Button.TurnLeft:
                self.left()
            elif b == self.virtual_create.Button.TurnRight:
                self.right()
            elif b == self.virtual_create.Button.Sense:
                pos = []
                distance = self.sonar.get_distance()
                pos, theta = self.pf.Sensing(distance)
                self.virtual_create.set_pose(pos, theta)
                err = pow(self.odometry.x - pos[0], 2) + pow(self.odometry.y - pos[1], 2)
                print(math.sqrt(err))
                if math.sqrt(err) < 0.8:
                    print("Complete")
                    break

            self.time.sleep(0.01)
