rm(list= ls())
graphics.off()
# ==========================================================================
library(ncdf4)
source('TOOLS/R/Rnoc_350.R')
source('TOOLS/R/listexp.R')
# ==========================================================================
refperiod=c(2004,2008)
valperiod=c(2004,2012)
# ==========================================================================
# OBS
# ===
fobs = '../data/moc_transports.nc'
# NEMO
# ====
#diagid='valormoc'
diagid='valmocGEOtot'
freq='d05'
n6   = lexp[['N006']]
e7m1 = lexp[['N12_2007_01']]
e7m2 = lexp[['N12_2007_02']]
e7m3 = lexp[['N12_2007_03']]
e9m1 = lexp[['N12_2009_01']]
e9m2 = lexp[['N12_2009_02']]
e9m3 = lexp[['N12_2009_03']]
#
n6.fname   = sprintf('%s/%s', n6$cdfdir,   diagfname( n6,   diagid, freq))
e7m1.fname = sprintf('%s/%s', e7m1$cdfdir, diagfname( e7m1, diagid, freq))
e7m2.fname = sprintf('%s/%s', e7m2$cdfdir, diagfname( e7m2, diagid, freq))
e7m3.fname = sprintf('%s/%s', e7m3$cdfdir, diagfname( e7m3, diagid, freq))
e9m1.fname = sprintf('%s/%s', e9m1$cdfdir, diagfname( e9m1, diagid, freq))
e9m2.fname = sprintf('%s/%s', e9m2$cdfdir, diagfname( e9m2, diagid, freq))
e9m3.fname = sprintf('%s/%s', e9m3$cdfdir, diagfname( e9m3, diagid, freq))
#
# Read data OBS
# =============
obs.fst = mynt( fobs, variable = 't_gs10'      )
obs.ekm = mynt( fobs, variable = 't_ek10'      )
obs.umo = mynt( fobs, variable = 't_umo10'     )
obs.moc = mynt( fobs, variable = 'moc_mar_hc10')
#
# Time issu (lag of one day due to wrong definition of unit in netcdf file)
obs.fst$time = obs.fst$time - 86400
obs.ekm$time = obs.ekm$time - 86400
obs.umo$time = obs.umo$time - 86400
obs.moc$time = obs.moc$time - 86400
#
# select common period with simulation
options(warn=-1)
obs.fst = select_period( obs.fst, period = valperiod)
obs.ekm = select_period( obs.ekm, period = valperiod)
obs.umo = select_period( obs.umo, period = valperiod)
obs.moc = select_period( obs.moc, period = valperiod)
options(warn=0)
#
obs.axt = to.date(obs.fst$time,obs.fst$timeu,cal=obs.fst$timec)
#
# read data NEMO
# ==============
n6.fstz    = mynt( n6.fname,   variable='FST'   )
e7m1.fstz  = mynt( e7m1.fname, variable='FST'   )
e7m2.fstz  = mynt( e7m2.fname, variable='FST'   )
e7m3.fstz  = mynt( e7m3.fname, variable='FST'   )
e9m1.fstz  = mynt( e9m1.fname, variable='FST'   )
e9m2.fstz  = mynt( e9m2.fname, variable='FST'   )
e9m3.fstz  = mynt( e9m3.fname, variable='FST'   )
#
n6.ekmz    = mynt( n6.fname,   variable='EKM'   )
e7m1.ekmz  = mynt( e7m1.fname, variable='EKM'   )
e7m2.ekmz  = mynt( e7m2.fname, variable='EKM'   )
e7m3.ekmz  = mynt( e7m3.fname, variable='EKM'   )
e9m1.ekmz  = mynt( e9m1.fname, variable='EKM'   )
e9m2.ekmz  = mynt( e9m2.fname, variable='EKM'   )
e9m3.ekmz  = mynt( e9m3.fname, variable='EKM'   )
#
n6.com0z   = mynt( n6.fname,   variable='COM0'  )
e7m1.com0z = mynt( e7m1.fname, variable='COM0'  )
e7m2.com0z = mynt( e7m2.fname, variable='COM0'  )
e7m3.com0z = mynt( e7m3.fname, variable='COM0'  )
e9m1.com0z = mynt( e9m1.fname, variable='COM0'  )
e9m2.com0z = mynt( e9m2.fname, variable='COM0'  )
e9m3.com0z = mynt( e9m3.fname, variable='COM0'  )
#
n6.mocrz   = mynt( n6.fname,   variable='MOCobs')
e7m1.mocrz = mynt( e7m1.fname, variable='MOCobs')
e7m2.mocrz = mynt( e7m2.fname, variable='MOCobs')
e7m3.mocrz = mynt( e7m3.fname, variable='MOCobs')
e9m1.mocrz = mynt( e9m1.fname, variable='MOCobs')
e9m2.mocrz = mynt( e9m2.fname, variable='MOCobs')
e9m3.mocrz = mynt( e9m3.fname, variable='MOCobs')
#
n6.umoz    = mynt( n6.fname,   variable='GEOobs')
e7m1.umoz  = mynt( e7m1.fname, variable='GEOobs')
e7m2.umoz  = mynt( e7m2.fname, variable='GEOobs')
e7m3.umoz  = mynt( e7m3.fname, variable='GEOobs')
e9m1.umoz  = mynt( e9m1.fname, variable='GEOobs')
e9m2.umoz  = mynt( e9m2.fname, variable='GEOobs')
e9m3.umoz  = mynt( e9m3.fname, variable='GEOobs')
#

