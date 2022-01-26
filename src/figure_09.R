rm(list= ls())
library(ncdf4)
source('TOOLS/R/Rnoc_350.R')
source('TOOLS/R/listexp.R')
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
e7period = c(2007,2011)
e9period = c(2009,2012)
# ==========================================================================
n6   = lexp[['N006'       ]]
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
n6.geoz    = mynt( n6.f,   variable='GEOobs')
e7m1.geoz  = mynt( e7m1.f, variable='GEOobs')
e7m2.geoz  = mynt( e7m2.f, variable='GEOobs')
e7m3.geoz  = mynt( e7m3.f, variable='GEOobs')
e9m1.geoz  = mynt( e9m1.f, variable='GEOobs')
e9m2.geoz  = mynt( e9m2.f, variable='GEOobs')
e9m3.geoz  = mynt( e9m3.f, variable='GEOobs')
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
e9m1.com0z = select_period( e9m1.com0z, e9period)
e9m2.com0z = select_period( e9m2.com0z, e9period)
e9m3.com0z = select_period( e9m3.com0z, e9period)
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
n6.moc      = n6.mocz
e7m1.moc    = e7m1.mocz
e7m2.moc    = e7m2.mocz
e7m3.moc    = e7m3.mocz
e9m1.moc    = e9m1.mocz
e9m2.moc    = e9m2.mocz
e9m3.moc    = e9m3.mocz
#
n6.mocr     = n6.mocrz
e7m1.mocr   = e7m1.mocrz
e7m2.mocr   = e7m2.mocrz
e7m3.mocr   = e7m3.mocrz
e9m1.mocr   = e9m1.mocrz
e9m2.mocr   = e9m2.mocrz
e9m3.mocr   = e9m3.mocrz
#
n6.ekm      = n6.ekmz
e7m1.ekm    = e7m1.ekmz
e7m2.ekm    = e7m2.ekmz
e7m3.ekm    = e7m3.ekmz
e9m1.ekm    = e9m1.ekmz
e9m2.ekm    = e9m2.ekmz
e9m3.ekm    = e9m3.ekmz
#
n6.geo      = n6.geoz
e7m1.geo    = e7m1.geoz
e7m2.geo    = e7m2.geoz
e7m3.geo    = e7m3.geoz
e9m1.geo    = e9m1.geoz
e9m2.geo    = e9m2.geoz
e9m3.geo    = e9m3.geoz
#
n6.fst      = n6.fstz
e7m1.fst    = e7m1.fstz
e7m2.fst    = e7m2.fstz
e7m3.fst    = e7m3.fstz
e9m1.fst    = e9m1.fstz
e9m2.fst    = e9m2.fstz
e9m3.fst    = e9m3.fstz
#
n6.com0     = n6.com0z
e7m1.com0   = e7m1.com0z
e7m2.com0   = e7m2.com0z
e7m3.com0   = e7m3.com0z
e9m1.com0   = e9m1.com0z
e9m2.com0   = e9m2.com0z
e9m3.com0   = e9m3.com0z
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
n6.mocr$values   = n6.mocrz$values[   array(data=c(n6.iz,   seq(n6.Nt)),   dim=c(n6.Nt,2))  ]
e7m1.mocr$values = e7m1.mocrz$values[ array(data=c(e7m1.iz, seq(e7m1.Nt)), dim=c(e7m1.Nt,2))]
e7m2.mocr$values = e7m2.mocrz$values[ array(data=c(e7m2.iz, seq(e7m2.Nt)), dim=c(e7m2.Nt,2))]
e7m3.mocr$values = e7m3.mocrz$values[ array(data=c(e7m3.iz, seq(e7m3.Nt)), dim=c(e7m3.Nt,2))]
e9m1.mocr$values = e9m1.mocrz$values[ array(data=c(e9m1.iz, seq(e9m1.Nt)), dim=c(e9m1.Nt,2))]
e9m2.mocr$values = e9m2.mocrz$values[ array(data=c(e9m2.iz, seq(e9m2.Nt)), dim=c(e9m2.Nt,2))]
e9m3.mocr$values = e9m3.mocrz$values[ array(data=c(e9m3.iz, seq(e9m3.Nt)), dim=c(e9m3.Nt,2))]
#
n6.ekm$values    = n6.ekmz$values[    array(data=c(n6.iz,   seq(n6.Nt)),   dim=c(n6.Nt,2))  ]
e7m1.ekm$values  = e7m1.ekmz$values[  array(data=c(e7m1.iz, seq(e7m1.Nt)), dim=c(e7m1.Nt,2))]
e7m2.ekm$values  = e7m2.ekmz$values[  array(data=c(e7m2.iz, seq(e7m2.Nt)), dim=c(e7m2.Nt,2))]
e7m3.ekm$values  = e7m3.ekmz$values[  array(data=c(e7m3.iz, seq(e7m3.Nt)), dim=c(e7m3.Nt,2))]
e9m1.ekm$values  = e9m1.ekmz$values[  array(data=c(e9m1.iz, seq(e9m1.Nt)), dim=c(e9m1.Nt,2))]
e9m2.ekm$values  = e9m2.ekmz$values[  array(data=c(e9m2.iz, seq(e9m2.Nt)), dim=c(e9m2.Nt,2))]
e9m3.ekm$values  = e9m3.ekmz$values[  array(data=c(e9m3.iz, seq(e9m3.Nt)), dim=c(e9m3.Nt,2))]
#
n6.geo$values    = n6.geoz$values[    array(data=c(n6.iz,   seq(n6.Nt)),   dim=c(n6.Nt,2))  ]
e7m1.geo$values  = e7m1.geoz$values[  array(data=c(e7m1.iz, seq(e7m1.Nt)), dim=c(e7m1.Nt,2))]
e7m2.geo$values  = e7m2.geoz$values[  array(data=c(e7m2.iz, seq(e7m2.Nt)), dim=c(e7m2.Nt,2))]
e7m3.geo$values  = e7m3.geoz$values[  array(data=c(e7m3.iz, seq(e7m3.Nt)), dim=c(e7m3.Nt,2))]
e9m1.geo$values  = e9m1.geoz$values[  array(data=c(e9m1.iz, seq(e9m1.Nt)), dim=c(e9m1.Nt,2))]
e9m2.geo$values  = e9m2.geoz$values[  array(data=c(e9m2.iz, seq(e9m2.Nt)), dim=c(e9m2.Nt,2))]
e9m3.geo$values  = e9m3.geoz$values[  array(data=c(e9m3.iz, seq(e9m3.Nt)), dim=c(e9m3.Nt,2))]
#
n6.fst$values   = n6.fstz$values[   1, ]
e7m1.fst$values = e7m1.fstz$values[ 1, ]
e7m2.fst$values = e7m2.fstz$values[ 1, ]
e7m3.fst$values = e7m3.fstz$values[ 1, ]
e9m1.fst$values = e9m1.fstz$values[ 1, ]
e9m2.fst$values = e9m2.fstz$valuse[ 1, ]
e9m3.fst$values = e9m3.fstz$values[ 1, ]
#
n6.com0$values   = n6.com0z$values[ 1,]   - n6.com0z$values[   array(data=c(n6.iz,   seq(n6.Nt)),   dim=c(n6.Nt,2))  ]
e7m1.com0$values = e7m1.com0z$values[ 1,] - e7m1.com0z$values[ array(data=c(e7m1.iz, seq(e7m1.Nt)), dim=c(e7m1.Nt,2))]
e7m2.com0$values = e7m2.com0z$values[ 1,] - e7m2.com0z$values[ array(data=c(e7m2.iz, seq(e7m2.Nt)), dim=c(e7m2.Nt,2))]
e7m3.com0$values = e7m3.com0z$values[ 1,] - e7m3.com0z$values[ array(data=c(e7m3.iz, seq(e7m3.Nt)), dim=c(e7m3.Nt,2))]
e9m1.com0$values = e9m1.com0z$values[ 1,] - e9m1.com0z$values[ array(data=c(e9m1.iz, seq(e9m1.Nt)), dim=c(e9m1.Nt,2))]
e9m2.com0$values = e9m2.com0z$values[ 1,] - e9m2.com0z$values[ array(data=c(e9m2.iz, seq(e9m2.Nt)), dim=c(e9m2.Nt,2))]
e9m3.com0$values = e9m3.com0z$values[ 1,] - e9m3.com0z$values[ array(data=c(e9m3.iz, seq(e9m3.Nt)), dim=c(e9m3.Nt,2))]
#
n6.moc$values   = getts( n6.mocz,   variable='moc')$values
e7m1.moc$values = getts( e7m1.mocz, variable='moc')$values
e7m2.moc$values = getts( e7m2.mocz, variable='moc')$values
e7m3.moc$values = getts( e7m3.mocz, variable='moc')$values
e9m1.moc$values = getts( e9m1.mocz, variable='moc')$values
e9m2.moc$values = getts( e9m2.mocz, variable='moc')$values
e9m3.moc$values = getts( e9m3.mocz, variable='moc')$values
#
n6.geo$values   = n6.geo$values   - n6.com0$values
e7m1.geo$values = e7m1.geo$values - e7m1.com0$values
e7m2.geo$values = e7m2.geo$values - e7m2.com0$values
e7m3.geo$values = e7m3.geo$values - e7m3.com0$values
e9m1.geo$values = e9m1.geo$values - e9m1.com0$values
e9m2.geo$values = e9m2.geo$values - e9m2.com0$values
e9m3.geo$values = e9m3.geo$values - e9m3.com0$values
#
#
# Monthly values
# ==============
thalf=3
n6.moc.mo.smooth  = myrunmean( n6.moc$values,  thalf)

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
e7.moc   = array( c(e7m1.moc$values, e7m2.moc$values, e7m3.moc$values,
    select_period(n6.moc,e7period)$values),
    dim=c(e7m1.Nt,4))
