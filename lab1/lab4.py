from p_controller import PController
from pd_controller import PDController
import time
class Run:
    def __init__(self, factory):
        self.create = factory.create_create()
        self.time = factory.create_time_helper()
        self.sonar = factory.create_sonar()
        self.servo = factory.create_servo()
        # define the gains here
        self.kp = 300
        self.kd = 3
        self.minOutput = -500
        self.maxOutput = 500
        # instantiate your controllers here
        #self.p_controller = PController(self.kp, self.minOutput, self.maxOutput)
        self.pd_controller = PDController(self.kp, self.kd, self.minOutput, self.maxOutput)


    def run(self):
        self.create.start()
        self.create.safe()

        self.servo.go_to(70)
        self.time.sleep(3)

        goal_distance = 0.5
        base_speed = 100

        prev_time = time.time()
        prev_distance = goal_distance

        while True:
            distance = self.sonar.get_distance()
            if distance is not None:
                print(distance)

                change_time = time.time() - prev_time
                change_distance = distance - prev_distance
                vX, vY = self.pd_controller.update(distance, base_speed, goal_distance, change_distance, change_time)
                # vX, vY = self.p_controller.update(distance, base_speed, goal_distance)
                # print(str(vX) + ", " + str(vY))
                self.create.drive_direct(vX,vY)
                self.time.sleep(0.01)
                prev_time = time.time()
                prev_distance = distance