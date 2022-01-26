rm(list= ls())
library(ncdf)
source('~/TOOLS/R/Rnoc.R')
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
freq='d05'
e7period=c(2007,2010)
e9period=c(2009,2012)
# ==========================================================================
n6   = lexp[['N006']]
e7m1 = lexp[['N12_2007_01']]
e7m2 = lexp[['N12_2007_02']]
e7m3 = lexp[['N12_2007_03']]
e9m1 = lexp[['N12_2009_01']]
e9m2 = lexp[['N12_2009_02']]
e9m3 = lexp[['N12_2009_03']]

n6.f   = sprintf('%s/%s', n6$cdfdir,   diagfname( n6,   diagid, freq))
e7m1.f = sprintf('%s/%s', e7m1$cdfdir, diagfname( e7m1, diagid, freq))
e7m2.f = sprintf('%s/%s', e7m2$cdfdir, diagfname( e7m2, diagid, freq))
e7m3.f = sprintf('%s/%s', e7m3$cdfdir, diagfname( e7m3, diagid, freq))
e9m1.f = sprintf('%s/%s', e9m1$cdfdir, diagfname( e9m1, diagid, freq))
e9m2.f = sprintf('%s/%s', e9m2$cdfdir, diagfname( e9m2, diagid, freq))
e9m3.f = sprintf('%s/%s', e9m3$cdfdir, diagfname( e9m3, diagid, freq))
#
# read data
# =========
n6.mocz    = mynt( n6.f,   variable='MOC'   )
e7m1.mocz  = mynt( e7m1.f, variable='MOC'   )
e7m2.mocz  = mynt( e7m2.f, variable='MOC'   )
e7m3.mocz  = mynt( e7m3.f, variable='MOC'   )
e9m1.mocz  = mynt( e9m1.f, variable='MOC'   )
e9m2.mocz  = mynt( e9m2.f, variable='MOC'   )
e9m3.mocz  = mynt( e9m3.f, variable='MOC'   )
#
n6.mocrz   = mynt( n6.f,   variable='MOCobs')
e7m1.mocrz = mynt( e7m1.f, variable='MOCobs')
e7m2.mocrz = mynt( e7m2.f, variable='MOCobs')
e7m3.mocrz = mynt( e7m3.f, variable='MOCobs')
e9m1.mocrz = mynt( e9m1.f, variable='MOCobs')
e9m2.mocrz = mynt( e9m2.f, variable='MOCobs')
e9m3.mocrz = mynt( e9m3.f, variable='MOCobs')
#
n6.ekmz    = mynt( n6.f,   variable='EKM'   )
e7m1.ekmz  = mynt( e7m1.f, variable='EKM'   )
e7m2.ekmz  = mynt( e7m2.f, variable='EKM'   )
e7m3.ekmz  = mynt( e7m3.f, variable='EKM'   )
e9m1.ekmz  = mynt( e9m1.f, variable='EKM'   )
e9m2.ekmz  = mynt( e9m2.f, variable='EKM'   )
e9m3.ekmz  = mynt( e9m3.f, variable='EKM'   )
#
n6.geoz     = mynt( n6.f,   variable='GEOobs')
e7m1.geoz   = mynt( e7m1.f, variable='GEOobs')
e7m2.geoz   = mynt( e7m2.f, variable='GEOobs')
e7m3.geoz   = mynt( e7m3.f, variable='GEOobs')
e9m1.geoz   = mynt( e9m1.f, variable='GEOobs')
e9m2.geoz   = mynt( e9m2.f, variable='GEOobs')
e9m3.geoz   = mynt( e9m3.f, variable='GEOobs')
#
n6.fstz    = mynt( n6.f,   variable='FST'   )
e7m1.fstz  = mynt( e7m1.f, variable='FST'   )
e7m2.fstz  = mynt( e7m2.f, variable='FST'   )
e7m3.fstz  = mynt( e7m3.f, variable='FST'   )
e9m1.fstz  = mynt( e9m1.f, variable='FST'   )
e9m2.fstz  = mynt( e9m2.f, variable='FST'   )
e9m3.fstz  = mynt( e9m3.f, variable='FST'   )
#
n6.com0z   = mynt( n6.f,   variable='COM0'  )
e7m1.com0z = mynt( e7m1.f, variable='COM0'  )
e7m2.com0z = mynt( e7m2.f, variable='COM0'  )
e7m3.com0z = mynt( e7m3.f, variable='COM0'  )
e9m1.com0z = mynt( e9m1.f, variable='COM0'  )
e9m2.com0z = mynt( e9m2.f, variable='COM0'  )
e9m3.com0z = mynt( e9m3.f, variable='COM0'  )
#
n6.fstz$values    = n6.com0z$values   - n6.fstz$values
e7m1.fstz$values = e7m1.com0z$values - e7m1.fstz$values
e7m2.fstz$values = e7m2.com0z$values - e7m2.fstz$values
e7m3.fstz$values = e7m3.com0z$values - e7m3.fstz$values
e9m1.fstz$values = e9m1.com0z$values - e9m1.fstz$values
e9m2.fstz$values = e9m2.com0z$values - e9m2.fstz$values
e9m3.fstz$values = e9m3.com0z$values - e9m3.fstz$values