e7.mocr  = array( c(e7m1.mocr$values, e7m2.mocr$values, e7m3.mocr$values,
    select_period(n6.mocr,e7period)$values),
    dim=c(e7m1.Nt,4))
e7.ekm   = array( c(e7m1.ekm$values, e7m2.ekm$values, e7m3.ekm$values,
    select_period(n6.ekm,e7period)$values),
    dim=c(e7m1.Nt,4))
e7.geo   = array( c(e7m1.geo$values, e7m2.geo$values, e7m3.geo$values,
    select_period(n6.geo,e7period)$values),
    dim=c(e7m1.Nt,4))
e7.fst   = array( c(e7m1.fst$values, e7m2.fst$values, e7m3.fst$values,
    select_period(n6.fst,e7period)$values),
    dim=c(e7m1.Nt,4))
#
e9.moc   = array( c(e9m1.moc$values, e9m2.moc$values, e9m3.moc$values,
    select_period(n6.moc,e9period)$values),
    dim=c(e9m1.Nt,4))
e9.mocr  = array( c(e9m1.mocr$values, e9m2.mocr$values, e9m3.mocr$values,
    select_period(n6.mocr,e9period)$values),
    dim=c(e9m1.Nt,4))
e9.ekm   = array( c(e9m1.ekm$values, e9m2.ekm$values, e9m3.ekm$values,
    select_period(n6.ekm,e9period)$values),
    dim=c(e9m1.Nt,4))
