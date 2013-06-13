import re as regexp
from sympy import *
from string import *
from subprocess import call
def ml(ex):
    st=latex(ex)
    st=regexp.sub("smallmatrix","matrix",st)
    st=regexp.sub("left\[","left(",st)
    st=regexp.sub("right\]","right)",st)
    return(st) 

class LatexTemplate(Template):
     def substitute(self, *args, **kws):
         if len(args) > 1:
             raise TypeError('Too many positional arguments')
         if not args:
              mapping = kws
         elif kws:
              mapping = _multimap(kws, args[0])
         else:
              mapping = args[0]
         # Helper function for .sub()
         def convert(mo):
             # Check the most common path first.
             named = mo.group('named') or mo.group('braced')
             if named is not None:
                 val = ml(mapping[named])
                 # We use this idiom instead of str() because the latter will
                 # fail if val is a Unicode containing non-ASCII characters.
                 return '%s' % (val,)
             if mo.group('escaped') is not None:
	         return self.delimiter
             if mo.group('invalid') is not None:
                 self._invalid(mo)
             raise ValueError('Unrecognized named group in pattern', self.pattern)
         return self.pattern.sub(convert, self.template)
class Latex:
    def __init__(self,dirname):
        self.dirname=dirname
	self.main="main.tex"
	self.input="inputPart.tex"
	self.values={}
	self.textParts=[]
    def addExpression(self,string):
        self.values["string"]=eval(string)
    def addText(self,tString,*args,**kws):
         t=LatexTemplate(tString).substitute(*args,**kws)
         self.textParts.append(t)
    def addDisplayMath(self,mathString,*args,**kws):
         t=LatexTemplate(mathString).substitute(*args,**kws)
         self.textParts.append("\n\\[\n"+t+"\n\\]\n")
    def printParts(self):
	return("".join(self.textParts))
    def writeMain(self):
        Text="\
        \\documentclass[10pt,a4paper]{article}\n\
        \\usepackage{amsmath,amssymb,amsfonts,amscd,graphicx}\n\
        \\begin{document}\n"
        Text+=self.printParts()\
	+"\
        \\end{document}".replace("        ","")
        f=open(self.main,"w")
        f.write(Text)
        f.close()

        
    def write(self):
        self.writeMain()
        call(["pdflatex", self.main])



