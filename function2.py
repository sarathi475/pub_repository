def absolute_value(n):
	if n<0:
		n=-n
	return n
a=23
b=-23
if absolute_value(a)==absolute_value(b):
	print "the absolute values of",a,"&",b,"equal" 
else:
	print "the absolute values of",a,"&",b,"not equal" 

