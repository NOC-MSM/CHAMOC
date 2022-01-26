# -*-coding:Latin-1-*
# =========================================================================
# Packages de fonctions utilse à l'analyse de données climatiques
#
# --------------------------
# Author : A. Germe
# moving : after 8 May. 2014
# version 3 (en cours d'évolution)
# ---------------------------
# La version 2 figée est celle utilisant le module MA pour les masked_array
# Dans cette nouvelle version on est passé au module numpy.ma 
# Ce module semble avoir plus de possibilité et être plus utilisé dans la
# communauté.
# J'ai vérifié la compatibilité des modules en recalculant le diag AMOindex
# sur l'expérience OWN3DT256A avec cette nouvelle version de climtools.
# Les séries temporelles entre vielle et nouvelle version sont identiques.
# =========================================================================
import sys, os
import netCDF4 as nc
import datetime
#
import numpy.ma as ma
import numpy as N
from scipy import stats as S
#
from direxp import *
from myaxes import *
# =========================================================================
dseason = dict(JJA=range(6,9), DJF=[12,1,2], FMA=range(2,5), MAM=range(3,6),\
                 SON=range(9,12), JFM=[1,2,3], AMJ=range(4,7), JAS=range(7,10),\
                 OND=range(10,13),JAN=[1], FEB=[2], MAR=[3], APR=[4], MAY=[5],\
                 JUN=[6], JUL=[7], AUG=[8], \
                 SEP=[9], OCT=[10], NOV=[11], DEC=[12], ALL=range(1,13),\
                 JJAS=range(6,10), DJFM=[12,1,2,3], MJ=[5,6])
# =========================================================================
def nclist(filein) :
  """ List le contenu dans un netcdf et le place dans un dictionnaire
  """
  try :
    f = nc.Dataset(filein)
  except :
    """Couldn't find the file %s"""%(filein)
  listvar = f.variables.keys()
  contenu={}
  for varid in listvar :
    myvar = f.variables[varid]
    contenu[varid] = {test:myvar.units, shape: myvar.shape} 
  #
  return contenu
# =========================================================================
def read(filein,varname,years=None) :
  """ tab, timeval, timeu, timecal = read(filein,varname, years=None)
      Fonction de lecture de netcdf
  """
  try :
    f=nc.Dataset(filein)
  except :
    """Couldn't find the file %s"""%(filein)
  timevar = f.variables['time_counter']
  #
  if years is not None :
    tdeb = datetime.datetime(years[0],1,1) # 1er Jan de la 1ere année
    tfin = datetime.datetime(years[-1],12,31,23,59,59) #31/12 de la dernière année
    ideb = nc.date2index(tdeb,timevar,calendar=timevar.calendar,select='after')
    ifin = nc.date2index(tfin,timevar,calendar=timevar.calendar,select='before')
    timeval = timevar[ideb:ifin+1]
    tab = f.variables[varname][ideb:ifin+1,:,:]
  else :
    tab = f.variables[varname][:,:,:]
    timeval=timevar[:]
  #  
  timedates=nc.num2date(timeval,timevar.units,calendar=timevar.calendar)
  timex = timeaxis(timedates,units=timevar.units,calendar=timevar.calendar)
  f.close()
  tab = tab.astype(N.float64) # evite des warning d'overflow
  return tab, timex
# ----------------------------------------------------------------------
def readfield(filein,varname,years=None) :
  """ tab,timex, lon, lat = readfield(dirin,fieldin,varname,years=None)
      Lecture de la variable varname, fichier filein dans repertoire dirin.
      PossibilitÃ© deseelctionner une sous periode.
  """
  try :
    f=nc.Dataset(filein)
  except :
    """Couldn't find the file %s"""%(filein)
  timevar = f.variables['time_counter']
  if 'nav_lon' in f.variables.keys() : 
    lonvar = f.variables['nav_lon']
    latvar = f.variables['nav_lat']
  else :
    lonvar = f.variables['longitude']
    latvar = f.variables['latitude']
    #
  #
  if years is not None :
    tdeb = datetime.datetime(years[0],1,1) # 1er Jan de la 1ere année
    tfin = datetime.datetime(years[-1],12,31) #31/12 de la dernière année
    ideb = nc.date2index(tdeb,timevar,calendar=timevar.calendar,select='after')
    ifin = nc.date2index(tfin,timevar,calendar=timevar.calendar,select='before')
    timeval = timevar[ideb:ifin+1]
    tab = f.variables[varname][ideb:ifin+1,:,:]
  else :
    tab = f.variables[varname][:,:,:]
    timeval=timevar[:]
  #  
  # axis
  timedates=nc.num2date(timeval,timevar.units,calendar=timevar.calendar)
  if 'time_origin' not in dir(timevar) : 
    time_origin=None
  else :
    time_origin=timevar.time_origin
  #
  timex = timeaxis(timedates,units=timevar.units,calendar=timevar.calendar,origin=time_origin)
  lon = axis(lonvar[...],units=lonvar.units,id='longitude')
  lat = axis(latvar[...],units=latvar.units,id='longitude')
  f.close()
  return tab, timex, lon, lat
