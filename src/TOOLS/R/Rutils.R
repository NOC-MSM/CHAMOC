# ================================================================
# Fonctions de base utilisees par autres scripts #
# Et chargement des librairies usuelles          #
# ================================================================
# ================================================================
library(ncdf4) # dans ancienne version de R, remplacer par ncdf (sans le 4, n'est plus compatible avec les vesions récentes
library(abind,lib.loc="/home/users/agathe/R/x86_64-redhat-linux-gnu-library/3.5")
library(PCICt,lib.loc="/home/users/agathe/R/x86_64-redhat-linux-gnu-library/3.5")
# this need to be change to 3.2 to come back to old version
# ================================================================
#                        useful list 
# ================================================================
list_mth = list(JAN='01',FEB='02',MAR='03',APR='04',MAY='05',JUN='06',JUL='07',AUG='08',SEP='09',OCT='10',NOV='11',DEC='12')

list_season = list(JFM=c(1,2,3),AMJ=c(4,5,6),JAS=c(7,8,9),OND=c(10,11,12),
                   JJA=c(6,7,8),JJAS=c(6,7,8,9),DJF=c(12,1,2),FMA=c(2,3,4),
                   DJFM=c(12,1,2,3),NDJFM=c(11,12,1,2,3),JFMA=c(1,2,3,4),
                   ALL=c(1,2,3,4,5,6,7,8,9,10,11,12),
                   JAN=1,FEB=2,MAR=3,APR=4,MAY=5,JUN=6,
                   JUL=7,AUG=8,SEP=9,OCT=10,NOV=11,DEC=12)

sf=1e-12 # scale factor for sea ice

# axe des temps pour cycle annuel :
tyr = seq(as.Date("1970-01-15"), as.Date("1970-12-15"), by = "month")
timeud = "seconds since 1970-01-01" # default time unit


# ================================================================
#                        useful values
# ================================================================
SurfaceGrid = function(grid='ORCA2'){

    if (grid=='ORCA2') {
        fmask='/net/cratos/usr/cratos/varclim/IPSLCM5A/PROD/piControl2/OCE/piControl2_mesh_mask.nc'
        e1t = mynt(fmask,'e1t')$values
        e2t = mynt(fmask,'e2t')$values
        tmask = mynt(fmask,'tmask')$values[,,1]
        S = e1t*e2t*tmask #tmask met a zero les mailles Land
        Stot=sum(S)
    } else if (grid=='Atm') {
        fmask = '/net/cratos/usr/cratos/varclim/IPSLCM5A/PROD/piControl2/ATM/Output/MO/piControl2_18000401_18000430_1M_histmth.nc'
        ncm = open.ncdf(fmask)
        lat = get.var.ncdf(ncm,ncm$dim[['lat']])
        R = 6400
        dy = 2*pi*R/96
        dx = R*cos(abs(lat)*pi/180)*sin(2*pi/96)
        Slat = dx*dy
        S = array(Slat,dim=c(96,96))
        Stot = sum(S)
    } else {stop(' !!! SurfaceGrid error : I don\'t know this grid !!!')}
    list(grid=S, total=Stot)
}
# -------------------------------
VolumeGrid = function(grid='ORCA2'){
    # !!! fonction non testee ! a verifier !!!
    if (grid=='ORCA2') {
        fmask='/net/cratos/usr/cratos/varclim/IPSLCM5A/PROD/piControl2/OCE/piControl2_mesh_mask.nc'
        e1t = mynt(fmask,'e1t')$values
        e2t = mynt(fmask,'e2t')$values
        e3t = mynt(fmask,'e3t')$values
        tmask = mynt(fmask,'tmask')$values
        #
        dx = array(e1t,dim=dim(e3t))
        dy = array(e2t,dim=dim(e3t))
        #
        V = dx*dy*e3t*tmask #tmask met a zero les mailles Land
        Soce=sum(V)
    } else {stop('I don\'t know this grid')}
    voce
}
# -----------------------------------
getMask = function(grid='ORCA2',tuvw='t'){

    if (grid=='ORCA2') {
        fmask='/net/cratos/usr/cratos/varclim/IPSLCM5A/PROD/piControl2/OCE/piControl2_mesh_mask.nc'
        if (tuvw=='t') { mask = mynt(fmask,'tmask')$values }
        else if (tuvw=='u') { mask = mynt(fmask,'umask')$values }
        else if (tuvw=='v') { mask = mynt(fmask,'vmask')$values }
        else if (tuvw=='w') { mask = mynt(fmask,'wmask')$values }
        else {stop(' !!! getMask error : I don\t know this grid and tuvw !!!')}
}
    mask
}

# ================================================================
# Fonctions de traitement de fichiers
# ================================================================
# Fonction qui recupere les dimensions des netcdf (2D) et sort une liste
mynd=function(file,grid='regu'){
  nc=open.ncdf(file)
  if (grid=='regu') {
    lon=nc$dim$lon$vals; lonu=nc$dim$lon$units
    lat=nc$dim$lat$vals; latu=nc$dim$lat$units
    time=floor(as.numeric(nc$dim$time$vals)); timeu=nc$dim$time$units
    list(lon=lon,lonu=lonu,lat=lat,latu=latu,time=time,timeu=timeu)
  } else if (grid=='nemo'){
    jpjb = nc$dim$jpjb$vals; jpjb = nc$dim$jpjb$units
    jpib = nc$dim$jpib$vals; jpjb = nc$dim$jpib$units
    time=floor(as.numeric(nc$dim$time$vals)); timeu=nc$dim$time$units
    lon=get.var.ncdf(nc,nc$var[['longitude']])
    lonu = nc$var[['longitude']]$units
    lat=get.var.ncdf(nc,nc$var[['latitude']])
    latu = nc$var[['latitude']]$units
    list(jpjb=jpjb,jpib=jpib,lon=lon,lonu=lonu,lat=lat,latu=latu,time=time,timeu=timeu)
  }
} # j.c. 
 
