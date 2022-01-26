rm(list= ls())
library(ncdf4)
source('~/TOOLS/R/Rnoc_350.R')
source('~/TOOLS/R/listexp.R')
# ==========================================================================
#
#
# MOCobs = (COM0 - FST) + EKM + GEOobs
#
# EKM : Ekman compensated
#
# FST : Florida non compensated
# COM0 : compensation for lorida
# ==> COM0 - FST : Florida compensated
# GEO obs : Geostrophic component computed as it is in the RAPID array.
#
diagid='valmocGEOtot'
#diagid='valormoc'
freq='d05'
e7period=c(2007,2011)
e9period=c(2009,2012)
# ==========================================================================
# RAPID dataset
# =============
#obs.f = '/group_workspaces/jasmin2/nemo/vol5/public/OBS/VALOR/moc_transports.nc'
obs.f = '/gws/nopw/j04/nemo_vol5/public/OBS/VALOR/moc_transports.nc'

obs.moc = mynt(obs.f, variable = 'moc_mar_hc10')
obs.ekm = mynt(obs.f, variable = 't_ek10'      )
obs.geo = mynt(obs.f, variable = 't_umo10'     )
obs.fst = mynt(obs.f, variable = 't_gs10'      )
#
obs.moc$time = obs.moc$time - 86400
obs.ekm$time = obs.ekm$time - 86400
obs.geo$time = obs.geo$time - 86400
obs.fst$time = obs.fst$time - 86400
#
# select_period
obs.moc = select_period(obs.moc, period=c(2004,2012))
obs.ekm = select_period(obs.ekm, period=c(2004,2012))
obs.geo = select_period(obs.geo, period=c(2004,2012))
obs.fst = select_period(obs.fst, period=c(2004,2012))
#
# 5-day average
obs.moc.tmp = array( obs.moc$values, dim=c(10,length(obs.moc$values)/10))
obs.ekm.tmp = array( obs.ekm$values, dim=c(10,length(obs.ekm$values)/10))
obs.geo.tmp = array( obs.geo$values, dim=c(10,length(obs.geo$values)/10))
obs.fst.tmp = array( obs.fst$values, dim=c(10,length(obs.fst$values)/10))
obs.moc.5d.values = apply( obs.moc.tmp, 2, mean)
obs.ekm.5d.values = apply( obs.ekm.tmp, 2, mean)
obs.geo.5d.values = apply( obs.geo.tmp, 2, mean)
obs.fst.5d.values = apply( obs.fst.tmp, 2, mean)
obs.moc.5d.time = obs.moc$time[seq(from=5,to=length(obs.moc$values),by=10)]
obs.ekm.5d.time = obs.ekm$time[seq(from=5,to=length(obs.ekm$values),by=10)]
obs.geo.5d.time = obs.geo$time[seq(from=5,to=length(obs.geo$values),by=10)]
obs.fst.5d.time = obs.fst$time[seq(from=5,to=length(obs.fst$values),by=10)]
#
obs.moc$values = obs.moc.5d.values
obs.ekm$values = obs.ekm.5d.values
obs.geo$values = obs.geo.5d.values
obs.fst$values = obs.fst.5d.values
#
obs.moc$time = obs.moc.5d.time
obs.ekm$time = obs.ekm.5d.time
obs.geo$time = obs.geo.5d.time
obs.fst$time = obs.fst.5d.time

# ==========================================================================
n6   = lexp[['N006']] 

n6.f   = sprintf('%s/%s', n6$cdfdir,   diagfname( n6,   diagid, freq))
#
# read data
# =========
n6.mocz    = mynt( n6.f,   variable='MOC'   )
#
n6.mocrz   = mynt( n6.f,   variable='MOCobs')
n6.ekmz    = mynt( n6.f,   variable='EKM'   )
n6.geoz    = mynt( n6.f,   variable='GEOobs')
n6.fstz    = mynt( n6.f,   variable='FST'   )
n6.com0z   = mynt( n6.f,   variable='COM0'  )

# Time axis
n6.mocz$timec  = 'gregorian'
n6.mocrz$timec = 'gregorian'
n6.ekmz$timec  = 'gregorian'
n6.geoz$timec  = 'gregorian'
n6.fstz$timec  = 'gregorian'
n6.com0z$timec = 'gregorian'
#
# Select Period
# =============
#
n6.Nt   = length( n6.mocz$time  )

