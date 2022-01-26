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
#        cdat calc_AMOindex.py EXP_ID (yrfin)
# Exemple :
#        cdat calc_AMOindex.py piControl2 
#        cdat calc_AMOindex.py piControl2 1805
# =======================================================================
# Valeurs utiles
Cp = 4181.3*1e3 # J/(m3*K) Valeur donn�e par Pablo

# =======================================================================
EXP_ID  = sys.argv[1]
if len(sys.argv)<3 :
  fin = None
else :
  fin = sys.argv[2]
#
DIAG_ID = 'HCZ_MO'

# Repertoires des inputs :
# ~~~~~~~~~~~~~~~~~~~~~~~
exp = dexp[EXP_ID]
domains = ['AMO','PACIFIC','ATLTROP10','PACTROP10']

filein = exp.locfile('votemper',realm='O')
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
hc= dict()
if os.path.exists(fileout) :
  fileo = nc.Dataset(fileout,'a')
  if 'HCZ_AMO' in fileo.variables.keys() :
    times = fileo.variables['time_counter']
    last_year_done = nc.num2date(times[-1],times.units).year
    last_year_to_do = yrfin
    yrdeb = last_year_done+1
    if fin is not None :
      last_year_to_do=int(fin)
    print last_year_done+1, last_year_to_do+1
  for dom in domains :
    hc[dom] = fileo.variables['HCZ_%s'%dom]
else :
  datefile = datetime.date.today() 
  fileo = nc.Dataset(fileout,'w')
  fileo.date = str(datefile)
  #fileo.code = diag.codefile
  fileo.author = 'A. Germe'
  fileo.comment = 'The HC is computed as the spatial integration of Cp*votemper*thkcello*e1t*e2t'
  time = fileo.createDimension('time',None)
  level  = fileo.createDimension('level',31) 
  times = fileo.createVariable('time_counter','f',('time',))
  depthaxis = fileo.createVariable('deptht','f',('level',))
  depthaxis[:]=depth
  depthaxis.units='m'
  for dom in domains :
    hc[dom] = fileo.createVariable('HCZ_%s'%dom,'f',('time','level'))
    hc[dom].units = '1e22 J'
    hc[dom].long_name = 'Heat content in %s'%dom
    hc[dom].domain = '%s in mask_ORCA2.nc'%dom
#
#
for year in range(yrdeb,yrfin+1) :
  #
  print """computing year %i"""%(year)
  tab,timex = ct.read(filein,'votemper',years=range(year,year+1))
  #
  # heat content par unit� de surface :
  HC_2d = Cp*tab[:,:,:,:]*thkcello[:,:,:]
 
  if times.shape[0]==0 :
    times[:]=timex.num()
    for dom in domains :
      tab_av = ct.regional_average(HC_2d,dom,operation='sum')
      #
      # Writing in netcdf file
      # ---------------------- 
      hc[dom][:,:]=tab_av.filled()*1e-22
      del tab_av
  else :
    i1=len(times)
    times[i1:i1+12]=timex.num()
    for dom in domains : 
      tab_av = ct.regional_average(HC_2d,dom,operation='sum')
      #
      # Writing in netcdf file
      # ---------------------- 
      hc[dom][i1:i1+12,:]=tab_av.filled()*1e-22
      del  tab_av
  del timex.values
 
times.calendar=timex.calendar
times.units=timex.units
fileo.close()

# on efface les variables globales 
#del location EXP_ID



