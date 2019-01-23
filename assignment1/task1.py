# create function called mysum1
#use a for loop



def mysum1(inputArray):
	sum = 0
	for elements in inputArray:
		sum += elements
	print(sum) 

def myfib1(n):
	n = n
	a,b = 0,1
	for i in range(n):
		a,b = b,a+b
	print(a)

def main():
	print("Testing mysum1...")
	mysum1([1,5,7])
	mysum1([])
	mysum1([-5,3])
	print()
	
	print("Testing myfib1...")
	myfib1(3)
	myfib1(5)
	myfib1(7)

if __name__ == "__main__":
	main()