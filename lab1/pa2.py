"""
Code for PA2
Use "run.py [--sim] pa2" to execute
"""


class Run:
    def __init__(self, factory):
        """Constructor.

        Args:
            factory (factory.FactorySimulation)
        """
        self.arm = factory.create_kuka_lbr4p()
        self.time = factory.create_time_helper()

    def run(self):
        pass

    #     def go_to(self, joint, angle):
    #         Args:
    #             joint (int): number of joint to change (0 to 7)
    #             angle (float): radians

    #     def enable_painting(self):
    #     def disable_painting(self):
    #     def set_color(self, r, g, b):
    #             r (float): red component (0 to 1)
    #             g (float): green component (0 to 1)
    #             b (float): blue component (0 to 1)

