import math
class Particle:
	def __init__(self, temp_x, temp_y, temp_theta, temp_prob):
		self.x = temp_x
		self.y = temp_y
		self.theta = temp_theta
		self.prob = temp_prob
		self.z = 0

	def update(self, d, theta):
		self.theta = theta
		self.x += d * math.cos(self.theta)
		self.y += d * math.sin(self.theta)