# Fonction qui extrait une variable (time serie) d'un netcdf et sort une liste
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
mynt=function(file,variable='ts'){
  nc=open.ncdf(file)
  values = get.var.ncdf(nc,nc$var[[variable]])
  units  = nc$var[[variable]]$units
  if ('time_counter' %in% names(nc$var)) {
   time   = get.var.ncdf(nc,'time_counter')
   timeu  = att.get.ncdf(nc,'time_counter','units')$value
   timec  = att.get.ncdf(nc,'time_counter','calendar')$value
  } else if ('time' %in% names(nc$var)) {
   time   = get.var.ncdf(nc,'time')
   timeu  = nc$var$time$units
   timec  = att.get.ncdf(nc,'time','calendar')$value
  } else if ('TIME' %in% names(nc$var)) {
   time   = get.var.ncdf(nc,'TIME')
   timeu  = nc$var$TIME$units
   timec  = att.get.ncdf(nc,'TIME','calendar')$value
  } else if ('time_counter' %in% names(nc$dim)) {
   time   = nc$dim$time_counter$vals
   timeu  = nc$dim$time_counter$units
   timec  = att.get.ncdf(nc,'time_counter','calendar')$value
  } else if ('time' %in% names(nc$dim)) {
   time   = nc$dim$time$vals
   timeu  = nc$dim$time$units
   timec  = att.get.ncdf(nc,'time','calendar')$value
  } else if ('TIME' %in% names(nc$dim)) {
   time   = nc$dim$TIME$vals
   timeu  = nc$dim$TIME$units
   timec  = att.get.ncdf(nc,'TIME','calendar')$value
  } else {stop('mynt : no time dimension found in the netcdf file')}
  #
  # test time unit in seconds
  if (typeof(timeu)=="character") {
   tmp=strsplit(timeu,split=' ')[[1]]
   if ("days" %in% tmp) {
    time = time*86400
    timeu = sprintf("seconds since %s",timeorigin(timeu))
   } else if ("seconds" %in% tmp) {
    time = time
    timeu = timeu
   } else {warning('mynt : time unit unknown')}
  } else {warning('mynt : time unit unknown')}
  #
  close.ncdf(nc)
  #
  list(values=values,units=units,time=time,timeu=timeu,timec=timec)
} #a.g.
#
# Fonction qui extrait une dimension d'un netcdf et sort une liste
# ================================================================
ncgetdim = function(file,dimname='time'){
  nc = open.ncdf(file)
  #
  values = nc$dim[[dimname]]$vals
  units  = nc$dim[[dimname]]$units
  #
  list(values=values,units=units)
} #a.g.
#
# Fonction qui extrait une variable (time serie) d'un netcdf et sort une liste
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
myntz=function(file,variable='ts',zid='deptht'){
  nc=open.ncdf(file)
  values = get.var.ncdf(nc,nc$var[[variable]])
  units  = nc$var[[variable]]$units
  if ('time_counter' %in% names(nc$var)) {
   time   = get.var.ncdf(nc,'time_counter')
   timeu  = att.get.ncdf(nc,'time_counter','units')$value
   timec  = att.get.ncdf(nc,'time_counter','calendar')$value
  } else if ('time' %in% names(nc$var)) {
   time   = get.var.ncdf(nc,'time')
   timeu  = nc$var$time$units
   timec  = att.get.ncdf(nc,'time','calendar')$value
  } else if ('time_counter' %in% names(nc$dim)) {
   time   = nc$dim$time_counter$vals
   timeu  = nc$dim$time_counter$units
   timec  = att.get.ncdf(nc,'time_counter','calendar')$value
  } else if ('time' %in% names(nc$dim)) {
   time   = nc$dim$time$vals
   timeu  = nc$dim$time$units
   timec  = att.get.ncdf(nc,'time','calendar')$value
  } else {stop('mynt : no time dimension found in the netcdf file')}

  z = get.var.ncdf(nc,nc$var[[zid]])
  zu = nc$var[[zid]]$units
  
  list(values=values,units=units,time=time,timeu=timeu,timec=timec,z=z,zu=zu)
} #a.g.

# Fonction qui extrait une variable (4D) d'un netcdf et sort une liste
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
mynt3D=function(file,variable='soicecov',latid='lat',lonid='lon',period=NULL){
  nc=open.ncdf(file)
  units  = nc$var[[variable]]$units
  if ('time_counter' %in% names(nc$var)) {
   time   = get.var.ncdf(nc,'time_counter')
   timeu  = att.get.ncdf(nc,'time_counter','units')$value
   timec  = att.get.ncdf(nc,'time_counter','calendar')$value
  } else if ('time' %in% names(nc$var)) {
   time   = get.var.ncdf(nc,'time')
   timeu  = nc$var$time$units
   timec  = att.get.ncdf(nc,'time','calendar')$value
  } else if ('time_counter' %in% names(nc$dim)) {
   time   = nc$dim$time_counter$vals
   timeu  = nc$dim$time_counter$units
   timec  = att.get.ncdf(nc,'time_counter','calendar')$value
  } else if ('time' %in% names(nc$dim)) {
   time   = nc$dim$time$vals
   timeu  = nc$dim$time$units
   timec  = att.get.ncdf(nc,'time','calendar')$value
  } else {stop('mynt : no time dimension found in the netcdf file')}
      
  lat    = nc$dim$lat$vals
  latu   = nc$dim$lat$units
  lon    = nc$dim$lon$vals
  lonu   = nc$dim$lon$units

  if (is.null(period)) {
    values = get.var.ncdf(nc,nc$var[[variable]])
  } else {
    indices = selperind(to.date(time,timeu,cal=timec),period[1],period[2])
    startt=indices[1]
    countt=length(indices)-1
    dimvar=nc$var[[variable]]$varsize
    values = get.var.ncdf(nc,nc$var[[variable]],start=c(1,1,startt),count=c(dimvar[1],dimvar[2],countt))
    timenew=time[indices]
    rm(time)
    time=timenew
  }
  list(values=values,units=units,lon=lon, lonu=lonu, lat=lat, latu=latu,
       time=time,timeu=timeu,timec=timec)
} #a.g.


# Fonction qui cree des netcdf (2D)
mync=function(file,dat,var,lon,lon.units,lat,lat.units,time,time.units){
  LON=dim.def.ncdf("lon",lon.units,lon,create_dimvar=TRUE)
  LAT=dim.def.ncdf("lat",lat.units,lat,create_dimvar=TRUE)
  TIME=dim.def.ncdf("time",time.units,time,unlim=TRUE,create_dimvar=TRUE)
  varnc=var.def.ncdf(var,"",list(LON,LAT,TIME),missval=1.e+30)
  ncnew=create.ncdf(file,varnc)
  if (length(dim(dat))==2) dat=array(dat,dim=c(dim(dat),1))
  put.var.ncdf(ncnew,var,dat,start=NA,count=dim(dat))
  close.ncdf(ncnew)
  system(paste("ncatted -a _FillValue,",var,",c,f,1.e+30 ",file,sep=""))
} #j.c.

# Fonction qui cree des netcdf (time serie)
serienc=function(file,datalist,time,time.units,cal='gregorian'){
  TIME=dim.def.ncdf("time",time.units,time,unlim=TRUE,create_dimvar=TRUE)

  Nvar = length(datalist)
  timenc=var.def.ncdf("time_counter","",list(TIME),missval=1.e+30)
  varnc=list(timenc)
  for (var in names(datalist)) {
    varnc = c(varnc,list(var.def.ncdf(var,"",list(TIME),missval=1.e+30)))
  }  
  ncnew=create.ncdf(file,varnc)
  for (var in names(datalist)) {
    if (length(dim(datalist[[var]]))>1) {
      close.ncdf(ncnew)
      stop('Error : serienc is used only for 1D time series!')
    }
    put.var.ncdf(ncnew,var,datalist[[var]],start=NA,count=length(datalist[[var]]))
  }
  put.var.ncdf(ncnew,'time_counter',time,start=NA,count=length(time))
  att.put.ncdf(ncnew,'time_counter','units',time.units)
  att.put.ncdf(ncnew,'time_counter','calendar',timec)
  close.ncdf(ncnew)
  system(paste("ncatted -a _FillValue,",var,",c,f,1.e+30 ",file,sep=""))
} #a.g.



# ================================================================
# Fonctions de manipulation de matrice et arrays
# ================================================================
# Repetition d'une array suivant la dimension
# INPUTS:
#       tab : array a repeter
#       posdim : dimension suivant laquelle on repete l'array tab
#       nrep   : nombre de fois que l'on repete l'array tab
#
# Exemple : tab de dimension (3,5,2)
#      rep.abin(tab,2,3) donnera une array de dimension (3,15,2)
#      avec tabout[,1:5,] == tabout[,6:10,] == tabout[,11:15,] == tab
# ----------------------------------------------------------------
rep.abind=function(tab,posdim,nrep){
  d=dim(tab)[posdim]
  tmp = tab
  for (t in c(1:nrep)){
    tab=abind(tab,tmp,along=posdim)
  }
  tab
} # a.g.
#
#
# Moyenne glissante d'un vecteur
# la moyenne est faite sur l'intervalle glissant de taille thalf*2+1
# ---------------------------------------------------------------
myrunmean=function(data,thalf){ 
 Nt=length(data)
 runmean=array(dim=Nt)
 for (t in seq(Nt)) {
   tav = min(t+thalf,Nt)-max(t-thalf,1)+1
   moyenne = mean(data[max(t-thalf,1):min(t+thalf,Nt)])
   runmean[t]=moyenne
 }
 runmean
} #a.g.