# Time axis
n6.mocz$timec  = 'gregorian'
n6.mocrz$timec = 'gregorian'
n6.ekmz$timec  = 'gregorian'
n6.geoz$timec  = 'gregorian'
n6.fstz$timec  = 'gregorian'
#
# Select Period
# =============
e7m1.mocz  = select_period( e7m1.mocz,  e7period)
e7m2.mocz  = select_period( e7m2.mocz,  e7period)
e7m3.mocz  = select_period( e7m3.mocz,  e7period)
e7m1.mocrz = select_period( e7m1.mocrz, e7period)
e7m2.mocrz = select_period( e7m2.mocrz, e7period)
e7m3.mocrz = select_period( e7m3.mocrz, e7period)
e7m1.ekmz  = select_period( e7m1.ekmz,  e7period)
e7m2.ekmz  = select_period( e7m2.ekmz,  e7period)
e7m3.ekmz  = select_period( e7m3.ekmz,  e7period)
e7m1.geoz  = select_period( e7m1.geoz,  e7period)
e7m2.geoz  = select_period( e7m2.geoz,  e7period)
e7m3.geoz  = select_period( e7m3.geoz,  e7period)
e7m1.fstz  = select_period( e7m1.fstz,  e7period)
e7m2.fstz  = select_period( e7m2.fstz,  e7period)
e7m3.fstz  = select_period( e7m3.fstz,  e7period)
#
e9m1.mocz  = select_period( e9m1.mocz,  e9period)
e9m2.mocz  = select_period( e9m2.mocz,  e9period)
e9m3.mocz  = select_period( e9m3.mocz,  e9period)
e9m1.mocrz = select_period( e9m1.mocrz, e9period)
e9m2.mocrz = select_period( e9m2.mocrz, e9period)
e9m3.mocrz = select_period( e9m3.mocrz, e9period)
e9m1.ekmz  = select_period( e9m1.ekmz,  e9period)
e9m2.ekmz  = select_period( e9m2.ekmz,  e9period)
e9m3.ekmz  = select_period( e9m3.ekmz,  e9period)
e9m1.geoz  = select_period( e9m1.geoz,  e9period)
e9m2.geoz  = select_period( e9m2.geoz,  e9period)
e9m3.geoz  = select_period( e9m3.geoz,  e9period)
e9m1.fstz  = select_period( e9m1.fstz,  e9period)
e9m2.fstz  = select_period( e9m2.fstz,  e9period)
e9m3.fstz  = select_period( e9m3.fstz,  e9period)
#
n6.Nt   = length( n6.mocz$time  )
e7m1.Nt = length( e7m1.mocz$time)
e7m2.Nt = length( e7m2.mocz$time)
e7m3.Nt = length( e7m3.mocz$time)
e9m1.Nt = length( e9m1.mocz$time)
e9m2.Nt = length( e9m2.mocz$time)
e9m3.Nt = length( e9m3.mocz$time)
#
# Time series
# ===========
# init
n6.moc    = n6.mocz
e7m1.moc  = e7m1.mocz
e7m2.moc  = e7m2.mocz
e7m3.moc  = e7m3.mocz
e9m1.moc  = e9m1.mocz
e9m2.moc  = e9m2.mocz
e9m3.moc  = e9m3.mocz
#
n6.mocr   = n6.mocrz
e7m1.mocr = e7m1.mocrz
e7m2.mocr = e7m2.mocrz
e7m3.mocr = e7m3.mocrz
e9m1.mocr = e9m1.mocrz
e9m2.mocr = e9m2.mocrz
e9m3.mocr = e9m3.mocrz
#
n6.ekm    = n6.ekmz
e7m1.ekm  = e7m1.ekmz
e7m2.ekm  = e7m2.ekmz
e7m3.ekm  = e7m3.ekmz
e9m1.ekm  = e9m1.ekmz
e9m2.ekm  = e9m2.ekmz
e9m3.ekm  = e9m3.ekmz
#
n6.geo    = n6.geoz
e7m1.geo  = e7m1.geoz
e7m2.geo  = e7m2.geoz
e7m3.geo  = e7m3.geoz
e9m1.geo  = e9m1.geoz
e9m2.geo  = e9m2.geoz
e9m3.geo  = e9m3.geoz
#
n6.fst    = n6.fstz
e7m1.fst  = e7m1.fstz
e7m2.fst  = e7m2.fstz
e7m3.fst  = e7m3.fstz
e9m1.fst  = e9m1.fstz
e9m2.fst  = e9m2.fstz
e9m3.fst  = e9m3.fstz
#
# depth
n6.iz   = getts(n6.mocrz,   variable='moc', index=T)$values
e7m1.iz = getts(e7m1.mocrz, variable='moc', index=T)$values
e7m2.iz = getts(e7m2.mocrz, variable='moc', index=T)$values
e7m3.iz = getts(e7m3.mocrz, variable='moc', index=T)$values
e9m1.iz = getts(e9m1.mocrz, variable='moc', index=T)$values
e9m2.iz = getts(e9m2.mocrz, variable='moc', index=T)$values
e9m3.iz = getts(e9m3.mocrz, variable='moc', index=T)$values
#
n6.mocr$values   = n6.mocrz$values[   array(data=c(n6.iz,   seq(n6.Nt)),  dim=c(n6.Nt,2))  ]
e7m1.mocr$values = e7m1.mocrz$values[ array(data=c(e7m1.iz, seq(e7m1.Nt)),dim=c(e7m1.Nt,2))]
e7m2.mocr$values = e7m2.mocrz$values[ array(data=c(e7m2.iz, seq(e7m2.Nt)),dim=c(e7m2.Nt,2))]
e7m3.mocr$values = e7m3.mocrz$values[ array(data=c(e7m3.iz, seq(e7m3.Nt)),dim=c(e7m3.Nt,2))]
e9m1.mocr$values = e9m1.mocrz$values[ array(data=c(e9m1.iz, seq(e9m1.Nt)),dim=c(e9m1.Nt,2))]
e9m2.mocr$values = e9m2.mocrz$values[ array(data=c(e9m2.iz, seq(e9m2.Nt)),dim=c(e9m2.Nt,2))]
e9m3.mocr$values = e9m3.mocrz$values[ array(data=c(e9m3.iz, seq(e9m3.Nt)),dim=c(e9m3.Nt,2))]
#
n6.ekm$values   = n6.ekmz$values[  array(data=c(n6.iz,   seq(n6.Nt)),   dim=c(n6.Nt,2))  ]
e7m1.ekm$values = e7m1.ekmz$values[array(data=c(e7m1.iz, seq(e7m1.Nt)), dim=c(e7m1.Nt,2))]
e7m2.ekm$values = e7m2.ekmz$values[array(data=c(e7m2.iz, seq(e7m2.Nt)), dim=c(e7m2.Nt,2))]
e7m3.ekm$values = e7m3.ekmz$values[array(data=c(e7m3.iz, seq(e7m3.Nt)), dim=c(e7m3.Nt,2))]
e9m1.ekm$values = e9m1.ekmz$values[array(data=c(e9m1.iz, seq(e9m1.Nt)), dim=c(e9m1.Nt,2))]
e9m2.ekm$values = e9m2.ekmz$values[array(data=c(e9m2.iz, seq(e9m2.Nt)), dim=c(e9m2.Nt,2))]
e9m3.ekm$values = e9m3.ekmz$values[array(data=c(e9m3.iz, seq(e9m3.Nt)), dim=c(e9m3.Nt,2))]
#
n6.geo$values   = n6.geoz$values[  array(data=c(n6.iz,   seq(n6.Nt)),   dim=c(n6.Nt,2))  ]
e7m1.geo$values = e7m1.geoz$values[array(data=c(e7m1.iz, seq(e7m1.Nt)), dim=c(e7m1.Nt,2))]
e7m2.geo$values = e7m2.geoz$values[array(data=c(e7m2.iz, seq(e7m2.Nt)), dim=c(e7m2.Nt,2))]
e7m3.geo$values = e7m3.geoz$values[array(data=c(e7m3.iz, seq(e7m3.Nt)), dim=c(e7m3.Nt,2))]
e9m1.geo$values = e9m1.geoz$values[array(data=c(e9m1.iz, seq(e9m1.Nt)), dim=c(e9m1.Nt,2))]
e9m2.geo$values = e9m2.geoz$values[array(data=c(e9m2.iz, seq(e9m2.Nt)), dim=c(e9m2.Nt,2))]
e9m3.geo$values = e9m3.geoz$values[array(data=c(e9m3.iz, seq(e9m3.Nt)), dim=c(e9m3.Nt,2))]
#
n6.fst$values   = n6.fstz$values[  array(data=c(n6.iz,   seq(n6.Nt)),   dim=c(n6.Nt,2))  ]
e7m1.fst$values = e7m1.fstz$values[array(data=c(e7m1.iz, seq(e7m1.Nt)), dim=c(e7m1.Nt,2))]
e7m2.fst$values = e7m2.fstz$values[array(data=c(e7m2.iz, seq(e7m2.Nt)), dim=c(e7m2.Nt,2))]
e7m3.fst$values = e7m3.fstz$values[array(data=c(e7m3.iz, seq(e7m3.Nt)), dim=c(e7m3.Nt,2))]
e9m1.fst$values = e9m1.fstz$values[array(data=c(e9m1.iz, seq(e9m1.Nt)), dim=c(e9m1.Nt,2))]
e9m2.fst$values = e9m2.fstz$values[array(data=c(e9m2.iz, seq(e9m2.Nt)), dim=c(e9m2.Nt,2))]
e9m3.fst$values = e9m3.fstz$values[array(data=c(e9m3.iz, seq(e9m3.Nt)), dim=c(e9m3.Nt,2))]
#
n6.moc$values   = getts( n6.mocz,   variable='moc')$values
e7m1.moc$values = getts( e7m1.mocz, variable='moc')$values
e7m2.moc$values = getts( e7m2.mocz, variable='moc')$values
e7m3.moc$values = getts( e7m3.mocz, variable='moc')$values
e9m1.moc$values = getts( e9m1.mocz, variable='moc')$values
e9m2.moc$values = getts( e9m2.mocz, variable='moc')$values
e9m3.moc$values = getts( e9m3.mocz, variable='moc')$values
## #
#
#
# Axes des temps
# ==============
e7.axt  = to.date(e7m1.moc$time,e7m1.moc$timeu,cal=e7m1.moc$timec)
e7.axt0 = as.POSIXct(as.character(e7.axt)) - as.POSIXct("2007-01-01")
e9.axt  = to.date(e9m1.moc$time,e9m1.moc$timeu,cal=e9m1.moc$timec)
e9.axt0 = as.POSIXct(as.character(e9.axt)) - as.POSIXct("2009-01-01")
n6.axt  = to.date(n6.moc$time,n6.moc$timeu,cal=n6.moc$timec)
#
## # ==========================================================================
## # ENSEMBLES
## # =========
#
# 5-day mean
e7.moc  = array( c(e7m1.moc$values, e7m2.moc$values, e7m3.moc$values,
    select_period(n6.moc,e7period)$values),
    dim=c(e7m1.Nt,4))
