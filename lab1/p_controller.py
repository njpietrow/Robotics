class PController:
	def __init__(self, kp, minOutput, maxOutput):
		self.kp = kp 
		#constant gain
		self.minOutput = minOutput
		#minimum output value to limit calculated value
		self.maxOutput = maxOutput
		#maximum output value to limit calculated value

	def update(self, currDistance, goalSpeed, goalDistance):
		return 0,0