# Ecart-type glissant d'un vecteur
# la moyenne est faite sur l'intervalle glissant de taille thalf*2+1
# ---------------------------------------------------------------
myrunsd=function(data,thalf){ 
 Nt=length(data)
 runsd=array(dim=Nt)
 for (t in seq(Nt)) {
   tav = min(t+thalf,Nt)-max(t-thalf,1)+1
   std = sd(data[max(t-thalf,1):min(t+thalf,Nt)])
   runsd[t]=std
 }
 runsd
} #a.g.


# Normalisation d'une serie temporelle
mynorm=function(x,mean=NULL,sd=NULL){
  if (length(mean)==0) mean=mean(x,na.rm=TRUE)
  if (length(sd)==0) sd=sd(x,na.rm=TRUE)
  (x-mean)/sd
} # j.c.


# norme euclidienne d'un vecteur
mynormeuclid=function(x) sqrt(sum((x)^2)) # a.g.

# distance euclidienne entre deux vecteurs
mydisteuclid=function(x,y) sqrt(sum((x-y)^2)) # a.g.

# distance euclidienne entre deux series temporelles
mydistts=function(x,y) sum(sqrt((x-y)^2)) # a.g.

# biai entre deux series temporelles
mybias=function(x,ref) mean(x-ref) # a.g.

# Find the closest match
# INPUTS:
#       v : valeur
#       tab : vecteur
#
# OUPUTS:
#       $ind : indice de la plus proche valeur de v dans tab
#       $value : plus proche valeur de v dans tab
# ----------------------------------------------------------------
closestval=function(v,tab) {
  ind=which.min(abs(tab-v))
  value=tab[ind]
  list(ind=ind,value=value)
} # a.g.

# ================================================================
# DATES AND TIME
# ================================================================
# Modulo 12 pour les mois
# mymod=function(x,n=12){
#   mm=c()
#   for (i in 1:length(x)){
#     if (x[i]>=1) mm=c(mm,x[i]-n*trunc(x[i]/n))
#     if (x[i]<1)  mm=c(mm,x[i]+n*ceiling((-x[i])/n))
#   }
#   mm
# } # a.g.
mymod=function(x,n=12){
   mm=c()
   for (i in 1:length(x)){
      mm=c(mm,x[i]-n*floor(x[i]/n))
   }
   mm
 } # a.g.


# Nombre de jours du mois m,y
ndays=function(m,y,cal="leap"){
  if (caltype=="360_day") n=rep(30,12)[m]
  else if (cal=="noleap") n=c(31,28,31,30,31,30,31,31,30,31,30,31)[m]
  else n=c(31,28+is.bissex(y,cal),31,30,31,30,31,31,30,31,30,31)[m]
  n
}

# extraction de l'année, mois et jours d'un objet date (construit par as.Date)
# l'entrée doit être une array
# ----------------------------------------------------------------
which_yr = function(date){
  yr = strsplit(as.character(date),'-')[[1]][1]
  yr
}
which_mth = function(date){
  mth = strsplit(as.character(date),'-')[[1]][2]
  mth
}
which_mth2 = function(date){
  print(class(date))
  mth = strsplit(as.character(date),'-')[[1]][2]
  mth
}
which_day = function(date){
  day = strsplit(as.character(date),'-')[[1]][3]
  day
}
which_yr2d=function(tab){
  sapply(tab, which_yr) 
}
# extraction de l'origine des temps du time.units
timeorigin = function(timeu){
  timeo = strsplit(timeu,split=' ')[[1]][3]
  timeo
}

## conversion d'un vecteur temps relatif en date
# (pour un format standard =  nb de secondes since YYYY-MM-DD)
to.date = function(t,timeu,cal='gregorian'){
  tdate = as.PCICt.numeric(t,cal=cal,origin=timeorigin(timeu))
  tdate
}

# Annee y est-elle bissextile..
is.bissex=function(y,caltype="leap"){
  if (caltype %in% c("noleap","360_day")) biss=FALSE
  else  biss=(trunc(y/400)*400==y | (trunc(y/4)*4==y & trunc(y/100)*100!=y))
  biss
} # by J.C.


# selection d'une saison
# ~~~~~~~~~~~~~~~~~~~~~~~
# timedate est un vecteur contenant des dates (Sys.Date)

# selction des indices uniquement
selseasind = function(timedate,season='JFM') {
  timedate = as.character.PCICt(timedate)
  ids_season = which(as.integer(sapply(timedate,which_mth)) %in% list_season[[season]])
  if (season=='DJF') ids_season=ids_season[3:(length(ids_season)-1)] 
  if (season=='DJFM') ids_season=ids_season[4:(length(ids_season)-1)]
  if (season=='NDJFM') ids_season=ids_season[4:(length(ids_season)-2)]
  ids_season
}

# selection de la saison directement dans la serie temporelle
select_season=function(serie,season='MAR') {
  Ndim = length(dim(serie$values))
  timedate = to.date(serie$time,serie$timeu,cal=serie$timec)
  ind_seas = selseasind(timedate,season=season)
  if (Ndim==1 | Ndim==0) {
    serie$values=serie$values[ind_seas]
  } else if (Ndim==3) {
    serie$values=serie$values[,,ind_seas]
  } else {
    stop("ERROR : select_season : wrong dimension of time series")
  }
  serie$time=serie$time[ind_seas]

  if (length(serie$values)==0) {
          serie$values = NA
          serie$time   = NA
      }
  serie
}


# selection d'une periode
# ~~~~~~~~~~~~~~~~~~~~~~~
# timedate est un vecteur contenant des dates (Sys.Date)

# selection des indices uniquement
selperind = function(timedate,yrmin,yrmax) {
  timedate = as.character.PCICt(timedate)
  ids_period = which(as.integer(sapply(timedate,which_yr)) %in% seq(yrmin,yrmax))
  ids_period
}

# selection de la période direct dans le serie temporelle
select_period=function(serie,period=c(1979,2008)) {
  Ndim = length(dim(serie$values))
  if (serie$timec==0) {
   serie$timec='gregorian'
   warning('select_period : no specified calendar for time serie, using default (gregorian)')}

  timedate = to.date(serie$time,serie$timeu,cal=serie$timec)
  ind_period = selperind(timedate,period[1],period[2])
  if (Ndim==1 | Ndim==0) {
    serie$values=serie$values[ind_period]
  } else if (Ndim==2) {
    serie$values=serie$values[,ind_period]
  } else if (Ndim==3) {
    serie$values=serie$values[,,ind_period]
  } else {
      stop("ERROR : select_period : wrong dimension of time serie")
  }
  serie$time=serie$time[ind_period]
  serie
}


# Selction d'un periode ET d'un saison
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# selection des indices uniquement
seltime = function(timedate,yrmin,yrmax,season) {
  timedate = as.character.PCICt(timedate)
  ids_time = which(as.integer(sapply(timedate,which_mth)) %in% list_season[[season]] & as.integer(sapply(timedate,which_yr)) %in% seq(yrmin,yrmax))
  if (season=='DJF') ids_time=ids_time[3:(length(ids_time)-1)] 
  if (season=='DJFM') ids_time=ids_time[4:(length(ids_time)-1)]
  if (season=='NDJFM') ids_time=ids_time[4:(length(ids_time)-2)]
  ids_time
}
# selection de la serie temporelle
select_time=function(serie,period=c(1979,2008),season="ALL") {
  Ndim = length(dim(serie$values))
  if (serie$timec==0) {
   serie$timec='gregorian'
   warning('select_time : no specified calendar for time serie, using default (gregorian)')}

  timedate = to.date(serie$time,serie$timeu,cal=serie$timec)
  ind_time = seltime(timedate,period[1],period[2],season)
  if (Ndim==1 | Ndim==0) {
    serie$values=serie$values[ind_time]
  } else if (Ndim==2) {
    serie$values=serie$values[,ind_time]
  } else if (Ndim==3) {
    serie$values=serie$values[,,ind_time]
  }
  serie$time=serie$time[ind_time]
  serie
}