e7.mocr = array( c(e7m1.mocr$values, e7m2.mocr$values, e7m3.mocr$values,
    select_period(n6.mocr,e7period)$values),
    dim=c(e7m1.Nt,4))
e7.ekm  = array( c(e7m1.ekm$values, e7m2.ekm$values, e7m3.ekm$values,
    select_period(n6.ekm,e7period)$values),
    dim=c(e7m1.Nt,4))
e7.geo  = array( c(e7m1.geo$values, e7m2.geo$values, e7m3.geo$values,
    select_period(n6.geo,e7period)$values),
    dim=c(e7m1.Nt,4))
e7.fst  = array( c(e7m1.fst$values, e7m2.fst$values, e7m3.fst$values,
    select_period(n6.fst,e7period)$values),
    dim=c(e7m1.Nt,4))
#
e9.moc  = array( c(e9m1.moc$values, e9m2.moc$values, e9m3.moc$values,
    select_period(n6.moc,e9period)$values),
    dim=c(e9m1.Nt,4))
e9.mocr = array( c(e9m1.mocr$values, e9m2.mocr$values, e9m3.mocr$values,
    select_period(n6.mocr,e9period)$values),
    dim=c(e9m1.Nt,4))
e9.ekm  = array( c(e9m1.ekm$values, e9m2.ekm$values, e9m3.ekm$values,
    select_period(n6.ekm,e9period)$values),
    dim=c(e9m1.Nt,4))
