a = 2

def test():
	global a
	print("inside test", a)
	a = 3

test()
print("after test", a)