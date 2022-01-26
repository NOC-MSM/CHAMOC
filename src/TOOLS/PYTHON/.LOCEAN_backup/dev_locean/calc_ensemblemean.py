#!/usr/bin/env cdat
# -*-coding:Latin-1 -*
# Created : 2014/01 (A. Germe)
# Modified: no 00
# CONSTRUCTION Du champs de moyenne d'ensemble d'une variable
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
from dirensemble import *
import climtools as ct
#======================================================================== 
# utilisation :
#        cdat calc_ensemblemean.py ENS_ID varid (yrfin)
# Exemple :
#        cdat calc_ensemblemean.py EPCT256 votemper 
#        cdat calc_ensemblemean.py WN votemper 2060
# =======================================================================
ENS_ID  = sys.argv[1]
varid = sys.argv[2]
if len(sys.argv)<4 :
  fin = None
else :
  fin = sys.argv[3]
#
DIAG_ID = 'ensemblemean'
#varid = 'votemper'
ens = dens[ENS_ID]
mbs = ens.listmember
Nmb = len(mbs)
expref = mbs[0]
exp=dexp[expref]
#
# Repertoires des outputs :
# ~~~~~~~~~~~~~~~~~~~~~~~~~
dirout = '/net/argos/data/parvati/agglod/mydiag3D/Ocean/%s/%s/%s/'%(ens.stream,ens.group,ENS_ID)
fileout = '%s%s_%s_%s.nc'%(dirout,ENS_ID,DIAG_ID,varid)

# à finir pour lire automatiquement yrdeb et yrfin
[yrdeb,yrfin]=exp.year
print('Dates available for %s : %i-%i'%(ENS_ID,yrdeb,yrfin))
#print('attention : yrdeb et yrfin sont codés en dure dans le script')
#print('a finir pour lecture automatique')
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
  if 'em_%s'%(varid) in fileo.variables.keys() :
    times = fileo.variables['time_counter']
    last_year_done = nc.num2date(times[-1],times.units,calendar=times.calendar).year
    last_year_to_do = yrfin
    yrdeb = last_year_done+1
    if fin is not None :
      last_year_to_do=int(fin)
    print last_year_done+1, last_year_to_do+1
    emnc  = fileo.variables['em_%s'%(varid)]
    stdnc = fileo.variables['em_%s'%(varid)]
else :
  datefile = datetime.date.today() 
  fileo = nc.Dataset(fileout,'w')
  fileo.date = str(datefile)
  #fileo.code = 'climtools.climato'
  fileo.author = 'A. Germe'
  fileo.comment = 'Has been computed with the script calc_ensemblemean.py'
  fileo.ensid = ENS_ID
  fileo.diagid = '%s_%s'%(DIAG_ID,varid)
  #
  k = fileo.createDimension('k',31)
  i = fileo.createDimension('i',149)
  j = fileo.createDimension('j',182)
  t = fileo.createDimension('time',None)
  times  = fileo.createVariable('time_counter','f',('time',))
  emnc = fileo.createVariable('em_votemper','f',('time','k','i','j'))
  stdnc  = fileo.createVariable('std_votemper','f',('time','k','i','j'))
  #
  emnc.long_name = 'Ensemble mean'
  stdnc.long_name = 'Standard deviation'
#
#
for year in range(yrdeb,yrfin+1) :
  #
  print """computing year %i"""%(year)
  #
  ensemble = ma.empty([Nmb,12,31,149,182])
  for mb in mbs :
    # Repertoires des inputs :
    # ~~~~~~~~~~~~~~~~~~~~~~~
    EXP_ID =  mb
    mbindex=mbs.index(mb)
    print(EXP_ID)
    exp = dexp[EXP_ID]
    filein = exp.locfile(varid,realm='O')
    #
    tab,timex = ct.read(filein,varid,years=range(year,year+1))
    ensemble[mbindex,...] = tab
  #
  print('Computing ensemble mean and std')
  em = ensemble.mean(axis=0)
  sd = ensemble.std(axis=0)
  #
  # writing in netcdf
  if emnc.shape[0]==0 :
    emnc[0:12,...]  = em
    stdnc[0:12,...] = sd
    times[:] = timex.num()
  else :
    i1 = emnc.shape[0]
    emnc[i1:i1+12,...]  = em
    stdnc[i1:i1+12,...] = sd
    times[i1:i1+12] = timex.num()
#
times.calendar = timex.calendar
times.units=timex.units
emnc.units = 'degC' # à changer pour aller chercher l'info dans le fichier source
stdnc.units = 'degC'
print('done !')
fileo.close()






