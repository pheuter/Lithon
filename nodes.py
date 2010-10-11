from fractions import Fraction
indent_counter = 0; # For maintaining indents
def repeat(object, times=None): # For creating arbitrary amount of indents
    # repeat(10, 3) --> 10 10 10
    if times is None:
        while True:
            yield object
    else:
        for i in xrange(times):
            yield object

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
    print "body: %s" % self.body
    global indent_counter
    indent_counter += 1
    indents = ""
    for i in repeat("\t",indent_counter): indents += i
    if (self.body[-1].__class__ == If): self.body[-1] = "return %s if %s else %s" % (self.body[-1].expressions[1], self.body[-1].expressions[0],self.body[-1].expressions[2]) # broken for functions where last statement consists of nested ifs, for now
    out = "def %s(%s):\n%s%s\n" % (str(self.ident),", ".join([str(a) for a in self.args]),indents,"\n\t".join([str(exp) for exp in self.body]))
    indent_counter -= 1
    return out

class Defvar():
  def __init__(self, ident, val):
    self.ident = ident
    self.val = val
    
  def __str__(self):
    if (self.val.__class__ == If):
      return "%s = %s if %s else %s" % (self.ident,self.val.expressions[1],self.val.expressions[0],self.val.expressions[2]) 
    else:
      return "%s = %s" % (self.ident,str(self.val))
    
class Anon():
  def __init__(self, args, body):
    self.args = args
    self.body = body
  
  def __str__(self):
    if (len(self.args) > 0):
      return "lambda %s: %s" % (", ".join([str(a) for a in self.args]),str(self.body))
    else:
      return "lambda: %s" % str(self.body)
      
class If():
  def __init__(self,expressions):
    self.expressions = expressions
  
  def __str__(self):
    global indent_counter
    indent_counter += 1
    indents = ""
    for i in repeat("\t",indent_counter): indents += i
    out = "if (%s):\n%s%s\n%selse:\n%s%s" % (str(self.expressions[0]),indents,self.expressions[1],"\t".join(indents.split("\t")[1:]),indents,self.expressions[2])
    indent_counter -= 1
    return out
    
class Sexp():
  def __init__(self, function,args):
    self.function = function
    self.args = args
      
  def optimize(self):
    f = str(self.function)
    if (f == "map"): 
      if (self.args[0].__class__ == Anon): return "[%s for %s in %s]" % (self.args[0].body,str(self.args[0].args[0]),self.args[1])
      else: return "[%s(x) for x in %s]" % (self.args[0],self.args[1])
    elif (f == "filter"):
      if (self.args[0].__class__ == Anon): return "[%s for %s in %s if %s]" % (self.args[0].args[0],self.args[0].args[0],self.args[1],self.args[0].body)
      else: return "[x for x in %s if %s(x)]" % (self.args[1],self.args[0])
    elif (f == "+"): return "(%s)" % "+".join([str(a) for a in self.args])
    elif (f == "-"): return "(%s)" % "-".join([str(a) for a in self.args])
    elif (f == "*"): return "(%s)" % "*".join([str(a) for a in self.args])
    elif (f == "/"): return "Fraction(\"%s\")" % reduce(Fraction,[int(str(a)) for a in self.args])
    elif (f == "="): return "%s == %s" % (self.args[0], self.args[1])
    elif (f == "<"): return "%s < %s" % (self.args[0], self.args[1])
    elif (f == "<="): return "%s <= %s" % (self.args[0], self.args[1])
    elif (f == ">"): return "%s > %s" % (self.args[0], self.args[1])
    elif (f == ">="): return "%s >= %s" % (self.args[0], self.args[1])
    else: return None  
    
  def __str__(self):
    if self.function:
      opt = self.optimize()
      return opt if opt else "%s(%s)" % (self.function,", ".join([str(a) for a in self.args])) # regular function call
    elif (self.args[0].__class__ == Anon):
      return "(%s)(%s)" % (str(self.args[0]),", ".join([str(a) for a in self.args][1:])) # anonymous function call
    else:
      return "%s" % " ".join([str(a) for a in self.args])

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
    