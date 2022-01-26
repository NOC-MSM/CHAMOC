#!/usr/bin/env cdat
# -*-coding:Latin-1 -*
# Created : 2013/11 (A. Germe)
# Modified: no 02
# !!!!! Par rapport à la version 01, j'ai rajouter la pondération de l'épaisseur par la SIC pour le volume ! C'était fait pour le SIindex sur l'Arctique totale.
# le fait que ca n'était pas dans la version 01 est un oubli.
# Il faut recacluler toutes les séries temporelles régionales.
#
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
import numpy.ma as ma
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
DIAG_ID = 'SIindex_REGIONSipsl'
#
domains = ['NSARCTON','BARKARAS','BERINGXX','LABIPSL','GINIPSL','IRMIPSL','OKHIPSL']

# Repertoires des inputs :
# ~~~~~~~~~~~~~~~~~~~~~~~
exp = dexp[EXP_ID]

fileinsic = exp.locfile('soicecov',realm='I')
fileinsit = exp.locfile('iicethic',realm='I')


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
sia=dict()
sie=dict()
siv=dict()
#
if os.path.exists(fileout) :
  fileo = nc.Dataset(fileout,'a')
  if 'SIA_GINIPSL' in fileo.variables.keys() :
    for dom in domains : 
      sia[dom] = fileo.variables['SIA_%s'%dom]
      sie[dom] = fileo.variables['SIE_%s'%dom]
      siv[dom] = fileo.variables['SIV_%s'%dom]
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
  fileo.comment = 'Regional  domains are chosen in the aim of capture the regional variability in ISL-CM, and therefore take into account the overestimation of sea ice extent in the model. The regional domain can be found in /net/argos/data/parvati/agglod/DATA/IPSLCM/otherMASK/Mask_ORCA2_MIZipsl.nc'
  time = fileo.createDimension('time',None)
  times = fileo.createVariable('time_counter','f',('time',))
  for dom in domains :
    sia[dom] = fileo.createVariable('SIA_%s'%dom,'f',('time',))
    sie[dom] = fileo.createVariable('SIE_%s'%dom,'f',('time',))
    siv[dom] = fileo.createVariable('SIV_%s'%dom,'f',('time',))
    sia[dom].units = 'm2'
    sie[dom].units = 'm2'
    siv[dom].units = 'm3'
    sia[dom].long_name = '%s sea ice area'%dom
    sie[dom].long_name = '%s sea ice extent'%dom
    siv[dom].long_name = '%s sea ice volume'%dom
  #

#
#
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
  if times.shape[0]==0 :
    times[:]=timex.num()
    for dom in domains : 
      tab_av  = ct.regional_average(tab,dom)
      tabe_av = ct.regional_average(tabe,dom)
      tabv_av = ct.regional_average(ma.multiply(tabv,tab),dom)
      #
      # Writing in netcdf file
      # ---------------------- 
      sia[dom][:]=tab_av.filled()
      sie[dom][:]=tabe_av.filled()
      siv[dom][:]=tabv_av.filled()  
      del tab_av, tabe_av, tabv_av
  else :
    i1=len(times[:])
    times[i1:i1+12]=timex.num()
    for dom in domains : 
      tab_av  = ct.regional_average(tab,dom)
      tabe_av = ct.regional_average(tabe,dom)
      tabv_av = ct.regional_average(tabv,dom)
      #
      # Writing in netcdf file
      # ---------------------- 
      sia[dom][i1:i1+12]=tab_av.filled()
      sie[dom][i1:i1+12]=tabe_av.filled()
      siv[dom][i1:i1+12]=tabv_av.filled()
      del tab_av, tabe_av, tabv_av
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




