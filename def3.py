print
def hello():
	print "hello !"
def area(w,h):
	return w * h
def print_welcome(name):
	print "welcome",name
name =raw_input('Your Name:')
hello()
print_welcome(name)
w=input("Width:")
while w<0:
	print "Enter only positive value"
	w=input("width:")
h=input("height:")
while h<0:
	print "Enter only positive value"
	h=input("height:")
print 'width=',w,'height=',h,'area',area(w,h)