# serie des moyennes annuelles, qques soit le nb de mois dispos
# longue à tourner, season mean plus rapide, si pas de trou ...
annualmean=function(serie,option='average'){
  Ndim = length(dim(serie$values))
  years = unique(sapply(as.character.PCICt(to.date(serie$time,serie$timeu,cal=serie$timec)),which_yr))
  if (Ndim==1){    
    values  = array(dim=c(length(years)))
  } else if (Ndim==3) {
    values = array(dim=c(dim(serie$values)[1:2],length(years)))
  } else {
    stop("ERROR : annualmean : wrong dimension of the time series")
  }
  timenew = array(dim=c(length(years)))
  
  for (year in years) {
    year = as.integer(year)
    datayr = select_period(serie,c(year,year))
    if (option=='average'){
      if (Ndim==1) {
        values[which(years %in% year)]=mean(datayr$values)
      } else if (Ndim==3) {
        values[,,which(years %in% year)]=apply(datayr$values,c(1,2),mean)
      }
    } else if (option=='sum') {
      if (Ndim==1) {
        values[which(years %in% year)]=sum(datayr$values)
      } else if (Ndim==3) {
        values[,,which(years %in% year)]=apply(datayr$values,c(1,2),sum)
      }
    }
    timenew[which(years %in% year)]=as.double(as.PCICt(paste(year,'-01-01',sep=''),cal=serie$timec))
    #timenew[which(years %in% year)]=as.PCICt.numeric(as.PCICt(paste(year,'-01-01',sep=''),cal=serie$timec),origin=timeorigin(serie$timeu),cal=serie$timec)
  }
  list(values=values,units=serie$units,time=timenew,timeu=timeud,timec=serie$timec)
}

# Moyenne saisonniere :
# doit pouvoir se substituer a annualmean avec season='ALL'
# testee sur ALL, et JFM, marche bien.
seasonalmean=function(serie,season='ALL',option='average') {
  Ndim = length(dim(serie$values))
  years = unique(sapply(as.character.PCICt(to.date(serie$time,serie$timeu,cal=serie$timec)),which_yr))
  if (Ndim==0 | Ndim==1){    
    values  = array(dim=c(length(years)))
  } else if (Ndim==3) { #dim(LON,LAT,TIME)
    values = array(dim=c(dim(serie$values)[1:2],length(years)))
  } else if (Ndim==2) { #dim(Z,TIME)
    values = array(dim=c(dim(serie$values)[1],length(years)))
  } else {
    stop("ERROR : seasonalmean : wrong dimension of the time series")
  }
  timenew = array(dim=c(length(years)))
  
  for (year in years) {
    year = as.integer(year)
    datayr = select_time(serie,season=season,period=c(year,year))
    if (option=='average'){
      if (Ndim==0 | Ndim==1) {
        values[which(years %in% year)]=mean(datayr$values)
      } else if (Ndim==3) {
        values[,,which(years %in% year)]=apply(datayr$values,c(1,2),mean)
      } else if (Ndim==2) {
        values[,which(years %in% year)]=apply(datayr$values,1,mean)
      }
    } else if (option=='sum') {
      if (Ndim==0 | Ndim==1) {
        values[which(years %in% year)]=sum(datayr$values)
      } else if (Ndim==3) {
        values[,,which(years %in% year)]=apply(datayr$values,c(1,2),sum)
      } else if (Ndim==2) {
        values[,which(years %in% year)]=apply(datayr$values,1,sum)
      }
    }
    timenew[which(years %in% year)]=as.double(as.PCICt(paste(year,'-01-01',sep=''),cal=serie$timec))
    #timenew[which(years %in% year)]=as.PCICt.numeric(as.PCICt(paste(year,'-01-01',sep=''),cal=serie$timec),origin=timeorigin(serie$timeu),cal=serie$timec)
  }
  list(values=values,units=serie$units,time=timenew,timeu=timeud,timec=serie$timec)
}
#
# monthly mean
# ============
monthlymean=function(serie,option='average') {
  Ndim = length(dim(serie$values))
  years = unique(sapply(as.character.PCICt(to.date(serie$time,serie$timeu,cal=serie$timec)),which_yr))
  if (Ndim==0 | Ndim==1){    
    values  = array(dim=c(length(years)*12))
  } else if (Ndim==3) { #dim(LON,LAT,TIME)
    values = array(dim=c(dim(serie$values)[1:2],length(years)*12))
  } else if (Ndim==2) { #dim(Z,TIME)
    values = array(dim=c(dim(serie$values)[1],length(years)*12))
  } else {
    stop("ERROR : seasonalmean : wrong dimension of the time series")
  }
  timenew = array(dim=c(length(years)*12))

  indnew = 1
  for (year in years) {
    year = as.integer(year)
    for (mth in seq(12)) {
        datamth = select_time(serie,season=names(list_mth[mth]),period=c(year,year))
        if (option=='average'){
            if (Ndim==0 | Ndim==1) {
                values[indnew]   = mean(datamth$values)
            } else if (Ndim==3) {
                values[,,indnew] = apply(datamth$values,c(1,2),mean)
            } else if (Ndim==2) {
                values[,indnew]  = apply(datamth$values,1,mean)
            }
        } else if (option=='sum') {
            if (Ndim==0 | Ndim==1) {
                values[indnew]   = sum(datamth$values)
            } else if (Ndim==3) {
                values[,,indnew] = apply(datamth$values,c(1,2),sum)
            } else if (Ndim==2) {
                values[,indnew]  = apply(datamth$values,1,sum)
            }
        }
        timenew[indnew]=as.double(as.PCICt(paste(year,'-',mth,'-01',sep=''),cal=serie$timec))
        indnew = indnew + 1
    }
  }
  list(values=values,units=serie$units,time=timenew,timeu=timeud,timec=serie$timec)
}


## # Moyenne saisonnière d'une serie temporelle
## seasonalmean=function(serie,season='ALL') {
##   Ndim = length(dim(serie$values))
##   Nmth = length(list_season[[season]])
##   data.season = select_season(serie,season=season)
##   if (Ndim==1) {
##     tab = matrix(data=serie$values,ncol=length(serie$values)/Nmth)
##     tabt = matrix(data=serie$time,ncol=length(serie$time)/Nmth)
             

##   values = apply(tab,2,mean,na.rm=TRUE)
##   time =  apply(tabt,2,mean,na.rm=TRUE)
##   list(values=values,units=serie$units,time=time,timeu=serie$timeu,timec=serie$timec)
## }

# Cycle saisonnier moyen d'une serie temporelle
seasonalcycle=function(serie) {
  if (serie$timec==0) {
   serie$timec='gregorian'
   warning('seasonalcyle : no specified calendar for time serie, using default (gregorian)')}
  timedate = to.date(serie$time,serie$timeu,cal=serie$timec)
  values=array(dim=12)
  std=array(dim=12)
  i = 1
  for (mth in names(list_mth)) {
    indmth = selseasind(timedate,season=mth)
    tmp = serie$values[indmth]
    values[i] = mean(tmp,na.rm=T)
    std[i] = sd(tmp,na.rm=T)
    i=i+1
  }
  list(values=values,sd=std,units=serie$units)
}

