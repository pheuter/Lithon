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
    return "def %s(%s):\n\t%s\n" % (str(self.ident),", ".join([str(a) for a in self.args]),"\n\t".join([str(exp) for exp in self.body]))

class Defvar():
  def __init__(self, ident, val):
    self.ident = ident
    self.val = val
    
  def __str__(self):
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
    
class Sexp():
  def __init__(self, function,args):
    self.function = function
    self.args = args
    try:
      self.opts = {
        "map": "[%s(x) for x in %s]" % (self.args[0],self.args[1]),
        "map_anon": "[(%s)(x) for x in %s]" % (self.args[0],self.args[1]),
        "filter": "[x for x in %s if %s(x)]" % (self.args[1],self.args[0]),
        "filter_anon": "[x for x in %s if (%s)(x)]" % (self.args[1],self.args[0]),
        "+": "add(%s)" % ", ".join([str(a) for a in self.args]),
        "-": "sub(%s)" % ", ".join([str(a) for a in self.args]),
        "*": "mult(%s)" % ", ".join([str(a) for a in self.args]),
        "/": "add(%s)" % ", ".join([str(a) for a in self.args])
      }
    except: # We wont always have those conditions, so populate with regular calls
      self.opts = {
        "call": "%s(%s)" % (self.function,", ".join([str(a) for a in self.args])),
        "call_anon": "(%s)(%s)" % (str(self.args[0]),", ".join([str(a) for a in self.args][1:]))
      }
    
  def __str__(self):
    if self.function:
      try:
        if (self.args[0].__class__ == Anon): return self.opts[str(self.function)+"_anon"]
        else: return self.opts[str(self.function)]
      except KeyError, e:
        return self.opts['call']
    else:
      return self.opts['call_anon']
    

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
    