## # TEST BEGIN
## # +++++++++++++
## n6.fstz.av  = apply( n6.fstz$values,  1,mean)
## n6.com0z.av = apply( n6.com0z$values, 1,mean)
## n6.geoz.av  = apply( n6.geoz$values,  1,mean)
## n6.mocz.av  = apply( n6.mocz$values,  1,mean)
## n6.mocrz.av = apply( n6.mocrz$values, 1,mean)

## options(warn=-1)
## zz = get.lev()
## options(warn=0)

## fileout = "./RAPID_profiles_MOCobs_v2.pdf"
## pdf(fileout,width=8,height=10)
## ylim=c(-6000,0)
## xlim=c(-35,35)
## #
## par(oma = c(6,1,2,2))#,mar=c(2.5,2.4,2,1.6), mgp=c(1.5, 0.5, 0))
## plot(n6.fstz.av,-zz$values,
##      type='l',col='blue',lwd=2,
##      yaxt='n',xlim=xlim,
##      ylab='',xlab='Sv',main='')
## par(new=T)
## points(n6.com0z.av,-zz$values,
##      type='l',col='purple', lwd=2)
## par(new=T)
## points(n6.geoz.av,-zz$values,
##      type='l',col='pink',lwd=2)
## par(new=T)
## points(n6.mocz.av,-zz$values,
##      type='l',col='black',lwd=2)
## par(new=T)
## points(n6.mocrz.av,-zz$values,
##      type='l',col='red',lwd=2)
## axis(2,at=-zz$values,labels=round(zz$values))
## par(fig = c(0, 1, 0.05, 1), oma = c(0, 0, 0, 0), mar = c(0, 0, 0, 0), new = T)
## plot(0, 0, type = "n", bty = "n", xaxt = "n", yaxt = "n")
## legend('bottom',c('Florida Strait','Com0','Geostrophic obs','moc','mocr'),
##        col=c('blue','purple','pink','black','red'),
##        lty=rep(1,3),lwd = rep(2,3),bty='n',
##        horiz=T,xpd=T,inset=c(0,0))
## graphics.off()


## # TEST END
## # +++++++++++++
#
# Time series
# ===========
# init
n6.moc    = n6.mocz
n6.mocr   = n6.mocrz
n6.ekm    = n6.ekmz
n6.geo    = n6.geoz
n6.fst    = n6.fstz
n6.com0    = n6.fstz
#
# depth
n6.iz   = getts(n6.mocrz,   variable='moc', index=T)$values
test = getts(n6.geoz, variable='umo')
#
n6.mocr$values  = n6.mocrz$values[ array(data=c(n6.iz,   seq(n6.Nt)),  dim=c(n6.Nt,2))  ]
n6.ekm$values   = n6.ekmz$values[  array(data=c(n6.iz,   seq(n6.Nt)),   dim=c(n6.Nt,2))  ]
n6.geo$values   = n6.geoz$values[  array(data=c(n6.iz,   seq(n6.Nt)),   dim=c(n6.Nt,2))  ]
n6.fst$values   = n6.fstz$values[  1,]
n6.com0$values  = n6.com0z$values[ 1,] - n6.com0z$values[ array(data=c(n6.iz,   seq(n6.Nt)),   dim=c(n6.Nt,2))  ]
n6.moc$values   = getts( n6.mocz,   variable='moc')$values

n6.geo$values = n6.geo$values - n6.com0$values

#
# Monthly values
# ==============
smooth=T
if (smooth) {
  thalf = 3
  obs.moc$values   = myrunmean( obs.moc$values,   thalf) 
  n6.moc$values    = myrunmean( n6.moc$values,    thalf)
  n6.mocr$values   = myrunmean( n6.mocr$values,   thalf)
  #
  obs.ekm$values   = myrunmean( obs.ekm$values,  thalf)
  n6.ekm$values    = myrunmean( n6.ekm$values,   thalf)
  #
  obs.geo$values   = myrunmean( obs.geo$values,  thalf)
  n6.geo$values    = myrunmean( n6.geo$values,   thalf)
  #
  obs.fst$values   = myrunmean( obs.fst$values,  thalf)
  n6.fst$values    = myrunmean( n6.fst$values,   thalf)
}
#
# Mean and STD
# ============
# suppression de janvier-mars 2004
tmp = select_time(n6.moc,season='JFM',period=c(2004,2004))
jfm.len = length(tmp$values)
i0 = jfm.len+1