# Detrend d'une serie temporelle
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
mydetrend=function(x,ref=NULL,pval=0.05){
  if (length(ref)==0) ref=1:length(x)
  if (cor.test(x,ref)$p.value<pval) out=x-lm(x~ref)$fitted.values + mean(x)
  else out=x
  out
} #j.c.

# Detrendage d'une serie temporelle sans test de significativité
# si je detrend une matrice, il faut utiliser celle là pour ne pas provoquer un effet seuil du au seuil en significativité dans le champ final
mydetrend2=function(x,ref=NULL,type='linear'){
  if (length(ref)==0) ref=1:length(x)
  if (type=='linear') {
      out=x-lm(x~ref)$fitted.values + mean(x)
  } else if (type=='poly') {
      out = x - lm(x ~ poly(ref,2))$fitted.values + mean(x)
  } else if (type=='cubic') {
      out = x - lm(x ~ poly(ref,3))$fitted.values + mean(x)
  } else {
      print(paste('error in mydetrend2, I don t know the type ',type,sep=''))
  }
  out
} #a.g.

# calcule du trend d'une serie temporelle
mytrendserie=function(x,ref=NULL){
  if (length(ref)==0) ref=1:length(x)
  myfit = lm(x~ref)
  values=myfit$fitted.values
  coef = myfit$coefficient['ref'][[1]]
  pvalue = cor.test(x,ref)$p.value
  varexp=(cor(x,ref))^2
  out = list(values=values, coefficients=coef,pvalue=pvalue,varexp=varexp)
} #a.g.
# 

# Smooth par splines intelligent pour les NAs et possibilite
# de contraindre les df selon longueur de la serie (sdf=)
mysmoothy=function(x,df=NULL,sdf=30){
  if (length(df)==0 & length(sdf)==0) sdf=length(x)
  if (length(df)==0) df=length(x)/sdf
  if (df>1){
    sms=smooth.spline(which(!is.na(x)),na.omit(x),df=df)
    out=predict(sms$fit,1:length(x))$y
  }
  if (df<=1) out=lm(x~c(1:length(x)))$fitted.values
  out
} #j.c.

# calcule du trend lineaire d'une serie temporelle
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
mytrend=function(x){
  ref=1:length(x)
  trend = lm(x~ref)$coefficients[[2]]
  trend
} # a.g.

# anomaly time series
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
anoserie=function(serie,ref=NULL){

    if (is.null(ref)) {
        ref = mean(serie$values)
    } 
    newvalues = serie$values - ref

    list(values = newvalues, time=serie$time, timeu=serie$timeu, timec=serie$timec)
}
# anomaly vector
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
ano=function(x,ref=NULL,na.rm=T){

    if (is.null(ref)) {
        ref = mean(x, na.rm=na.rm)
    } 
    newvalues = x - ref
    
    newvalues
}
# amplitude of a set of values
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
amplitude=function(x){
    a = range(x)[2] - range(x)[1]

    a
}


# ================================================================
# Fonctions graphiques
# ================================================================
palano  = colorRampPalette(c("blue","cyan", "white","yellow", "red"))
palano2 = colorRampPalette(c("black","blue", "cyan", "yellow", "red"))
pal1    = colorRampPalette(c("blue", "cyan", "yellow", "red","purple","brown"))

# Initfig
# ----------------------------------------------------------------
initfig <- function(Nfig=6) {

  if (Nfig==6) {
    par('mar'=c(3.1,3.3, 4.1, 1.5)) #marges
    par(cex.axis=1.2,cex.lab=1.2,cex.main=1.5) # labels
    par(mgp=c(2.2,0.7,0)) # lab pos
  } else {
    print('initfig is not define for this layout')
  }
  
}

initfig2 <- function(fname,Nfig=6) {
  postscript(fname,paper="a4",width=8,height=10,horizontal=F)

  if (Nfig==6) {
    layout(matrix(1:6,3,2,byrow=T))
    par('mar'=c(3.1,3.3, 4.1, 1.5)) #marges
    par(cex.axis=1.2,cex.lab=1.2,cex.main=1.5) # labels
    par(mgp=c(2.2,0.7,0)) # lab pos
  } else if (Nfig==4) {
    layout(matrix(1:4,4,1,byrow=T))
    par('mar'=c(3.1,3.3, 4.1, 1.5)) #marges
    par(cex.axis=1.2,cex.lab=1.2,cex.main=1.5) # labels
    par(mgp=c(2.2,0.7,0)) # lab pos    
  } else if (Nfig==3) {
    layout(matrix(1:3,3,1,byrow=T))
    par('mar'=c(3.1,3.3, 4.1, 1.5)) #marges
    par(cex.axis=1.2,cex.lab=1.2,cex.main=1.5) # labels
    par(mgp=c(2.2,0.7,0)) # lab pos    
  } else {
    print('initfig is not define for this layout')
  }

  # paramètre du plot
  par('lwd' = 2)
  
}

# Plot vide
# ----------------------------------------------------------------
plot0=function(xlim=c(0,1),ylim=c(0,1),xlab="",ylab="",frame.plot=FALSE)
  plot(1,type="n",frame.plot=frame.plot,axes=F,xlim=xlim,ylim=ylim,xlab=xlab,ylab=ylab) # by j.c.
# ----------------------------------------------------------------


