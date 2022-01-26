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
def coord2indice(axe,axlim) :
  coordindice = MA.masked_where(MA.logical_or(axe<axlim[0],axe>axlim[1]),MA.arange((len(axe))))
  return MA.minimum(coordindice), MA.maximum(coordindice)
# -----------------------------------------------------------------------
# Les boites Drakkar : 
fref = nc.Dataset('/group_workspaces/jasmin2/nemo/vol1/ORCA0083-N006/domain/mask.nc')
lat = fref.variables['lat'][:]
depth = fref.variables['depthw'][:]
#
latindicemin = dict() ; latindicemax = dict()
depthindicemin = dict() ; depthindicemax = dict()
#
latindicemin['AMOCmax'], latindicemax['AMOCmax'] = coord2indice(lat,(0,60)) # valeurs Monitoring Drakkar pour l'Atla
ntique
depthindicemin['AMOCmax'], depthindicemax['AMOCmax'] = coord2indice(depth, (500,2000)) # valeurs Monitoring Drakkar 
pour l'Atlantique

