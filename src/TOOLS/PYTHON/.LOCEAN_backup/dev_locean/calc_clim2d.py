#!/usr/bin/env cdat
# -*-coding:Latin-1 -*
# Created : 2013/07 (A. Germe)
# Modified: no 01
# CONSTRUCTION D'UNE CLIM D'UN CHAMPS 2D : CHAMPS MOYEN, ECART-TYPE, TREND
#======================================================================== 
import sys, os
import netCDF4 as nc
import datetime
#
#import agutils as AG
from direxp import *
#======================================================================== 
# utilisation :
#        cdat ?
# Exemple :
#        cdat -i ?
# =======================================================================
EXP_ID = sys.argv[1]
DIAG_ID = 'clim2d'

# Repertoires des inputs :
# ~~~~~~~~~~~~~~~~~~~~~~~
exp = dexp[EXP_ID]
dirin=exp.loc('I')

fileinsic = exp.fname('soicecov')
fileinsit = exp.fname('iicethic')

timeu = 'seconds since %s-01-01 00:00:00'%(exp.datedeb[0:4])

# Repertoires des outputs :
# ~~~~~~~~~~~~~~~~~~~~~~~~~
exp = dexp[EXP_ID]

if exp.ismember :
  dirout = '/net/cratos/usr/cratos/varclim/agglod/mydiags/OUTPUTS/SeaIce/clim2d/%s/%s/%s/'%(exp.stream,exp.group,exp.ensemblename)
else :
  dirout = '/net/cratos/usr/cratos/varclim/agglod/mydiags/OUTPUTS/SeaIce/clim2d/%s/%s/'%(exp.stream,exp.group)
#
fileout = '%s%s_%s.nc'%(dirout,EXP_ID,DIAG_ID)

# Indices à cacluler
# ~~~~~~~~~~~~~~~~~~
listindex = ['SIA','SIE','SIV']

# années disponibles
# ~~~~~~~~~~~~~~~~~~
exp=dexp.get(EXP_ID, expe(EXP_ID))
[yrdeb,yrfin]=exp.years('sic',mod='I')
print('Dates available for '+EXP_ID+' : '+str(yrdeb)+'-'+str(yrfin))

# Definition de l'index
# ~~~~~~~~~~~~~~~~~~~~~~~
def INDEX(data) :
  if data is not None :
    sel = AG.domsel_dict['sel_NH']
    if EXP_ID in AG.listexp_sicpercent and var2D[location]=='sic' :
      data=data/100
    if location is 'SIE' :
      data[data<0.15]=0
      data[data>0.15]=1
    tab_av = AG.nemo_avxy(tab=data,dom_sel=sel)
    fileo.write(tab_av, id=location)
    del tab_av
  return data

# ========================================================================
# Main routine
# ========================================================================
if not os.path.exists(dirout) : os.makedirs(dirout)
#
var2D = dict(SIA='sic', SIE='sic', SIV='sit')
step_years = 5
step = dict()
data = dict()
#
#
if os.path.exists(fileout) :
  fileo = cdms.open(fileout,'r+')
  if listloc[0] in fileo.listvariable() :
    ax_time = fileo[listloc[0]].getTime()
    last_year_done = ax_time.asComponentTime()[-1].year
    last_year_to_do = exp.years('sic', mod='I')[-1]
    exp.year = range(last_year_done+1, last_year_to_do+1)
    print last_year_done+1, last_year_to_do+1
else :
  datefile = datetime.date.today() 
  fileo = cdms.open(fileout,'w')
  fileo.date = str(datefile)
  fileo.code = diag.codefile
  fileo.author = 'A. Germe'
#
# 
if exp.index('I') is not None :
# Pour ne pas tomber dans le cas ou l'on traite une seule annee a la fois...
  if exp.year is None :
     years =  exp.years('sic', mod='I')
     if years is not None :
       nyears = years[1] - years[0] + 1
  else :
     nyears = len(exp.year)
  if (nyears - 1)%step_years == 0 :
     step[exp] = step_years + 1
     if (nyears - 1)%step[exp] == 0 :
       step[exp] = step_years + 2
  for location in listloc :
    exp.read(var2D[location], mod='I', operator=INDEX, step_years=step.get(exp, step_years))
    
fileo.close()

# on efface les variables globales 
#del location EXP_ID