# ----------------------------------------------------------------
# Plot avec couleur entre 2 courbes
#
# trans : de 0 (opaque) à 1 (totalement transparent)
# ----------------------------------------------------------------
myfill = function(x,y_high,y_low=NULL,col='pink',border='NA',trans=NULL,device = 'pdf') {
    
  if(is.null(y_low)) {y_low = rep(0,length(y_high))}
  if(is.null(trans)) {trans=0.2 }
  #
  yu = y_high[!is.nan(y_high)]
  yl = y_low[!is.nan(y_high)]
  xx = x[!is.nan(y_high)]
  #
  r = col2rgb(col)[1,1]/255
  g = col2rgb(col)[2,1]/255
  b = col2rgb(col)[3,1]/255
  #
  polygon(c(xx,rev(xx)),c(yu,rev(yl)),col=rgb(r,g,b,trans),border=border)
}
# ----------------------------------------------------------------
# idem but along y axis
# ----------------------------------------------------------------
myfilly = function(x_right,x_left,y,col='pink',border='NA',trans=NULL,device = 'pdf') {
    
  if(is.null(trans)) {trans=0.2 }
  #
  yy = y[!is.nan(x_right)]
  xr = x_right[!is.nan(x_right)]
  xl = x_left[!is.nan(x_right)]
  #
  r = col2rgb(col)[1,1]/255
  g = col2rgb(col)[2,1]/255
  b = col2rgb(col)[3,1]/255
  #
  polygon(c(xl,rev(xr)),c(yy,rev(yy)),col=rgb(r,g,b,trans),border=border)
}
# ---------------------------------------------------------------
# plot d'un cycle saisonnier moyen
# ---------------------------------------------------------------
plotcycle = function(cycle,xlim=NULL,ylim=NULL,xlab="",ylab=NULL,title=NULL,scalef=1,col="black",SD=T,trans=0.8) {
    up = (cycle$values + cycle$sd)*scalef
    do = (cycle$values - cycle$sd)*scalef

    if (is.null(dev.list())) X11(width=8, height=6)
    if (is.null(ylab)) ylab=cycle$units
    if (is.null(ylim)) ylim=range(c(do,up))
    if (is.null(xlim)) xlim=range(tyr)
    if (is.null(title)) title='Seasonal cycle'
    plot(tyr,cycle$values*scalef,type='l',col=col,
         xlim=xlim,ylim=ylim,xlab=xlab,ylab=ylab,
         main=title,
         xaxt='n')
    par(new='TRUE')
    if (SD) {
      myfill(tyr,up,y_low=do,
             col=col,trans=trans)
    }
    axis(side=1,at=tyr,labels=names(list_mth))
}
# ---------------------------------------------------------------
# visualisation d'une matrice
# ---------------------------------------------------------------
mcolor <- function(tab,cmin=NULL,cmax=NULL,xlim=NULL,ylim=NULL,
                   xlab='',ylab='',titre=NULL,breaks=NULL,
                   Nbreaks=20, colorbar=T, blab=NULL,yfsize=0.7,
                   barfsize=0.8,tabcontour=NULL,tabcontour2=NULL,
                   tabcontour3=NULL,lwc1=3,lwc2=3,lwc3=3,
                   colc1='magenta',colc2='black',colc3='blue') {
    if (is.null(cmin)) {cmin=min(tab,na.rm=T)}
    if (is.null(cmax)) {cmax=max(tab,na.rm=T)}
    xlabels = colnames(tab)
    ylabels = rownames(tab)
    #
    if (is.null(xlabels)) {xlabels = c(1:ncol(tab))}
    if (is.null(ylabels)) {ylabels = c(1:nrow(tab))}
    #
    # reverse Y axis :
    reverse = nrow(tab):1
    ylabels = ylabels[reverse]
    tab = tab[reverse,]
    if ( !is.null(tabcontour)){
        tabcontour=tabcontour[reverse,]
    }
    if( !is.null(tabcontour2)){
        tabcontour2=tabcontour2[reverse,]
    }
    if( !is.null(tabcontour3)){
        tabcontour3=tabcontour3[reverse,]
    }
    #
    # color levels and palette
    if (is.null(breaks)) {
        breaks=seq(cmin,cmax,length=Nbreaks)
    }
    #colpal = terrain.colors(length(breaks)-1)
    colpal = topo.colors(length(breaks)-1)
    #colpal[length(colpal)]="tan3"
    
    # drawing map :
#    posgraph=c(0.1,0.77,0.15,0.9)
#    par(plt=posgraph)
    image(1:length(xlabels), 1:length(ylabels), t(tab), xlab=xlab,
          ylab=ylab, axes=FALSE, zlim=c(cmin,cmax), useRaster=TRUE,
          breaks=breaks,col=colpal)
    if ( !is.null(tabcontour)) {
        contour(1:length(xlabels), 1:length(ylabels), t(tabcontour), xlab=xlab,
          ylab=ylab, col=colc1,nlevels=1,drawlabels=F,lwd=lwc1,axes=FALSE,add=T)
    }
    if ( !is.null(tabcontour2)) {
        contour(1:length(xlabels), 1:length(ylabels), t(tabcontour2), xlab=xlab,
          ylab=ylab, col=colc2,nlevels=1,drawlabels=F,lwd=lwc2,axes=FALSE,add=T)
    }
    if ( !is.null(tabcontour3)) {
        contour(1:length(xlabels), 1:length(ylabels), t(tabcontour3), xlab=xlab,
          ylab=ylab, col=colc3,nlevels=1,drawlabels=F,lwd=lwc3,axes=FALSE,add=T)
    }
    if( !is.null(titre) ){
        title(main=titre)
    }
    #
    # the axis
    axis(BELOW<-1, at=1:length(xlabels), labels=xlabels, cex.axis=0.7)
    axis(LEFT <-2, at=1:length(ylabels), labels=ylabels, las= HORIZONTAL<-1,
         cex.axis=yfsize)
    #
    # colorbar
    if (colorbar) {
        if (is.null(blab)) {blab=''}
        posgraph = par("plt")
        posbar = c(posgraph[2]+0.005,posgraph[2]+0.02,posgraph[3],posgraph[4])
#        posbar=c(0.8,0.82,0.15,0.9)
        par(new=T,plt = posbar)
        image(1, breaks,
              matrix(data=breaks, ncol=length(breaks),nrow=1),
              col=colpal,
              xlab="",ylab='',axes=FALSE,
              xaxt="n", useRaster=TRUE)
        #axis(RIGHT <-4, at=breaks, labels=breaks, las= HORIZONTAL<-1,
        axis(RIGHT <- 4,las=1,ylab=ylab,
             cex.axis=barfsize)
        par(plt=posgraph)
    }
    
    
}

# ---------------------------------------------------------------
# plot double axe y
# ---------------------------------------------------------------
#plotyy <- function(xr,yr,xl,yl,xlim=NULL,yliml=NULL,ylimr=NULL,
#                   coll=NULL,colr=NULL,xlab=NULL,ylabl=NULL,ylabr=NULL,
#                   type=NULL) {
#    plot(xl,yl,
#     xlim=xlim,ylim=yliml,yaxt="n",xlab=xlab,ylab=ylabl,
#      type='b',lwd=lwd,pch=4,col='blue',
#     main='W')
#par(new=T)
#x <- 1:5
#y1 <- rnorm(5)
#y2 <- rnorm(5,20)
#par(mar=c(5,4,4,5)+.1)
#plot(x,y1,type="l",col="red")
#par(new=TRUE)
#plot(x, y2,,type="l",col="blue",xaxt="n",yaxt="n",xlab="",ylab="")
#axis(4)
#mtext("y2",side=4,line=3)
#legend("topleft",col=c("red","blue"),lty=1,legend=c("y1","y2"))


#}
#
# ---------------------------------------------------------------
# plot une serie temporelle qque
# ---------------------------------------------------------------
plotserie <-  function(serie,trend=F,stat=F,scalef=1,type='l',lty=1,lwd=2,help=F,title='',xlab ='Time',ylab=NULL,xlimits=NULL,ylimits=NULL,period=NULL,serie2=NULL) {
  if (help) {
    print("Plot a time series")
    print("usage : plotserie(serie)")
    stop("Help mode")
  }
  #
  serie$values = serie$values*scalef
  if (!is.null(period)) serie = select_time(serie,period=period)  
  axt = to.date(serie$time,serie$timeu,cal=serie$timec)

  if (!is.null(serie2)) {
    serie2$values = serie2$values*scalef
    if (!is.null(period)) serie2 = select_time(serie2,period=period)  
  }
  
  # Trend :
  if (trend) {
    tendance = mytrendserie(serie$values)
    tendancetx = formatC(tendance$coef,digits=3,width=6)
    varexptx   = formatC(tendance$varexp, digits=3,width=6)
    infotendance = paste('Linear Trend =',tendancetx,'/time unit')
    infovarexp = paste('Explained variance =',varexptx)
  }
  # Stat :
  if (stat) {
    moy = mean(serie$values)
    sig = sd(serie$values)
  }

  if (is.null(xlimits)) xlimits=range(axt)
  if (is.null(ylimits)) ylimits=range(serie$values)
  if (is.null(ylab)) ylab=serie$units

  plot(axt,serie$values,
       type=type,lty=lty,lwd=lwd,col=mycolors[1],
       xlim=xlimits,ylim=ylimits,
       xlab=xlab,ylab=ylab,main=titre)

  if (! is.null(serie2)) {
    par(new=T)
    plot(axt,serie2$values,
         type=type,lty=lty,lwd=lwd,col=mycolors[2],
         xlim=xlimits,ylim=ylimits,
         xlab=xlab,ylab=ylab,main=titre)   
  }
  
  if (trend) {
    par(new=T)
    plot(axt,tendance$values,
         type=type,lty=2,lwd=lwd,col=mycolors[1],
         xlim=xlimits,ylim=ylimits,
         xlab='',ylab='',main='')
    par(new=T)
    textplot(infotendance,xlim=xlimits,ylim=ylimits,
             col=mycolors[1],distmargin=1)
    textplot(infovarexp,xlim=xlimits,ylim=ylimits,
             col=mycolors[1],distmarginx=1,distmarginy=2)
  }
  if (stat) {
    par(new=T)
    plot(axt,rep(moy,length(axt)),
         type=type,lty=1,lwd=1,col=mycolors[1],
         xlim=xlimits,ylim=ylimits,
         xlab='',ylab='',main='')
    par(new=T)
    plot(axt,rep(moy+sig,length(axt)),
         type=type,lty=2,lwd=0.5,col=mycolors[1],
         xlim=xlimits,ylim=ylimits,
         xlab='',ylab='',main='')
    par(new=T)
    plot(axt,rep(moy-sig,length(axt)),
         type=type,lty=2,lwd=0.5,col=mycolors[1],
         xlim=xlimits,ylim=ylimits,
         xlab='',ylab='',main='')
    par(new=T)
    plot(axt,rep(moy+2*sig,length(axt)),
         type=type,lty=3,lwd=0.5,col=mycolors[1],
         xlim=xlimits,ylim=ylimits,
         xlab='',ylab='',main='')
    par(new=T)
    plot(axt,rep(moy-2*sig,length(axt)),
         type=type,lty=3,lwd=0.5,col=mycolors[1],
         xlim=xlimits,ylim=ylimits,
         xlab='',ylab='',main='')
   
    
  }


}

