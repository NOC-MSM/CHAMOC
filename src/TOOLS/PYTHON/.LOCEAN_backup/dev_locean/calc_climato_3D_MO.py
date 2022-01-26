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
varname = sys.argv[2]
exp = dexp[EXP_ID]
if len(sys.argv)<4 :
  yrdeb = exp.year[0]
  yrfin = exp.year[1]
else :
  yrdeb = int(sys.argv[3])
  yrfin = int(sys.argv[4])
#
DIAG_ID = 'clim_%s'%(varname)

# Repertoires des inputs :
# ~~~~~~~~~~~~~~~~~~~~~~~

filein = exp.locfile(varname,realm='O')
#
#
# Repertoires des outputs :
# ~~~~~~~~~~~~~~~~~~~~~~~~~
#diag = ddiag[DIAG_ID]
if exp.ismember :
  dirout = '/net/cratos/usr/cratos/varclim/agglod/clim/Ocean/%s/%s/%s/'%(exp.stream,exp.group,exp.ensemblename)
else :
  dirout = '/net/cratos/usr/cratos/varclim/agglod/clim/Ocean/MO/%s/%s/'%(exp.stream,exp.group)
fileout = '%s%s_%s_%s_%s.nc'%(dirout,EXP_ID,DIAG_ID,yrdeb,yrfin)


# ========================================================================
# Main routine
# ========================================================================
tab,timex = ct.read(filein,varname,years=range(yrdeb,yrfin+1))

tabclim,tabstd=ct.climato(tab,timex)


if not os.path.exists(dirout) : os.makedirs(dirout)
#
datefile = datetime.date.today() 
fileo = nc.Dataset(fileout,'w')
fileo.date = str(datefile)
#fileo.code = 'climtools.climato'
fileo.author = 'A. Germe'
fileo.comment = 'Has been computed with python diagnostic calc_climato_votemper.py using the function climato of the personal modul climtools.py. Flag 1.'
fileo.expid = EXP_ID
fileo.diagid = 'climatology'
fileo.period = '%s-%s included'%(yrdeb,yrfin)
fileo.freq = 'MO'
#
k = fileo.createDimension('k',tab.shape[1])
i = fileo.createDimension('i',tab.shape[2])
j = fileo.createDimension('j',tab.shape[3])
t = fileo.createDimension('time',12)
times  = fileo.createVariable('time_counter','f',('time',))
climnc = fileo.createVariable('clim_%s'%varname,'f',('time','k','i','j'))
stdnc  = fileo.createVariable('std_%s'%varname,'f',('time','k','i','j'))
#
times.units='days since 0001-01-01'
times.calendar='noleap'
times[:]=range(1,360,30)
#
climnc[...] = tabclim
stdnc[...]  = tabstd

fileo.close()






