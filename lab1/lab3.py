"""
Sample Code for Lab3
Use "run.py [--sim] lab3" to execute
"""

from pyCreate2 import create2
from my_robot import MyRobot


class Run:
    def __init__(self, factory):
        """Constructor.

        Args:
            factory (factory.FactoryCreate)
        """
        self.create = factory.create_create()
        self.time = factory.create_time_helper()

    def run(self):
        self.create.start()
        self.create.safe()

        # request sensors
        self.create.start_stream([
            create2.Sensor.LeftEncoderCounts,
            create2.Sensor.RightEncoderCounts,
        ])

        self.setBaseSpeed(.1)
        mr = MyRobot(self)

        while True:
            mr.forward(1)
            state = self.create.update()
            if state is not None:
                print(state.__dict__)