e9.geo  = array( c(e9m1.geo$values, e9m2.geo$values, e9m3.geo$values,
    select_period(n6.geo,e9period)$values),
    dim=c(e9m1.Nt,4))
e9.fst  = array( c(e9m1.fst$values, e9m2.fst$values, e9m3.fst$values,
    select_period(n6.fst,e9period)$values),
    dim=c(e9m1.Nt,4))
## #
#
#
# Ensemble SPREAD
# ===============
# ref N06
# -------
n6.moc.ref = select_period(n6.moc,c(1960,2012))
n6.moc.av  = mean( n6.moc.ref$values, na.rm=T)
n6.moc.var = var(  n6.moc.ref$values, na.rm=T)
#
# 5-day means
# -----------
e7.moc.em  = apply( e7.moc,  1, mean, na.rm=T)
e7.mocr.em = apply( e7.mocr, 1, mean, na.rm=T)
e7.ekm.em  = apply( e7.ekm,  1, mean, na.rm=T)
e7.geo.em  = apply( e7.geo,  1, mean, na.rm=T)
e7.fst.em  = apply( e7.fst,  1, mean, na.rm=T)
e7.moc.var  = apply( e7.moc,  1, var,   na.rm=T)
e7.mocr.var = apply( e7.mocr, 1, var,   na.rm=T)
e7.ekm.var  = apply( e7.ekm,  1, var,   na.rm=T)
e7.geo.var  = apply( e7.geo,  1, var,   na.rm=T)
e7.fst.var  = apply( e7.fst,  1, var,   na.rm=T)
#
e9.moc.em  = apply( e9.moc,  1, mean, na.rm=T)
e9.mocr.em = apply( e9.mocr, 1, mean, na.rm=T)
e9.ekm.em  = apply( e9.ekm,  1, mean, na.rm=T)
e9.geo.em  = apply( e9.geo,  1, mean, na.rm=T)
e9.fst.em  = apply( e9.fst,  1, mean, na.rm=T)
e9.moc.var  = apply( e9.moc,  1, var,   na.rm=T)
e9.mocr.var = apply( e9.mocr, 1, var,   na.rm=T)
e9.ekm.var  = apply( e9.ekm,  1, var,   na.rm=T)
e9.geo.var  = apply( e9.geo,  1, var,   na.rm=T)
e9.fst.var  = apply( e9.fst,  1, var,   na.rm=T)
#
# lissage :
smooth = F
if (smooth) {
    thalf = 3    # monthly
    # thalf = 9  # seasonal
    # thalf = 36 # annual
    e7.moc.var  = myrunmean( e7.moc.var,  thalf)
    e7.mocr.var = myrunmean( e7.mocr.var, thalf)
    e7.ekm.var  = myrunmean( e7.ekm.var,  thalf)
    e7.geo.var  = myrunmean( e7.geo.var,  thalf)
    e7.fst.var  = myrunmean( e7.fst.var,  thalf)
    e9.moc.var  = myrunmean( e9.moc.var,  thalf)
    e9.mocr.var = myrunmean( e9.mocr.var, thalf)
    e9.ekm.var  = myrunmean( e9.ekm.var,  thalf)
    e9.geo.var  = myrunmean( e9.geo.var,  thalf)
    e9.fst.var  = myrunmean( e9.fst.var,  thalf)
}
thalf=9
e7.moc.var.smooth  = myrunmean( e7.moc.var,  thalf)
e7.mocr.var.smooth = myrunmean( e7.mocr.var, thalf)
e7.ekm.var.smooth  = myrunmean( e7.ekm.var,  thalf)
e7.geo.var.smooth  = myrunmean( e7.geo.var,  thalf)
e7.fst.var.smooth  = myrunmean( e7.fst.var,  thalf)
e9.moc.var.smooth  = myrunmean( e9.moc.var,  thalf)
e9.mocr.var.smooth = myrunmean( e9.mocr.var, thalf)
e9.ekm.var.smooth  = myrunmean( e9.ekm.var,  thalf)
e9.geo.var.smooth  = myrunmean( e9.geo.var,  thalf)
e9.fst.var.smooth  = myrunmean( e9.fst.var,  thalf)