n6.moc.ref  = select_period(n6.moc,  period=c(2004,2012))
n6.mocr.ref = select_period(n6.mocr, period=c(2004,2012))
n6.ekm.ref  = select_period(n6.ekm,  period=c(2004,2012))
n6.geo.ref  = select_period(n6.geo,  period=c(2004,2012))
n6.fst.ref  = select_period(n6.fst,  period=c(2004,2012))
#
n6.moc.ref$values  = n6.moc.ref$values[  i0:length(n6.moc.ref$values) ]
n6.moc.ref$time    = n6.moc.ref$time[    i0:length(n6.moc.ref$time)   ]
n6.mocr.ref$values = n6.mocr.ref$values[ i0:length(n6.mocr.ref$values)]
n6.mocr.ref$time   = n6.mocr.ref$time[   i0:length(n6.mocr.ref$time)  ]
n6.ekm.ref$values  = n6.ekm.ref$values[  i0:length(n6.ekm.ref$values) ]
n6.ekm.ref$time    = n6.ekm.ref$time[    i0:length(n6.ekm.ref$time)   ]
n6.geo.ref$values  = n6.geo.ref$values[  i0:length(n6.geo.ref$values) ]
n6.geo.ref$time    = n6.geo.ref$time[    i0:length(n6.geo.ref$time)   ]
n6.fst.ref$values  = n6.fst.ref$values[  i0:length(n6.fst.ref$values) ]
n6.fst.ref$time    = n6.fst.ref$time[    i0:length(n6.fst.ref$time)   ]

n6.moc.mean  = mean( n6.moc.ref$values )
n6.mocr.mean = mean( n6.mocr.ref$values)
n6.ekm.mean  = mean( n6.ekm.ref$values )
n6.geo.mean  = mean( n6.geo.ref$values )
n6.fst.mean  = mean( n6.fst.ref$values )
#
obs.moc.mean  = mean( obs.moc$values )
obs.ekm.mean  = mean( obs.ekm$values )
obs.geo.mean  = mean( obs.geo$values )
obs.fst.mean  = mean( obs.fst$values )
#
# Correlation # values in the paper should be without wmoothing, but the figure 01 is with smoothing easy reading
## mocr.cor = cor(obs.moc$values, n6.mocr.ref$values)
## ekm.cor  = cor(obs.ekm$values, n6.ekm.ref$values )
## geo.cor  = cor(obs.geo$values, n6.geo.ref$values )
## fst.cor  = cor(obs.fst$values, n6.fst.ref$values )
mocr.cor = cor(mydetrend2(obs.moc$values), mydetrend2(n6.mocr.ref$values))
ekm.cor  = cor(mydetrend2(obs.ekm$values), mydetrend2(n6.ekm.ref$values ))
geo.cor  = cor(mydetrend2(obs.geo$values), mydetrend2(n6.geo.ref$values ))
fst.cor  = cor(mydetrend2(obs.fst$values), mydetrend2(n6.fst.ref$values ))
#
# Anomalies
# =========
anomalies = F
if(anomalies) {
    obs.moc$values  = obs.moc$values  - obs.moc.mean
    n6.moc$values   = n6.moc$values   - n6.moc.mean
    n6.mocr$values   = n6.mocr$values   - n6.mocr.mean
    #
    obs.ekm$values   = obs.ekm$values  - obs.ekm.mean
    n6.ekm$values    = n6.ekm$values   - n6.ekm.mean
    #
    obs.geo$values   = obs.geo$values  - obs.geo.mean
    n6.geo$values    = n6.geo$values   - n6.geo.mean
    #
    obs.fst$values   = obs.fst$values  - obs.fst.mean
    n6.fst$values    = n6.fst$values   - n6.fst.mean
}
#
# Axes des temps
# ==============
n6.axt  = to.date(n6.moc$time,n6.moc$timeu,cal=n6.moc$timec)
obs.axt = to.date(obs.moc$time,obs.moc$timeu,cal=obs.moc$timec)
#
#
## # ==========================================================================
# PLOT
# ===========================================================================
fileout = "./figure_07_ATB.pdf"
pdf(fileout,width=6,height=6)
#
lwd = 1.4
xlim  = c(as.PCICt("2004-01-01",cal="gregorian"),as.PCICt("2013-01-01",cal="gregorian"))
xtickpos = c(as.PCICt("2004-01-01",cal="gregorian"),as.PCICt("2005-01-01",cal="gregorian"),as.PCICt("2006-01-01",cal="gregorian"),as.PCICt("2007-01-01",cal="gregorian"),as.PCICt("2008-01-01",cal="gregorian"),as.PCICt("2009-01-01",cal="gregorian"),as.PCICt("2010-01-01",cal="gregorian"),as.PCICt("2011-01-01",cal="gregorian"),as.PCICt("2012-01-01",cal="gregorian"),as.PCICt("2013-01-01",cal="gregorian"))#,as.PCICt("2012-01-01",cal="gregorian"),as.PCICt("2013-01-01",cal="gregorian"))
yrlist=c('2004','2005','2006','2007','2008','2009','2010','2011','2012','2013')
yrlist0 = c('','','','','','','','','','')

