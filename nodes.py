class Quote():
  def __init__(self, elements):
    self.elements = elements
    
  def __str__(self):
    return "["+", ".join([str(e) for e in self.elements])+"]"
   
class Define():
  def __init__(self, ident, args, body):
    self.ident = ident
    self.args = args
    self.body = body

  def __str__(self):
    return "def "+str(self.ident)+"("+", ".join([str(a) for a in self.args])+"):\n\t"+"\n\t".join([str(exp) for exp in self.body])+"\n"

class Defvar():
  def __init__(self, ident, val):
    self.ident = ident
    self.val = val
    
  def __str__(self):
    return "%s = %s" % (self.ident,str(self.val))
    
class Sexp():
  def __init__(self, function,args):
    self.function = function
    self.args = args
    
  def __str__(self):
    return "%s(%s)" % (self.function,', '.join([str(a) for a in self.args]))
    

class Id():
  def __init__(self, value):
    self.value = value

  def __str__(self):
    return self.value
    
class String():
  def __init__(self, value):
    self.value = value[1:-1].decode('string_escape')
    
  def __str__(self):
      return "\""+self.value+"\""
    

class Number():
  def __init__(self, value):
    if '.' in value:
      self.value = float(value)
    else:
      self.value = int(value)
      
  def __str__(self):
    return str(self.value)


class Bool():
  def __init__(self, value):
    self.value = {'#t':True, '#f': False}[value]
    
  def __str__(self):
    return str(self.value)
    