## #
#
# saturation value
# ================
tmin = 2*365+1
tmax = 4*365
e7.index = which(e7.axt0>=tmin & e7.axt0<tmax)
e9.index = which(e9.axt0>=tmin-1 & e9.axt0<tmax)
#
e.moc.sat  = mean(c( e7.moc.var[ e7.index], e9.moc.var[ e9.index]))
e.mocr.sat = mean(c( e7.mocr.var[e7.index], e9.mocr.var[e9.index]))
e.ekm.sat  = mean(c( e7.ekm.var[ e7.index], e9.ekm.var[ e9.index]))
e.geo.sat  = mean(c( e7.geo.var[ e7.index], e9.geo.var[ e9.index]))
e.fst.sat  = mean(c( e7.fst.var[ e7.index], e9.fst.var[ e9.index]))
#
# ===========================================================================
# PLOT
# ===========================================================================
fileout = "./figure_05.pdf"
pdf(fileout,width=6,height=6)
#
ylim.moc  = c(0,30)
xlim  = c(as.PCICt("2007-01-01",cal="gregorian"),as.PCICt("2011-01-01",cal="gregorian"))
xtickpos = c(as.PCICt("2007-01-01",cal="gregorian"),as.PCICt("2008-01-01",cal="gregorian"),as.PCICt("2009-01-01",cal="gregorian"),as.PCICt("2010-01-01",cal="gregorian"),as.PCICt("2011-01-01",cal="gregorian"),as.PCICt("2012-01-01",cal="gregorian"),as.PCICt("2013-01-01",cal="gregorian"))#,as.PCICt("2012-01-01",cal="gregorian"),as.PCICt("2013-01-01",cal="gregorian"))
yrlist=c('2007','2008','2009','2010','2011','2012','2013')
yrlist0 = c('','','','','','','','','','')
#
#
lwd = 1.5
#
# AMOC ensemble 2007
par(fig = c(0, 1, 0.7, 1),mar=c(0.5,2.4,1,1), mgp=c(1.3, 0.5, 0))
plot(n6.axt,n6.moc$values,
     main = '(a) Ensemble 2007',
     ylab='AMOC (Sv)',xlab='',
     lwd=lwd,type='l',col='black',
     xaxt='n',
     xlim=xlim,ylim=ylim.moc,
     cex=.6,cex.main=.9,cex.axis=.7,cex.lab=0.7)
