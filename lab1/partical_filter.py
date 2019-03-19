import numpy as np
import math
import Particle as Particle
from pyCreate2 import create2
import lab8_map

class ParticleFilter:
	def __init__(self):
		self.current_x = .5
		self.current_y = .5
		self.current_theta = 0
		self.map_x = 3
		self.map_y = 3
		self.prob_cutoff = .05
		self.num_particles = 300
		temp_xs = np.random.uniform(0,3,self.num_particles)
		temp_ys = np.random.uniform(0,3,self.num_particles)
		temp_thetas = np.random.uniform(0, 2*math.pi, self.num_particles)
		temP_prob = 1/self.num_particles
		self.Particle_List = []
		self.p_List = []
		for x in range(self.num_particles):
			self.p = Particle.Particle(temp_xs[x], temp_ys[x], temp_thetas[x], temP_prob)
			self.p_List.append(temp_xs[x])
			self.p_List.append(temp_ys[x])
			self.p_List.append(0)
			self.p_List.append(temp_thetas[x])
			self.Particle_List.append(self.p)
		print(len(self.Particle_List))
		self.w = create2.Specs.WheelDistanceInMM/1000

		self.map = lab8_map.Map("lab8_map.json")
	
	def update_particles(self):
		self.p_List = []
		print("num particle:")
		print(self.num_particles)
		for x in range(self.num_particles):
			self.p_List.append(self.Particle_List[x].x)
			self.p_List.append(self.Particle_List[x].y)
			self.p_List.append(0)
			self.p_List.append(self.Particle_List[x].theta)
		print(len(self.p_List))

	def Movement(self, action):
		update_x = 0
		update_y = 0
		for i in range(self.num_particles):
			if action == "Move Foward":
				update_x += .1 * math.cos(self.current_theta)
				update_y += .1 * math.sin(self.current_theta)
				self.Particle_List[i].x += update_x
				self.Particle_List[i].y += update_y
			if action == "Turn Left":
				update_theta = .2/self.w 
				update_theta = math.fmod(update_theta+self.Particle_List[i].theta, 2 * math.pi)
				self.Particle_List[i].theta = update_theta
			if action == "Turn Right":
				update_theta = -.2/self.w 
				update_theta = math.fmod(update_theta+self.Particle_List[i].theta, 2 * math.pi)
				self.Particle_List[i].theta = update_theta
		self.Estimation()
		self.update_particles()

	def Sensing(self):
		for i in range(self.num_particles):
			d = self.map.closest_distance((self.Particle_List[i].x,self.Particle_List[i].y),self.Particle_List[i].theta)
			

	# use closest_distance to find actual distance from wall for each particle
	# use normal distribution funciton to find probaility of sonar given location
	# use this and bayes theorem to get the probability of the location given the sonar reading

	# keep track of point so that they can be normalized and all add up to 1

	def Estimation(self):
		num_popped = 0
		popped_probability = 0
		i = 0
		while i < self.num_particles:
			if self.Particle_List[i].x > self.map_x:
				popped_probability += self.Particle_List[i].prob
				self.Particle_List.pop(i)
				num_popped += 1
				self.num_particles -= 1
			elif self.Particle_List[i].x < 0:
				popped_probability += self.Particle_List[i].prob
				self.Particle_List.pop(i)
				num_popped += 1
				self.num_particles -= 1
			elif self.Particle_List[i].y > self.map_y:
				popped_probability += self.Particle_List[i].prob
				self.Particle_List.pop(i)
				num_popped += 1
				self.num_particles -= 1
			elif self.Particle_List[i].y < 0:
				popped_probability += self.Particle_List[i].prob
				self.Particle_List.pop(i)
				num_popped += 1
				self.num_particles -= 1
			i += 1
			# elif self.Particle_List[i].prob < self.prob_cutoff:
			# 	popped_probability += self.Particle_List[i].prob
			# 	self.Particle_List.pop(i)
			# 	num_popped += 1
			# 	self.num_particles -= 1
			# else:
			# 	pass
				#potentially double probability
		print("num popped")
		print(num_popped)
		# 	TODO
		# self.current_theta = 0
		# self.current_y = 0
		# self.current_x = 0
