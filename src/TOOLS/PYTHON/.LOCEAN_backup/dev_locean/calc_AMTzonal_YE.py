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
DIAG_ID = 'AMTzonal_YE'


# Repertoires des inputs :
# ~~~~~~~~~~~~~~~~~~~~~~~
exp = dexp[EXP_ID]
dom = 'ATL5060N'

filein = exp.locfile('votemper',realm='O')
#
thkcello = ct.get_thkcello()
#
#
fref = nc.Dataset('/net/cratos/usr/cratos/varclim/IPSLCM5A/PROD/piControl2/OCE/Analyse/TS_MO/piControl2_18000101_27991231_1M_zomsfatl.nc')
depth = fref.variables['deptht'][:]

depthindicemin, depthindicemax = ct.coord2indice(depth,(300,10000))


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
    hc = fileo.variables['T']
else :
  datefile = datetime.date.today() 
  fileo = nc.Dataset(fileout,'w')
  fileo.date = str(datefile)
  #fileo.code = diag.codefile
  fileo.author = 'A. Germe'
  fileo.comment = 'The temperature averaged is computed as the weighted averaged of votemper.'
  fileo.expid = EXP_ID
  fileo.diagid = DIAG_ID
  time = fileo.createDimension('time',None)
  times = fileo.createVariable('time_counter','f',('time',))
  hc = fileo.createVariable('T','f',('time','x'))
  hc.units = 'degC'
  hc.long_name = 'Meridional averaged Temperature, 3D temperature averaged in %s'%dom
  hc.domain = '%s in mask_ORCA2.nc'%dom
  hc.Nlevels = '%i'%(len(depth[depthindicemin:depthindicemax+1]))
  hc.bottomleveldepth = '%f m'%(depth[depthindicemax])
  hc.topleveldepth = '%f m'%(depth[depthindicemin])
#
#
for year in range(yrdeb,yrfin+1) :
  #
  print """computing year %i"""%(year)
  tab,timex = ct.read(filein,'votemper',years=range(year,year+1))
  #
  # Poids sur l'horizontal et vertical
  Ndt = tab.shape[0] 
  Ndz = tab.shape[1] 
  dz = ma.repeat( ma.reshape(thkcello, (1,)+thkcello.shape), Ndt, axis=0)
  ds = ct.myweights()
  ds = ma.repeat( ma.reshape(ds, (1,)+ds.shape), Ndz, axis=0)
  ds = ma.repeat( ma.reshape(ds, (1,)+ds.shape), Ndt, axis=0)
  wt = ds*dz #dim = (t,z,y,x)
  #
  # Manque le mask horizonal !!!!!!!!!!!!!!!!!!!!!
  # possible pb lié à la dimension (,Y) au lieu de (1,Y) de l'array de sortie.
  tabwt = tab[:,depthindicemin:depthindicemax+1,:,:]*wt[:,depthindicemin:depthindicemax+1,:,:]
  tab_xy = tabwt.sum(axis=1) # dim = (t,y,x)
  tab_x = tab_xy.sum(axis=1) # dim = (t,x)

  V_xy = wt[:,depthindicemin:depthindicemax+1,:,:].sum(axis=1)
  V_y = V_xy.sum(axis=1)
  V_y = ma.repeat( ma.reshape(V_y, (1,)+dV_y.shape), Ndt, axis=0)
  #
  #
  tab_av = tab_x/V_y
  tab_yr = MA.average(tab_av,axis=0)

  if times.shape[0]==0 :
    times[0]=timex.num()[0]
    hc[0,:]=tab_amoyr
  else :
    i1=len(times)
    hc[i1,:]=tab_amoyr
    del  tab_av, tab_amoyr
  del timex.values
 
times.calendar=timex.calendar
times.units=timex.units
fileo.close()

# on efface les variables globales 
#del location EXP_ID