# Time axis
n6.fstz$timec  = 'gregorian'
n6.ekmz$timec  = 'gregorian'
n6.umoz$timec  = 'gregorian'
n6.mocrz$timec = 'gregorian'
n6.com0z$timec = 'gregorian'
n6.Nt   = length( n6.mocrz$time )
e7m1.Nt = length( e7m1.mocrz$time)
e7m2.Nt = length( e7m2.mocrz$time)
e7m3.Nt = length( e7m3.mocrz$time)
e9m1.Nt = length( e9m1.mocrz$time)
e9m2.Nt = length( e9m2.mocrz$time)
e9m3.Nt = length( e9m3.mocrz$time)
#
#
# Time series
# -----------
# init :
n6.fst   = n6.fstz
e7m1.fst = e7m1.fstz
e7m2.fst = e7m2.fstz
e7m3.fst = e7m3.fstz
e9m1.fst = e9m1.fstz
e9m2.fst = e9m2.fstz
e9m3.fst = e9m3.fstz
#
n6.com0   = n6.com0z
e7m1.com0 = e7m1.com0z
e7m2.com0 = e7m2.com0z
e7m3.com0 = e7m3.com0z
e9m1.com0 = e9m1.com0z
e9m2.com0 = e9m2.com0z
e9m3.com0 = e9m3.com0z
#
n6.ekm   = n6.ekmz
e7m1.ekm = e7m1.ekmz
e7m2.ekm = e7m2.ekmz
e7m3.ekm = e7m3.ekmz
e9m1.ekm = e9m1.ekmz
e9m2.ekm = e9m2.ekmz
e9m3.ekm = e9m3.ekmz
#
n6.umo   = n6.umoz
e7m1.umo = e7m1.umoz
e7m2.umo = e7m2.umoz
e7m3.umo = e7m3.umoz
e9m1.umo = e9m1.umoz
e9m2.umo = e9m2.umoz
e9m3.umo = e9m3.umoz
#
n6.mocr   = n6.mocrz
e7m1.mocr = e7m1.mocrz
e7m2.mocr = e7m2.mocrz
e7m3.mocr = e7m3.mocrz
e9m1.mocr = e9m1.mocrz
e9m2.mocr = e9m2.mocrz
e9m3.mocr = e9m3.mocrz
#
n6.iz   = getts( n6.mocrz,   variable='moc', index=T)$values
e7m1.iz = getts( e7m1.mocrz, variable='moc', index=T)$values
e7m2.iz = getts( e7m2.mocrz, variable='moc', index=T)$values
e7m3.iz = getts( e7m3.mocrz, variable='moc', index=T)$values
e9m1.iz = getts( e9m1.mocrz, variable='moc', index=T)$values
e9m2.iz = getts( e9m2.mocrz, variable='moc', index=T)$values
e9m3.iz = getts( e9m3.mocrz, variable='moc', index=T)$values
#
n6.mocr$values   = n6.mocrz$values[   array(data=c(n6.iz,   seq(n6.Nt)),  dim=c(n6.Nt,2))]
e7m1.mocr$values = e7m1.mocrz$values[ array(data=c(e7m1.iz, seq(e7m1.Nt)),dim=c(e7m1.Nt,2))]
e7m2.mocr$values = e7m2.mocrz$values[ array(data=c(e7m2.iz, seq(e7m2.Nt)),dim=c(e7m2.Nt,2))]
e7m3.mocr$values = e7m3.mocrz$values[ array(data=c(e7m3.iz, seq(e7m3.Nt)),dim=c(e7m3.Nt,2))]
e9m1.mocr$values = e9m1.mocrz$values[ array(data=c(e9m1.iz, seq(e9m1.Nt)),dim=c(e9m1.Nt,2))]
e9m2.mocr$values = e9m2.mocrz$values[ array(data=c(e9m2.iz, seq(e9m2.Nt)),dim=c(e9m2.Nt,2))]
e9m3.mocr$values = e9m3.mocrz$values[ array(data=c(e9m3.iz, seq(e9m3.Nt)),dim=c(e9m3.Nt,2))]
#
n6.fst$values   = n6.fstz$values[   1, ]
e7m1.fst$values = e7m1.fstz$values[ 1, ]
e7m2.fst$values = e7m2.fstz$values[ 1, ]
e7m3.fst$values = e7m3.fstz$values[ 1, ]
e9m1.fst$values = e9m1.fstz$values[ 1, ]
e9m2.fst$values = e9m2.fstz$valuse[ 1, ]
e9m3.fst$values = e9m3.fstz$values[ 1, ]
#
n6.com0$values    = n6.com0z$values[ 1,] - n6.com0z$values[ array(data=c(n6.iz,   seq(n6.Nt)),   dim=c(n6.Nt,2))  ]
e7m1.com0$values  = e7m1.com0z$values[ 1,] - e7m1.com0z$values[ array(data=c(e7m1.iz,   seq(e7m1.Nt)),   dim=c(e7m1.Nt,2))  ]
e7m2.com0$values  = e7m2.com0z$values[ 1,] - e7m2.com0z$values[ array(data=c(e7m2.iz,   seq(e7m2.Nt)),   dim=c(e7m2.Nt,2))  ]
e7m3.com0$values  = e7m3.com0z$values[ 1,] - e7m3.com0z$values[ array(data=c(e7m3.iz,   seq(e7m3.Nt)),   dim=c(e7m3.Nt,2))  ]
e9m1.com0$values  = e9m1.com0z$values[ 1,] - e9m1.com0z$values[ array(data=c(e9m1.iz,   seq(e9m1.Nt)),   dim=c(e9m1.Nt,2))  ]
e9m2.com0$values  = e9m2.com0z$values[ 1,] - e9m2.com0z$values[ array(data=c(e9m2.iz,   seq(e9m2.Nt)),   dim=c(e9m2.Nt,2))  ]
e9m3.com0$values  = e9m3.com0z$values[ 1,] - e9m3.com0z$values[ array(data=c(e9m3.iz,   seq(e9m3.Nt)),   dim=c(e9m3.Nt,2))  ]

#
n6.ekm$values   = n6.ekmz$values[  array(data=c(n6.iz,   seq(n6.Nt)),   dim=c(n6.Nt,2))  ]
e7m1.ekm$values = e7m1.ekmz$values[array(data=c(e7m1.iz, seq(e7m1.Nt)), dim=c(e7m1.Nt,2))]
e7m2.ekm$values = e7m2.ekmz$values[array(data=c(e7m2.iz, seq(e7m2.Nt)), dim=c(e7m2.Nt,2))]
e7m3.ekm$values = e7m3.ekmz$values[array(data=c(e7m3.iz, seq(e7m3.Nt)), dim=c(e7m3.Nt,2))]
e9m1.ekm$values = e9m1.ekmz$values[array(data=c(e9m1.iz, seq(e9m1.Nt)), dim=c(e9m1.Nt,2))]
e9m2.ekm$values = e9m2.ekmz$values[array(data=c(e9m2.iz, seq(e9m2.Nt)), dim=c(e9m2.Nt,2))]
e9m3.ekm$values = e9m3.ekmz$values[array(data=c(e9m3.iz, seq(e9m3.Nt)), dim=c(e9m3.Nt,2))]
#
n6.umo$values   = n6.umoz$values[  array(data=c(n6.iz,   seq(n6.Nt)),   dim=c(n6.Nt,2))  ]
e7m1.umo$values = e7m1.umoz$values[array(data=c(e7m1.iz, seq(e7m1.Nt)), dim=c(e7m1.Nt,2))]
e7m2.umo$values = e7m2.umoz$values[array(data=c(e7m2.iz, seq(e7m2.Nt)), dim=c(e7m2.Nt,2))]
e7m3.umo$values = e7m3.umoz$values[array(data=c(e7m3.iz, seq(e7m3.Nt)), dim=c(e7m3.Nt,2))]
e9m1.umo$values = e9m1.umoz$values[array(data=c(e9m1.iz, seq(e9m1.Nt)), dim=c(e9m1.Nt,2))]
e9m2.umo$values = e9m2.umoz$values[array(data=c(e9m2.iz, seq(e9m2.Nt)), dim=c(e9m2.Nt,2))]
e9m3.umo$values = e9m3.umoz$values[array(data=c(e9m3.iz, seq(e9m3.Nt)), dim=c(e9m3.Nt,2))]
#
n6.umo$values   = n6.umo$values   - n6.com0$values
e7m1.umo$values = e7m1.umo$values - e7m1.com0$values
e7m2.umo$values = e7m2.umo$values - e7m2.com0$values
e7m3.umo$values = e7m3.umo$values - e7m3.com0$values
e9m1.umo$values = e9m1.umo$values - e9m1.com0$values
e9m2.umo$values = e9m2.umo$values - e9m2.com0$values
e9m3.umo$values = e9m3.umo$values - e9m3.com0$values



