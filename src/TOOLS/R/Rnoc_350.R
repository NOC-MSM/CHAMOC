# ================================================================
# Fonctions de base propre au NOC                                #
# par exemple : chargement des infos d'une grille NEMO           #
# ================================================================
source('~/TOOLS/R/Rutils_350.R')
# ================================================================
# useful lists :
# ==============
colrapid=list(EKM='Green',UMO='deeppink',FS='blue',MOC='red')



# ================================================================
get.lev = function(grid='ORCA0083'){
    if (grid=='ORCA0083') {
        fmask = '/group_workspaces/jasmin2/nemo/vol1/ORCA0083-N006/domain/mask.nc'
        levels = mynt(fmask,variable='nav_lev')$values
        
    } else if (grid=='RAPID'){
        f = '/noc/msm/working/meso-clip/agathe/DATA/VALOR/moc_vertical.nc'
        nc=open.ncdf(f)
        levels = nc$dim$depth$vals
        close.ncdf(nc)
    } else {stop('!!! get.lev() error : grid unknown !!!')}

    list(values=levels, units='m')
}
# -----------------------------------------------------------------
get.time = function(run='N006') {
    if (run=='N006') {
        ftime = '/noc/msm/working/meso-clip/agathe/DATA/ORCA0083-N06/CDFToutputs/d05/ORCA0083-N06_time_stamp.txt'
        ft = read.table(ftime,col.names='tstep',colClasses='character')
        origin = "1958-01-01"
        origin.pcict = as.PCICt(origin,'noleap')
        timeval = sapply(ft$tstep,as.PCICt,cal='noleap',format='%Y%m%d',USE.NAMES = FALSE)
        timeval.origin = timeval - as.numeric(origin.pcict)
    } else {
        stop(paste('Run unkown :',run))
    }

    timedate=list(values=timeval.origin,units='seconds since 1958-01-01',cal='noleap')
}
# -----------------------------------------------------------------
getts = function(serie,variable='moc',index=F) {
  if(! variable %in% c('moc','umo','fs','ekm')) {
    stop("getts error : option should be one of these : moc, umo, fs, ekm")
  }
  
  if (variable == 'moc') {
    idepth    = apply(serie$values[40:50,],2,which.max) + 39
    newvalues = apply(serie$values[40:50,],2,max)
    
  } else if (variable == 'umo') {
    idepth    = apply(serie$values[40:46,],2,which.min) + 39
    newvalues = apply(serie$values[40:46,],2,min)
    
  } else if (variable == 'fs') {
    idepth    = apply(serie$values,2,which.max)
    newvalues = apply(serie$values,2,max)
    
  } else if (variable == 'ekm') {
    Nt        = length(serie$time)
    idepth    = apply(abs(serie$values),2,which.max)
    newvalues = serie$values[array(data=c(idepth,seq(Nt)),dim=c(Nt,2))]
    
  }
  if (index == T) {
    newvalues = idepth
  }
  list(values=newvalues,time=serie$time,timeu=serie$timeu,timec=serie$timec)
}

# -----------------------------------------------------------------
change.time = function(serie,timenew) {
    serienew = serie
    serienew$time = timenew$values
    serienew$timeu = timenew$units
    serienew$timec = timenew$cal

    serienew
}
