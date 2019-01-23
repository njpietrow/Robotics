import numpy as np
import matplotlib.pyplot as plt

def mysum2(inputArray):
	print(np.sum(inputArray, dtype=np.int32))

def plotcircle1():
	# plot a circle
	t = np.linspace(0, 2*np.pi, 50)
	r = 3
	x1=[]
	y1=[]
	x1 = r*np.cos(t)
	y1 = r*np.sin(t)

	plt.plot(x1, y1)
	plt.axis("equal")
	plt.show()

def plotnorm1():
	# normal distribution plot
	mu, sigma = 50, 10
	s = np.random.normal(mu, sigma, 10000)
	plt.hist(s, 20)
	plt.show()


def main():
	print("Testing mysum2...")
	mysum2([1,5,7])
	mysum2([])
	mysum2([-5,3])
	print()
	
	print("Testing plotcircle1...")
	plotcircle1()
	print()

	print("Testing plotnorm1...")
	plotnorm1()
	print()


if __name__ == "__main__":
	main()
