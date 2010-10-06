from fractions import Fraction # Might eventually be optional

def factorial_rec(n):
	
	return 1 if n == 0 else (n*factorial_rec((n-1)))

def factorial_iter(n):
	
	return reduce(lambda x, y: (x*y), xrange(1, (1+n)))

print([factorial_rec(x) for x in xrange(1, 11)])
print([factorial_iter(x) for x in xrange(11, 16)])
