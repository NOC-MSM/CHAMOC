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
import climtools as ct
#======================================================================== 
# utilisation :
#        cdat calc_SSTbassin EXP_ID
# Exemple :
#        cdat -i calc_SSTbassin.py piControl2
# =======================================================================
# Some functions
# ==============
def years(filein) :
  info=filein.split('/')[-1]
  info=info.split('_')
  yrdeb=int(info[1][0:4])
  yrfin=int(info[2][0:4])
  return [yrdeb,yrfin]
# -----------------------------------------------------------------------
#def read(dirin,filein,varname,years=None) :
#  try :
#    f=nc.Dataset(dirin+filein)
#  except :
#    """Couldn't find the file %s"""%(dirin+filein)
#  #tab = f.variables[varname][0:12,:,:]
#  timeaxis = f.variables['time_counter']
#  timeu = timeaxis.units
#  timecal = timeaxis.calendar
#  #
#  if years is not None :
#    tdeb = datetime.datetime(years[0],1,1) # 1er Jan de la 1ere année
#    tfin = datetime.datetime(years[-1],12,31,23,59,00) #31/12 de la dernière année
#    ideb = nc.date2index(tdeb,timeaxis,calendar=timeaxis.calendar,select='after')
#    ifin = nc.date2index(tfin,timeaxis,calendar=timeaxis.calendar,select='before')
#    timeval = timeaxis[ideb:ifin+1]
#    tab = f.variables[varname][ideb:ifin+1,:,:]
#  else :
#    tab = f.variables[varname][:,:,:]
#    timeval=timeaxis[:]
#  #  
#  f.close()
#  return tab, timeval, timeu, timecal
# =======================================================================
# =======================================================================
EXP_ID  = sys.argv[1]
if len(sys.argv)<3 :
  fin = None
else :
  fin = sys.argv[2]
#
DIAG_ID = 'SSTbassin_DA'

# Repertoires des inputs :
# ~~~~~~~~~~~~~~~~~~~~~~~
exp = dexp[EXP_ID]
filein = exp.locfile('sosstsst',realm='O',freq='DA')

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
  tab,timex = ct.read(filein,'sosstsst',years=range(year,year+1))
  #
  tab_glo  = ct.regional_average(tab,'GLOOCEAN',operation='average')
  tab_atl = ct.regional_average(tab,'ATLANTIC',operation='average')
  tab_pac = ct.regional_average(tab,'PACIFIC',operation='average')

  # Writing in netcdf file
  # ---------------------- 
  if sstglo.shape[0]==0 :
    sstglo[:]=tab_glo.filled()
    sstatl[:]=tab_atl.filled()
    sstpac[:]=tab_pac.filled()
    times[:]=timex.num()
  else :
    i1=len(sstglo)
    di = tab_glo.shape[0]
    sstglo[i1:i1+di]=tab_glo.filled()
    sstatl[i1:i1+di]=tab_atl.filled()
    sstpac[i1:i1+di]=tab_pac.filled()
    times[i1:i1+di]=timex.num()
  del tab_glo, tab_atl
 
times.calendar=timex.calendar
times.units=timex.units  
fileo.close()

# on efface les variables globales 
#del location EXP_ID




