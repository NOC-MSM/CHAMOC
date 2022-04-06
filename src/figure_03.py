#!/usr/bin/env cdat
# -*-coding:Latin-1 -*
#===========================================================================
import sys, os
import netCDF4 as nc
import datetime
import numpy.ma as ma
import numpy as np
#
import matplotlib as mpl
mpl.rcParams['lines.linewidth'] = 2
mpl.rcParams['axes.linewidth'] = 2
mpl.rcParams['axes.titlesize'] = 18
mpl.rcParams['axes.titleweight'] = 'bold'
mpl.rcParams['axes.labelsize'] = 14
mpl.rcParams['xtick.major.width'] = 2
mpl.rcParams['ytick.major.width'] = 2
mpl.rcParams['xtick.direction'] = 'out'
mpl.rcParams['ytick.direction'] = 'out'
mpl.rcParams['xtick.labelsize'] = 12
mpl.rcParams['ytick.labelsize'] = 12
mpl.rcParams['ps.useafm'] = True
mpl.rcParams['pdf.use14corefonts'] = True
# Issues with tex on JASMIN, so set this to False...
mpl.rcParams['text.usetex'] = False
mpl.rcParams['font.family']= 'sans-serif'
mpl.rcParams['font.sans-serif'] = 'Helvetica'
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D    
from mpl_toolkits.axes_grid1 import make_axes_locatable
#
import climtools as ct
import plottools as pt
#===========================================================================
expid   = 'ORCA0083-N06'
varname = 'zomsfatl'
freq    = 'd05'
yrstart = 1960
yrend   = 2012
#
filemean          = '../data/data_figure_01a.nc'
filestd           = '../data/data_figure_02a.nc'
fileclimvarBTR    = '../data/ORCA0083-N06_timestd_19602012_BTRvalor_d05.nc'
fileclimvarEKM    = '../data/ORCA0083-N06_timestd_19602012_EKMvalor_d05.nc'
fileclimvarRES    = '../data/ORCA0083-N06_timestd_19602012_RESvalor_d05.nc'
fileclimvarGEO    = '../data/ORCA0083-N06_timestd_19602012_GEOvalor_d05.nc'
fileclimvarGEOBTR = '../data/ORCA0083-N06_timestd_19602012_GEOBTRvalor_d05.nc'
#===========================================================================
if not os.path.exists(filemean) :
    sys.exit('The timemean file does not exit, I quit !')
if not os.path.exists(filestd) :
    sys.exit('The timestd file does not exit, I quit !')
#
# readfile
# -------
ncid = nc.Dataset(filemean)
climmean = np.squeeze(ncid.variables[varname][:,:,:,:])
depth    = ncid.variables["depthw"][:]
lat      = np.squeeze(ncid.variables["nav_lat"][:,:])
ncid.close()
#
ncid = nc.Dataset(filestd)
climstd = np.squeeze(ncid.variables[varname][:,:,:,:])
ncid.close()
#
ncid = nc.Dataset(fileclimvarBTR)
tabclimvarBTR  = np.squeeze(ncid.variables['BTR'][:,:,:,:])
latBTR         = np.squeeze(ncid.variables["nav_lat"][:,:])
ncid.close()
#
ncid = nc.Dataset(fileclimvarEKM)
tabclimvarEKM  = np.squeeze(ncid.variables['EKM'][:,:,:,:])
ncid.close()
#
ncid = nc.Dataset(fileclimvarRES)
tabclimvarRES  = np.squeeze(ncid.variables['RES'][:,:,:,:])
ncid.close()
#
ncid = nc.Dataset(fileclimvarGEO)
tabclimvarGEO  = np.squeeze(ncid.variables['GEO'][:,:,:,:])
ncid.close()
#
ncid = nc.Dataset(fileclimvarGEOBTR)
tabclimvarGEOBTR  = np.squeeze(ncid.variables['GEOBTR'][:,:,:,:])
ncid.close()
#
print(climmean.shape)
print(climstd.shape)
#
# Convert data into masked array
# ------------------------------
climmean         = np.nan_to_num( climmean)
climstd          = np.nan_to_num( climstd )
tabclimvarBTR    = np.nan_to_num( tabclimvarBTR   )
tabclimvarEKM    = np.nan_to_num( tabclimvarEKM   )
tabclimvarRES    = np.nan_to_num( tabclimvarRES   )
tabclimvarGEO    = np.nan_to_num( tabclimvarGEO   )
tabclimvarGEOBTR = np.nan_to_num( tabclimvarGEOBTR)
climmean         = ma.masked_values( climmean, 0.)
climstd          = ma.masked_values( climstd,  0.)
tabclimvarBTR    = ma.masked_values( tabclimvarBTR,   0.)
tabclimvarEKM    = ma.masked_values( tabclimvarEKM,   0.)
tabclimvarRES    = ma.masked_values( tabclimvarRES,   0.)
tabclimvarGEO    = ma.masked_values( tabclimvarGEO,   0.)
tabclimvarGEOBTR = ma.masked_values( tabclimvarGEOBTR,0.)
#
id5N = ma.abs(latBTR-5).argmin()
id5S = ma.abs(latBTR+5).argmin()
id5Nmoc = ma.abs(lat-5).argmin()
id5Smoc = ma.abs(lat+5).argmin()
#
# AMOC max
# --------
climmean_box = climmean[ (ma.abs(depth+500)).argmin(): (ma.abs(depth+2000)).argmin(),:]
climstd_box  = climstd[  (ma.abs(depth+500)).argmin(): (ma.abs(depth+2000)).argmin(),:]
id_amoc_max = ma.argmax(climmean_box , axis=0)
amoc_max    = climmean_box[ id_amoc_max, np.arange(0,3059)]
std_max     = climstd_box[  id_amoc_max, np.arange(0,3059)]
secdepth = depth[(ma.abs(depth+500)).argmin(): (ma.abs(depth+2000)).argmin()][id_amoc_max]
#
tabclimvarBTR_box    = tabclimvarBTR[    (ma.abs(depth+500)).argmin(): (ma.abs(depth+2000)).argmin(),:]
tabclimvarEKM_box    = tabclimvarEKM[    (ma.abs(depth+500)).argmin(): (ma.abs(depth+2000)).argmin(),:]
tabclimvarRES_box    = tabclimvarRES[    (ma.abs(depth+500)).argmin(): (ma.abs(depth+2000)).argmin(),:]
tabclimvarGEO_box    = tabclimvarGEO[    (ma.abs(depth+500)).argmin(): (ma.abs(depth+2000)).argmin(),:]
tabclimvarGEOBTR_box = tabclimvarGEOBTR[ (ma.abs(depth+500)).argmin(): (ma.abs(depth+2000)).argmin(),:]
varBTR    = tabclimvarBTR_box[    id_amoc_max[999:999+1800], np.arange(0,1800)]
varEKM    = tabclimvarEKM_box[    id_amoc_max[999:999+1800], np.arange(0,1800)]
varRES    = tabclimvarRES_box[    id_amoc_max[999:999+1800], np.arange(0,1800)]
varGEO    = tabclimvarGEO_box[    id_amoc_max[999:999+1800], np.arange(0,1800)]
varGEOBTR = tabclimvarGEOBTR_box[ id_amoc_max[999:999+1800], np.arange(0,1800)]