# =========================================================================
# Moyenne et clim
# =========================================================================
def climato(tab,timex,freq='MO') :
  """ tabmoy,tabstd = climato(tab,timex, freq='MO')
      
      INPUTS :
         tab = (t,...) array
         timex = timeaxis
         freq = 'MO' for monthly , or 'DA' for daily
  """
  # MAIN
  if freq=='MO' : 
    newshape=(12,)+tab.shape[1:]
  elif freq=='DA' :
    newshape=(365,)+tab.shape[1:]
  elif freq=='YE' :
    newshape=tab.shape[1:]
  else :
    print "unknown frequency in the function climato in the package climtools"
  #
  #
  clim = N.empty(newshape)
  sd = N.empty(newshape)
  #
  #
  if freq=='MO' :
    for mth in range(1,13) :
      tmp = tab[timex.month()==mth,...]
      clim[mth-1,...] = tmp.mean(axis=0)
      sd[mth-1,...] = tmp.std(axis=0)
  elif freq=='DA' :
    for day in range(1,366) :
      tmp = tab[timex.day()==day,...]
      clim[day-1,...] = tmp.mean(axis=0)
      sd[day-1,...] = tmp.std(axis=0)
  elif freq=='YE' :
    clim=tab.mean(axis=0)
    sd = tab.std(axis=0)
  #
  #
  return clim, sd
# =========================================================================
def clim2d(expid,varname,period=None,mod='I') :
    """clim2d(expid,varname,period=None,mod='I')
    """
    exp = dexp[expid]
    if period is None : period=exp.year
    # INPUTS :
    tab,tax,lon,lat = readfield(exp.locfile(varname,realm=mod),varname,years=period)
    # OUTDIR :
    climout='/net/cratos/usr/cratos/varclim/agglod/mydiags/OUTPUTS/'
    if mod is 'I' : ssrep='SeaIce/clim2d'
    if mod is 'A' : ssrep='Atmo/clim2d'
    if mod is 'O' : ssrep='Ocean/clim2d'
    try :
        climout = climout+ssrep
    except :
        print """There is no realm %s for the expe %S"""%(mod,expid)
    if exp.ismember :
        dirout = '%s/%s/%s/%s/'%(climout,exp.stream,exp.group,exp.ensemblename)
    else :
        dirout = '%s/%s/%s/'%(climout,exp.stream,exp.group)

    if not os.path.exists(dirout) : os.makedirs(dirout)
    fileout = '%s%s_clim2d_%s_%i-%i.nc'%(dirout,expid,varname,period[0],period[-1])
    print """OUTPUTS will be placed in %s"""%(fileout)

    # MAIN
    newshape=(12,)+tab.shape[1:]
    clim = N.empty(newshape)
    sd = N.empty(newshape)
    #
    for mth in range(1,13) :
        tmp = tab[tax.month()==mth,...]
        clim[mth-1,...] = tmp.mean(axis=0)
        sd[mth-1,...] = tmp.std(axis=0)
    #
    #
    # WRITE NETCDF
    fileo = nc.Dataset(fileout,'w')
    fileo.date = str(datetime.date.today())
    fileo.author = 'A. Germe'
    fileo.code = 'climtools/clim2d'
    fileo.period = '%i-%i'%period
    fileo.description = 'Climatology of %s for the experience %s'%(varname,expid)
    i = fileo.createDimension('i',tab.shape[1])
    j = fileo.createDimension('j',tab.shape[2])
    t = fileo.createDimension('time_counter',12)
    climnc = fileo.createVariable('clim_%s'%varname,'f',('time_counter','i','j'))
    sdnc = fileo.createVariable('std_%s'%varname,'f',('time_counter','i','j'))
    lonnc = fileo.createVariable('longitude','f',('i','j'))
    latnc = fileo.createVariable('latitude','f',('i','j'))
    time = fileo.createVariable('time_counter','f',('time_counter',))
    lonnc.units=lon.units
    latnc.units=lat.units
    time.units='days since 0001-01-01'
    time.calendar='noleap'
    #
    latnc[...]=lat.values
    lonnc[...]=lon.values
    climnc[...]=clim
    sdnc[...]=sd
    time[:]=range(1,360,30)
    #
    fileo.close()
