#!/usr/bin/env cdat
# -*-coding:Latin-1 -*
# Created : 2013/12 (A. Germe)
# Modified: no 01
# CONSTRUCTION DES SERIES TEMPORELLES SSTglo, SSTatl, SSTpac
#======================================================================== 
#global AG
#global EXP_ID, location, fileo
# Cet declacration en global est utile uniquement lorsque le diag
# est lancÃ© depuis la mÃ©thode "compute" de la class "diag"
# ============================================================================
import sys, os
import netCDF4 as nc
import datetime
import copy
import MA
import numpy as N
#
from direxp import *
#======================================================================== 
# utilisation :
#        cdat calc_SSTbassin EXP_ID
# Exemple :
#        cdat -i calc_SSTbassin.py piControl2
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
    moyenne = MA.sum(tmp,axis=2)
    moyenne = MA.sum(moyenne,axis=1)
    surfacetot = MA.sum(wtmsk,axis=2)
    surfacetot = MA.sum(surfacetot,axis=1)
    moyenne = moyenne/surfacetot
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
  #tab = f.variables[varname][0:12,:,:]
  timeaxis = f.variables['time_counter']
  timeu = timeaxis.units
  timecal = timeaxis.calendar
  #
  if years is not None :
    tdeb = datetime.datetime(years[0],1,1) # 1er Jan de la 1ere année
    tfin = datetime.datetime(years[-1],12,31,23,59,00) #31/12 de la dernière année
    ideb = nc.date2index(tdeb,timeaxis,calendar=timeaxis.calendar,select='after')
    ifin = nc.date2index(tfin,timeaxis,calendar=timeaxis.calendar,select='before')
    timeval = timeaxis[ideb:ifin+1]
    tab = f.variables[varname][ideb:ifin+1,:,:]
  else :
    tab = f.variables[varname][:,:,:]
    timeval=timeaxis[:]
  #  
  f.close()
  return tab, timeval, timeu, timecal
# =======================================================================
# =======================================================================
EXP_ID  = sys.argv[1]
if len(sys.argv)<3 :
  fin = None
else :
  fin = sys.argv[2]
#
DIAG_ID = 'SSTbassin'

# Repertoires des inputs :
# ~~~~~~~~~~~~~~~~~~~~~~~
exp = dexp[EXP_ID]
dirin=exp.loc('O')

filein = exp.fname('sosstsst')

# Repertoires des outputs :
# ~~~~~~~~~~~~~~~~~~~~~~~~~
#diag = ddiag[DIAG_ID]
if exp.ismember :
  dirout = '/net/cratos/usr/cratos/varclim/agglod/mydiags/OUTPUTS/Ocean/%s/%s/%s/'%(exp.stream,exp.group,exp.ensemblename)
else :
  dirout = '/net/cratos/usr/cratos/varclim/agglod/mydiags/OUTPUTS/Ocean/%s/%s/'%(exp.stream,exp.group)
fileout = '%s%s_%s.nc'%(dirout,EXP_ID,DIAG_ID)

# années disponibles
# ~~~~~~~~~~~~~~~~~~
[yrdeb,yrfin]=years(filein)
print('Dates available for %s : %i-%i'%(EXP_ID,yrdeb,yrfin))
if fin is not None :
  yrfin=int(fin)
  print('To your request, the computation will stop for yrfin = %s'%(fin))
#
# ========================================================================
# Main routine
# ========================================================================
if not os.path.exists(dirout) : os.makedirs(dirout)
#
if os.path.exists(fileout) :
  fileo = nc.Dataset(fileout,'a')
  sstglo = fileo.variables['SSTglo']
  sstatl = fileo.variables['SSTatl']
  sstpac = fileo.variables['SSTpac']
  times = fileo.variables['time_counter']
  if 'SSTglo' in fileo.variables.keys() :
    last_year_done = nc.num2date(times[-1],times.units).year
    last_year_to_do = yrfin
    yrdeb = last_year_done+1
    if fin is not None :
      last_year_to_do=int(fin)
    print last_year_done+1, last_year_to_do+1
else :
  datefile = datetime.date.today() 
  fileo = nc.Dataset(fileout,'w')
  fileo.date = str(datefile)
  #fileo.code = diag.codefile
  fileo.author = 'A. Germe'
  time = fileo.createDimension('time',None)
  times = fileo.createVariable('time_counter','f',('time',))
  sstglo = fileo.createVariable('SSTglo','f',('time',))
  sstatl = fileo.createVariable('SSTatl','f',('time',))
  sstpac = fileo.createVariable('SSTpac','f',('time',))
  sstglo.units = 'degC'
  sstatl.units = 'degC'
  sstpac.units = 'degC'
  sstglo.long_name = 'Global Ocean sea surface temperature average'
  sstatl.long_name = 'Atlantic Ocean sea surface temperature average'
  sstpac.long_name = 'Pacific Ocean sea surface temperature average'
  #times.units=timeu
#
#
for year in range(yrdeb,yrfin+1) :
  #
  print """computing year %i"""%(year)
  tab,timeval,timeu,timecal = read(dirin,filein,'sosstsst',years=range(year,year+1))
  #
  tab_glo  = regional_average(tab,'GLOOCEAN',operation='average')
  tab_atl = regional_average(tab,'ATLANTIC',operation='average')
  tab_pac = regional_average(tab,'PACIFIC',operation='average')

  # Writing in netcdf file
  # ---------------------- 
  if sstglo.shape[0]==0 :
    sstglo[:]=tab_glo.filled()
    sstatl[:]=tab_atl.filled()
    sstpac[:]=tab_pac.filled()
    times[:]=timeval
  else :
    i1=len(sstglo)
    sstglo[i1:i1+12]=tab_glo.filled()
    sstatl[i1:i1+12]=tab_atl.filled()
    sstpac[i1:i1+12]=tab_pac.filled()
    times[i1:i1+12]=timeval
  del tab_glo, tab_atl, timeval
 
times.calendar=timecal
times.units=timeu  
fileo.close()

# on efface les variables globales 
#del location EXP_ID




