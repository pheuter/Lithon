def add(*args):
  return reduce(lambda x,y: x+y,args)
  
def sub(*args):
  return reduce(lambda x,y: x-y,args)

def mult(*args):
  return reduce(lambda x,y: x*y,args)
  
def div(*args):
  return reduce(lambda x,y: x/y,args)