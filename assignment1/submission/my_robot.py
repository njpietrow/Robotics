from lab1 import Run

class MyRobot:
    def __init__(self, Run):
        self.run = Run
    def forward(self,distance):
        self.run.create.drive_direct(self.run.base_speed*1000, self.run.base_speed*1000)
        self.run.time.sleep(distance/self.run.base_speed)
    def backward(self,distance):
        self.run.create.drive_direct(-self.run.base_speed*1000, -self.run.base_speed*1000)
        self.run.time.sleep(distance/self.run.base_speed)
    def turn_left(self,duration):
        self.run.create.drive_direct(-self.run.base_speed*1000, self.run.base_speed*1000)
        self.run.time.sleep(duration)
    def turn_right(self,duration):
        self.run.create.drive_direct(self.run.base_speed*1000, -self.run.base_speed*1000)
        self.run.time.sleep(duration)
    def stop(self):
        self.run.create.drive_direct(0, 0)
        self.run.create.stop()
