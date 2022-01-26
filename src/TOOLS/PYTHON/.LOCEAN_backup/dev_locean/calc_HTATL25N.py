# -*-coding:Latin-1 -*
# Created : 2013/12 (A. Germe)
# Modified: no 03
# CONSTRUCTION DES SERIES TEMPORELLES AMOCmin, AMOCmax ,GMOCmin ...
# ============================================================================
import sys, os
import netCDF4 as nc
import datetime
import numpy.ma as ma
import numpy as N
#
from direxp import *
import climtools as ct
# ============================================================================
# utilisation :
# python -i calc_MOC_minmax.py EXP_ID
# Exemple :
#        cdat -i calc_MOC_minmax.py HISTNUD15 
#
# Index :
# ~~~~~~~
# AMOC == MOC Atlantique min et max
# GMOC == MOC sur diags globaux min et max
# IPMOC == MOC sur diags Indo-Pacifique min et max
# ============================================================================
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
#    tfin = datetime.datetime(years[-1],12,31) #31/12 de la dernière année
#    ideb = nc.date2index(tdeb,timeaxis,calendar=timeaxis.calendar,select='after#')
#    ifin = nc.date2index(tfin,timeaxis,calendar=timeaxis.calendar,select='befor#e')
#    timeval = timeaxis[ideb:ifin+1]
#    tab = f.variables[varname][ideb:ifin+1,:,:]
#  else :
#    tab = f.variables[varname][:,:,:]
#    timeval=timeaxis[:]
#  #  
#  f.close()
#  return tab, timeval, timeu, timecal
# -----------------------------------------------------------------------
def MOC(data,index) :
    data = N.average(data,axis=0) # moyenne annuelle
    var = index + 'min' 
    mocmin = N.min( data[depthindicemin[var]:depthindicemax[var],\
              latindicemin[var]:latindicemax[var]])
    var = index + 'max' 
    mocmax = N.max( data[depthindicemin[var]:depthindicemax[var],\
              latindicemin[var]:latindicemax[var]])
    return mocmin,mocmax
# ============================================================================
#                    
# ============================================================================
EXP_ID = sys.argv[1]
if len(sys.argv)<3 :
  fin = None
else :
  fin = sys.argv[2]
#
DIAG_ID = 'HTATL25N'

# Repertoires des inputs :
# ~~~~~~~~~~~~~~~~~~~~~~~~~
exp = dexp[EXP_ID]
dirin=exp.loc('O')
fileinatl = exp.locfile('sohtatl',realm='O')
#
# Repertoires des outputs :
# ~~~~~~~~~~~~~~~~~~~~~~~~~
if exp.ismember : 
  dirout = '/net/cratos/usr/cratos/varclim/agglod/mydiags/OUTPUTS/Ocean/%s/%s/%s/'%(exp.stream,exp.group,exp.ensemblename)
else :
  dirout =  '/net/cratos/usr/cratos/varclim/agglod/mydiags/OUTPUTS/Ocean/%s/%s/'%(exp.stream,exp.group)
fileout = '%s%s_%s.nc'%(dirout,EXP_ID,DIAG_ID)
#

# annÃ©es disponibles
# ~~~~~~~~~~~~~~~~~~
[yrdeb,yrfin]=years(fileinatl)
print('Dates available for %s : %i-%i'%(EXP_ID,yrdeb,yrfin))
if fin is not None :
  yrfin=int(fin)
  print('To your request, the computation will stop for yrfin = %s'%(fin))
#
#
# latitude axis and reference value
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
flat = nc.Dataset(fileinatl)
latref = flat.variables['lat'][:]
flat.close()
ilat25 = ct.find_nearest(latref,25)
lat25 = latref[ilat25]



# ========================================================================
# Main routine
# ========================================================================
if not os.path.exists(dirout) : os.makedirs(dirout)
#
if os.path.exists(fileout) :
  fileo = nc.Dataset(fileout,'a')
  htatl25n = fileo.variables['HTATL25N']
  times = fileo.variables['time_counter']
  if 'HTATL25N' in fileo.variables.keys() :
    last_year_done = nc.num2date(times[-1],times.units,calendar=times.calendar).year
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
  htatl25n = fileo.createVariable('HTATL25N','f',('time',))
  htatl25n.units = 'PW'
  htatl25n.long_name = 'Atlantic meridional heat transport at 25N. Extracted from the NEMO diag sohtatl in diaptr file'
  htatl25n.latitude=lat25
  htatl25n.latindex='%s with first index counted as 0'%ilat25
#
#
#
for year in range(yrdeb,yrfin+1) :
  #
  print """ Computing year %i"""%(year)
  tabatl,timex = ct.read(fileinatl,'sohtatl',years=range(year,year+1))

  # Moyenne annuelle
  tabyr = ma.average(tabatl,axis=0)

  if htatl25n.shape[0]==0 :
    htatl25n[0] = tabyr[ilat25,0]
    times[0] = timex.num()[0]
  else :
    i1=len(htatl25n) 
    htatl25n[i1] = tabyr[ilat25,0]
    times[i1] = timex.num()[0]
  del tabatl, timex.values
#
times.calendar = timex.calendar
times.units = timex.units  
fileo.close()

# the end