if (anomalies) {
    ylim.moc  = c(-13,10)
    ylim.mocr = ylim.moc
    ylim.ekm  = c(-8,6)
    ylim.geo  = c(-10,10)
    ylim.fst  = c(-6,6) 
} else {
    ylim.moc  = c(5,   25)
    ylim.mocr = ylim.moc
    ylim.ekm  = c(-5,  10)
    ylim.geo  = c(-25, 2 )
    ylim.fst  = c(15,  30)
    ylim.all  = c(-25, 37)
}

par(fig = c(0, 1, 0.71, 1),mar=c(0.5,2.4,1,1), mgp=c(1.3, 0.5, 0))
plot(n6.axt,n6.mocr$values,
     main = 'AMOC',
     ylab='Sv',xlab='',
     lwd=lwd,type='l',col='red',
     xaxt='n',
     xlim=xlim,ylim=ylim.moc,
     cex=.6,cex.main=.9,cex.axis=.7,cex.lab=0.7)
points(n6.axt,n6.moc$values,
 ##    lwd=2,lty='dotted',type='l',col='black')
     lwd=1,type='l',col='black')
points(obs.axt,obs.moc$values,
     lwd=1,lty='dashed',type='l',col='red')
abline(h=0,col='black',lwd=0.5)
axis(side = 1, at = xtickpos,labels=yrlist0,cex.axis=0.7)
#
# Components
par(new=T,fig = c(0, 1, 0.05, 0.70),mar=c(0.5,2.4,1,1), mgp=c(1.3, 0.5, 0))
plot(n6.axt,n6.ekm$values,
     main = 'Components',
     ylab='Sv',xlab='',
     lwd=lwd,type='l',col='black',
     xaxt='n',
     xlim=xlim,ylim=ylim.all,
     cex=.6,cex.main=.9,cex.axis=.7,cex.lab=0.7)
points(obs.axt,obs.ekm$values,
     lwd=1,lty='dashed',type='l',col='black')
#
points(n6.axt,n6.geo$values,
     lwd=lwd,type='l',col='deeppink')
points(obs.axt,obs.geo$values,
     lwd=1,lty='dashed',type='l',col='deeppink')
#
points(n6.axt,n6.fst$values,
     main = 'Florida Strait',
     lwd=lwd,type='l',col='blue')
points(obs.axt,obs.fst$values,
     lwd=1,lty='dashed',type='l',col='blue')
#abline(h=0,col='black',lwd=0.5)
axis(side = 1, at = xtickpos,labels=yrlist0,cex.axis=0.7)
#
#axis(side = 1, at = xtickpos, labels = yrlist0,cex.axis=0.7, padj=-.5)
#
# year axis
par(new=T,fig = c(0, 1, 0, .05),mar=c(0.5,2.4,1,1), mgp=c(1.3, 0.5, 0))
plot0(xlim=xlim)
axis(side = 3, col='white',col.axis='black',at = xtickpos, labels = yrlist,cex.axis=0.8, padj=1)
graphics.off()
 
# ===========================================================================