# ==========================================================================
# monthly smooth
# ==============
if (FALSE) {
  print("monthly smoothing switch on")
  thalf=3 
  n6.fst$values   = myrunmean( n6.fst$values,   thalf)
  e7m1.fst$values = myrunmean( e7m1.fst$values, thalf)
  e7m2.fst$values = myrunmean( e7m2.fst$values, thalf)
  e7m3.fst$values = myrunmean( e7m3.fst$values, thalf)
  e9m1.fst$values = myrunmean( e9m1.fst$values, thalf)
  e9m2.fst$values = myrunmean( e9m2.fst$values, thalf)
  e9m3.fst$values = myrunmean( e9m3.fst$values, thalf)
  #
  n6.ekm$values   = myrunmean( n6.ekm$values,   thalf)
  e7m1.ekm$values = myrunmean( e7m1.ekm$values, thalf)
  e7m2.ekm$values = myrunmean( e7m2.ekm$values, thalf)
  e7m3.ekm$values = myrunmean( e7m3.ekm$values, thalf)
  e9m1.ekm$values = myrunmean( e9m1.ekm$values, thalf)
  e9m2.ekm$values = myrunmean( e9m2.ekm$values, thalf)
  e9m3.ekm$values = myrunmean( e9m3.ekm$values, thalf)
  #
  n6.umo$values   = myrunmean( n6.umo$values,   thalf)
  e7m1.umo$values = myrunmean( e7m1.umo$values, thalf)
  e7m2.umo$values = myrunmean( e7m2.umo$values, thalf)
  e7m3.umo$values = myrunmean( e7m3.umo$values, thalf)
  e9m1.umo$values = myrunmean( e9m1.umo$values, thalf)
  e9m2.umo$values = myrunmean( e9m2.umo$values, thalf)
  e9m3.umo$values = myrunmean( e9m3.umo$values, thalf)
  #
  n6.mocr$values   = myrunmean( n6.mocr$values,   thalf)
  e7m1.mocr$values = myrunmean( e7m1.mocr$values, thalf)
  e7m2.mocr$values = myrunmean( e7m2.mocr$values, thalf)
  e7m3.mocr$values = myrunmean( e7m3.mocr$values, thalf)
  e9m1.mocr$values = myrunmean( e9m1.mocr$values, thalf)
  e9m2.mocr$values = myrunmean( e9m2.mocr$values, thalf)
  e9m3.mocr$values = myrunmean( e9m3.mocr$values, thalf)
}
# ===========================================================================
# select_period : valor period
# ----------------------------
n6.fst  = select_period( n6.fst,  period = valperiod)
n6.ekm  = select_period( n6.ekm,  period = valperiod)
n6.umo  = select_period( n6.umo,  period = valperiod)
n6.mocr = select_period( n6.mocr, period = valperiod)

# suppression de janvier-mars 2004
tmp = select_time(n6.fst,season='JFM',period=c(2004,2004))
jfm.len = length(tmp$values)
i0 = jfm.len+1

n6.fst$values  = n6.fst$values[  i0:length(n6.fst$values) ]
n6.fst$time    = n6.fst$time[    i0:length(n6.fst$time)   ]
n6.ekm$values  = n6.ekm$values[  i0:length(n6.ekm$values) ]
n6.ekm$time    = n6.ekm$time[    i0:length(n6.ekm$time)   ]
n6.umo$values  = n6.umo$values[  i0:length(n6.umo$values) ]
n6.umo$time    = n6.umo$time[    i0:length(n6.umo$time)   ]
n6.mocr$values = n6.mocr$values[ i0:length(n6.mocr$values)]
n6.mocr$time   = n6.mocr$time[   i0:length(n6.mocr$time)  ]
#
axt.n6   = to.date(n6.fst$time,n6.fst$timeu,cal=n6.fst$timec)

