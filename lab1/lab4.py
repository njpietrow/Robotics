from p_controller import PController
class Run:
    def __init__(self, factory):
        self.create = factory.create_create()
        self.time = factory.create_time_helper()
        self.sonar = factory.create_sonar()
        self.servo = factory.create_servo()
        # define the gains here
        self.kp = 300
        self.kd = ...
        self.minOutput = -500
        self.maxOutput = 500
        # instantiate your controllers here
        self.p_controller = PController(self.kp, self.minOutput, self.maxOutput)
        # self.pd_controller = PDController(self.kp, self.kd, self.minOutput, self.maxOutput)


    def run(self):
        self.create.start()
        self.create.safe()

        self.servo.go_to(70)
        self.time.sleep(2)

        goal_distance = 0.5
        base_speed = 100

        while True:
            distance = self.sonar.get_distance()
            if distance is not None:
                print(distance)
                vX, vY = self.p_controller.update(distance, base_speed, goal_distance)
                # print(str(vX) + ", " + str(vY))
                self.create.drive_direct(vX,vY)
                self.time.sleep(0.01)