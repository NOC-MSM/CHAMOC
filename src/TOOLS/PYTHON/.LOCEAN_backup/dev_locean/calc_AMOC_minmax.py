# -*-coding:Latin-1 -*
# Created : 2013/12 (A. Germe)
# Modified: no 03
# CONSTRUCTION DES SERIES TEMPORELLES AMOCmin, AMOCmax ,GMOCmin ...
# ============================================================================
import sys, os
import netCDF4 as nc
import datetime
import MA
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
def coord2indice(axe,axlim) :
  coordindice = MA.masked_where(MA.logical_or(axe<axlim[0],axe>axlim[1]),MA.arange((len(axe))))
  return MA.minimum(coordindice), MA.maximum(coordindice)
# -----------------------------------------------------------------------
# Les boites Drakkar : 
fref = nc.Dataset('/net/cratos/usr/cratos/varclim/IPSLCM5A/PROD/piControl2/OCE/Analyse/TS_MO/piControl2_18000101_27991231_1M_zomsfatl.nc')
lat = fref.variables['lat'][:]
depth = fref.variables['depthw'][:]
#
latindicemin = dict() ; latindicemax = dict()
depthindicemin = dict() ; depthindicemax = dict()
#
latindicemin['AMOCmax'], latindicemax['AMOCmax'] = coord2indice(lat,(0,60)) # valeurs Monitoring Drakkar pour l'Atlantique
depthindicemin['AMOCmax'], depthindicemax['AMOCmax'] = coord2indice(depth, (500,2000)) # valeurs Monitoring Drakkar pour l'Atlantique
#
latindicemin['AMOCmin'], latindicemax['AMOCmin'] = coord2indice(lat,(-20,40)) # valeurs Monitoring Drakkar pour l'Atlantique
depthindicemin['AMOCmin'], depthindicemax['AMOCmin'] = coord2indice(depth, (2000,5500)) # valeurs Monitoring Drakkar pour l'Atlantique
#
latindicemin['GMOCmax'], latindicemax['GMOCmax'] = coord2indice(lat,(20,60)) # valeurs Monitoring Drakkar pour le global
depthindicemin['GMOCmax'], depthindicemax['GMOCmax'] = coord2indice(depth, (500,2000)) # valeurs Monitoring Drakkar pour le global
#
latindicemin['GMOCmin'], latindicemax['GMOCmin'] = coord2indice(lat,(-40,30)) # valeurs Monitoring Drakkar pour le global
depthindicemin['GMOCmin'], depthindicemax['GMOCmin'] = coord2indice(depth, (2000,5500)) # valeurs Monitoring Drakkar pour le global
#
latindicemin['IPMOCmax'], latindicemax['IPMOCmax'] = coord2indice(lat,(15,50)) # valeurs Monitoring Drakkar pour l'Indo-Pacifique
depthindicemin['IPMOCmax'], depthindicemax['IPMOCmax'] = coord2indice(depth, (100,1000)) # valeurs Monitoring Drakkar pour l'Indo-Pacifique
#
latindicemin['IPMOCmin'], latindicemax['IPMOCmin'] = coord2indice(lat,(-30,20)) # valeurs Monitoring Drakkar pour l'Indo-Pacifique
depthindicemin['IPMOCmin'], depthindicemax['IPMOCmin'] = coord2indice(depth, (1000,5500)) # valeurs Monitoring Drakkar pour l'Indo-Pacifique
#
# ----------------------------------------------------------------------------
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
DIAG_ID = 'AMOC_minmax'

# Repertoires des inputs :
# ~~~~~~~~~~~~~~~~~~~~~~~~~
exp = dexp[EXP_ID]
dirin=exp.loc('O')
fileinatl = exp.locfile('zomsfatl',realm='O')
#
# Repertoires des outputs :
# ~~~~~~~~~~~~~~~~~~~~~~~~~
if exp.ismember : 
  dirout = '/net/cratos/usr/cratos/varclim/agglod/mydiags/OUTPUTS/Ocean/%s/%s/%s/'%(exp.stream,exp.group,exp.ensemblename)
else :
  dirout =  '/net/cratos/usr/cratos/varclim/agglod/mydiags/OUTPUTS/Ocean/%s/%s/'%(exp.stream,exp.group)
fileout = '%s%s_%s.nc'%(dirout,EXP_ID,DIAG_ID)
#
# Indices Ã  cacluler
# ~~~~~~~~~~~~~~~~~~
listindex = ['AMOC']

# annÃ©es disponibles
# ~~~~~~~~~~~~~~~~~~
[yrdeb,yrfin]=years(fileinatl)
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
  amocmin = fileo.variables['AMOCmin']
  amocmax = fileo.variables['AMOCmax']
  times = fileo.variables['time_counter']
  if 'AMOCmin' in fileo.variables.keys() :
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
  amocmin = fileo.createVariable('AMOCmin','f',('time',))
  amocmax = fileo.createVariable('AMOCmax','f',('time',))
  amocmin.units = 'Sv'
  amocmax.units = 'Sv'
  amocmin.long_name = 'Atlantic meridional overturning circulation minimum value'
  amocmax.long_name = 'Atlantic meridional overturning circulation maximum value'
#
#
for year in range(yrdeb,yrfin+1) :
  #
  print """ Computing year %i"""%(year)
  tabatl,timex = ct.read(fileinatl,'zomsfatl',years=range(year,year+1))

  if amocmin.shape[0]==0 :
    amocmin[0],amocmax[0] = MOC(tabatl,'AMOC')
    times[0] = timex.num()[0]
  else :
    i1=len(amocmin) 
    amocmin[i1], amocmax[i1] = MOC(tabatl,'AMOC')
    times[i1] = timex.num()[0]
  del tabatl, timex.values
#
times.calendar = timex.calendar
times.units = timex.units  
fileo.close()

# the end