# --------------------------------------------------------------------------
def clim2dsit(expid,period=None) :
    mod = 'I'
    exp = dexp[expid]
    if period is None : period=exp.year
    # INPUTS :
    sit,tax,lon,lat = readfield(exp.locfile('iicethic',realm=mod),'iicethic',years=period)
    sic,tax2,lon2,lat2 = readfield(exp.locfile('soicecov',realm=mod),'soicecov',years=period)
    tab = N.multiply(sit,sic)
    # OUTDIR :
    climout='/net/cratos/usr/cratos/varclim/agglod/mydiags/OUTPUTS/SeaIce/clim2d'
    if exp.ismember :
        dirout = '%s/%s/%s/%s/'%(climout,exp.stream,exp.group,exp.ensemblename)
    else :
        dirout = '%s/%s/%s/'%(climout,exp.stream,exp.group)

    if not os.path.exists(dirout) : os.makedirs(dirout)
    fileout = '%s%s_clim2d_sit_%i-%i.nc'%(dirout,expid,period[0],period[1])
    print """OUTPUTS will be placed in %s"""%(fileout)
    # MAIN
    newshape=(12,)+tab.shape[1:]
    clim = N.empty(newshape)
    sd = N.empty(newshape)
    #
    for mth in range(1,13) :
        tmp = tab[tax.month()==mth,...]
        clim[mth-1,...] = tmp.mean(axis=0)
        sd[mth-1,...] = tmp.std(axis=0)
    #
    #
    # WRITE NETCDF
    fileo = nc.Dataset(fileout,'w')
    fileo.date = str(datetime.date.today())
    fileo.author = 'A. Germe'
    fileo.code = 'climtools/clim2dsit'
    fileo.period = '%i-%i'%period
    fileo.description = 'Climatology of sea ice thickness (sit- for the experience %s. SIT is sea ice thickness per unit of grid cell area'%(expid)
    i = fileo.createDimension('i',tab.shape[1])
    j = fileo.createDimension('j',tab.shape[2])
    t = fileo.createDimension('time_counter',12)
    climnc = fileo.createVariable('clim_sit','f',('time_counter','i','j'))
    sdnc = fileo.createVariable('std_sit','f',('time_counter','i','j'))
    lonnc = fileo.createVariable('longitude','f',('i','j'))
    latnc = fileo.createVariable('latitude','f',('i','j'))
    time = fileo.createVariable('time_counter','f',('time_counter',))
    lonnc.units=lon.units
    latnc.units=lat.units
    time.units='days since 0001-01-01'
    time.calendar='noleap'
    #
    latnc[...]=lat.values
    lonnc[...]=lon.values
    climnc[...]=clim
    sdnc[...]=sd
    time[:]=range(1,360,30)
    #
    fileo.close()
# =========================================================================
#                Masque et moyenne
# =========================================================================
def get_mask(domain,grid='ORCA2') :
  if grid is 'ORCA2':
    fgrid='/net/argos/data/parvati/agglod/DATA/IPSLCM/Mask_ORCA2.nc'
  if grid is 'ORCA2IPSL':
    fgrid='/net/argos/data/parvati/agglod/DATA/IPSLCM/otherMASK/Mask_ORCA2_MIZipsl.nc'
  try :
    f = nc.Dataset(fgrid)
  except :
    print """Couldn't find de file : %s"""%(fgrid)
  #
  rmask = f.variables[domain][:,:,:]
  f.close()
  return rmask
# -----------------------------------------------------------------------
def myweights(grid='ORCA2') :
  """ myweights(grid='ORCA2')
      Charge les poids correspondant à la grille grid.
  """
  if grid is 'ORCA2' :
    fgrid='/net/cratos/usr/cratos/varclim/IPSLCM5A/PROD/piControl2/OCE/piControl2_mesh_mask.nc'
  else :
    print """I don't know this grid : %s"""%(grid)
  #
  try :
    f = nc.Dataset(fgrid)
  except :
    print """Couldn't find the file : %s """%(fgrid)
  #
  e1t = f.variables['e1t'][0,:,:]
  e2t = f.variables['e2t'][0,:,:]
  f.close()
  #
  wt = e1t*e2t
  # traite le recouvrement sur les pôles, attention, à adapter si
  # on n'utilise pas une grille de type ORCA
  wt[0,:]  = 0.
  wt[-1,:] = 0.
  wt[:,0]  = 0.
  wt[:,-1] = 0.
  return wt