e9.geo   = array( c(e9m1.geo$values, e9m2.geo$values, e9m3.geo$values,
    select_period(n6.geo,e9period)$values),
    dim=c(e9m1.Nt,4))
e9.fst   = array( c(e9m1.fst$values, e9m2.fst$values, e9m3.fst$values,
    select_period(n6.fst,e9period)$values),
    dim=c(e9m1.Nt,4))
#
#
#
# Ensemble SPREAD
# ===============
#
# 5-day means
# -----------
e7.moc.em  = apply( e7.moc,  1, mean, na.rm=T)
e7.mocr.em = apply( e7.mocr, 1, mean, na.rm=T)
e7.ekm.em  = apply( e7.ekm,  1, mean, na.rm=T)
e7.geo.em  = apply( e7.geo,  1, mean, na.rm=T)
e7.fst.em  = apply( e7.fst,  1, mean, na.rm=T)
e7.moc.sd  = apply( e7.moc,  1, sd,   na.rm=T)
e7.mocr.sd = apply( e7.mocr, 1, sd,   na.rm=T)
e7.ekm.sd  = apply( e7.ekm,  1, sd,   na.rm=T)
e7.geo.sd  = apply( e7.geo,  1, sd,   na.rm=T)
e7.fst.sd  = apply( e7.fst,  1, sd,   na.rm=T)
#
e9.moc.em  = apply( e9.moc,  1, mean, na.rm=T)
e9.mocr.em = apply( e9.mocr, 1, mean, na.rm=T)
e9.ekm.em  = apply( e9.ekm,  1, mean, na.rm=T)
e9.geo.em  = apply( e9.geo,  1, mean, na.rm=T)
e9.fst.em  = apply( e9.fst,  1, mean, na.rm=T)
e9.moc.sd  = apply( e9.moc,  1, sd,   na.rm=T)
e9.mocr.sd = apply( e9.mocr, 1, sd,   na.rm=T)
e9.ekm.sd  = apply( e9.ekm,  1, sd,   na.rm=T)
e9.geo.sd  = apply( e9.geo,  1, sd,   na.rm=T)
e9.fst.sd  = apply( e9.fst,  1, sd,   na.rm=T)
#
# lissage :
smooth = T
if (smooth) {
  # thalf = 3    # monthly
  thalf = 9    # seasonal
  # thalf = 36 # annual
  e7.moc.sd  = myrunmean( e7.moc.sd,  thalf)
  e7.mocr.sd = myrunmean( e7.mocr.sd, thalf)
  e7.ekm.sd  = myrunmean( e7.ekm.sd,  thalf)
  e7.geo.sd  = myrunmean( e7.geo.sd,  thalf)
  e7.fst.sd  = myrunmean( e7.fst.sd,  thalf)
  e9.moc.sd  = myrunmean( e9.moc.sd,  thalf)
  e9.mocr.sd = myrunmean( e9.mocr.sd, thalf)
  e9.ekm.sd  = myrunmean( e9.ekm.sd,  thalf)
  e9.geo.sd  = myrunmean( e9.geo.sd,  thalf)
  e9.fst.sd  = myrunmean( e9.fst.sd,  thalf)
}
#
# Table 2
# =======
# saturation value
# ================
tmin = 2*365+1
tmax = 4*365
e7.index = which( e7.axt0 >= tmin   & e7.axt0 < tmax)
e9.index = which( e9.axt0 >= tmin-1 & e9.axt0 < tmax)
#
e.moc.sat  = mean(c( e7.moc.sd[  e7.index], e9.moc.sd[  e9.index]))
e.mocr.sat = mean(c( e7.mocr.sd[ e7.index], e9.mocr.sd[ e9.index]))
e.ekm.sat  = mean(c( e7.ekm.sd[  e7.index], e9.ekm.sd[  e9.index]))
e.geo.sat  = mean(c( e7.geo.sd[  e7.index], e9.geo.sd[  e9.index]))
e.fst.sat  = mean(c( e7.fst.sd[  e7.index], e9.fst.sd[  e9.index]))
#
#
# in percentage
e.moc.varexp       = (e.moc.sat       / sd( n6.moc$values)      )^2
e.mocr.varexp      = (e.mocr.sat      / sd( n6.mocr$values)     )^2
e.ekm.varexp       = (e.ekm.sat       / sd( n6.ekm$values)      )^2
e.geo.varexp       = (e.geo.sat       / sd( n6.geo$values)      )^2
e.fst.varexp       = (e.fst.sat       / sd( n6.fst$values)      )^2
#
#
# Fisher test
# ===========
nfensemble = 3
# nombre de valeurs utilisées pour calculer la valeur moyenne de saturation
nfsatvalue = length(c(e7.fst.sd[e7.index], e9.fst.sd[e9.index]))
# nombre de valeurs utilisées pour calculer la running mean .seas
nfseasvalue = 9*2+1

