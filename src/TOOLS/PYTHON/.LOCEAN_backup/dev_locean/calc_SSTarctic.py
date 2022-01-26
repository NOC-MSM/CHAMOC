#!/usr/bin/env cdat
# -*-coding:Latin-1 -*
# Created : 2014/01 (A. Germe)
# Modified: no 00
# CONSTRUCTION DES SERIES TEMPORELLES SST moyennes sur boites atlantiques
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
#        cdat calc_AMOindex.py EXP_ID (yrfin)
# Exemple :
#        cdat calc_AMOindex.py piControl2 
#        cdat calc_AMOindex.py piControl2 1805
# =======================================================================
EXP_ID  = sys.argv[1]
if len(sys.argv)<3 :
  fin = None
else :
  fin = sys.argv[2]
#
DIAG_ID = 'SSTarctic_YE'
domains = ['ARCTICXX','CENTRARC','WCENTARC','GINSEASX']

# Repertoires des inputs :
# ~~~~~~~~~~~~~~~~~~~~~~~
exp = dexp[EXP_ID]
filein = exp.locfile('sosstsst',realm='O')

# Repertoires des outputs :
# ~~~~~~~~~~~~~~~~~~~~~~~~~
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
vout=dict()
if os.path.exists(fileout) :
  fileo = nc.Dataset(fileout,'a')
  if 'SST_ARCTICXX' in fileo.variables.keys() :
    times = fileo.variables['time_counter']
    last_year_done = nc.num2date(times[-1],times.units,calendar=times.calendar).year
    last_year_to_do = yrfin
    yrdeb = last_year_done+1
    if fin is not None :
      last_year_to_do=int(fin)
    print last_year_done+1, last_year_to_do
  for dom in domains :
    vout[dom]  = fileo.variables['SST_%s'%dom]
else :
  datefile = datetime.date.today() 
  fileo = nc.Dataset(fileout,'w')
  fileo.date = str(datefile)
  #fileo.code = diag.codefile
  fileo.author = 'A. Germe'
  fileo.comment = 'None'
  time = fileo.createDimension('time',None)
  times = fileo.createVariable('time_counter','f',('time',))
  for dom in domains :
    vout[dom]  = fileo.createVariable('SST_%s'%dom,'f',('time',))
    vout[dom].units = 'degC'
    vout[dom].long_name = 'sosstsst averaged in %s'%dom
    vout[dom].domain = '%s in mask_ORCA2.nc'%dom
#
#
for year in range(yrdeb,yrfin+1) :
  #
  print """computing year %i"""%(year)
  tab,timex = ct.read(filein,'sosstsst',years=range(year,year+1))
  #
  # Writing in netcdf file
  # ---------------------- 
  if times.shape[0]==0 :
    times[0]=timex.num()[0]
    for dom in domains :
      tabav = ct.regional_average(tab,dom,operation='average')
      tabyr = MA.average(tabav,axis=0)
      vout[dom][0]=tabyr
  else :
    i1=len(times)
    times[i1]=timex.num()[0]
    for dom in domains :
      tabav = ct.regional_average(tab,dom,operation='average')
      tabyr = MA.average(tabav,axis=0)
      vout[dom][i1]=tabyr
    #print timex.year()[0]
  del  tabav, tabyr, timex.values
 
times.calendar=timex.calendar
times.units=timex.units
fileo.close()
#
# the end




