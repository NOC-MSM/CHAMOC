#!/usr/bin/env cdat
# -*-coding:Latin-1 -*
# Created : 2013/11 (A. Germe)
# Modified: no 01
# CONSTRUCTION DES SERIES TEMPORELLES USUELLE, SIE, SIA, SIV
# Dans les MIZ comme définies par le NSIDC
#======================================================================== 
#global AG
#global EXP_ID, location, fileo
# Cet declacration en global est utile uniquement lorsque le diag
# est lancÃ© depuis la mÃ©thode "compute" de la class "diag"
#
# ============================================================================
import sys, os
import netCDF4 as nc
import datetime
import copy
import MA
#
from direxp import *
import climtools as ct
#======================================================================== 
# utilisation :
#        cdat calc_SIindex.py EXP_ID
# Exemple :
#        cdat -i calc_SIindex.py HISTNUD15
# =======================================================================
# =======================================================================
EXP_ID  = sys.argv[1]
if len(sys.argv)<3 :
  fin = None
else :
  fin = sys.argv[2]
#
DIAG_ID = 'GINDWFindex'
#
domain = 'GINIPSL'

# Repertoires des inputs :
# ~~~~~~~~~~~~~~~~~~~~~~~
exp = dexp[EXP_ID]

filein = exp.locfile('somxl010',realm='O')


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

# Definition de l'index
# ~~~~~~~~~~~~~~~~~~~~~~~
# ========================================================================
# Main routine
# ========================================================================
if not os.path.exists(dirout) : os.makedirs(dirout)
#
if os.path.exists(fileout) :
  fileo = nc.Dataset(fileout,'a')
  if 'DWF_%s'%domain in fileo.variables.keys() :
    dwf = fileo.variables['DWF_%s'%domain]
    #
    times = fileo.variables['time_counter']
    last_year_done = nc.num2date(times[-1],times.units).year
    last_year_to_do = yrfin
    yrdeb = last_year_done+1
    if fin is not None :
      last_year_to_do=int(fin)
    print last_year_done+1, last_year_to_do+1
  else : 
    print "No variable in file %s"%fileout
    sys.exit("Please remove %s to start again ! "%fileout)
else :
  datefile = datetime.date.today() 
  fileo = nc.Dataset(fileout,'w')
  fileo.date = str(datefile)
  #fileo.code = diag.codefile
  fileo.author = 'A. Germe'
  fileo.comment = 'The regional domain can be found in /net/argos/data/parvati/agglod/DATA/IPSLCM/otherMASK/Mask_ORCA2_MIZipsl.nc'
  time = fileo.createDimension('time',None)
  times = fileo.createVariable('time_counter','f',('time',))
  dwf = fileo.createVariable('DWF_%s'%domain,'f',('time',))
  dwf.units = 'm3'
  dwf.long_name = '%s deep water formation index computed as the volume of the convection patch = somxl010 * cell area'%domain
  #
#
#
#
#
for year in range(yrdeb,yrfin+1) :
  #
  print """computing year %i"""%(year)
  tab,timex = ct.read(filein,'somxl010',years=range(year,year+1))
  #
  if times.shape[0]==0 :
    times[:]=timex.num()
    tab_av  = ct.regional_average(tab,domain)
    #
    # Writing in netcdf file
    # ---------------------- 
    dwf[:]=tab_av.filled()
    del tab_av
  else :
    i1=len(times[:])
    times[i1:i1+12]=timex.num()
    tab_av  = ct.regional_average(tab,domain)
    #
    # Writing in netcdf file
    # ---------------------- 
    dwf[i1:i1+12]=tab_av.filled()
    del tab_av
  del timex.values
  #
  # fin du if
#
# fin de la boucle sur les années
times.calendar=timex.calendar
times.units=timex.units
fileo.close()

# on efface les variables globales 
#del location EXP_ID




