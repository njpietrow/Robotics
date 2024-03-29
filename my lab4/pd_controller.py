import math

class PDController:
	def __init__(self, kp, kd, minOutput, maxOutput):
		self.kp = kp 
		#constant gain
		self.kd = kd
		self.minOutput = minOutput
		#minimum output value to limit calculated value
		self.maxOutput = maxOutput
		#maximum output value to limit calculated value
		self.vLeft = 0
		self.vRight = 0

		self.totalLeftError = 0
		self.totalRightError = 0

	def update(self, currDistance, goalSpeed, goalDistance, change_distance, change_time):
		dError = currDistance - goalDistance
		rateOfChange = change_distance/change_time
		print("Rate of Change: " + str(self.kd*rateOfChange))

		#if negative, need to go right
		self.vLeft = goalSpeed + self.kp*dError + self.kd*rateOfChange
		self.vRight = goalSpeed - self.kp*dError - self.kd*rateOfChange

		if(self.vLeft < self.minOutput):
			self.vLeft = self.minOutput
		elif(self.vLeft > self.maxOutput):
			self.vLeft = self.maxOutput	
		if(self.vRight < self.minOutput):
			self.vRight = -self.minOutput
		elif(self.vRight > self.maxOutput): 
			self.vRight = self.maxOutput

		return self.vLeft , self.vRight