# N2009 : fin en 2012 pour match avec N06
e9m1.fst  = select_period( e9m1.fst,  period = c(2009,2012))
e9m2.fst  = select_period( e9m2.fst,  period = c(2009,2012))
e9m3.fst  = select_period( e9m3.fst,  period = c(2009,2012))
e9m1.ekm  = select_period( e9m1.ekm,  period = c(2009,2012))
e9m2.ekm  = select_period( e9m2.ekm,  period = c(2009,2012))
e9m3.ekm  = select_period( e9m3.ekm,  period = c(2009,2012))
e9m1.umo  = select_period( e9m1.umo,  period = c(2009,2012))
e9m2.umo  = select_period( e9m2.umo,  period = c(2009,2012))
e9m3.umo  = select_period( e9m3.umo,  period = c(2009,2012))
e9m1.mocr = select_period( e9m1.mocr, period = c(2009,2012))
e9m2.mocr = select_period( e9m2.mocr, period = c(2009,2012))
e9m3.mocr = select_period( e9m3.mocr, period = c(2009,2012))
#
# N2007 : fake time serie avec N06 before 2007 :
e7m1.fst$values  = c( select_period(n6.fst,  period=c(2004,2006))$values, e7m1.fst$values )
e7m2.fst$values  = c( select_period(n6.fst,  period=c(2004,2006))$values, e7m2.fst$values )
e7m3.fst$values  = c( select_period(n6.fst,  period=c(2004,2006))$values, e7m3.fst$values )
e7m1.ekm$values  = c( select_period(n6.ekm,  period=c(2004,2006))$values, e7m1.ekm$values )
e7m2.ekm$values  = c( select_period(n6.ekm,  period=c(2004,2006))$values, e7m2.ekm$values )
e7m3.ekm$values  = c( select_period(n6.ekm,  period=c(2004,2006))$values, e7m3.ekm$values )
e7m1.umo$values  = c( select_period(n6.umo,  period=c(2004,2006))$values, e7m1.umo$values )
e7m2.umo$values  = c( select_period(n6.umo,  period=c(2004,2006))$values, e7m2.umo$values )
e7m3.umo$values  = c( select_period(n6.umo,  period=c(2004,2006))$values, e7m3.umo$values )
e7m1.mocr$values = c( select_period(n6.mocr, period=c(2004,2006))$values, e7m1.mocr$values)
e7m2.mocr$values = c( select_period(n6.mocr, period=c(2004,2006))$values, e7m2.mocr$values)
e7m3.mocr$values = c( select_period(n6.mocr, period=c(2004,2006))$values, e7m3.mocr$values)
#
e7m1.fst$time  = c( select_period(n6.fst,  period=c(2004,2006))$time, e7m1.fst$time )
e7m2.fst$time  = c( select_period(n6.fst,  period=c(2004,2006))$time, e7m2.fst$time )
e7m3.fst$time  = c( select_period(n6.fst,  period=c(2004,2006))$time, e7m3.fst$time )
e7m1.ekm$time  = c( select_period(n6.ekm,  period=c(2004,2006))$time, e7m1.ekm$time )
e7m2.ekm$time  = c( select_period(n6.ekm,  period=c(2004,2006))$time, e7m2.ekm$time )
e7m3.ekm$time  = c( select_period(n6.ekm,  period=c(2004,2006))$time, e7m3.ekm$time )
e7m1.umo$time  = c( select_period(n6.umo,  period=c(2004,2006))$time, e7m1.umo$time )
e7m2.umo$time  = c( select_period(n6.umo,  period=c(2004,2006))$time, e7m2.umo$time )
e7m3.umo$time  = c( select_period(n6.umo,  period=c(2004,2006))$time, e7m3.umo$time )
e7m1.mocr$time = c( select_period(n6.mocr, period=c(2004,2006))$time, e7m1.mocr$time)
e7m2.mocr$time = c( select_period(n6.mocr, period=c(2004,2006))$time, e7m2.mocr$time)
e7m3.mocr$time = c( select_period(n6.mocr, period=c(2004,2006))$time, e7m3.mocr$time)
#
# ===========================================================================
## # TREND and DETREND
## # =================
# Trend in obs
# ------------
obs.fst.trend = lm( obs.fst$values ~ obs.axt )$fitted.values
obs.ekm.trend = lm( obs.ekm$values ~ obs.axt )$fitted.values
obs.umo.trend = lm( obs.umo$values ~ obs.axt )$fitted.values
obs.moc.trend = lm( obs.moc$values ~ obs.axt )$fitted.values

# Trend on valor period
# ---------------------
n6.fst.trend  = lm( n6.fst$values  ~ axt.n6  )$fitted.values
n6.ekm.trend  = lm( n6.ekm$values  ~ axt.n6  )$fitted.values
n6.umo.trend  = lm( n6.umo$values  ~ axt.n6  )$fitted.values
n6.mocr.trend = lm( n6.mocr$values ~ axt.n6  )$fitted.values
#
# Select E2009 period : for E2009 detrend
# ---------------------------------------
n6.fst.trend.0912  = select_period(
    list(values = n6.fst.trend,time=n6.fst$time,timeu=n6.fst$timeu,timec=n6.fst$timec),
    c(2009,2012))
n6.ekm.trend.0912  = select_period(
    list(values = n6.ekm.trend,time=n6.ekm$time,timeu=n6.ekm$timeu,timec=n6.ekm$timec),
    c(2009,2012))
n6.umo.trend.0912  = select_period(
    list(values = n6.umo.trend,time=n6.umo$time,timeu=n6.umo$timeu,timec=n6.umo$timec),
    c(2009,2012))
n6.mocr.trend.0912 = select_period(
    list(values = n6.mocr.trend,time=n6.mocr$time,timeu=n6.mocr$timeu,timec=n6.mocr$timec),
    c(2009,2012))
#
# Select E2007 period : for E2007 detrend
# ---------------------------------------
n6.fst.trend.0711  = select_period(
    list(values=n6.fst.trend,time=n6.fst$time,timeu=n6.fst$timeu,timec=n6.fst$timec),
    c(2004,2011))
n6.ekm.trend.0711  = select_period(
    list(values=n6.ekm.trend,time=n6.ekm$time,timeu=n6.ekm$timeu,timec=n6.ekm$timec),
    c(2004,2011))
n6.umo.trend.0711  = select_period(
    list(values=n6.umo.trend,time=n6.umo$time,timeu=n6.umo$timeu,timec=n6.umo$timec),
    c(2004,2011))
n6.mocr.trend.0711 = select_period(
    list(values=n6.mocr.trend,time=n6.mocr$time,timeu=n6.mocr$timeu,timec=n6.mocr$timec),
    c(2004,2011))

# DETREND
# =======
# OBS
#-----
obs.fst.hf = obs.fst
obs.ekm.hf = obs.ekm
obs.umo.hf = obs.umo
obs.moc.hf = obs.moc
#
obs.fst.hf$values = obs.fst$values - obs.fst.trend
obs.ekm.hf$values = obs.ekm$values - obs.ekm.trend
obs.umo.hf$values = obs.umo$values - obs.umo.trend
obs.moc.hf$values = obs.moc$values - obs.moc.trend
#
# N06
#-----
n6.fst.hf  = n6.fst
n6.ekm.hf  = n6.ekm
n6.umo.hf  = n6.umo
n6.mocr.hf = n6.mocr
#
n6.fst.hf$values  = n6.fst$values  - n6.fst.trend
n6.ekm.hf$values  = n6.ekm$values  - n6.ekm.trend
n6.umo.hf$values  = n6.umo$values  - n6.umo.trend
n6.mocr.hf$values = n6.mocr$values - n6.mocr.trend

## # E2009
## # =======
## e9m1.fst.hf$values  = e9m1.fst$values  - n6.fst.trend.0912$values
## e9m2.fst.hf$values  = e9m2.fst$values  - n6.fst.trend.0912$values
## e9m3.fst.hf$values  = e9m3.fst$values  - n6.fst.trend.0912$values
## e9m1.ekm.hf$values  = e9m1.ekm$values  - n6.ekm.trend.0912$values
## e9m2.ekm.hf$values  = e9m2.ekm$values  - n6.ekm.trend.0912$values
## e9m3.ekm.hf$values  = e9m3.ekm$values  - n6.ekm.trend.0912$values
## e9m1.umo.hf$values  = e9m1.umo$values  - n6.umo.trend.0912$values
## e9m2.umo.hf$values  = e9m2.umo$values  - n6.umo.trend.0912$values
## e9m3.umo.hf$values  = e9m3.umo$values  - n6.umo.trend.0912$values
## e9m1.mocr.hf$values = e9m1.mocr$values - n6.mocr.trend.0912$values
## e9m2.mocr.hf$values = e9m2.mocr$values - n6.mocr.trend.0912$values
## e9m3.mocr.hf$values = e9m3.mocr$values - n6.mocr.trend.0912$values

