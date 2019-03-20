import numpy as np
import math
import scipy.stats
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
		temp_prob = 1/self.num_particles
		self.Particle_List = []
		self.p_List = []
		for x in range(self.num_particles):
			self.p = Particle.Particle(temp_xs[x], temp_ys[x], temp_thetas[x], temp_prob)
			self.p_List.append(temp_xs[x])
			self.p_List.append(temp_ys[x])
			self.p_List.append(0)
			self.p_List.append(temp_thetas[x])
			self.Particle_List.append(self.p)

		self.w = create2.Specs.WheelDistanceInMM/1000

		self.map = lab8_map.Map("lab8_map.json")
	
	def update_particles(self):
		self.p_List = []
		for x in range(self.num_particles):
			self.p_List.append(self.Particle_List[x].x)
			self.p_List.append(self.Particle_List[x].y)
			self.p_List.append(0)
			self.p_List.append(self.Particle_List[x].theta)

	def Movement(self, action):
		if action == "Move Foward":
			pass
		elif action == "Turn Left":
			update_theta = .2 / self.w
			update_self_theta = math.fmod(update_theta + self.current_theta, 2 * math.pi)
			self.current_theta = update_self_theta
		elif action == "Turn Right":
			update_theta = -.2 / self.w
			update_self_theta = math.fmod(update_theta + self.current_theta, 2 * math.pi)
			self.current_theta = update_self_theta

		for i in range(self.num_particles):
			update_x = 0
			update_y = 0
			if action == "Move Foward":
				update_x += .1 * math.cos(self.current_theta)
				update_y += .1 * math.sin(self.current_theta)
				self.Particle_List[i].x += update_x
				self.Particle_List[i].y += update_y
			if action == "Turn Left":
				update_theta = .2/self.w
				update_theta = math.fmod(update_theta + self.Particle_List[i].theta, 2 * math.pi)
				self.Particle_List[i].theta = update_theta
			if action == "Turn Right":
				update_theta = -.2/self.w
				update_theta = math.fmod(update_theta + self.Particle_List[i].theta, 2 * math.pi)
				self.Particle_List[i].theta = update_theta
		self.Cropping()
		self.update_particles()

	def Cropping(self):
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

	def Sensing(self,distance):
		probs = []

		for i in range(self.num_particles):
			# get distance from each particle to wall of map
			d = self.map.closest_distance((self.Particle_List[i].x,self.Particle_List[i].y),self.Particle_List[i].theta)
			# calculate probability given the sonar reading
			prob_sonar_given_loc = scipy.stats.norm(distance,.2).pdf(d)
			p_loc = self.Particle_List[i].prob
			# print(p_loc)

			p_final = prob_sonar_given_loc * p_loc
			probs.append(p_final)

		print(sum(probs))
		y = 1/sum(probs)

		counter = 0
		x = 0
		max = 0
		for i in probs:
			self.Particle_List[x].prob = y * i
			print(self.Particle_List[x].prob)
			if self.Particle_List[x].prob > max:
				max = self.Particle_List[x].prob
			counter += self.Particle_List[x].prob
			x += 1

		print("---max probability-----")
		print(max)
		print("----sum----")
		print(counter)

		self.Estimation()



	def Estimation(self):
		pass
		# TODO
		# need to implement refiltering