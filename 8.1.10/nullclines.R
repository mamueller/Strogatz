#!/usr/bin/Rscript
# vim: set expandtab ts=2
ET=seq(0,1,by=0.01)
pdf("nullclines.pdf")
ST=ET
plot(ST,ET)
ST=1/(ET-ET^2)
lines(ST,ET)
lines(ST,0.1*ET)
lines(ST,10*ET)
dev.off()