# E2007
# =======
e7m1.fst.hf  = e7m1.fst
e7m2.fst.hf  = e7m2.fst
e7m3.fst.hf  = e7m3.fst
e7m1.ekm.hf  = e7m1.ekm
e7m2.ekm.hf  = e7m2.ekm
e7m3.ekm.hf  = e7m3.ekm
e7m1.umo.hf  = e7m1.umo
e7m2.umo.hf  = e7m2.umo
e7m3.umo.hf  = e7m3.umo
e7m1.mocr.hf = e7m1.mocr
e7m2.mocr.hf = e7m2.mocr
e7m3.mocr.hf = e7m3.mocr
#
e7m1.fst.hf$values  = e7m1.fst$values  - n6.fst.trend.0711$values
e7m2.fst.hf$values  = e7m2.fst$values  - n6.fst.trend.0711$values
e7m3.fst.hf$values  = e7m3.fst$values  - n6.fst.trend.0711$values
e7m1.ekm.hf$values  = e7m1.ekm$values  - n6.ekm.trend.0711$values
e7m2.ekm.hf$values  = e7m2.ekm$values  - n6.ekm.trend.0711$values
e7m3.ekm.hf$values  = e7m3.ekm$values  - n6.ekm.trend.0711$values
e7m1.umo.hf$values  = e7m1.umo$values  - n6.umo.trend.0711$values
e7m2.umo.hf$values  = e7m2.umo$values  - n6.umo.trend.0711$values
e7m3.umo.hf$values  = e7m3.umo$values  - n6.umo.trend.0711$values
e7m1.mocr.hf$values = e7m1.mocr$values - n6.mocr.trend.0711$values
e7m2.mocr.hf$values = e7m2.mocr$values - n6.mocr.trend.0711$values
e7m3.mocr.hf$values = e7m3.mocr$values - n6.mocr.trend.0711$values
#
# NORM
# ====
# OBS
obs.fst.norm      = mean( select_period( obs.fst,      refperiod )$values)
obs.ekm.norm      = mean( select_period( obs.ekm,      refperiod )$values)
obs.umo.norm      = mean( select_period( obs.umo,      refperiod )$values)
obs.moc.norm      = mean( select_period( obs.moc,      refperiod )$values)
#
obs.fst.hf.norm   = mean( select_period( obs.fst.hf,   refperiod )$values)
obs.ekm.hf.norm   = mean( select_period( obs.ekm.hf,   refperiod )$values)
obs.umo.hf.norm   = mean( select_period( obs.umo.hf,   refperiod )$values)
obs.moc.hf.norm   = mean( select_period( obs.moc.hf,   refperiod )$values)

# N06
n6.fst.norm       = mean( select_period( n6.fst,       refperiod )$values)
n6.ekm.norm       = mean( select_period( n6.ekm,       refperiod )$values)
n6.umo.norm       = mean( select_period( n6.umo,       refperiod )$values)
n6.mocr.norm      = mean( select_period( n6.mocr,      refperiod )$values)
#
n6.fst.hf.norm    = mean( select_period( n6.fst.hf,    refperiod )$values)
n6.ekm.hf.norm    = mean( select_period( n6.ekm.hf,    refperiod )$values)
n6.umo.hf.norm    = mean( select_period( n6.umo.hf,    refperiod )$values)
n6.mocr.hf.norm   = mean( select_period( n6.mocr.hf,   refperiod )$values)
#
# E2007
e7m1.fst.norm     = mean( select_period( e7m1.fst,     refperiod )$values)
e7m2.fst.norm     = mean( select_period( e7m2.fst,     refperiod )$values)
e7m3.fst.norm     = mean( select_period( e7m3.fst,     refperiod )$values)
e7m1.ekm.norm     = mean( select_period( e7m1.ekm,     refperiod )$values)
e7m2.ekm.norm     = mean( select_period( e7m2.ekm,     refperiod )$values)
e7m3.ekm.norm     = mean( select_period( e7m3.ekm,     refperiod )$values)
e7m1.umo.norm     = mean( select_period( e7m1.umo,     refperiod )$values)
e7m2.umo.norm     = mean( select_period( e7m2.umo,     refperiod )$values)
e7m3.umo.norm     = mean( select_period( e7m3.umo,     refperiod )$values)
e7m1.mocr.norm    = mean( select_period( e7m1.mocr,    refperiod )$values)
e7m2.mocr.norm    = mean( select_period( e7m2.mocr,    refperiod )$values)
e7m3.mocr.norm    = mean( select_period( e7m3.mocr,    refperiod )$values)
#
e7m1.fst.hf.norm  = mean( select_period( e7m1.fst.hf,  refperiod )$values)
e7m2.fst.hf.norm  = mean( select_period( e7m2.fst.hf,  refperiod )$values)
e7m3.fst.hf.norm  = mean( select_period( e7m3.fst.hf,  refperiod )$values)
e7m1.ekm.hf.norm  = mean( select_period( e7m1.ekm.hf,  refperiod )$values)
e7m2.ekm.hf.norm  = mean( select_period( e7m2.ekm.hf,  refperiod )$values)
e7m3.ekm.hf.norm  = mean( select_period( e7m3.ekm.hf,  refperiod )$values)
e7m1.umo.hf.norm  = mean( select_period( e7m1.umo.hf,  refperiod )$values)
e7m2.umo.hf.norm  = mean( select_period( e7m2.umo.hf,  refperiod )$values)
e7m3.umo.hf.norm  = mean( select_period( e7m3.umo.hf,  refperiod )$values)
e7m1.mocr.hf.norm = mean( select_period( e7m1.mocr.hf, refperiod )$values)
e7m2.mocr.hf.norm = mean( select_period( e7m2.mocr.hf, refperiod )$values)
e7m3.mocr.hf.norm = mean( select_period( e7m3.mocr.hf, refperiod )$values)
#