points(e7.axt,e7.moc.em,
     lwd=1,type='l',col='red',lty=2)
myfill(e7.axt,
       e7.moc.em+2*sqrt(e7.moc.var),y_low=e7.moc.em-2*sqrt(e7.moc.var),
       col='red',trans=0.3)
axis(side = 1, at = xtickpos,labels=yrlist,cex.axis=0.7)
#
# AMOC ensemble 2009
xlim  = c(as.PCICt("2009-01-01",cal="gregorian"),as.PCICt("2013-01-01",cal="gregorian"))
xtickpos = c(as.PCICt("2009-01-01",cal="gregorian"),as.PCICt("2010-01-01",cal="gregorian"),as.PCICt("2011-01-01",cal="gregorian"),as.PCICt("2012-01-01",cal="gregorian"),as.PCICt("2013-01-01",cal="gregorian"))#,as.PCICt("2012-01-01",cal="gregorian"),as.PCICt("2013-01-01",cal="gregorian"))
yrlist=c('2009','2010','2011','2012','2013')
yrlist0 = c('','','','','','','','','','')
par(new=T,fig = c(0, 1, 0.36, 0.66),mar=c(0.5,2.4,1,1), mgp=c(1.3, 0.5, 0))
plot(n6.axt,n6.moc$values,
     main = '(b) Ensemble 2009',
     ylab='AMOC (Sv)',xlab='',
     lwd=lwd,type='l',col='black',
     xaxt='n',
     xlim=xlim,ylim=ylim.moc,
     cex=.6,cex.main=.9,cex.axis=.7,cex.lab=0.7)
