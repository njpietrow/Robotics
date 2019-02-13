import math
class PController:
	def __init__(self, kp, minOutput, maxOutput):
		self.kp = kp 
		#constant gain
		self.minOutput = minOutput
		#minimum output value to limit calculated value
		self.maxOutput = maxOutput
		#maximum output value to limit calculated value
		self.vLeft = 0
		self.vRight = 0
		self.IntegralLeftError = 0
		self.IntegralRightError = 0
	def update(self, currDistance, goalSpeed, goalDistance):
		dError = currDistance - goalDistance
		
		#if negative, need to go right
		self.vLeft = goalSpeed + self.kp*dError 
		self.vRight = goalSpeed - self.kp*dError

		if(self.vLeft < self.minOutput):
			self.vLeft = self.minOutput
		elif(self.vLeft > self.maxOutput):
			self.vLeft = self.maxOutput	
		if(self.vRight < self.minOutput):
			self.vRight = -self.minOutput
		elif(self.vRight > self.maxOutput): 
			self.vRight = self.maxOutput

		return self.vLeft , self.vRight
		
