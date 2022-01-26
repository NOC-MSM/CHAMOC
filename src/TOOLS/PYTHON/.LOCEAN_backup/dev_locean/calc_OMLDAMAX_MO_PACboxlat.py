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
#import numpy.ma as MA
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
DIAG_ID = 'OMLDAMAX_MO_PACboxlat'

# Repertoires des inputs :
# ~~~~~~~~~~~~~~~~~~~~~~~
exp = dexp[EXP_ID]
domains = ['PAC0010N','PAC1020N','PAC2030N','PAC3040N','PAC4050N','PAC5060N','PAC5070N']

filein = exp.locfile('omldamax',realm='O')
#
thkcello = ct.get_thkcello()
#
#
fref = nc.Dataset('/net/cratos/usr/cratos/varclim/IPSLCM5A/PROD/piControl2/OCE/Analyse/TS_MO/piControl2_18000101_27991231_1M_zomsfatl.nc')
depth = fref.variables['deptht'][:]



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
MLDmean= dict()
MLDmax= dict()
if os.path.exists(fileout) :
  fileo = nc.Dataset(fileout,'a')
  if 'OMLDAMAXmax_PAC0010N' in fileo.variables.keys() :
    times = fileo.variables['time_counter']
    last_year_done = nc.num2date(times[-1],times.units,calendar=times.calendar).year
    last_year_to_do = yrfin
    yrdeb = last_year_done+1
    if fin is not None :
      last_year_to_do=int(fin)
    print last_year_done+1, last_year_to_do+1
  for dom in domains :
    MLDmean[dom] = fileo.variables['OMLDAMAXmean_%s'%dom]
    MLDmax[dom]  = fileo.variables['OMLDAMAXmax_%s'%dom]
else :
  datefile = datetime.date.today() 
  fileo = nc.Dataset(fileout,'w')
  fileo.date = str(datefile)
  #fileo.code = diag.codefile
  fileo.author = 'A. Germe'
  fileo.comment = 'The OMLDAMAXmax and OMLDAMAXmean are computed as the maximum and the average of omldamax in the domain. omldamax is a daily field. It is averaged as monthly outputs via cdo because for EPCT, the direct monthly output omlmax has been discard.'
  time = fileo.createDimension('time',None)
  times = fileo.createVariable('time_counter','f',('time',))
  for dom in domains :
    MLDmean[dom] = fileo.createVariable('OMLDAMAXmean_%s'%dom,'f',('time'))
    MLDmean[dom].units = 'm'
    MLDmean[dom].long_name = 'mixed layer thickness averaged over %s'%dom
    MLDmean[dom].domain = '%s in mask_ORCA2.nc'%dom
    MLDmax[dom] = fileo.createVariable('OMLDAMAXmax_%s'%dom,'f',('time'))
    MLDmax[dom].units = 'm'
    MLDmax[dom].long_name = 'mixed layer thickness maximum in %s'%dom
    MLDmax[dom].domain = '%s in mask_ORCA2.nc'%dom
#
#
for year in range(yrdeb,yrfin+1) :
  #
  print """computing year %i"""%(year)
  tab,timex = ct.read(filein,'omldamax',years=range(year,year+1))
  #
 
  if times.shape[0]==0 :
    times[:]=timex.num()
    for dom in domains :
      tab_av  = ct.regional_average(tab,dom,operation='average')
      tab_max = ct.regional_average(tab,dom,operation='max')
      #
      # Writing in netcdf file
      # ---------------------- 
      MLDmean[dom][:] = tab_av.filled()
      MLDmax[dom][:]  = tab_max.filled()
      del tab_av
  else :
    i1=len(times)
    times[i1:i1+12]=timex.num()
    for dom in domains : 
      tab_av  = ct.regional_average(tab,dom,operation='average')
      tab_max = ct.regional_average(tab,dom,operation='max')
      #
      # Writing in netcdf file
      # ---------------------- 
      MLDmax[dom][i1:i1+12]  = tab_max.filled()
      MLDmean[dom][i1:i1+12] = tab_av.filled()
      del  tab_av, tab_max
  del timex.values
 
times.calendar=timex.calendar
times.units=timex.units
fileo.close()

# on efface les variables globales 
#del location EXP_ID




