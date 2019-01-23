"""
Example to move robot forward for 10 seconds
Use "python3 run.py [--sim] example1" to execute
"""


class Run:
    def __init__(self, factory):
        """Constructor.
    
        Args:
            factory (factory.FactoryCreate)
        """
        self.create = factory.create_create()
        self.time = factory.create_time_helper()


    def setBaseSpeed(self,speed):
        # takes speed parameter in m/s
        self.base_speed = speed

    def run(self):
        self.create.start()
        self.create.safe()

        # enter base speed here in m/s
        self.setBaseSpeed(.1)

        mr = MyRobot(self)
        mr.forward(1)
        mr.turn_left(6)
        mr.forward(.5)
        mr.turn_right(8)
        mr.backward(1)
        mr.stop()


from my_robot import MyRobot