# ANOMALIES
# =========
# OBS
# ---
obs.fst.ano      = anoserie( obs.fst,      ref = obs.fst.norm     )
obs.ekm.ano      = anoserie( obs.ekm,      ref = obs.ekm.norm     )
obs.umo.ano      = anoserie( obs.umo,      ref = obs.umo.norm     )
obs.moc.ano      = anoserie( obs.moc,      ref = obs.moc.norm     )
#
obs.fst.hf.ano   = anoserie( obs.fst.hf,   ref = obs.fst.hf.norm  )
obs.ekm.hf.ano   = anoserie( obs.ekm.hf,   ref = obs.ekm.hf.norm  )
obs.umo.hf.ano   = anoserie( obs.umo.hf,   ref = obs.umo.hf.norm  )
obs.moc.hf.ano   = anoserie( obs.moc.hf,   ref = obs.moc.hf.norm  )

# N06
# ---
n6.fst.ano       = anoserie( n6.fst,       ref = n6.fst.norm      )
n6.ekm.ano       = anoserie( n6.ekm,       ref = n6.ekm.norm      )
n6.umo.ano       = anoserie( n6.umo,       ref = n6.umo.norm      )
n6.mocr.ano      = anoserie( n6.mocr,      ref = n6.mocr.norm     )
#
n6.fst.hf.ano    = anoserie( n6.fst.hf,    ref = n6.fst.hf.norm   )
n6.ekm.hf.ano    = anoserie( n6.ekm.hf,    ref = n6.ekm.hf.norm   )
n6.umo.hf.ano    = anoserie( n6.umo.hf,    ref = n6.umo.hf.norm   )
n6.mocr.hf.ano   = anoserie( n6.mocr.hf,   ref = n6.mocr.hf.norm  )
#
# E2007
# -----
e7m1.fst.ano     = anoserie( e7m1.fst,     ref = e7m1.fst.norm    )
e7m2.fst.ano     = anoserie( e7m2.fst,     ref = e7m2.fst.norm    )
e7m3.fst.ano     = anoserie( e7m3.fst,     ref = e7m3.fst.norm    )
e7m1.ekm.ano     = anoserie( e7m1.ekm,     ref = e7m1.ekm.norm    )
e7m2.ekm.ano     = anoserie( e7m2.ekm,     ref = e7m2.ekm.norm    )
e7m3.ekm.ano     = anoserie( e7m3.ekm,     ref = e7m3.ekm.norm    )
e7m1.umo.ano     = anoserie( e7m1.umo,     ref = e7m1.umo.norm    )
e7m2.umo.ano     = anoserie( e7m2.umo,     ref = e7m2.umo.norm    )
e7m3.umo.ano     = anoserie( e7m3.umo,     ref = e7m3.umo.norm    )
e7m1.mocr.ano    = anoserie( e7m1.mocr,    ref = e7m1.mocr.norm   )
e7m2.mocr.ano    = anoserie( e7m2.mocr,    ref = e7m2.mocr.norm   )
e7m3.mocr.ano    = anoserie( e7m3.mocr,    ref = e7m3.mocr.norm   )
#
e7m1.fst.hf.ano  = anoserie( e7m1.fst.hf,  ref = e7m1.fst.hf.norm )
e7m2.fst.hf.ano  = anoserie( e7m2.fst.hf,  ref = e7m2.fst.hf.norm )
e7m3.fst.hf.ano  = anoserie( e7m3.fst.hf,  ref = e7m3.fst.hf.norm )
e7m1.ekm.hf.ano  = anoserie( e7m1.ekm.hf,  ref = e7m1.ekm.hf.norm )
e7m2.ekm.hf.ano  = anoserie( e7m2.ekm.hf,  ref = e7m2.ekm.hf.norm )
e7m3.ekm.hf.ano  = anoserie( e7m3.ekm.hf,  ref = e7m3.ekm.hf.norm )
e7m1.umo.hf.ano  = anoserie( e7m1.umo.hf,  ref = e7m1.umo.hf.norm )
e7m2.umo.hf.ano  = anoserie( e7m2.umo.hf,  ref = e7m2.umo.hf.norm )
e7m3.umo.hf.ano  = anoserie( e7m3.umo.hf,  ref = e7m3.umo.hf.norm )
e7m1.mocr.hf.ano = anoserie( e7m1.mocr.hf, ref = e7m1.mocr.hf.norm)
e7m2.mocr.hf.ano = anoserie( e7m2.mocr.hf, ref = e7m2.mocr.hf.norm)
e7m3.mocr.hf.ano = anoserie( e7m3.mocr.hf, ref = e7m3.mocr.hf.norm)
#
## # E2009
## # -----
## e9m1.fst.ano     = anoserie( e9m1.fst,  ref = n6.fst.norm      )
## e9m2.fst.ano     = anoserie( e9m2.fst,  ref = n6.fst.norm      )
## e9m3.fst.ano     = anoserie( e9m3.fst,  ref = n6.fst.norm      )
## e9m1.ekm.ano     = anoserie( e9m1.ekm,  ref = n6.ekm.norm      )
## e9m2.ekm.ano     = anoserie( e9m2.ekm,  ref = n6.ekm.norm      )
## e9m3.ekm.ano     = anoserie( e9m3.ekm,  ref = n6.ekm.norm      )
## e9m1.umo.ano     = anoserie( e9m1.umo,  ref = n6.umo.norm      )
## e9m2.umo.ano     = anoserie( e9m2.umo,  ref = n6.umo.norm      )
## e9m3.umo.ano     = anoserie( e9m3.umo,  ref = n6.umo.norm      )
## e9m1.mocr.ano    = anoserie( e9m1.mocr, ref = n6.mocr.norm     )
## e9m2.mocr.ano    = anoserie( e9m2.mocr, ref = n6.mocr.norm     )
## e9m3.mocr.ano    = anoserie( e9m3.mocr, ref = n6.mocr.norm     )
#
#
# Cumulative transport computation
# ================================
# time factor
n6.timefactor  = 5/365
obs.timefactor = 0.5/365
#
# OBS
obs.fst.sum      = cumsum( obs.fst.ano$values      * obs.timefactor)
obs.ekm.sum      = cumsum( obs.ekm.ano$values      * obs.timefactor)
obs.umo.sum      = cumsum( obs.umo.ano$values      * obs.timefactor)
obs.moc.sum      = cumsum( obs.moc.ano$values      * obs.timefactor)
#
obs.fst.hf.sum   = cumsum( obs.fst.hf.ano$values   * obs.timefactor)
obs.ekm.hf.sum   = cumsum( obs.ekm.hf.ano$values   * obs.timefactor)
obs.umo.hf.sum   = cumsum( obs.umo.hf.ano$values   * obs.timefactor)
obs.moc.hf.sum   = cumsum( obs.moc.hf.ano$values   * obs.timefactor)
#
# N06
n6.fst.sum       = cumsum( n6.fst.ano$values       * n6.timefactor )
n6.ekm.sum       = cumsum( n6.ekm.ano$values       * n6.timefactor )
n6.umo.sum       = cumsum( n6.umo.ano$values       * n6.timefactor )
n6.mocr.sum      = cumsum( n6.mocr.ano$values      * n6.timefactor )
#
n6.fst.hf.sum    = cumsum( n6.fst.hf.ano$values    * n6.timefactor )
n6.ekm.hf.sum    = cumsum( n6.ekm.hf.ano$values    * n6.timefactor )
n6.umo.hf.sum    = cumsum( n6.umo.hf.ano$values    * n6.timefactor )
n6.mocr.hf.sum   = cumsum( n6.mocr.hf.ano$values   * n6.timefactor )
#
# E2007
#------
e7m1.fst.sum     = cumsum( e7m1.fst.ano$values     * n6.timefactor )
e7m2.fst.sum     = cumsum( e7m2.fst.ano$values     * n6.timefactor )
e7m3.fst.sum     = cumsum( e7m3.fst.ano$values     * n6.timefactor )
e7m1.ekm.sum     = cumsum( e7m1.ekm.ano$values     * n6.timefactor )
e7m2.ekm.sum     = cumsum( e7m2.ekm.ano$values     * n6.timefactor )
e7m3.ekm.sum     = cumsum( e7m3.ekm.ano$values     * n6.timefactor )
e7m1.umo.sum     = cumsum( e7m1.umo.ano$values     * n6.timefactor )
e7m2.umo.sum     = cumsum( e7m2.umo.ano$values     * n6.timefactor )
e7m3.umo.sum     = cumsum( e7m3.umo.ano$values     * n6.timefactor )
e7m1.mocr.sum    = cumsum( e7m1.mocr.ano$values    * n6.timefactor )
e7m2.mocr.sum    = cumsum( e7m2.mocr.ano$values    * n6.timefactor )
e7m3.mocr.sum    = cumsum( e7m3.mocr.ano$values    * n6.timefactor )
#
e7m1.fst.hf.sum  = cumsum( e7m1.fst.hf.ano$values  * n6.timefactor )
e7m2.fst.hf.sum  = cumsum( e7m2.fst.hf.ano$values  * n6.timefactor )
e7m3.fst.hf.sum  = cumsum( e7m3.fst.hf.ano$values  * n6.timefactor )
e7m1.ekm.hf.sum  = cumsum( e7m1.ekm.hf.ano$values  * n6.timefactor )
e7m2.ekm.hf.sum  = cumsum( e7m2.ekm.hf.ano$values  * n6.timefactor )
e7m3.ekm.hf.sum  = cumsum( e7m3.ekm.hf.ano$values  * n6.timefactor )
e7m1.umo.hf.sum  = cumsum( e7m1.umo.hf.ano$values  * n6.timefactor )
e7m2.umo.hf.sum  = cumsum( e7m2.umo.hf.ano$values  * n6.timefactor )
e7m3.umo.hf.sum  = cumsum( e7m3.umo.hf.ano$values  * n6.timefactor )
e7m1.mocr.hf.sum = cumsum( e7m1.mocr.hf.ano$values * n6.timefactor )
e7m2.mocr.hf.sum = cumsum( e7m2.mocr.hf.ano$values * n6.timefactor )
e7m3.mocr.hf.sum = cumsum( e7m3.mocr.hf.ano$values * n6.timefactor )
#
## # E2009
## #------
## e9m1.fst.sum     = cumsum( e9m1.fst.ano$values     * n6.timefactor )
## e9m2.fst.sum     = cumsum( e9m2.fst.ano$values     * n6.timefactor )
## e9m3.fst.sum     = cumsum( e9m3.fst.ano$values     * n6.timefactor )
## e9m1.ekm.sum     = cumsum( e9m1.ekm.ano$values     * n6.timefactor )
## e9m2.ekm.sum     = cumsum( e9m2.ekm.ano$values     * n6.timefactor )
## e9m3.ekm.sum     = cumsum( e9m3.ekm.ano$values     * n6.timefactor )
## e9m1.umo.sum     = cumsum( e9m1.umo.ano$values     * n6.timefactor )
## e9m2.umo.sum     = cumsum( e9m2.umo.ano$values     * n6.timefactor )
## e9m3.umo.sum     = cumsum( e9m3.umo.ano$values     * n6.timefactor )
## e9m1.mocr.sum    = cumsum( e9m1.mocr.ano$values    * n6.timefactor )
## e9m2.mocr.sum    = cumsum( e9m2.mocr.ano$values    * n6.timefactor )
## e9m3.mocr.sum    = cumsum( e9m3.mocr.ano$values    * n6.timefactor )
## #
#
# ===========================================================================
# PLOT
# ===========================================================================
n6.axt = to.date( n6.fst$time,   n6.fst$timeu,   cal=n6.fst$timec  )
e9.axt = to.date( e9m1.fst$time, e9m1.fst$timeu, cal=e9m1.fst$timec)
e7.axt = to.date( e7m1.fst$time, e7m1.fst$timeu, cal=e7m1.fst$timec)

