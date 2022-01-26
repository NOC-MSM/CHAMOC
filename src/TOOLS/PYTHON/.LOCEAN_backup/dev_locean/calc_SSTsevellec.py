#!/usr/bin/env cdat
# -*-coding:Latin-1 -*
# Created : 2014/01 (A. Germe)
# Modified: no 00
# CONSTRUCTION DE LA SERIE TEMPORELLE AMO index
#======================================================================== 
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
#        cdat calc_SSTsevellec.py EXP_ID (yrfin)
# Exemple :
#        cdat calc_SSTsevellec.py piControl2 
#        cdat calc_SSTsevellec.py piControl2 1805
# =======================================================================
# Some functions
# ==============
#def years(filein) :
#  info=filein.split('_')
#  yrdeb=int(info[1][0:4])
#  yrfin=int(info[2][0:4])
#  return [yrdeb,yrfin]
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
#    tfin = datetime.datetime(years[-1],12,31,23,59,00) #31/12 de la dernière a#nnée
#    ideb = nc.date2index(tdeb,timeaxis,calendar=timeaxis.calendar,select='after#')
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
DIAG_ID = 'SSTsevellec'

# Repertoires des inputs :
# ~~~~~~~~~~~~~~~~~~~~~~~
exp = dexp[EXP_ID]
domains=['ATL3070N','ATL3070NnoH']

filein = exp.locfile('sosstsst',realm='O')

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
[yrdeb,yrfin]=exp.year
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
sstav=dict()
if os.path.exists(fileout) :
  fileo = nc.Dataset(fileout,'a')
  times = fileo.variables['time_counter']
  if 'SST_ATL3070N' in fileo.variables.keys() :
    last_year_done = nc.num2date(times[-1],times.units,calendar=times.calendar).year
    last_year_to_do = yrfin
    yrdeb = last_year_done+1
    if fin is not None :
      last_year_to_do=int(fin)
    print last_year_done+1, last_year_to_do
  for dom in domains :
    sstav[dom] = fileo.variables['SST_%s'%dom]
else :
  datefile = datetime.date.today() 
  fileo = nc.Dataset(fileout,'w')
  fileo.date = str(datefile)
  #fileo.code = diag.codefile
  fileo.author = 'A. Germe'
  fileo.comment = 'The SST is computed as the spatial averaged of the annual SST in the 30N-70N domain North Atlantic domain(with and without the Hudson bay)'
  time = fileo.createDimension('time',None)
  times = fileo.createVariable('time_counter','f',('time',))
  for dom in domains :
    sstav[dom] = fileo.createVariable('SST_%s'%dom,'f',('time',))
    sstav[dom].units = 'degC'
    sstav[dom].long_name = 'SST averaged over ATL3070NnoH domain'
    sstav[dom].domain = '%s  in mask_ORCA2.nc'%dom
  #amorev.long_name = 'Revised Altantic Multidecadal Oscillation index'
  #times.units=timeu
#
#
for year in range(yrdeb,yrfin+1) :
  #
  print """computing year %i"""%(year)
  tab,timex = ct.read(filein,'sosstsst',years=range(year,year+1))
  #

  #
  # revised amo index
  #tab_amorev = tab_amoyr - tab_gloyr

  # Writing in netcdf file
  # ---------------------- 
  if times.shape[0]==0 :
    times[0]=timex.num()[0]
    for dom in domains :
      tab_amo = ct.regional_average(tab,dom,operation='average')
      #
      # Annual mean
      tab_amoyr = MA.average(tab_amo,axis=0)
      sstav[dom][0]=tab_amoyr
      del  tab_amo, tab_amoyr
  else :
    i1=len(times)
    times[i1]=timex.num()[0]
    for dom in domains :
      tab_amo = ct.regional_average(tab,dom,operation='average')
      #
      # Annual mean
      tab_amoyr = MA.average(tab_amo,axis=0)
      sstav[dom][i1]=tab_amoyr
      del  tab_amo, tab_amoyr
  del timex.values
times.calendar=timex.calendar
times.units=timex.units
fileo.close()

# on efface les variables globales 
#del location EXP_ID




