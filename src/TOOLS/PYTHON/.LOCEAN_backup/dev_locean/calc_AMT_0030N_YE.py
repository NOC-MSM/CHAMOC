#!/usr/bin/env cdat
# -*-coding:Latin-1 -*
# Created : 2014/01 (A. Germe)
# Modified: no 02
# CONSTRUCTION DE LA SERIE TEMPORELLE AMT index (Florian LOP variable)
# Ce diag est identique au diag TAV3D3070N_YE; mais en version plus simple
# (domaine unique), et avec nom cohérent avec diag de Florian.
# La version 00 était buggé. 
#======================================================================== 
import sys, os
import netCDF4 as nc
import datetime
import copy
import MA
import numpy.ma as ma
import numpy as N
#
from direxp import *
import climtools as ct
#======================================================================== 
# utilisation :
#        cdat calc_AMTindex.py EXP_ID (yrfin)
# Exemple :
#        cdat calc_AMTindex.py piControl2 
#        cdat calc_AMTindex.py piControl2 1805
# =======================================================================
EXP_ID  = sys.argv[1]
if len(sys.argv)<3 :
  fin = None
else :
  fin = sys.argv[2]
#
DIAG_ID = 'AMT_ATL0030N_YE'

# Repertoires des inputs :
# ~~~~~~~~~~~~~~~~~~~~~~~
exp = dexp[EXP_ID]
dom = 'ATL0030N'

filein = exp.locfile('votemper',realm='O')
#
thkcello = ct.get_thkcello()
#
#

# Repertoires des outputs :
# ~~~~~~~~~~~~~~~~~~~~~~~~~
#diag = ddiag[DIAG_ID]
if exp.ismember :
  dirout = '/net/cratos/usr/cratos/varclim/agglod/mydiags/OUTPUTS/Ocean/%s/%s/%s/'%(exp.stream,exp.group,exp.ensemblename)
else :
  dirout = '/net/cratos/usr/cratos/varclim/agglod/mydiags/OUTPUTS/Ocean/%s/%s/'%(exp.stream,exp.group)
fileout = '%s%s_%s.nc'%(dirout,EXP_ID,DIAG_ID)

# annÃ©es disponibles
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
hc= dict()
if os.path.exists(fileout) :
  fileo = nc.Dataset(fileout,'a')
  if 'AMT' in fileo.variables.keys() :
    times = fileo.variables['time_counter']
    last_year_done = nc.num2date(times[-1],times.units,calendar=times.calendar).year
    last_year_to_do = yrfin
    yrdeb = last_year_done+1
    if fin is not None :
      last_year_to_do=int(fin)
    print last_year_done+1, last_year_to_do+1
    hc = fileo.variables['AMT']
else :
  datefile = datetime.date.today() 
  fileo = nc.Dataset(fileout,'w')
  fileo.date = str(datefile)
  #fileo.code = diag.codefile
  fileo.author = 'A. Germe'
  fileo.comment = 'The temperature averaged is computed as the weighted averaged of votemper. Version 01 (bug resolved)'
  fileo.expid = EXP_ID
  fileo.diagid = DIAG_ID
  time = fileo.createDimension('time',None)
  times = fileo.createVariable('time_counter','f',('time',))
  hc = fileo.createVariable('AMT','f',('time',))
  hc.units = 'degC'
  hc.long_name = 'Atlantic Mean Temperature, 3D temperature averaged in %s'%dom
  hc.domain = '%s in mask_ORCA2.nc'%dom
#
#
for year in range(yrdeb,yrfin+1) :
  #
  print """computing year %i"""%(year)
  tab,timex = ct.read(filein,'votemper',years=range(year,year+1))
  #
  # Moyenne sur la verticale (pondérée par dz) :
  wt = ma.repeat( ma.reshape(thkcello, (1,)+thkcello.shape), tab.shape[0], axis=0)
  tabwt = tab*wt
  tab_2d = tabwt.sum(axis=1)
  H_2d = wt.sum(axis=1)
  Vtot = ct.regional_average(H_2d,dom,operation='sum')

  if times.shape[0]==0 :
    times[0]=timex.num()[0]
    tab_av = ct.regional_average(tab_2d,dom,operation='sum')/Vtot
    #
    # Annual mean
    tab_amoyr = MA.average(tab_av,axis=0)
    #
    # Writing in netcdf file
    # ---------------------- 
    hc[0]=tab_amoyr
  else :
    i1=len(times)
    times[i1]=timex.num()[0]
    tab_av = ct.regional_average(tab_2d,dom,operation='sum')/Vtot
    #
    # Annual mean
    tab_amoyr = MA.average(tab_av,axis=0)
    #
    # Writing in netcdf file
    # ---------------------- 
    hc[i1]=tab_amoyr
    del  tab_av, tab_amoyr
  del timex.values
 
times.calendar=timex.calendar
times.units=timex.units
fileo.close()

# on efface les variables globales 
#del location EXP_ID




