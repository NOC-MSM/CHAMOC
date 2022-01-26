#!/usr/bin/env cdat
# -*-coding:Latin-1 -*
# ==========================================================================
import sys
import netCDF4 as nc
import MA
import numpy as N
import datetime
# ==========================================================================
dom_dict = dict()
lname_dict = dict()
# ============================================================================
option_grid = 't'
fmask = nc.Dataset('/net/cratos/usr/cratos/varclim/IPSLCM5A/PROD/piControl2/OCE/piControl2_mesh_mask.nc')
mask_v = fmask.variables[option_grid + 'mask'][0]
longitude = fmask.variables['nav_lon'][:,:]
latitude  = fmask.variables['nav_lat'][:,:]
level = fmask.variables['nav_lev'][:]
fmask.close()
# ===========================================================================
finit = nc.Dataset('/net/argos/data/parvati/agglod/DATA/IPSLCM/Mask_ORCA2.nc')
#
ginseasx = finit.variables['GINSEASX'][:,:,:]
barents = finit.variables['BARENTSX'][:,:,:]
barkaras = finit.variables['BARKARAS'][:,:,:]
nsarcton = finit.variables['NSARCTON'][:,:,:]
bering =  finit.variables['BERINGXX'][:,:,:]
dom_dict['NSARCTON']=nsarcton
lname_dict['NSARCTON']='NSIDC Arctic Central Ocean'
dom_dict['BARKARAS']=barkaras
lname_dict['BARKARAS']='Barents + Kara Seas'
dom_dict['BERINGXX'] = bering
lname_dict['BERINGXX'] = 'Bering Sea'
# ============================================================================
# IPSL and CNRM marginal seas
# ---------------------------
# Larbador
bool_labipsl = N.logical_and(N.logical_and(latitude>43,latitude<80),N.logical_and(longitude<-40,longitude>-75))
bool_labipsl = N.logical_and(bool_labipsl,N.logical_or(N.logical_or(latitude>55,latitude<43),N.logical_or(longitude<-90,longitude>-55)))
labipsl = N.where(bool_labipsl,mask_v,0)
dom_dict['LABIPSL']=labipsl
lname_dict['LABIPSL'] = 'Labrador Sea in IPSL-CM'
#
# Okhotsk
bool_okhipsl = N.logical_and(N.logical_and(latitude>43,latitude<70),N.logical_and(longitude>133,longitude<163))
okhipsl = N.where(bool_okhipsl,mask_v,0)
dom_dict['OKHIPSL']=okhipsl
lname_dict['OKHIPSL'] = 'Okhotsk Sea in IPSL-CM'
#
bool_okhcnrm = N.logical_and(N.logical_and(latitude>43,latitude<70),N.logical_and(longitude>133,longitude<165))
okhcnrm = N.where(bool_okhcnrm,mask_v,0)
dom_dict['OKHCNRM']=okhcnrm
lname_dict['OKHCNRM'] = 'Okhotsk Sea in CNRM-CM'
#
# GIN
bool_ginipsl=N.logical_and(ginseasx==1,barents==0)
ginipsl=N.where(bool_ginipsl,mask_v,0)
dom_dict['GINIPSL']=ginipsl
lname_dict['GINIPSL'] = 'GIN Seas in IPSL-CM'
# Irminger 
bool_irmipsl=N.logical_and(N.logical_and(latitude>55,latitude<67),N.logical_and(longitude>-40,longitude<-20))
bool_irmipsl=N.logical_and(bool_irmipsl==1,ginipsl==0.)
bool_irmipsl=N.logical_and(bool_irmipsl==1,labipsl==0.)
irmipsl=N.where(bool_irmipsl,mask_v,0)
dom_dict['IRMIPSL']=irmipsl
lname_dict['IRMIPSL'] = 'Irminger Sea in IPSL-CM'
#

fout = nc.Dataset('Mask_ORCA2_MIZipsl.nc','w')

fout.createDimension('z',mask_v.shape[0])
fout.createDimension('y',mask_v.shape[1])
fout.createDimension('x',mask_v.shape[2])
#
lons = fout.createVariable('nav_lon','f8',('y','x',))
lats = fout.createVariable('nav_lat','f8',('y','x',))
lons[:,:] = N.float32(longitude)
lats[:,:] = N.float32(latitude)
i=1
dom_image = mask_v
#
datefile = datetime.date.today() 
fout.author="A. Germe"
fout.Date = str(datefile)
fout.comment = "Regional domains used for Potential Arctic sea ice PPP analysis"
for dom in dom_dict:
    dom_var = fout.createVariable(dom,'f8',('z','y','x',))
    dom_var[:,:,:] = dom_dict[dom]
    dom_var.long_name = lname_dict[dom]
    dom_var.short_name = dom
fout.close()