xtickpos = c(as.PCICt("2004-01-01",cal="gregorian"),as.PCICt("2005-01-01",cal="gregorian"),as.PCICt("2006-01-01",cal="gregorian"),as.PCICt("2007-01-01",cal="gregorian"),as.PCICt("2008-01-01",cal="gregorian"),as.PCICt("2009-01-01",cal="gregorian"),as.PCICt("2010-01-01",cal="gregorian"),as.PCICt("2011-01-01",cal="gregorian"),as.PCICt("2012-01-01",cal="gregorian"),as.PCICt("2013-01-01",cal="gregorian"))
yrlist=c('2004','2005','2006','2007','2008','2009','2010','2011','2012','2013')
 
# ===========================================================================
fileout = "../figures/figure_08.pdf"
pdf(fileout,width=5,height=5)
#
ylim = c(-13,5)
lwd=1.3
lwde=0.8
# Subplot 1
# =========
par(fig = c(0, 0.5, 0.5, 1),mar=c(2,2.4,2,1.6), mgp=c(1.5, 0.5, 0))
plot(obs.axt, obs.fst.sum,
     main='(a) Observations raw',
     ylab='Sv year',xlab='',ylim=ylim,
     type='l',col=colrapid$FS,lwd=lwd,
     xaxt='n',
     cex.lab=.6,cex.main=.8,cex.axis=0.7)
#
points(obs.axt,obs.ekm.sum,
     lwd=lwd,type='l',col=colrapid$EKM)
