#!/usr/bin/env cdat
# -*-coding:Latin-1 -*
# Created : 2013/11 (A. Germe)
# Modified: no 01
# CONSTRUCTION DES SERIES TEMPORELLES USUELLE, SIE, SIA, SIV
# Dans les MIZ comme définies par le NSIDC
#======================================================================== 
#global AG
#global EXP_ID, location, fileo
# Cet declacration en global est utile uniquement lorsque le diag
# est lancÃ© depuis la mÃ©thode "compute" de la class "diag"
#
# ============================================================================
import sys, os
import netCDF4 as nc
import datetime
import copy
import MA
#
from direxp import *
#======================================================================== 
# utilisation :
#        cdat calc_SIindex.py EXP_ID
# Exemple :
#        cdat -i calc_SIindex.py HISTNUD15
# =======================================================================
# Some functions
# ==============
def years(filein) :
  info=filein.split('_')
  yrdeb=int(info[1][0:4])
  yrfin=int(info[2][0:4])
  return [yrdeb,yrfin]
# -----------------------------------------------------------------------
def get_mask(domain,grid='ORCA2') :
  if grid is 'ORCA2':
    fgrid='/net/cratos/usr/cratos/varclim/agglod/DATA/IPSLCM/Mask_ORCA2.nc'
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
  wt = myweights(grid=gridname)
  if len(tab.shape)>2:
    dt=tab.shape[0]
    wt = MA.repeat( MA.reshape(wt, (1,)+wt.shape), dt, axis=0)
  #
  region_mask = get_mask(domain,grid=gridname)[0]
  if len(tab.shape)>2:
    region_mask=MA.repeat( MA.reshape(region_mask, (1,)+region_mask.shape), dt, axis=0)
  #
  tab = MA.masked_where(region_mask==0.,tab)
  wtmsk = MA.masked_where(region_mask==0.,wt)
  tmp = tab*wtmsk
  if operation is 'sum' :
    moyenne = MA.sum(tmp,axis=2)
    moyenne = MA.sum(moyenne,axis=1)
  elif operation is 'average' :
    moyenne = MA.average(tmp,axis=2)
    moyenne = MA.average(moyenne,axis=1)
  else :
    print """ Operation : %s is unknown"""%(operation)
  #
  #
  return moyenne
# -----------------------------------------------------------------------
def read(dirin,filein,varname,years=None) :
  try :
    f=nc.Dataset(dirin+filein)
  except :
    """Couldn't find the file %s"""%(dirin+filein)
  tab = f.variables[varname][0:12,:,:]
  timeaxis = f.variables['time_counter']
  timeu = timeaxis.units
  #
  if years is not None :
    tdeb = datetime.datetime(years[0],1,1) # 1er Jan de la 1ere année
    tfin = datetime.datetime(years[-1],12,31) #31/12 de la dernière année
    ideb = nc.date2index(tdeb,timeaxis,calendar=timeaxis.calendar,select='after')
    ifin = nc.date2index(tfin,timeaxis,calendar=timeaxis.calendar,select='before')
    timeval = timeaxis[ideb:ifin+1]
    tab = f.variables[varname][ideb:ifin+1,:,:]
  else :
    tab = f.variables[varname][:,:,:]
    timeval=timeaxis[:]
  #  
  f.close()
  return tab, timeval, timeu
# =======================================================================
# =======================================================================
EXP_ID  = 'piControl2'
DIAG_ID = 'SIindex_MIZnsidc'
fin     = 1803
domains = ['NSARCTON','OKHOTSKX','BERINGXX','NSBAFFIN','GINSEASX','BARENTSX','BARKARAS']

# Repertoires des inputs :
# ~~~~~~~~~~~~~~~~~~~~~~~
exp = dexp[EXP_ID]
dirin=exp.loc('I')

fileinsic = exp.fname('soicecov')
fileinsit = exp.fname('iicethic')

timeu = 'seconds since %s-01-01 00:00:00'%(exp.datedeb[0:4])

# Repertoires des outputs :
# ~~~~~~~~~~~~~~~~~~~~~~~~~
#diag = ddiag[DIAG_ID]
if exp.ismember :
  dirout = '/net/cratos/usr/cratos/varclim/agglod/mydiags/OUTPUTS/SeaIce/%s/%s/%s/'%(exp.stream,exp.group,exp.ensemblename)