## nf.n6.fst  = nf(n6.fst$values )
## nf.n6.geo  = nf(n6.geo$values )
## nf.n6.moc  = nf(n6.moc$values )
## nf.n6.mocr = nf(n6.mocr$values)
## #
## signif.fst  = qf( 0.95, nf.n6.fst,  nfensemble)
## signif.geo  = qf( 0.95, nf.n6.geo,  nfensemble)
## signif.moc  = qf( 0.95, nf.n6.moc,  nfensemble)
## signif.mocr = qf( 0.95, nf.n6.mocr, nfensemble)
signif.3b.satmin   = qf( 0.95, nfensemble*nfseasvalue, nfensemble*nfsatvalue )
signif.3b.satmax   = qf( 0.95, nfensemble*nfsatvalue,  nfensemble*nfseasvalue)
#
ratio.max.moc  = pmax(e7.moc.sd/e.moc.sat,   e.moc.sat/e7.moc.sd  )
ratio.max.mocr = pmax(e7.mocr.sd/e.mocr.sat, e.mocr.sat/e7.mocr.sd)
ratio.max.geo  = pmax(e7.geo.sd/e.geo.sat,   e.geo.sat/e7.geo.sd  )
ratio.max.fst  = pmax(e7.fst.sd/e.fst.sat,   e.fst.sat/e7.fst.sd  )
index.satmin.moc  = (e7.moc.sd/e.moc.sat   == ratio.max.moc )
index.satmin.mocr = (e7.mocr.sd/e.mocr.sat == ratio.max.mocr)
index.satmin.geo  = (e7.geo.sd/e.geo.sat   == ratio.max.geo )
index.satmin.fst  = (e7.fst.sd/e.fst.sat   == ratio.max.fst )
index.satmax.moc  = (e.moc.sat/e7.moc.sd   == ratio.max.moc )
index.satmax.mocr = (e.mocr.sat/e7.mocr.sd == ratio.max.mocr)
index.satmax.geo  = (e.geo.sat/e7.geo.sd   == ratio.max.geo )
index.satmax.fst  = (e.fst.sat/e7.fst.sd   == ratio.max.fst )
signif.3b.moc  = array( dim= dim(ratio.max.moc ))
signif.3b.mocr = array( dim= dim(ratio.max.mocr))
signif.3b.geo  = array( dim= dim(ratio.max.geo ))
signif.3b.fst  = array( dim= dim(ratio.max.fst ))
signif.3b.moc[ index.satmin.moc ] = signif.3b.satmin
signif.3b.mocr[index.satmin.mocr] = signif.3b.satmin
signif.3b.geo[ index.satmin.geo ] = signif.3b.satmin
signif.3b.fst[ index.satmin.fst ] = signif.3b.satmin
signif.3b.moc[ index.satmax.moc ] = signif.3b.satmax
signif.3b.mocr[index.satmax.mocr] = signif.3b.satmax
signif.3b.geo[ index.satmax.geo ] = signif.3b.satmax
signif.3b.fst[ index.satmax.fst ] = signif.3b.satmax
test.3b.moc  = (ratio.max.moc  > signif.3b.moc )
test.3b.mocr = (ratio.max.mocr > signif.3b.mocr)
test.3b.geo  = (ratio.max.geo  > signif.3b.geo )
test.3b.fst  = (ratio.max.fst  > signif.3b.fst )
# ===========================================================================
# PLOT
# ===========================================================================
# indice pour le gray shading

