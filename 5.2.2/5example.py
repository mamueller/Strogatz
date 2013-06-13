#!/usr/bin/python
from sympy.interactive.printing import init_printing
init_printing(use_unicode=True, wrap_line=False, no_global=True)
import re as regexp
from sympy import *
#from sympy.matrices import *
#from sympy.matrices.matrices import exp_block
#from sympy.matrices.matrices import jblock_exponential
#from sympy import Symbol,exp,factorial
#from sympy import latex
#from sympy import latex
#from sympy import I
#from sympy import symbols
#from sympy import simplify
#from sympy import Basic, Symbol, Integer, C, S, Dummy, Rational, Add, Pow

def ml(ex):
    st=latex(ex)
    st=regexp.sub("smallmatrix","matrix",st)
    st=regexp.sub("left\[","left(",st)
    st=regexp.sub("right\]","right)",st)
    return(st) 

def exampleFromMatrix(m):
    Text="\
          consider the following matrix \n\
          \[\n \mathbf{M}="\
          +ml(m)\
          +"\\]"  
    
    l=m.eigenvects()
    e1=l[0][2][0]
    e2=l[1][2][0]
    lambda1=l[0][0]
    lambda2=l[1][0]
    Text+="\
          We compute the eigenvalues and the eigenvalues theire multiplicity and the eigenvectors:\n\
          \[\n"\
          +latex(m.eigenvects())\
	  +"\\]" 
    Text+="\
          In detail this means:\n\
          \[\n"\
	  +"\lambda_1="\
          +latex(lambda1)\
	  +"\hspace{1cm}"\
	  +"\lambda_2="\
          +latex(lambda2)\
	  +"\\]"\
          +"\[\n"\
	  +"\mathbf{e_1}="\
          +latex(e1)\
	  +"\hspace{1cm}"\
	  +"\mathbf{e_2}="\
          +latex(e2)\
	  +"\\]" 

    c_1,c_2=symbols("c_1,c_2")
    x,y=symbols("x,y")
    t=symbols("t",real=True)
    X=Matrix([x,y])
    gs=c_1*exp(lambda1*t)*e1+c_2*exp(lambda2*t)*e2
    Text+="\
          So the general solution is:\n"\
	  +"\\begin{eqnarray}\n"\
          +"\mathbf{x}(t)="+latex(X)+"&=&c_1 e^{\lambda_1 t}\mathbf{e_1}+c_2 e^{\lambda_2 t}\mathbf{e_2} \\nonumber \\\\"\
          +"&=&"+latex(gs)+"\\text{ with } c_1,c_2 \in \mathbb{C} \\nonumber \\\\"\
	  +"\\end{eqnarray}\n"

    c_1r, c_1i,c_2r, c_2i = symbols('c_1r, c_1i,c_2r, c_2i', real=True)
    c_1=c_1r+I*c_1i
    c_2=c_2r+I*c_2i
    Text+="\
          Remark:\\\\ \
          These two complex constants actually translate into  four real ones, since $c_1$ and $c_2$ both have a real and an imaginary part.\n\
	  \["\
	  +"c_1="+latex(c_1)\
	  +"\hspace{1cm}"\
	  +"c_2="+latex(c_2)\
	  +"\]\n"\
	  +"We can also look at it the other way round: From a more general point of view our two real initial conditions are actually complex ones with an imaginary part of zero.\
	  Either way four constants to fulfill four conditions look promising.\n\
	  Remark:\\\\ \
	  Any two dimensional vector-space can (by definition) be spanned by two linearly independent vectors.\
	  Any such set is called a base of the vector-space. \
	  To switch to another one one is free to  create new base vectors as linear combinations of the old ones.\
	  For convenience we would like to have real base vectors. (We do not loose generality by this choice since we \
	  can still multiply them with complex coefficients to regain the complex solutions)\
	  \\\\Remark:\\\\ \
	  Actually in our case of conjugate eigenvectors it is very easy to create an new (real only) base.\
	  We will proceed to do so right now."

    gs=c_1*exp(lambda1*t)*e1+c_2*exp(lambda2*t)*e2
    Text+="\
          Expressing the general solution by real constants only we get:\n\
	  \["\
	  +latex(X)+"="+latex(gs)\
	  +"\\]" 

    x=gs[0]
    y=gs[1]
    dic={\
    exp(t*(1+I)) :exp(t)*(cos(t)+I*sin(t)),
    exp(t*(1-I)) :exp(t)*(cos(t)-I*sin(t))}
    xn=x.subs(dic)
    yn=y.subs(dic)
    xnr=collect(simplify(re(xn)),[sin(t),cos(t)])
    xni=collect(simplify(im(xn)),[sin(t),cos(t)])
    ynr=collect(simplify(re(yn)),[sin(t),cos(t)])
    yni=collect(simplify(im(yn)),[sin(t),cos(t)])
    Text+="\
          in component form:\n"\
	  +"\\begin{eqnarray}\n"\
	  +"x &=&"+latex(x)+"\\nonumber \\\\"\
	  +"&=&"+latex(xn)+"\\nonumber \\\\" \
	  +"\Re(x)&=&"+latex(xnr)+"\\nonumber \\\\"\
	  +"\Im(x)&=&"+latex(xni)+"\\nonumber \\\\"\
	  +"y &=&"+latex(y)+"\\nonumber \\\\"\
	  +"&=&"+latex(yn)+"\\nonumber \\\\" \
	  +"\Re(y)&=&"+latex(ynr)+"\\nonumber \\\\"\
	  +"\Im(y)&=&"+latex(yni)+"\\nonumber \\\\"\
	  +"\\end{eqnarray}\n"
    Text+="\
          Sorting for real and imaginary parts leads to the following expression for the general solution:"\
	  +"\\begin{eqnarray}\n"\
	  +latex(X)+"&=&\\left(\\begin{array}{c}\Re(x) \\\\ \Re(y) \\end{array}\\right)"+"+i \\left(\\begin{array}{c}\Im(x) \\\\ \Im(y) \\end{array}\\right)\\nonumber \\\\ "\
	  +"&=&\\left(\\begin{array}{c}"+latex(xnr)+" \\\\ "+latex(ynr)\
	  +"\\end{array}\\right)\\nonumber \\\\" \
	  +"&& \\hspace{2cm} + i \\left(\\begin{array}{c}"+latex(xni)+" \\\\ "+latex(yni)+" \\end{array}\\right)\\label{realim}"\
	  +"\\end{eqnarray}\n"

    dic2={c_1i:-c_2i,c_1r:c_2r}
    Text+="\
          It is now obvious that we can produce the new real base vectors by tuning the four real parameters.\
	  We can force the imaginary part of the sum away by the choice"\
	  +"\["\
	  +latex(dic2)\
	  +"\\]"\
	  "which leads to the simplified first part:"\
	  +"\["\
	  +"\\left(\\begin{array}{c}\n"\
	  +latex(xnr.subs(dic2))+" \\\\ "+latex(ynr.subs(dic2))\
	  +"\\end{array}\\right)\\nonumber \\\\" \
	  +"\\]"\
    
    dic3={c_2i:Rational(1,2),c_2r:0}
    xs1=xnr.subs(dic2).subs(dic3)
    ys1=ynr.subs(dic2).subs(dic3)
    X1=Matrix([xs1,ys1])
    Text+="\
          We can further simplify this solution by the following choice:"\
	  +"\["\
	  +latex(dic3)\
	  +"\\]"\
	  "which leads to a very simple solution indeed:"\
	  +"\["\
	  +latex(X)\
	  +"=\\left(\\begin{array}{c}\n"\
	  +latex(xs1)+" \\\\ "+latex(ys1)\
	  +"\\end{array}\\right)\\nonumber \\\\" \
	  +"\\]"\
    
    dx=Matrix(2,1,[diff(xs1,t),diff(ys1,t)])
    
    Text+="\
         Lets test if it is indeed a solution of the ode:"\
	 +"\["\
	 +"\mathbf{\dot X}="+latex(dx)\
	 +"\\]"\
	 +"\["\
	 +"\mathbf{MX}="+latex(m*X1)\
	 +"\\]"

         	  
    dic4={c_1i:c_2i,c_1r:-c_2r}
    Text+="\
         Now we create a second real only solution by first creating a imaginary only solution and then multiplying it with $i$.\
	 To this end we force the real part in (\\ref{realim}) to zero.\
         We make the following choice:"\
	  +"\["\
	  +latex(dic4)\
	  +"\\]"\
	  "which leads to the simplified second part:"\
	  +"\["\
	  +"\\left(\\begin{array}{c}\n"\
	  +latex(xni.subs(dic4))+" \\\\ "+latex(yni.subs(dic4))\
	  +"\\end{array}\\right)\\nonumber \\\\" \
	  +"\\]"

    xs2=xni.subs(dic4).subs(dic3)
    ys2=yni.subs(dic4).subs(dic3)
    X2=Matrix([xs2,ys2])
    Text+="\
          We can further simplify this solution by the following choice, that also insures that our second solution is no multiple of the first:"\
	  +"\["\
	  +latex(dic3)\
	  +"\\]"\
	  "which leads to:"\
	  +"\["\
	  +latex(X)\
	  +"=\\left(\\begin{array}{c}\n"\
	  +latex(xs2)+" \\\\ "+latex(ys2)\
	  +"\\end{array}\\right)\\nonumber \\\\" \
	  +"\\]"

    dx2=Matrix(2,1,[diff(xs2,t),diff(ys2,t)])
    
    Text+="\
         Lets test if it is indeed a solution of the ode:"\
	 +"\["\
	 +"\mathbf{\dot X}="+latex(dx2)\
	 +"\\]"\
	 +"\["\
	 +"\mathbf{MX}="+latex(m*X2)\
	 +"\\]"


    dt=X1.row_join(X2)
    Text+="\
          To test that our solutions are not lineary dependent we joint them to a matrix and compute the determinant, which must not be zero."\
          +"\["\
	  +"\det"+latex(dt)+"="+latex(dt.det())+"="+latex(trigsimp(dt.det()))+"\\neq 0"\
	  +"\\]"

    Text+="\
          Since the new two solutions are linear independent they span the whole vector space of solutions, even the complex part that we are not interested in, \
	  since we can multiply them again with complex numbers $\\tilde{c_1}$ and $\\tilde{c_2}$. In fact we did not loose any generality. We just chose a differen base."


    return(Text)


t= Symbol("t")
t0= Symbol("t0")
k1= Symbol("k1")
k2= Symbol("k2")
k3= Symbol("k3")
a21=Symbol("a21")
a32=Symbol("a32")
#m=  Matrix(3,3,
#    [
#         k1,   0,  0, 
#        a21,  k2,  0,   
#          0, a32, k3    
#	])
#
#m=  Matrix(2,2,
#    [
#         k1,   0,  
#        a21,  k2    
#    ])
m= Matrix(2,2,
    [
         1,-1, 
         1, 1   
	])
Text=exampleFromMatrix(m)
A=m*t
EX=(A).exp()
    
#EX_back=EX.subs([[k1,-1],[k2,-2],[k3,-2],[a21,1],[a32,1]])
#print EX_back
#print (m2*t).exp()
f=open("example.tex","w")
f.write(Text)
f.close()

