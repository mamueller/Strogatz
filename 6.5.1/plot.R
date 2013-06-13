#!/usr/bin/Rscript
library(pplane)
#fDeriv <- predatorprey(lambda=3, epsilon=2, delta=3, eta=2)

fDeriv <- function(x,y){c(dx=y,dy=x^3-x)}

#
# set up a plotting window
# windows(width = 4.6, height = 3.2, pointsize = 10); par( las = 1, mar = c(2, 3.3, 0, 0) + 0.3, tck = 0.02, mgp = c(1.1, 0.2, 0))
#

# default: strength is colored, no arrow heads, same length

pdf(file="phasePlot.pdf")
tmp <- phaseArrows( fDeriv, c(-2,2),c(-2,2) );


#phaseContours(tmp$z, tmp$xy, add=TRUE)


#phaseNullclines(tmp$z, tmp$xy, add=TRUE)


#drawTrajectories( fDeriv, tEnd=3, tCut=600,x0=list(x=2*seq(0,1,by=.05),y=2*seq(0,1,by=.1)), fLapply=sfLapply  )    # initial starting point by script
#drawTrajectories( fDeriv, tEnd=3, tCut=600,x0=list(x=2*seq(-1,0,by=.05),y=2*seq(-1,0,by=.1)), fLapply=sfLapply  )    # initial starting point by script

#drawTrajectories( fDeriv, tEnd=3, tCut=600,x0=c(c(-2,1),c(-1,1),c(1,1),c(2,1) ))    # initial starting point by script



#drawTrajectories( fDeriv, tEnd=3, x0=locator(2,"p") )   # set the starting point in the graph: need to click several times
dev.off()
#
# add arrow heads and use colors for log scale, scale vector length


#phaseArrows( fDeriv, c(-2,5),c(-2,5), logLength=TRUE, arrowHeads=0.04, arrowLength=0 );

# for background, sometimes a decent color is useful

#tmp <- phaseArrows( fDeriv, c(-2,5),c(-2,5), col="grey" );

#


# may use parallel calculation of flow field and trajectories

if( FALSE ){    # do not run on R CMC check
    require(snowfall)
    tmp <- phaseArrows( fDeriv, c(-2,5),c(-2,5), useSnowfall=TRUE );       # using parallel calculation
    drawTrajectories( fDeriv, tEnd=3, x0=list(x=1,y=c(2:5)), fLapply=sfLapply )    # initial starting point by script
}
