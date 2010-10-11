#!/usr/bin/env python

from codetalker.pgm import Grammar, Translator
from codetalker.pgm.special import star, plus, _or, commas
from codetalker.pgm.tokens import STRING, NUMBER, EOF, NEWLINE, WHITE, ReToken, re, CharToken, StringToken

import os,sys
import re
import nodes

'''
A simple lisp that compiles to Python.
Mainly for educational purposes
'''

# special tokens

class SYMBOL(CharToken):
  chars = '\'()[]'
  num = 5
  
class ID(ReToken):
  rx = re.compile("[a-zA-Z\_\+\-\*\/\=\<\>]*")
  
class BOOL(StringToken):
  strings = ['#t','#f']
  
# rules

def program(rule):
  rule | (star(_or(expression,NEWLINE)),EOF)
  rule.astAttrs = {'body': [expression]}
program.astName = 'Program'

def expression(rule):
  rule | quote | define | defvar | anon | if_ | sexp | ID | STRING | NUMBER | BOOL
  rule.pass_single = True  
  
def quote(rule):
  rule | ('\'','(',star(expression),')')
  rule.astAttrs = {'values':[expression]}
quote.astName = 'Quote'
  
def define(rule):
  rule | ('(','define','(',ID,star(ID),')',plus(expression),')')
  rule.astAttrs = {'args': [ID], 'body': [expression]}
define.astName = 'Define'

def defvar(rule):
  rule | ('(','define',ID,expression,')')
  rule.astAttrs = {'ident': [ID], 'val': expression}
defvar.astName = 'Defvar'

def anon(rule):
  rule | ('(','lambda','(',star(ID),')',expression,')')
  rule.astAttrs = {'args': [ID], 'body': expression}
anon.astName = 'Anon'

def if_(rule):
  rule | ('(','if',expression,expression,expression,')')
  rule.astAttrs = {'expressions':[expression]}
if_.astName = 'If'

def sexp(rule):
  rule | ('(',ID,star(expression),')') | ('(',star(expression),')')
  rule.astAttrs = {'function': ID, 'args': [expression]}
sexp.astName = 'Sexp'


grammar = Grammar(start=program,
                  tokens=[SYMBOL],
                  ignore=[WHITE, NEWLINE],
                  ast_tokens=[ID, STRING, NUMBER, BOOL])
                  
# translation
Lithon = Translator(grammar)
ast = grammar.ast_classes
elements = []

@Lithon.translates(ast.Program)
def t_program(node):
  for exp in node.body: elements.append(Lithon.translate(exp))
  
@Lithon.translates(ast.Quote)
def t_quote(node):
  return nodes.Quote([Lithon.translate(v) for v in node.values])
  
@Lithon.translates(ast.Define)
def t_define(node):
  return nodes.Define(node.args[1],node.args[2:],[Lithon.translate(exp) for exp in node.body])
  
@Lithon.translates(ast.Defvar)
def t_defvar(node):
  return nodes.Defvar(node.ident[1],Lithon.translate(node.val))
  
@Lithon.translates(ast.Anon)
def t_anon(node):
  return nodes.Anon(node.args[1:],Lithon.translate(node.body))
  
@Lithon.translates(ast.If)
def t_if(node):
  return nodes.If([Lithon.translate(e) for e in node.expressions])

@Lithon.translates(ast.Sexp)
def t_sexp(node):
  return nodes.Sexp(node.function,[Lithon.translate(arg) for arg in node.args])
  
@Lithon.translates(ID)
def t_id(node):
  return nodes.Id(node.value)
  
@Lithon.translates(STRING)
def t_string(node):
  return nodes.String(node.value)
  
@Lithon.translates(NUMBER)
def t_number(node):
  return nodes.Number(node.value)
  
@Lithon.translates(BOOL)
def t_bool(node):
  return nodes.Bool(node.value)
  
input_file = sys.argv[1]
output_file = re.match("(.+)\.",sys.argv[1]).group()+"py"

Lithon.from_string(open(input_file,'r').read())
f = open(output_file,'w')
f.write("from fractions import Fraction # Might eventually be optional\n\n") 
for e in elements:
  print "VISITING: %s" % e.__class__
  f.write("print %s\n" % e) if (e.__class__ == nodes.Sexp or e.__class__ == nodes.Id) else f.write("%s\n" % e)
f.close()
print "Compiled!"
print "Executing %s ..." % output_file
os.system("python %s" % output_file)