#
fslab=10
fstlab=10
fsti=12
# 
# =============================================================================
#                                  PLOT
# =============================================================================
fig = plt.figure(figsize=(8,3), dpi=1000,facecolor='w')
cmapmean = plt.get_cmap( 'RdBu_r',  21)
cmapstd  = plt.get_cmap( 'ocean_r', 21)
shifted_cmap = pt.shiftedColorMap(cmapmean, midpoint=0.2, name='shifted')
labels = ['25$^\\circ$S','15$^\\circ$S','5$^\\circ$S','EQ','5$^\\circ$N','15$^\\circ$N','25$^\\circ$N','35$^\\circ$N','45$^\\circ$N','55$^\\circ$N','65$^\\circ$N']
#
#
ax3 = plt.subplot(111)
#plt.semilogy( lat,    std_max,  colAor='red',     lw=1.5)
ax3.plot( latBTR, varBTR,    color='blue',    lw=1.2)
ax3.plot( latBTR[0:id5S], varEKM[0:id5S],    color='lawngreen',   lw=1.2)
ax3.plot( latBTR[0:id5S], varRES[0:id5S],    color='black',   lw=1.2)
ax3.plot( latBTR[0:id5S], varGEO[0:id5S],    color='fuchsia', lw=1.2)
ax3.plot( latBTR[0:id5S], varGEOBTR[0:id5S], color='orange',  lw=1.2)
ax3.plot( lat, std_max,    color='red', lw=1.5)
ax3.plot( latBTR[id5N:1800], varEKM[id5N:1800],    color='lawngreen',   lw=1.2)
ax3.plot( latBTR[id5N:1800], varRES[id5N:1800],    color='black',   lw=1.2)
ax3.plot( latBTR[id5N:1800], varGEO[id5N:1800],    color='fuchsia', lw=1.2)
ax3.plot( latBTR[id5N:1800], varGEOBTR[id5N:1800], color='orange',  lw=1.2)

ax3.axvline( x=24,   ymin=0, ymax=6000, color='black', linewidth=1.3)
ax3.axvline( x=26.5, ymin=0, ymax=6000, color='red',   linewidth=1.3)
ax3.axvline( x=28,   ymin=0, ymax=6000, color='black', linewidth=1.3)

#ax3.fill_between(latBTR, 0, 15, facecolor='lightgray',where=ma.logical_and(latBTR>-5,latBTR<5),edgecolor="b", linewidth=0.0)
ti = ax3.set_title('Variability at AMOC index level',fontsize=fsti)
ax3.set_xticks([-25., -15., -5., 0., 5., 15., 25., 35., 45., 55., 65.])
ax3.set_xticklabels(labels,fontsize=fstlab)
ax3.set_xlim([-34., 65.])
ax3.set_ylim([0., 15.])
ax3.set_ylabel('Standard deviation (Sv)',fontsize=fslab)
#ax3.tick_params('y', colors='b')
#
# rajout d'un axe vide pour l'alignement des subplots
divider = make_axes_locatable(ax3)
cax3 = divider.append_axes("right", size="15%", pad=0.4)
cax3.set_facecolor('none')
for axis in ['top','bottom','left','right']:
    cax3.spines[axis].set_linewidth(0)
cax3.set_xticks([])
cax3.set_yticks([])
lamoc   = Line2D([], [], color='red',        label=' amoc'   )
lekm    = Line2D([], [], color='lawngreen',  label=' ekman'   )
lres    = Line2D([], [], color='black',      label=' residual'   )
lbtr    = Line2D([], [], color='blue',       label=' btr'    )
lgeo    = Line2D([], [], color='fuchsia',    label=' geosh'    )
lgeobtr = Line2D([], [], color='orange',     label=' geosh+btr')
cax3.legend(handles=[lamoc,lekm,lbtr,lgeo,lgeobtr,lres],frameon=False,loc=(-0.5,0.1),fontsize=12,handletextpad=0.,borderpad=1. )
#
#
fig.tight_layout()
plt.subplots_adjust(hspace=0.3)
plt.savefig('../figures/figure_03.png')

