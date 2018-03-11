def factorial(n):
	if n<=2:
		return 1
	return n * factorial(n-1)
print "2!=",factorial(2)

print "3!=",factorial(3)
print "4!=",factorial(4)
print "-1!=",factorial(-1)
