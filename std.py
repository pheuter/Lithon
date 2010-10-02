def add(*args):
  return sum(args)
  
def sub(*args):
  return reduce(lambda x,y: x-y,args)

def mult(*args):
  return reduce(lambda x,y: x*y,args)
  
def div(*args):
  return reduce(lambda x,y: x/y,args)