timeextreme = n6.axt[n6.moc.mo.smooth<(mean(n6.moc$values))]
x1 = as.PCICt("2009-09-10",cal="gregorian")
x2 = as.PCICt("2010-06-02",cal="gregorian")
x3 = as.PCICt("2010-10-25",cal="gregorian")
x4 = as.PCICt("2011-01-23",cal="gregorian")
# ===========================================================================
# Spread vs saturation
# =========================
lwd = 1.2
xlim  = c(as.PCICt("2007-01-01",cal="gregorian"),as.PCICt("2012-01-01",cal="gregorian"))
xtickpos = c(as.PCICt("2006-01-01",cal="gregorian"),as.PCICt("2007-01-01",cal="gregorian"),as.PCICt("2008-01-01",cal="gregorian"),as.PCICt("2009-01-01",cal="gregorian"),as.PCICt("2010-01-01",cal="gregorian"),as.PCICt("2011-01-01",cal="gregorian"),as.PCICt("2012-01-01",cal="gregorian"))#,as.PCICt("2011-01-01",cal="gregorian"),as.PCICt("2012-01-01",cal="gregorian"),as.PCICt("2013-01-01",cal="gregorian"))
yrlist=c('2006','2007','2008','2009','2010','2011','2012')#,'2011','2012','2013')
#
# Figure 03
fileout = "../figures/figure_09.pdf"
pdf(fileout,width=6,height=4)
#
par(fig = c(0, 1, 0.5, 1),mar=c(2,2.4,1,1.6), mgp=c(1.5, 0.5, 0))
plot(n6.axt,n6.moc$values,
     main = '(a) Full AMOC',
     ylab='Sv',xlab='',
     lwd=lwd,type='l',col='red',
     xaxt='n',
     xlim=xlim,ylim=c(0,30),
     cex=.8,cex.main=.8,cex.axis=.8,cex.lab=0.8)
points(n6.axt,n6.moc.mo.smooth,
     lwd=1,type='l',col='black',lty=1)
abline(h=mean(n6.moc$values))
abline(h=mean(n6.moc$values)+sd(n6.moc$values),lty=2)
abline(h=mean(n6.moc$values)-sd(n6.moc$values),lty=2)
rect(x1,-100,x2,100,
     col='#00000020',density=-0.9,border=NA)
rect(x3,-100,x4,100,
     col='#00000020',density=-0.9,border=NA)
