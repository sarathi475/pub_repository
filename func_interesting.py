def multi(a,b):
	if b==0:
		return 0
	rest=multi(a,b-1)
	value=a+rest
	return value
print "4*4=",multi(4,4)