points(e9.axt,e9.moc.em,
     lwd=1,type='l',col='blue',lty=2)
myfill(e9.axt,
       e9.moc.em+2*sqrt(e9.moc.var),y_low=e9.moc.em-2*sqrt(e9.moc.var),
       col='blue',trans=0.3)
axis(side = 1, at = xtickpos,labels=yrlist,cex.axis=0.7)


# Ensemble variance
ylim=c(0,5)
xlim  = c(0,1500)
xtickpos = seq(from=1,to=5000,by=365)
xlabels  = seq(0,13,1)
par(new=T,fig = c(0, 1, 0.03, 0.33),mar=c(0.5,2.4,1,1), mgp=c(1.3, 0.5, 0))
plot(e7.axt0,e7.moc.var,
     main = '(c) Ensemble variance',
     ylab='Sv^2',xlab='',
     lwd=1,type='l',lty='dotted',col='red',
     xaxt='n',
     xlim=xlim,ylim=ylim,
     cex=.6,cex.main=.9,cex.axis=.7,cex.lab=0.7)
points(e9.axt0,e9.moc.var,
     lwd=1,type='l',col='blue',lty='dotted')
points(e7.axt0,e7.moc.var.smooth,
     lwd=lwd,type='l',col='red',lty=1)
points(e9.axt0,e9.moc.var.smooth,
     lwd=lwd,type='l',col='blue',lty=1)
axis(side = 1, at = xtickpos, labels = xlabels,cex.axis=0.7,xlab='Lead time (year)')
mtext('Lead time (year)',side=1,line=1.4,cex=0.8)
abline(h=e.moc.sat)
graphics.off()

# ===========================================================================
