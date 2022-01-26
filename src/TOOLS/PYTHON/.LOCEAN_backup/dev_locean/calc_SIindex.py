 #!/usr/bin/env cdat
# -*-coding:Latin-1 -*
# Created : 2013/11 (A. Germe)
# Modified: no 01
# CONSTRUCTION DES SERIES TEMPORELLES USUELLE, SIE, SIA, SIV
#======================================================================== 
# Comments :
# par rapport à la version dans mydiags/SeaIce,
# le paclage MA est remplacé par numpy.ma
# 
#
# ============================================================================
import sys, os
import netCDF4 as nc
import datetime
import copy
import numpy.ma as ma
import numpy as N
#
from direxp import *
import climtools as ct
#import distutils # for udunits
#import udunits # marche pas pour l'instant, voir comment l'installer
# utile pour la conversion temps relatif, temps réaliste
#======================================================================== 
# utilisation :
#        cdat calc_SIindex.py EXP_ID
# Exemple :
#        cdat -i calc_SIindex.py HISTNUD15
# =======================================================================
# Some functions
# ==============
def years(filein) :
  info=filein.split('/')[-1]
  info=info.split('_')
  yrdeb=int(info[1][0:4])
  yrfin=int(info[2][0:4])
  return [yrdeb,yrfin]
# =======================================================================
EXP_ID  = sys.argv[1]
if len(sys.argv)<3 :
  fin = None
else :
  fin = sys.argv[2]
#
DIAG_ID = 'SIindex_NH'
domain = 'NHEMISPH'

# Repertoires des inputs :
# ~~~~~~~~~~~~~~~~~~~~~~~
exp = dexp[EXP_ID]

fileinsic = exp.locfile('soicecov')
fileinsit = exp.locfile('iicethic')

# Repertoires des outputs :
# ~~~~~~~~~~~~~~~~~~~~~~~~~
#diag = ddiag[DIAG_ID]
if exp.ismember :
  dirout = '/net/cratos/usr/cratos/varclim/agglod/mydiags/OUTPUTS/SeaIce/%s/%s/%s/'%(exp.stream,exp.group,exp.ensemblename)
else :
  dirout = '/net/cratos/usr/cratos/varclim/agglod/mydiags/OUTPUTS/SeaIce/%s/%s/'%(exp.stream,exp.group)
fileout = '%s%s_%s.nc'%(dirout,EXP_ID,DIAG_ID)

# Indices Ã  cacluler
# ~~~~~~~~~~~~~~~~~~
listindex = ['SIA','SIE','SIV']

# années disponibles
# ~~~~~~~~~~~~~~~~~~
[yrdeb,yrfin]=years(fileinsic)
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
  sia = fileo.variables['SIA']
  sie = fileo.variables['SIE']
  siv = fileo.variables['SIV']
  times = fileo.variables['time_counter']
  if listindex[0] in fileo.variables.keys() :
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
  sia = fileo.createVariable('SIA','f',('time',))
  sie = fileo.createVariable('SIE','f',('time',))
  siv = fileo.createVariable('SIV','f',('time',))
  sia.units = 'm2'
  sie.units = 'm2'
  siv.units = 'm3'
  sia.long_name = 'Arctic sea ice area'
  sie.long_name = 'Arctic sea ice extent'
  siv.long_name = 'Arctic sea ice volume'
  #times.units=timeu

#
#
for year in range(yrdeb,yrfin+1) :
  #
  print """computing year %i"""%(year)
  tab,timex = ct.read(fileinsic,'soicecov',years=range(year,year+1))
  tabe = copy.deepcopy(tab)
  tabe[tab<0.15]=0
  tabe[tab>0.15]=1
  tabv,timex = ct.read(fileinsit,'iicethic',years=range(year,year+1))
  #
  tab_av  = ct.regional_average(tab,domain)
  tabe_av = ct.regional_average(tabe,domain)
  tabv_av = ct.regional_average(ma.multiply(tabv,tab),domain)

  # Writing in netcdf file
  # ---------------------- 
  if sia.shape[0]==0 :
    sia[:]=tab_av.filled()
    sie[:]=tabe_av.filled()
    siv[:]=tabv_av.filled()
    times[:]=timex.num()
  else :
    i1=len(sia)
    sia[i1:i1+12]=tab_av.filled()
    sie[i1:i1+12]=tabe_av.filled()
    siv[i1:i1+12]=tabv_av.filled()
    times[i1:i1+12]=timex.num()
  del tab_av, tabe_av, tabv_av
 
times.calendar=timex.calendar
times.units=timex.units  
fileo.close()
# the end




