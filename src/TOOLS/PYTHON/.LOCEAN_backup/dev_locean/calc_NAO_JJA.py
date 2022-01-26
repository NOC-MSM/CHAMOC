#!/usr/bin/env cdat
# -*-coding:Latin-1 -*
# Created : 2014/01 (A. Germe)
# Modified: no 00
# CONSTRUCTION DE LA SERIE TEMPORELLE AMO index
#======================================================================== 
import sys, os
import netCDF4 as nc
import datetime
import copy
import MA
import numpy as N
import math
#
from direxp import *
import climtools as ct
#
# pour verification
from matplotlib import pyplot as plt
#======================================================================== 
# utilisation :
#        cdat calc_NAO.py EXP_ID (yrfin)
# Exemple :
#        cdat calc_NAO.py piControl2 
#        cdat calc_NAO.py piControl2 1805
# =======================================================================
# =======================================================================
EXP_ID  = sys.argv[1]
if len(sys.argv)<3 :
  fin = None
else :
  fin = sys.argv[2]
#
DIAG_ID = 'NAO_JJA'

# Repertoires des inputs :
# ~~~~~~~~~~~~~~~~~~~~~~~
exp = dexp[EXP_ID]

filein = exp.locfile('slp',realm='A')

# Repertoires des outputs :
# ~~~~~~~~~~~~~~~~~~~~~~~~~
#diag = ddiag[DIAG_ID]
if exp.ismember :
  dirout = '/net/cratos/usr/cratos/varclim/agglod/mydiags/OUTPUTS/Atmosphere/%s/%s/%s/'%(exp.stream,exp.group,exp.ensemblename)
else :
  dirout = '/net/cratos/usr/cratos/varclim/agglod/mydiags/OUTPUTS/Atmosphere/%s/%s/'%(exp.stream,exp.group)
fileout = '%s%s_%s.nc'%(dirout,EXP_ID,DIAG_ID)

# annÃ©es disponibles
# ~~~~~~~~~~~~~~~~~~
[yrdeb,yrfin]=exp.year
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
doit='y'
if os.path.exists(fileout) :
  doit = raw_input("WARNING : %s already exist !! Do you wan't to replace it ?(y/n)")
# #
# #
if doit=='y' :
  print """Loading time series %i-%i"""%(yrdeb,yrfin)
  tab,timex,lon,lat = ct.readfield(filein,'slp',years=range(yrdeb,yrfin+1))
  
  #
  # moyenne saisonnière
  tabseas,timeseas = ct.seasonalmean(tab,timex,season='JJA')
  #
  # select the domain
  ymin,ymax = ct.coord2indice(lat.values,(20,80))
  xmin,xmax = ct.coord2indice(lon.values,(-90,40))
  tabdom = tabseas[:,ymin:ymax,xmin:xmax]
  Nt,Ny,Nx=tabdom.shape
  M = tabdom.reshape(Nt,Ny*Nx)
  #
  # weights :
  wty   = N.array([math.cos(x*math.pi/180) for x in lat.values[ymin:ymax]])
  wtxy  = N.repeat(N.reshape(wty,(Ny,1)),Nx,axis=1)
  wttxy = N.repeat(N.reshape(wtxy,(1,Ny,Nx)),Nt,axis=0)
  wt = wttxy.reshape(Nt,Ny*Nx)
  
  print "Computing eofs ..."
  varexp,eofs,pcs = ct.eof_eco(M,wt=wt)
  EOF1 = N.reshape(eofs[:,0],(Ny,Nx))/wtxy
  EOF2 = N.reshape(eofs[:,1],(Ny,Nx))/wtxy
  PC1  = pcs[:,0]
  PC2  = pcs[:,1]
  # On peut aussi obtenir les EOF physique en projettant les données sur les PC
  # MC = M - M.mean(axis=0)  
  # EOF1 = N.reshape(N.dot(MC.transpose(),PC1),(Ny,Nx))
  # EOF2 = N.reshape(N.dot(MC.transpose(),PC2),(Ny,Nx))
  
  # Writing in netcdf file
  # ---------------------- 
  datefile = datetime.date.today() 
  fileo = nc.Dataset(fileout,'w')
  fileo.date = str(datefile)
  fileo.code = "calc_NAO_JJA.py"
  fileo.author = 'A. Germe'
  fileo.comment = 'The NAO and EAP are computed as the first and second EOF of SLP respectively'
  londim = fileo.createDimension('lon',Nx)
  latdim = fileo.createDimension('lat',Ny)
  time = fileo.createDimension('time',None)
  #
  times = fileo.createVariable('time_counter','f',('time',))
  lonnc = fileo.createVariable('lon','f',('lon',))
  latnc = fileo.createVariable('lat','f',('lat',))
  #
  nao = fileo.createVariable('NAO','f',('lat','lon'))
  eap = fileo.createVariable('EAP','f',('lat','lon'))
  nao_pc = fileo.createVariable('NAO_PC','f',('time',))
  eap_pc = fileo.createVariable('EAP_PC','f',('time',))
  nao.units = 'hPa'
  eap.units = 'hPa'
  nao_pc.units = '-'
  eap_pc.units = '-'
  nao.long_name = 'North Atlantic Oscillation index'
  eap.long_name = 'East Atlantic Pattern index'
  nao_pc.long_name = 'North Atlantic Oscillation index principal component'
  eap_pc.long_name = 'East Atlantic Pattern index principal component'
  nao.season='JJA'
  eap.Season='JJA'
  #
  latnc[...] = lat.values[ymin:ymax]
  lonnc[...] = lon.values[xmin:xmax]
  nao[:,:] = EOF1 * 1e-2 # hPa convertion
  eap[:,:] = EOF2 * 1e-2 # idem
  nao_pc[:] = PC1
  eap_pc[:] = PC2
  nao.varexp = varexp[0]
  eap.varexp = varexp[1]
  times[:]=timeseas.num()
  times.calendar=timeseas.calendar
  times.units=timeseas.units
  fileo.close()

else :
  print 'Interput at your request'