# 
# -----------------------------------------------------------------------
def regional_average(tab,domain,operation='sum',gridname='ORCA2'):
  """
  regional_average(tab,domain,operation='sum',gridname='ORCA2')

  Calcule la moyenne ou l'integrale regional d'un champs.
  Moyenne ou somme sont ponderee par la surface de la maille.
  peut également être utilisee pour determiner la valeur max ou min dans un domaine spatial, avec operation='min' et operation='max'. 
Attention, pour operation = 'min' et 'max', il n'y a pas de pondération par la surface de la maille.
  """
  wt = myweights(grid=gridname)
  if len(tab.shape)==3:
    dt=tab.shape[0]
    wt = ma.repeat( ma.reshape(wt, (1,)+wt.shape), dt, axis=0)
  if len(tab.shape)==4 :
    dt=tab.shape[0]
    dz=tab.shape[1]
    wt = ma.repeat( ma.reshape(wt, (1,)+wt.shape), dz, axis=0)
    wt = ma.repeat( ma.reshape(wt, (1,)+wt.shape), dt, axis=0)
  #
  region_mask = get_mask(domain,grid=gridname)[0]
  if len(tab.shape)==3:
    region_mask=ma.repeat( ma.reshape(region_mask, (1,)+region_mask.shape), dt, axis=0)
  if len(tab.shape)==4 :
    #print('taking into account the mask in 3d')
    region_mask = get_mask(domain,grid=gridname)
    region_mask=ma.repeat( ma.reshape(region_mask, (1,)+region_mask.shape), dt, axis=0) 
  #
  tab = ma.masked_where(region_mask==0.,tab)
  wtmsk = ma.masked_where(region_mask==0.,wt)
  tmp = tab*wtmsk
  if operation is 'sum' :
    moyenne = ma.sum(tmp,axis=(len(tmp.shape)-1))
    moyenne = ma.sum(moyenne,axis=(len(moyenne.shape)-1))
  elif operation is 'average' :
    moyenne = ma.sum(tmp,axis=(len(tmp.shape)-1))
    moyenne = ma.sum(moyenne,axis=(len(moyenne.shape)-1))
    surfacetot = ma.sum(wtmsk,axis=(len(wtmsk.shape)-1))
    surfacetot = ma.sum(surfacetot,axis=(len(surfacetot.shape)-1))
    moyenne = moyenne/surfacetot
  elif operation is 'max' :
    moyenne = ma.max(tab,axis=(len(tmp.shape)-1))
    moyenne = ma.max(moyenne,axis=(len(moyenne.shape)-1))
  elif operation is 'min' :
    moyenne = ma.min(tab,axis=(len(tmp.shape)-1))
    moyenne = ma.min(moyenne,axis=(len(moyenne.shape)-1))
  else :
    print """ Operation : %s is unknown"""%(operation)
  #
  #
  return moyenne
# -----------------------------------------------------------------------
def get_thkcello(grid='ORCA2') :
  if grid is 'ORCA2':
    fgrid='/net/cratos/usr/cratos/varclim/IPSLCM5A/PROD/piControl2/OCE/Analyse/TS_MO/piControl2_27500101_27991231_1M_thkcello.nc'
  try :
    f = nc.Dataset(fgrid)
  except :
    print """Couldn't find de file : %s"""%(fgrid)
  #
  thkcello = f.variables['thkcello'][0,:,:,:]
  thkcello = thkcello.astype(N.float64)
  f.close()
  return thkcello
# -----------------------------------------------------------------------
def coord2indice(axe,axlim) :
  """
  indmin, indmax = coord2index(axe,(V1,V2))
  
  Retourne les indices min et max permettant de selectionner l'intervalle axlim.
  """
  coordindice = ma.masked_where(ma.logical_or(axe<axlim[0],axe>axlim[1]),ma.arange((len(axe))))
  return ma.minimum(coordindice), ma.maximum(coordindice)
# -----------------------------------------------------------------------
def selectseason(tab,axt,postime=0,season='DJF') :
  """
      selectionne la saison d'un champs
    . postim = position de la dimension temporelle dans tab
  """
  indices = N.array(range(len(axt.month())))
  isinseason = N.array([x in dseason[season] for x in axt.month()])
  #
  tabout = N.take(tab,indices[isinseason],axis=posdim)
  timenew = timeaxis(axt.values[indices[isinseason]],units=axt.units,calendar=axt.calendar,origin=axt.origin)
  #
  return tabout, timenew
# -----------------------------------------------------------------------
def find_nearest(tab,value):
    idx = (ma.abs(tab-value)).argmin()
    return idx




    