points(obs.axt,obs.moc.sum,
     lwd=lwd,type='l',col='black')
points(obs.axt,obs.umo.sum,
     lwd=lwd,type='l',col=colrapid$UMO)
segments(as.PCICt("2004-01-01",cal="gregorian"),0,
         as.PCICt("2009-01-01",cal="gregorian"),0,
         col='black')
axis(side = 1, at = xtickpos, labels = yrlist,cex.axis=.7)

# subplot2
# ========
par(new=T, fig = c(0, 0.5, 0, 0.5),mar=c(2,2.4,2,1.6), mgp=c(1.5, 0.5, 0))
plot(obs.axt, obs.fst.hf.sum,
     main='(c) Observations detrended',
     ylab='Sv year',xlab='',ylim=ylim,
     type='l',col=colrapid$FS,lwd=lwd,
     xaxt='n',
     cex.lab=.6,cex.main=.8,cex.axis=0.7)
#
points(obs.axt,obs.ekm.hf.sum,
     lwd=lwd,type='l',col=colrapid$EKM)
points(obs.axt,obs.moc.hf.sum,
     lwd=lwd,type='l',col='black')
points(obs.axt,obs.umo.hf.sum,
     lwd=lwd,type='l',col=colrapid$UMO)
segments(as.PCICt("2004-01-01",cal="gregorian"),0,
         as.PCICt("2009-01-01",cal="gregorian"),0,
         col='black')
axis(side = 1, at = xtickpos, labels = yrlist,cex.axis=.7)


# Subplot 3
# =========
par(new=T,fig = c(0.5, 1, 0.5, 1),mar=c(2,2.4,2,1.6), mgp=c(1.5, 0.5, 0))
plot(n6.axt,n6.fst.sum,
     main='(b) ORCA12 raw',
     ylab='Sv year',xlab='',ylim=ylim,
     type='l',col=colrapid$FS,lwd=lwd,
     xaxt='n',
     cex.lab=.6,cex.main=.8,cex.axis=.7)
points( n6.axt,n6.ekm.sum,
     lwd=lwd,type='l',col=colrapid$EKM)
points( n6.axt,n6.mocr.sum,
     lwd=lwd,type='l',col='black')
points( n6.axt,n6.umo.sum,
     lwd=lwd,type='l',col=colrapid$UMO)
# e7
points( e7.axt,e7m1.fst.sum,
     lwd=lwde,type='l',col=colrapid$FS,lty=1)
points( e7.axt,e7m1.ekm.sum,
     lwd=lwde,type='l',col=colrapid$EKM,lty=1)
points( e7.axt,e7m1.umo.sum,
     lwd=lwde,type='l',col=colrapid$UMO,lty=1)
points( e7.axt,e7m1.mocr.sum,
     lwd=lwde,type='l',col='black',lty=1)
#
points( e7.axt,e7m2.fst.sum,
     lwd=lwde,type='l',col=colrapid$FS,lty=1)
points( e7.axt,e7m2.ekm.sum,
     lwd=lwde,type='l',col=colrapid$EKM,lty=1)
points( e7.axt,e7m2.umo.sum,
     lwd=lwde,type='l',col=colrapid$UMO,lty=1)
points( e7.axt,e7m2.mocr.sum,
     lwd=lwde,type='l',col='black',lty=1)
#
points( e7.axt, e7m3.fst.sum,
     lwd=lwde,type='l',col=colrapid$FS,lty=1)
points( e7.axt,e7m3.ekm.sum,
     lwd=lwde,type='l',col=colrapid$EKM,lty=1)
points( e7.axt,e7m3.umo.sum,
     lwd=lwde,type='l',col=colrapid$UMO,lty=1)
points(e7.axt,e7m3.mocr.sum,
     lwd=lwde,type='l',col='black',lty=1)
segments(as.PCICt("2004-01-01",cal="gregorian"),0,
         as.PCICt("2009-01-01",cal="gregorian"),0,
         col='black')
axis(side = 1, at = xtickpos, labels = yrlist,cex.axis=.7)
#
# Subplot 4
# =========
par(new=T,fig = c(0.5, 1, 0, 0.5),mar=c(2,2.4,2,1.6), mgp=c(1.5, 0.5, 0))
plot(n6.axt,n6.fst.hf.sum,
     main='(d) ORCA12 detrended',
     ylab='Sv year',xlab='',ylim=ylim,
     type='l',col=colrapid$FS,lwd=lwd,
     xaxt='n',
     cex.lab=.6,cex.main=.8,cex.axis=.7)
points( n6.axt,n6.ekm.hf.sum,
     lwd=lwd,type='l',col=colrapid$EKM)
points( n6.axt,n6.mocr.hf.sum,
     lwd=lwd,type='l',col='black')
points( n6.axt,n6.umo.hf.sum,
     lwd=lwd,type='l',col=colrapid$UMO)
# e7
points( e7.axt,e7m1.fst.hf.sum,
     lwd=lwde,type='l',col=colrapid$FS,lty=1)
points( e7.axt,e7m1.ekm.hf.sum,
     lwd=lwde,type='l',col=colrapid$EKM,lty=1)
points( e7.axt,e7m1.umo.hf.sum,
     lwd=lwde,type='l',col=colrapid$UMO,lty=1)
points( e7.axt,e7m1.mocr.hf.sum,
     lwd=lwde,type='l',col='black',lty=1)
#
points( e7.axt,e7m2.fst.hf.sum,
     lwd=lwde,type='l',col=colrapid$FS,lty=1)
points( e7.axt,e7m2.ekm.hf.sum,
     lwd=lwde,type='l',col=colrapid$EKM,lty=1)
points( e7.axt,e7m2.umo.hf.sum,
     lwd=lwde,type='l',col=colrapid$UMO,lty=1)
points( e7.axt,e7m2.mocr.hf.sum,
     lwd=lwde,type='l',col='black',lty=1)
#
points( e7.axt, e7m3.fst.hf.sum,
     lwd=lwde,type='l',col=colrapid$FS,lty=1)
points( e7.axt,e7m3.ekm.hf.sum,
     lwd=lwde,type='l',col=colrapid$EKM,lty=1)
points( e7.axt,e7m3.umo.hf.sum,
     lwd=lwde,type='l',col=colrapid$UMO,lty=1)
points(e7.axt,e7m3.mocr.hf.sum,
     lwd=lwde,type='l',col='black',lty=1)
segments(as.PCICt("2004-01-01",cal="gregorian"),0,
         as.PCICt("2009-01-01",cal="gregorian"),0,
         col='black')
axis(side = 1, at = xtickpos, labels = yrlist,cex.axis=.7)

graphics.off()
#
#
# ===========================================================================
