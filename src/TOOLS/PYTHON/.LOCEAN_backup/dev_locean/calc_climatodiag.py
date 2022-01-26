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
import numpy.ma as ma
import numpy as N
#
from direxp import *
import climtools as ct
#======================================================================== 
# utilisation :
#        python calc_climatodiag.py EXP_ID DIAG_ID freq
# Exemple :
#        python calc_climatodiag.py piControl2 T300_2D_YE YE 
# =======================================================================
EXP_ID   = sys.argv[1]
DIAG_ID  = sys.argv[2]
variable = sys.argv[3]
freq     = sys.argv[4]

# Repertoires des inputs :
# ~~~~~~~~~~~~~~~~~~~~~~~
exp = dexp[EXP_ID]

if exp.ismember :
  dirin = '/net/cratos/usr/cratos/varclim/agglod/mydiags/OUTPUTS/Ocean/%s/%s/%s/'%(exp.stream,exp.group,exp.ensemblename)
else :
  dirin = '/net/cratos/usr/cratos/varclim/agglod/mydiags/OUTPUTS/Ocean/%s/%s/'%(exp.stream,exp.group)
filein = '%s%s_%s.nc'%(dirin,EXP_ID,DIAG_ID)

fileout='%sclimato_%s_%s.nc'%(dirin,EXP_ID,DIAG_ID)
# ========================================================================
# Main routine
# ========================================================================
#
hc= dict()
if os.path.exists(fileout) :
  raise IOError('%s already exist'%fileout)
#
# Creating netcdf output file
# ---------------------------
datefile = datetime.date.today() 
fileo = nc.Dataset(fileout,'w')
fileo.date = str(datefile)
fileo.author = 'A. Germe'
fileo.comment = 'Created by the standard python script calc_climatodiag.py'
fileo.expid = EXP_ID
fileo.diagid = '%s climatology'%DIAG_ID
#
# dimension
if freq=='YE' :
  time = fileo.createDimension('time',1)
elif freq=='MO':
  time = fileo.createDimension('time',12)
elif freq=='DA':
  time = fileo.createDimension('time',365)
x = fileo.createDimension('x',182)
y = fileo.createDimension('y',149)
#
# variables
times = fileo.createVariable('time_counter','f',('time',))
clim = fileo.createVariable('clim','f',('time','y','x'))
sd = fileo.createVariable('sd','f',('time','y','x'))
#
# Computing climatology
# ---------------------
tab,timex = ct.read(filein,variable)
#
climtemp,sdtemp=ct.climato(tab,timex,freq=freq)
#
# Writing in netcdf file
# ----------------------
clim[:,...] = climtemp
sd[:,...]   = sdtemp

fileo.close()





