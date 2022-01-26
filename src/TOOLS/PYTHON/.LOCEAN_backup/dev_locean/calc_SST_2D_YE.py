# -*-coding:Latin-1 -*
# Created : 2015/06 (A. Germe)
# Modified: no 00
# CONSTRUCTION DE LA MOYENN ANNUELLE DU CHAMPS 2D SOSSTSST 
#======================================================================== 
import sys, os
import netCDF4 as nc
import datetime
import copy
import numpy.ma as ma
import numpy as N
#
from direxp import *
import climtools as ct
#======================================================================== 
# utilisation :
#        cdat calc_T300_2D_YE.py EXP_ID (yrfin)
# Exemple :
#        cdat calc_T300_2D_YE.py piControl2 
#        cdat calc_T300_2D_YE.py piControl2 1805
# =======================================================================
EXP_ID  = sys.argv[1]
if len(sys.argv)<3 :
  fin = None
else :
  fin = sys.argv[2]
#
DIAG_ID = 'SST_2D_YE'


# Repertoires des inputs :
# ~~~~~~~~~~~~~~~~~~~~~~~
exp = dexp[EXP_ID]
filein = exp.locfile('sosstsst',realm='O')
#

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
  if 'SST' in fileo.variables.keys() :
    times = fileo.variables['time_counter']
    last_year_done = nc.num2date(times[-1],times.units,calendar=times.calendar).year
    last_year_to_do = yrfin
    yrdeb = last_year_done+1
    if fin is not None :
      last_year_to_do=int(fin)
    print last_year_done+1, last_year_to_do+1
    hc = fileo.variables['SST']
else :
  datefile = datetime.date.today() 
  fileo = nc.Dataset(fileout,'w')
  fileo.date = str(datefile)
  #fileo.code = diag.codefile
  fileo.author = 'A. Germe'
  fileo.comment = 'The temperature average is computed as the yearly average of sosstsst.'
  fileo.expid = EXP_ID
  fileo.diagid = DIAG_ID
  #
  #
  time = fileo.createDimension('time',None)
  x = fileo.createDimension('x',182)
  y = fileo.createDimension('y',149)
  #
  #
  times = fileo.createVariable('time_counter','f',('time',))
  hc = fileo.createVariable('SST','f',('time','y','x'))
  hc.units = 'degC'
  hc.long_name = 'Mean Sea Surface Temperature'
#
#
for year in range(yrdeb,yrfin+1) :
  #
  print """computing year %i"""%(year)
  tab,timex = ct.read(filein,'sosstsst',years=range(year,year+1))
  #
  # Annual mean
  tabyr = ma.average(tab,axis=0)
  output = ma.reshape(tabyr, (1,)+tabyr.shape)
  #
  # Writing in netcdf file
  # ---------------------- 
  if times.shape[0]==0 :
    times[0]=timex.num()[0]
    hc[0,...]=tabyr
  else :
    i1=len(times)
    times[i1]=timex.num()[0]
    hc[i1,...]=tabyr
  del  tab, tabyr
  del timex.values
#
times.calendar=timex.calendar
times.units=timex.units
fileo.close()

# on efface les variables globales 
#del location EXP_ID




