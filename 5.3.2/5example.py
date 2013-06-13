#!/usr/bin/python
from Latex import *
from string import *
from sympy import *
import numpy as np
import matplotlib
matplotlib.use('PDF')
#from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt

L=Latex("Example")
m= Matrix(2,2,
    [
         0, 1, 
        -1, 1   
	])
t="\
      consider the following matrix \n\
      \[\n \mathbf{M}=\
      ${m}\
      \\]"
L.addText(t,m=m)
l=m.eigenvects()
L.addText("We compute the eigenvalues and the eigenvalues theire multiplicity and the eigenvectors:\n")
L.addDisplayMath("${out}",out=m.eigenvects())

e1=l[0][2][0]
e1=Matrix(map(radsimp,e1))
e2=l[1][2][0]
e2=Matrix(map(radsimp,e2))
lambda1=l[0][0]
lambda2=l[1][0]
t=Symbol("t",real=True)
L.addText("In detail and with some simplification this means:\n")
L.addDisplayMath("\lambda_1=${l1} \hspace{1cm} \lambda_2=${l2}",l1=lambda1,l2=lambda2)
L.addDisplayMath("\mathbf{e_1}=${e1} \hspace{1cm} \mathbf{e_2}=${e2}",e1=e1,e2=e2)
L.addText("Now we can write down two independent solutions")
ex1=exp(lambda1*t)
ex2=exp(lambda2*t)
#help sympy a little bit with the splitting of exp(x+iy) by doing it before multiplication 
def re_im_split(expr):
   return(re(expr)+I*im(expr))
ex1=re_im_split(ex1)
ex2=re_im_split(ex2)
s1=Matrix(map(collect,map(expand,ex1*e1),[I,I]))
s2=Matrix(map(collect,map(expand,ex2*e2),[I,I]))
L.addDisplayMath("\mathbf{s_1}(t)=e^{\\lambda_1 t}\mathbf{e_1}=${s1}",s1=s1)
L.addDisplayMath("\mathbf{s_2}(t)=e^{\\lambda_2 t}\mathbf{e_2}=${s2}",s2=s2)
L.addText("where we applied the euler formula and ordered for real and imaginary parts. From this representation it is obvious that these solutions are conjugent to each other. This suggests the following way to construct two real valued solutions as linear combinations of $$ \mathbf{s_1} $$ and $$ \mathbf{s_2} $$.")
# $$s_1$$")
n1=Matrix(map(simplify,s1+s2))
n2=Matrix(map(simplify,I*(s1-s2)))
L.addDisplayMath("\mathbf{n_1}(t)=  \mathbf{s_2}(t)+\mathbf{s_2}(t) =${n1}",n1=n1)
L.addDisplayMath("\mathbf{n_2}(t)=i(\mathbf{s_2}(t)-\mathbf{s_2}(t))=${n2}",n2=n2)

L.addText("We can now express any solution either in terms of $$ \mathbf{s_1} $$ and $$ \mathbf{s_2} $$ \
or $$ \mathbf{n_1} $$ and $$ \mathbf{n_2} $$. \
We will now proceed to do so for a solution that matches an arbitrary real start vector. \
We look for a set of (real) constants $$\{r_1,r_2\} $$ that fulfills the following equation:")

c_1,c_2=symbols("c_1,c_2")
x_0,y_0=symbols("x_0,y_0")
X=Matrix([x_0,y_0])
Xc=Matrix([3,-5])
n10=Matrix([n1[0].subs(t,0),n1[1].subs(t,0)])
n20=Matrix([n2[0].subs(t,0),n2[1].subs(t,0)])
L.addDisplayMath("${X}=${Xc}=r_1 \mathbf{n_1}(0)+ r_2 \mathbf{n_2}(0)=r_1 ${n10} r_2 ${n20}",X=X,Xc=Xc,n10=n10,n20=n20)
A=zeros(2,2)
A[:,0]=n10
A[:,1]=n20
r_1,r_2=symbols("r_1,r_2")
r=Matrix([r_1,r_2])
L.addText("So we have to solve the linear system:") 
L.addDisplayMath("${Xc}=${A} ${r}",Xc=Xc,A=A,r=r)
sol=A.LUsolve(Xc)
L.addText("The Solution is: \[ ${r}=${sol} \]",r=r,sol=sol) 
L.addText("We can now plot the solution.")
x,y=symbols("x,y")
r1=sol[0]
r2=sol[1]
X=r1*n1+r2*n2
x_vals=lambdify(t,X[0])
y_vals=lambdify(t,X[1])
T=np.linspace(0,100,500)   
Xv=map(x_vals,T)
Yv=map(y_vals,T)
X,Y = np.meshgrid(np.arange(-1000,1000),np.arange(-1000,1000))

fig = plt.figure()
fig.subplots_adjust(left=0.2, wspace=0.6)
ax1 = fig.add_subplot(111)
ax1.plot(Xv,Yv)
ax1.set_title('The vectorfield an a trajectory')
ax1.set_xlabel('Romeo')
ax1.set_ylabel('Juliet')
#ax1.set_ylim(0, 4)
plt.savefig("myfile.pdf", format='pdf')

L.addText("\
\\begin{figure}[t]\n\
\\includegraphics[width=12cm]{myfile}\n\
\\caption{TEXT}\n\
\\end{figure}\n\
")


L.write()






