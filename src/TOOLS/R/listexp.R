lexp = list()
#
# ============================================================================
# ORCA12
# ============================================================================
# N006
# ----
lexp[['N006']]=list(name='ORCA0083-N006',datedeb='19580101',datefin='20121231',stream='ORCA12',group='',grid_oce='ORCA12',ismember=F,nickname='N006',cdfdir='/gws/nopw/j04/nemo_vol5/atb299/DYNAMOC/Agathe_vol3/DATA/ORCA0083/N006/cdftools_outputs/TIMESERIES')
#
# ENSEMBLE N12_2007
# -----------------
for(i in seq(3)){
    expname = sprintf('N12_2007_%02d',i)
    lexp[[expname]] = list(name=expname,datedeb='20070101',datefin='20111231',stream='ORCA12',group='ENSEMBLE',grid_oce='ORCA12',ismember=T,ensemblename='N12_2007', cdfdir=sprintf('/gws/nopw/j04/nemo_vol5/atb299/DYNAMOC/Agathe_vol3/DATA/ORCA0083/ENSEMBLES/N12_2007/N12_2007_%02d/cdftools_outputs/TIMESERIES',i),parent='ORCA0083-N006',nickname=sprintf('E7m%s',i))
}
#
# ENSEMBLE N12_2008
# -----------------
for(i in seq(3)){
    expname = sprintf('N12_2008_%02d',i)
    lexp[[expname]] = list(name=expname,datedeb='20080101',datefin='20091231',stream='ORCA12',group='ENSEMBLE',grid_oce='ORCA12',ismember=T,ensemblename='N12_2008', cdfdir=sprintf('/gws/nopw/j04/nemo_vol5/atb299/DYNAMOC/Agathe_vol3/DATA/ORCA0083/ENSEMBLES/N12_2008/N12_2008_%02d/cdftools_outputs/TIMESERIES',i),parent='ORCA0083-N006',nickname=sprintf('E7m%s',i))
}
#
# ENSEMBLE N12_2009
# -----------------
for(i in seq(3)){
    expname = sprintf('N12_2009_0%s',i)
    lexp[[expname]] = list(name=expname,datedeb='20090101',datefin='20151231',stream='ORCA12',group='ENSEMBLE',grid_oce='ORCA12',ismember=T,ensemblename='N12_2009', cdfdir=sprintf('/gws/nopw/j04/nemo_vol5/atb299/DYNAMOC/Agathe_vol3/DATA/ORCA0083/ENSEMBLES/N12_2009/N12_2009_%02d/cdftools_outputs/TIMESERIES',i),parent='ORCA0083-N006')
}
for(i in seq(4,11)){
    expname = sprintf('N12_2009_%02d',i)
    lexp[[expname]] = list(name=expname,datedeb='20090101',datefin='20091231',stream='ORCA12',group='ENSEMBLE',grid_oce='ORCA12',ismember=T,ensemblename='N12_2009', cdfdir=sprintf('/gws/nopw/j04/nemo_vol5/atb299/DYNAMOC/Agathe_vol3/DATA/ORCA0083/ENSEMBLES/N12_2009/N12_2009_%02d/cdftools_outputs/TIMESERIES',i),parent='ORCA0083-N006',nickname=sprintf('E7m%s',i))
}

# ============================================================================
# FUNCTIONS
# ============================================================================
diagfname = function(exp,diagid='valormoc',freq='d05'){
  filediag=sprintf('%s_%s_%s_%s_%s.nc',exp$name,exp$datedeb,exp$datefin,diagid,freq)
  filediag
}