axis(side = 1, at = xtickpos, labels = yrlist,cex.axis=0.8)
#
## par(new=T,fig = c(0, 1, 0.33, 0.66),mar=c(2,2.4,1,1.6), mgp=c(1.5, 0.5, 0))
## plot(e7.axt,e7.moc.sd/e.moc.sat,
##      main = '(b) E2007 ensemble spread',
##      ylab='Sv',xlab='',
##      lwd=1,type='l',col='red',
##      xaxt='n',
##      xlim=xlim,ylim=c(0,2),
##      cex=.6,cex.main=.7,cex.axis=.7,cex.lab=0.7)
## points(e7.axt,e7.mocr.sd/e.mocr.sat,
##      lwd=1,type='l',col='red',lty=2)
## points(e7.axt,e7.fst.sd/e.fst.sat,
##      lwd=1,type='l',col='blue',lty=1)
## points(e7.axt,e7.geo.sd/e.geo.sat,
##      lwd=1,type='l',col='deeppink',lty=1)
## abline(h=1)
## rect(x1,-100,x2,100,
##      col='#00000020',density=-0.9,border=NA)
## rect(x3,-100,x4,100,
##      col='#00000020',density=-0.9,border=NA)
## axis(side = 1, at = xtickpos, labels = yrlist,cex.axis=0.7)

#
par(new=T,fig = c(0, 1, 0, 0.5),mar=c(2,2.4,1,1.6), mgp=c(1.5, 0.5, 0))
plot(e7.axt,e7.moc.sd/e.moc.sat,
     main = '(b) E2007 ensemble spread',
     ylab='',xlab='',
     lwd=1,type='l',col='black',
     xaxt='n',
     xlim=xlim,ylim=c(0,2.3),
     cex=.8,cex.main=.8,cex.axis=.8,cex.lab=0.8)
points(e7.axt,e7.mocr.sd/e.mocr.sat,
     lwd=lwd,type='l',col='black',lty=2)
points(e7.axt,e7.fst.sd/e.fst.sat,
     lwd=lwd,type='l',col='blue',lty=1)
points(e7.axt,e7.geo.sd/e.geo.sat,
     lwd=lwd,type='l',col='deeppink',lty=1)
#
points(e9.axt,e9.moc.sd/e.moc.sat,
     lwd=0.8,type='l',col='darkgray',lty=1)
points(e9.axt,e9.fst.sd/e.fst.sat,
     lwd=0.8,type='l',col='cornflowerblue',lty=1)
points(e9.axt,e9.geo.sd/e.geo.sat,
     lwd=0.8,type='l',col='pink',lty=1)
#
abline(h=1)
rect(x1,-100,x2,100,
     col='#00000020',density=-0.9,border=NA)
rect(x3,-100,x4,100,
     col='#00000020',density=-0.9,border=NA)
#
points(e7.axt[test.3b.moc],(e7.moc.sd/e.moc.sat)[test.3b.moc],
       type='p',pch=20,col='black',cex=0.8)
#points(e7.axt[test.3b.mocr],(e7.mocr.sd.seas/e.mocr.sat)[test.3b.mocr],
#       type='p',pch=20,col='red',cex=0.8)
points(e7.axt[test.3b.fst],(e7.fst.sd/e.fst.sat)[test.3b.fst],
       type='p',pch=20,col='blue',cex=0.8)
points(e7.axt[test.3b.geo],(e7.geo.sd/e.geo.sat)[test.3b.geo],
       type='p',pch=20,col='deeppink',cex=0.8)
axis(side = 1, at = xtickpos, labels = yrlist,cex.axis=0.8)

points(e9.axt[test.3b.moc],(e9.moc.sd/e.moc.sat)[test.3b.moc],
       type='p',pch=18,col='darkgray',cex=0.5)
#points(e9.axt[test.3b.mocr],(e9.mocr.sd.seas/e.mocr.sat)[test.3b.mocr],
#       type='p',pch=18,col='red',cex=0.5)
points(e9.axt[test.3b.fst],(e9.fst.sd/e.fst.sat)[test.3b.fst],
       type='p',pch=18,col='cornflowerblue',cex=0.5)
points(e9.axt[test.3b.geo],(e9.geo.sd/e.geo.sat)[test.3b.geo],
       type='p',pch=18,col='pink',cex=0.5)
axis(side = 1, at = xtickpos, labels = yrlist,cex.axis=0.8)


graphics.off()
                                        #
