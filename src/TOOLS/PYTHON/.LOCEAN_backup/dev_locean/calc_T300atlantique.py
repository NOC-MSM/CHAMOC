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
import numpy.ma as ma
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
DIAG_ID = 'T300atlantique_YE'
domains = ['AMO','ATL4070N','ATLTROP10','ATLTROP20','ATLSOUTH40','ATLSOUTH20']

# Repertoires des inputs :
# ~~~~~~~~~~~~~~~~~~~~~~~
exp = dexp[EXP_ID]
filein = exp.locfile('votemper',realm='O')
#
thkcello = ct.get_thkcello()
fref = nc.Dataset('/net/cratos/usr/cratos/varclim/IPSLCM5A/PROD/piControl2/OCE/Analyse/TS_MO/piControl2_18000101_27991231_1M_zomsfatl.nc')
depth = fref.variables['deptht'][:]
depthindicemin, depthindicemax = ct.coord2indice(depth,(0,300))
#
#
# Repertoires des outputs :
# ~~~~~~~~~~~~~~~~~~~~~~~~~
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
vout=dict()
if os.path.exists(fileout) :
  fileo = nc.Dataset(fileout,'a')
  if 'T300_AMO' in fileo.variables.keys() :
    times = fileo.variables['time_counter']
    last_year_done = nc.num2date(times[-1],times.units,calendar=times.calendar).year
    last_year_to_do = yrfin
    yrdeb = last_year_done+1
    if fin is not None :
      last_year_to_do=int(fin)
    print last_year_done+1, last_year_to_do
  for dom in domains :
    vout[dom]  = fileo.variables['T300_%s'%dom]
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
    vout[dom]  = fileo.createVariable('T300_%s'%dom,'f',('time',))
    vout[dom].units = 'degC'
    vout[dom].long_name = 'votemper averaged in depth (see level attributs and horizontaly in %s'%dom
    vout[dom].domain = '%s in mask_ORCA2.nc'%dom
    vout[dom].Nlevels = '%i'%(len(depth[depthindicemin:depthindicemax+1]))
    vout[dom].bottomleveldepth = '%f m'%(depth[depthindicemax])
    vout[dom].topleveldepth = '%f m'%(depth[depthindicemin])
##
#
for year in range(yrdeb,yrfin+1) :
  #
  print """computing year %i"""%(year)
  tab,timex = ct.read(filein,'votemper',years=range(year,year+1))
  # Moyenne sur la verticale (pondérée par dz) :
  wt = ma.repeat( ma.reshape(thkcello, (1,)+thkcello.shape), tab.shape[0], axis=0)
  tabwt = tab[:,depthindicemin:depthindicemax+1,:,:]*wt[:,depthindicemin:depthindicemax+1,:,:]
  tab_2d = tabwt.sum(axis=1)
  H_2d = wt[:,depthindicemin:depthindicemax+1,:,:].sum(axis=1)
  #
  # Writing in netcdf file
  # ---------------------- 
  if times.shape[0]==0 :
    times[0]=timex.num()[0]
    for dom in domains :
      Vtot  = ct.regional_average(H_2d,dom,operation='sum')
      tabav = ct.regional_average(tab_2d,dom,operation='sum')/Vtot
      tabyr = ma.average(tabav,axis=0)
      vout[dom][0]=tabyr
      del tabav, tabyr
  else :
    i1=len(times)
    times[i1]=timex.num()[0]
    for dom in domains :
      Vtot  = ct.regional_average(H_2d,dom,operation='sum')
      tabav = ct.regional_average(tab_2d,dom,operation='sum')/Vtot
      tabyr = ma.average(tabav,axis=0)
      vout[dom][i1]=tabyr
      del  tabav, tabyr
  del timex.values
# 
times.calendar=timex.calendar
times.units=timex.units
fileo.close()
#
# the end




