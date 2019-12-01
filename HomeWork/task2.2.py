def square_int(n:int)->dict:
	d = {x:x*x for x in range(1,n+1)}
	print(d)

square_int(7)