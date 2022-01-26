# -*-coding:Latin-1-*
# =========================================================================
# Packages de fonctions utilse à l'analyse de données climatiques
#
# Author : A. Germe
# 25 Nov. 2013
# =========================================================================
import sys, os
import netCDF4 as nc
import datetime
#
import MA
import numpy as N
from scipy import stats as S
#
from direxp import *
from myaxes import *
import climtools as ct
# =========================================================================
def readfield(dirin,filein,varname,years=None) :
  try :
    f=nc.Dataset(dirin+filein)
  except :
    """Couldn't find the file %s"""%(dirin+filein)
  #tab = f.variables[varname][0:12,:,:]
  timeaxis = f.variables['time_counter']
  timeu = timeaxis.units
  timecal = timeaxis.calendar
  #
  if years is not None :
    tdeb = datetime.datetime(years[0],1,1) # 1er Jan de la 1ere année
    tfin = datetime.datetime(years[-1],12,31,23,59,00) #31/12 de la dernière année
    ideb = nc.date2index(tdeb,timeaxis,calendar=timeaxis.calendar,select='after')
    ifin = nc.date2index(tfin,timeaxis,calendar=timeaxis.calendar,select='before')
    timeval = timeaxis[ideb:ifin+1]
    tab = f.variables[varname][ideb:ifin+1,:,:]
  else :
    tab = f.variables[varname][:,:,:]
    timeval=timeaxis[:]
  #  
  f.close()
  return tab, timeval, timeu, timecal
# =======================================================================
dirin ="/net/cratos/usr/cratos/varclim/agglod/DATA/IPSLCM/IPSLCM5A/piControl2/OCE/Analyse/TS_DA/"
filein = "piControl2_20000101_21991231_1D_sosstsst.nc"
#
period=(2066,2066)
outdir=dirin
varname='sosstsst'
fileout = "piControl2_%i0101_%i1231_1D_sosstsst.nc"%(period)
tab, timeval, timeu,timecal = readfield(dirin,filein,varname=varname,years=period)

# WRITE NETCDF
fileo = nc.Dataset(fileout,'w')
fileo.date = str(datetime.date.today())
fileo.author = 'A. Germe'
fileo.code = 'exctract_period'
fileo.period = '%i-%i'%period
fileo.description = 'Selected period extracting from %s/%s'%(dirin,filein)
i = fileo.createDimension('i',tab.shape[1])
j = fileo.createDimension('j',tab.shape[2])
t = fileo.createDimension('time',len(timeval))
climnc = fileo.createVariable('sosstsst','f',('time','i','j'))
time = fileo.createVariable('time','f',('time',))
time.units=timeu
time.calendar=timecal
#
climnc[...]=tab
time[:]=timeval
#
fileo.close()