else :
  dirout = '/net/cratos/usr/cratos/varclim/agglod/mydiags/OUTPUTS/SeaIce/%s/%s/'%(exp.stream,exp.group)
fileout = '%s%s_%s.nc'%(dirout,EXP_ID,DIAG_ID)

# Indices Ã  cacluler
# ~~~~~~~~~~~~~~~~~~
listindex = ['SIA','SIE','SIV']

# années disponibles
# ~~~~~~~~~~~~~~~~~~
[yrdeb,yrfin]=years(fileinsic)
print('Dates available for %s : %i-%i'%(EXP_ID,yrdeb,yrfin))
if fin is not None :
  yrfin=int(fin)
  print('To your request, the computation will stop for yrfin = %s'%(fin))

# Definition de l'index
# ~~~~~~~~~~~~~~~~~~~~~~~
# ========================================================================
# Main routine
# ========================================================================
if not os.path.exists(dirout) : os.makedirs(dirout)
#
for dom in domains :
  if os.path.exists(fileout) :
    fileo = nc.Dataset(fileout,'a')
    if 'SIA_%s'%dom in fileo.variables.keys() :
      sia = fileo.variables['SIA_%s'%dom]
      sie = fileo.variables['SIE_%s'%dom]
      siv = fileo.variables['SIV_%s'%dom]
      times = fileo.variables['time']
      last_year_done = nc.num2date(times[-1],times.units).year
      last_year_to_do = yrfin
      yrdeb = last_year_done+1
      if fin is not None :
        last_year_to_do=int(fin)
      print last_year_done+1, last_year_to_do+1
      writetime=True
    else :
      sia = fileo.createVariable('SIA_%s'%dom,'f',('time',))
      sie = fileo.createVariable('SIE_%s'%dom,'f',('time',))
      siv = fileo.createVariable('SIV_%s'%dom,'f',('time',))
      sia.units = 'm2'
      sie.units = 'm2'
      siv.units = 'm3'
      sia.long_name = '%s sea ice area'%dom
      sie.long_name = '%s sea ice extent'%dom
      siv.long_name = '%s sea ice volume'%dom
      writetime=False
  else :
    datefile = datetime.date.today() 
    fileo = nc.Dataset(fileout,'w')
    fileo.date = str(datefile)
    #fileo.code = diag.codefile
    fileo.author = 'A. Germe'
    time = fileo.createDimension('time',None)
    times = fileo.createVariable('time','f',('time',))
    sia = fileo.createVariable('SIA_%s'%dom,'f',('time',))
    sie = fileo.createVariable('SIE_%s'%dom,'f',('time',))
    siv = fileo.createVariable('SIV_%s'%dom,'f',('time',))
    sia.units = 'm2'
    sie.units = 'm2'
    siv.units = 'm3'
    sia.long_name = '%s sea ice area'%dom
    sie.long_name = '%s sea ice extent'%dom
    siv.long_name = '%s sea ice volume'%dom
    times.units=timeu
    times.calendar='no_leap'
    writetime=True
  #
  #
  #
  #
  for year in range(yrdeb,yrfin+1) :
    #
    print """computing domain %s for year %i"""%(dom,year)
    tab,timeval,timeu = read(dirin,fileinsic,'soicecov',years=range(year,year+1))
    tabe = copy.deepcopy(tab)
    tabe[tab<0.15]=0
    tabe[tab>0.15]=1
    tabv,timeval,timeu = read(dirin,fileinsit,'iicethic',years=range(year,year+1))
    #
    tab_av  = regional_average(tab,dom)
    tabe_av = regional_average(tabe,dom)
    tabv_av = regional_average(tabv,dom)
    1
    # Writing in netcdf file
    # ---------------------- 
    if sia.shape[0]==0 :
      sia[:]=tab_av.filled()
      sie[:]=tabe_av.filled()
      siv[:]=tabv_av.filled()
      if writetime : times[:]=timeval
    else :
      i1=len(sia[~sia[:].mask])
      sia[i1:i1+12]=tab_av.filled()
      sie[i1:i1+12]=tabe_av.filled()
      siv[i1:i1+12]=tabv_av.filled()
      if writetime : times[i1:i1+12]=timeval
    del tab_av, tabe_av, tabv_av, timeval
  #
  # fin de la boucle sur les années
#
# fin de la boucle sur les domaines
fileo.close()

# on efface les variables globales 
#del location EXP_ID




