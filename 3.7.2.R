#!/usr/bin/Rscript
r=function(x){x^3/(1+x^2)^2}
k=function(x){2*x^3/(x^2-1)}
x=seq(1,20,0.01)
x0=sqrt(3)
pdf("3.7.2.pdf")
plot(type="l",x,r(x))
points(x0,r(x0),col="red")
plot(type="l",x,k(x))
points(x0,k(x0),col="red")
plot(type="l",k(x),r(x))
points(k(x0),r(x0),col="red")
dev.off()