# ----------------------------------------------------------------
# plot de 2 series temporelles avec caclule et affichage de la corrélation
# ----------------------------------------------------------------
plotcor = function(serie1,serie2,serieu,name1,name2,ylimits=NULL,fout='plotcor_out.eps',scalef=1,lwd=2,cex=1.1,cex.main=1.2){
  #
  serie1=serie1*scalef
  serie2=serie2*scalef
    
  # paramètres des plots
  tdate=to.date(serie1$time,serie1$timeu,cal=serie1$timec)
  xlimits=range(to.date)
  if (is.null(ylimits)) {
    ylimits=range(c(serie1,serie2))
  }
  dy = (ylimits[2]-ylimits[1])/10

  #regression de serie1 sur serie2 et serie2 sur serie1
  lm.serie1=lm(serie1$values ~ serie2$values,na.action=na.omit)
  lm.serie2=lm(serie2$values ~ serie1$values,na.action=na.omit)

  #corrélation
  r=cor(serie1$values,serie2$values)
    
  #postscript(fout,width=550,height=300)
  # serie temporelle
  # ~~~~~~~~~~~~~~~~~
  par(mfrow = c(2,1))
  plot(tdate,serie1$values,type='l',col="blue",
       xlim=xlimits,ylim=ylimits,ylab=serie1$units,xlab='Time',
       main='Time series',lwd=lwd,cex.main=cex.main)
  par(new='TRUE')
  plot(tdate,serie2$values,type='l',col="red",
       xlim=xlimits,ylim=ylimits,ylab=serie2$units,xlab='Time',
       lwd=lwd,cex.main=cex.main)
  legend(xlimits[1],ylimits[1]+2*dy,list(name1,name2),col=c("blue","red"),lty=rep(1,2),,lwd=rep(lwd,2),bty='n',horiz=TRUE,cex=cex)

  # nuage et corrélation
  # ~~~~~~~~~~~~~~~~~~~~~
  plot(serie1$values,serie2$values,
       xlim=ylimits,ylim=ylimits,
       type='p',pch=16,col="grey34",
       xlab=name1,ylab=name2,main='Linear regressions',cex.main=cex.main)
  par(new='TRUE')
  plot(lm.serie1$fitted.value,serie2$values,
       xlim=ylimits,ylim=ylimits,type='l',lty=1,col="blue",
       xlab=name1,ylab=name2,cex.main=cex.main)
  par(new='TRUE')
  plot(serie1$values,lm.serie2$fitted.values,
       xlim=ylimits,ylim=ylimits,type='l',lty=2,col="red",
       xlab=name1,ylab=name2,cex.main=cex.main)
  legend(ylimits[1],ylimits[1]+9.5*dy,list(paste(name1,'on',name2),paste(name2,'on',name1)),col=c("blue","red"),lty=rep(1,2),bty='n',cex=cex)
  text(ylimits[2]-2*dy,ylimits[1]+2*dy,paste('r =',as.character(r)),cex=cex)


}
# ----------------------------------------------------------------
# Imagesc perso
# ----------------------------------------------------------------
imagesc = function(tab,clim=NULL,xlab='x',ylab='y',colors=topo.colors(50),
    xaxt=NULL,yaxt=NULL) {

  if(is.null(clim)){
    cmin = min(tab,na.rm=T)
    cmax = max(tab,na.rm=T)
    clim = c(cmin,cmax)
  } else {
    cmin = min(clim)
    cmax = max(clim)
  }
  defscreen=matrix(c(0.01,0.005,0.99,0.99,0.2,0.01,0.99,0.3),nrow=2)
  split.screen(defscreen)

  screen(1)
  image(seq(dim(tab)[2]),seq(dim(tab)[1]),t(tab),
        xlab=xlab,ylab=ylab,zlim=clim,col=colors,
        xaxt=xaxt,yaxt=yaxt)
  
  # colorbar
  # ~~~~~~~~
  screen(2)
  contours = seq(cmin,cmax,(cmax-cmin)/10)
  image(contours,1,array(contours,dim=c(length(contours),1)),col=colors,yaxt="n",ylab="")
}
#
# ----------------------------------------------------------------
# Nice hovmoeller for ORCA12, 75levels
# ----------------------------------------------------------------
hov75l = function(tab,clim=NULL,xlab='Time',ylab='level',colors=topo.colors(50),
    xaxt=NULL,yaxt=NULL,timeaxis=NULL,yaxis=NULL,yticks=NULL,
    linex=NULL,liney=NULL,
    l75=T) {
  #
  # l75 = T option pour tracer joliment les hovmoeller sur une grille ORCA à 75 niveaux verticaux
  #
  if (l75) {
    if (dim(tab)[1] != 75) {
      stop("hov75l error : dim(tab) should have 75 levels as first dim \n
            Try setting l75 option to FALSE")
    }
    # Reverse pour avoir les plus grande profondeur vers le bas.
    tabplot = t(tab)[,75:1]
    options(warn=-1)
    zz = get.lev()
    options(warn=1)
  } else {
    tabplot=t(tab)
  }
  #
  # Axes for plotting
  # -----------------
  if (is.null(timeaxis)) {timeaxis=seq(dim(tab)[2])}
  Ny = dim(tab)[1]
  if (is.null(yaxis)) {
    yplot = seq(Ny)
  } else { yplot=yaxis }
  #
  # plot limit
  # ----------
  if(is.null(clim)){
    cmin = min(tab,na.rm=T)
    cmax = max(tab,na.rm=T)
    clim = c(cmin,cmax)
  } else {
    cmin = min(clim)
    cmax = max(clim)
  }
  #
  # PLOT
  # ====
  # split the screen for colorbar
  defscreen=matrix(c(0.01,0.005,0.99,0.99,0.2,0.01,0.99,0.3),nrow=2)
  split.screen(defscreen)
  #
  # Hovmoeller
  screen(1)
  options(warn=-1)
  par(mar=c(3,2.4,4,3), mgp=c(1.5, 0.5, 0),cex.axis=0.9)
  image(timeaxis,yplot,tabplot,
        xlab=xlab,ylab=ylab,zlim=clim,col=colors,
        xaxt=xaxt,yaxt='n')
  options(warn=1)
  #
  # y axes
  if (l75) {
    axis(2,seq(1,75,by=5),label=rev(seq(75))[seq(1,75,by=5)],las=1) #las=1 --> ylabels horizontal
    axis(4,seq(1,75,by=5),label=rev(round(zz$values))[seq(1,75,by=5)],las=1)
  } else {
    if (is.null(yticks)) {yplot[seq(from=1,by=round(Ny/10),to=Ny)]}
    axis(2,round(yticks),las=1) #las=1 --> ylabels horizontal
    axis(4,round(yticks),las=1)    
  }
  if (!is.null(linex)) {
      for (xi in linex) {
          abline(v=xi)
          text(xi, Ny, as.character(xi), pos=3,xpd=TRUE)
      }
  }
  if (!is.null(liney)) {
    for (yi in liney) {
      if (l75) {
        abline(h=75-yi+1)
      text(min(timeaxis), 75-yi+1, as.character(yi), pos=3,xpd=TRUE,cex=0.7)
      } else {
        abline(h=yi)
        text(min(timeaxis), yi, as.character(yi), pos=3,xpd=TRUE,cex=0.7)
      }
    }
  }
  
  # colorbar
  # ~~~~~~~~
  screen(2)
  contours = seq(cmin,cmax,(cmax-cmin)/10)
  image(contours,1,array(contours,dim=c(length(contours),1)),col=colors,yaxt="n",ylab="")
}
#
# ----------------------------------------------------------------
# Nice hovmoeller for ORCA12, 75levels
# ----------------------------------------------------------------
hov75l_old= function(tab,clim=NULL,xlab='Time',ylab='level',colors=topo.colors(50),
    xaxt=NULL,yaxt=NULL,timeaxis=NULL,
    linex=NULL,liney=NULL,
    l75=T) {
  #
  # l75 = T option pour tracer joliment les hovmoeller sur une grille ORCA à 75 niveaux verticaux
  #
  # test qu'il y a ai 75 niveaux sino, stop
  if (dim(tab)[1] != 75) {stop("hov75l error : dim(tab) should have 75 levels as first dim")}
  #
  # Reverse pour avoir les plus grande profondeur vers le bas.
  if (l75) {
    tabplot = t(tab)[,75:1]
  }
  options(warn=-1)
  zz = get.lev()
  options(warn=1)
  if (is.null(timeaxis)) {timeaxis=seq(dim(tab)[2])}
  #
  # plot limit
  if(is.null(clim)){
    cmin = min(tab,na.rm=T)
    cmax = max(tab,na.rm=T)
    clim = c(cmin,cmax)
  } else {
    cmin = min(clim)
    cmax = max(clim)
  }
  #
  # split the screen for colorbar
  defscreen=matrix(c(0.01,0.005,0.99,0.99,0.2,0.01,0.99,0.3),nrow=2)
  split.screen(defscreen)

  #
  # Hovmoeller
  screen(1)
  options(warn=-1)
  par(mar=c(3,2.4,4,3), mgp=c(1.5, 0.5, 0),cex.axis=0.9)
  image(timeaxis,seq(75),tabplot,
        xlab=xlab,ylab=ylab,zlim=clim,col=colors,
        xaxt=xaxt,yaxt='n')
  options(warn=1)
  axis(2,seq(1,75,by=5),label=rev(seq(75))[seq(1,75,by=5)],las=1) #las=1 --> ylabels horizontal
  axis(4,seq(1,75,by=5),label=rev(round(zz$values))[seq(1,75,by=5)],las=1)
  if (!is.null(linex)) {
      for (xi in linex) {
          abline(v=xi)
          text(xi, 75, as.character(xi), pos=3,xpd=TRUE)
      }
  }
  if (!is.null(liney)) {
      for (yi in liney) {
          abline(h=75-yi+1)
          text(min(timeaxis), 75-yi+1, as.character(yi), pos=3,xpd=TRUE,cex=0.7)
      }
  }
  
  # colorbar
  # ~~~~~~~~
  screen(2)
  contours = seq(cmin,cmax,(cmax-cmin)/10)
  image(contours,1,array(contours,dim=c(length(contours),1)),col=colors,yaxt="n",ylab="")
}
#

# --------------------------------------------------------------------------
# Plot type histos (polygones) autour d'un moyenne
# se fait dans une fenetre deja existante
# --------------------------------------------------------------------------
# INPUTS:
#        y
# --------------------------------------------------------------------------
mybarplot=function(y,at=NULL,y0=0,width=1,pch=NULL,pbg=7,col=c("red","blue"),border=NULL,fill=NULL,lty=1,lwd=1,plot.ci=FALSE,ci.u=NULL,ci.l=NULL,ci.lty=1,ci.lwd=1,yaxis=FALSE,ylab="",y0line=TRUE,col.levs=NULL,col.vals=y-y0,add=FALSE){
  # Gestion arguments entree
  if (plot.ci & (length(ci.u)!=length(y) | length(ci.l)!=length(y)))
    {print("Error specifying CI"); stop()}
  if (length(at)==0) at=1:length(y)
  if (length(width)==1) width=rep(width,length(y))
  if (length(pch)==1) pch=rep(pch,length(y))
  if (length(col)==1) cls=rep(col,length(y))
  if (length(col)==2) cls=col[1.5-0.5*sign(y-y0)]
  if (col==c("red","blue") && length(col.levs)>0){
    lcl=length(col.levs); csq=seq(1,0,-1/lcl); myred=rgb(1,csq,csq); myblue=rgb(csq,csq,1)
    cls=c(); for (i in 1:length(y)){
      ic=which(sort(c(abs(col.vals[i]),col.levs))==abs(col.vals[i]))
      cls=c(cls,cbind(myred,myblue)[ic,1.5-0.5*sign(y[i]-y0)])
    }
  }
  # Plot
  xlim=range(at)+c(-1,1)*mean(width); ylim=range(c(y0,y,ci.u,ci.l))
  if (!add) plot0(xlim=xlim,ylim=ylim,ylab=ylab)
  for (i in 1:length(y)){
    xi=at[i]+c(-0.5,0.5,0.5,-0.5)*width[i]; yi=c(y0,y0,y[i],y[i])
    polygon(xi,yi,col=cls[i],border=border,density=fill[i],lty=lty,lwd=lwd)
    if (plot.ci){
      xi=at[i]+c(-0.25,0.25)*width[i]
      segments(at[i],ci.l[i],at[i],ci.u[i],lty=ci.lty,lwd=ci.lwd)
      segments(xi[1],ci.l[i],xi[2],ci.l[i],lty=ci.lty,lwd=ci.lwd)
      segments(xi[1],ci.u[i],xi[2],ci.u[i],lty=ci.lty,lwd=ci.lwd)
    }
    if (length(pch)>0) points(at[i],y[i],pch=pch[i],bg=pbg)
   }
   if (yaxis) axis(2)
   if (y0line) lines(xlim,rep(y0,2),lty=1)
} # j.c.

# -----------------------------------------------------------------------
#  Rajout de text sur la figure
# -----------------------------------------------------------------------
textplot=function(txt,xlim,ylim,position='upright',distmargin=2,col=NULL,cex=1,distmarginx=NULL,distmarginy=NULL){
  dx = (xlim[2]-xlim[1])/10
  dy = (ylim[2]-ylim[1])/10

  if (is.null(distmarginx)) distmarginx=distmargin
  if (is.null(distmarginy)) distmarginy=distmargin
 
  
  if (position=='upright') {
    x = xlim[2]-distmarginx*dx
    y = ylim[2]-distmarginy*dy
  } else if (position=='upleft') {
    x = xlim[1]+distmarginx*dx
    y = ylim[2]-distmarginy*dy
  } else if (position=='bottomright') {
    x = xlim[2]-distmarginx*dx
    y = ylim[1]+distmarginy*dy
  } else if (position=='bottomleft') {
    x = xlim[1]+distmarginx*dx
    y = ylim[1]+distmarginy*dy
  }

  text(x,y,txt,col=col)
}

# ================================================================
# Fonctions utile pour script
# ================================================================
    

