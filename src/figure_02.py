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
filemean       = '../data/data_figure_01a.nc'
filestd        = '../data/data_figure_02a.nc'
fileclimBTR    = '../data/ORCA0083-N06_timestd_19602012_BTRvalor_d05.nc'
fileclimEKM    = '../data/ORCA0083-N06_timestd_19602012_EKMvalor_d05.nc'
fileclimRES    = '../data/ORCA0083-N06_timestd_19602012_RESvalor_d05.nc'
fileclimGEO    = '../data/ORCA0083-N06_timestd_19602012_GEOvalor_d05.nc'
fileclimGEOBTR = '../data/ORCA0083-N06_timestd_19602012_GEOBTRvalor_d05.nc'
#===========================================================================
if not os.path.exists(filemean) :
    sys.exit('The timemean file does not exit, I quit !')
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
ncid = nc.Dataset(fileclimBTR)
tabclimBTR  = np.squeeze(ncid.variables['BTR'][:,:,:,:])
latBTR         = np.squeeze(ncid.variables["nav_lat"][:,:])
ncid.close()
#
ncid = nc.Dataset(fileclimEKM)
tabclimEKM  = np.squeeze(ncid.variables['EKM'][:,:,:,:])
ncid.close()
#
ncid = nc.Dataset(fileclimRES)
tabclimRES  = np.squeeze(ncid.variables['RES'][:,:,:,:])
ncid.close()
#
ncid = nc.Dataset(fileclimGEO)
tabclimGEO  = np.squeeze(ncid.variables['GEO'][:,:,:,:])
ncid.close()
#
ncid = nc.Dataset(fileclimGEOBTR)
tabclimGEOBTR  = np.squeeze(ncid.variables['GEOBTR'][:,:,:,:])
ncid.close()
#
print(climmean.shape)
#
# Convert data into masked array
# ------------------------------
climmean         = np.nan_to_num( climmean)
climstd          = np.nan_to_num( climstd)
tabclimBTR    = np.nan_to_num( tabclimBTR   )
tabclimEKM    = np.nan_to_num( tabclimEKM   )
tabclimRES    = np.nan_to_num( tabclimRES   )
tabclimGEO    = np.nan_to_num( tabclimGEO   )
tabclimGEOBTR = np.nan_to_num( tabclimGEOBTR)
climmean         = ma.masked_values( climmean, 0.)
climstd          = ma.masked_values( climstd,  0.)
tabclimBTR    = ma.masked_values( tabclimBTR,   0.)
tabclimEKM    = ma.masked_values( tabclimEKM,   0.)
tabclimRES    = ma.masked_values( tabclimRES,   0.)
tabclimGEO    = ma.masked_values( tabclimGEO,   0.)
tabclimGEOBTR = ma.masked_values( tabclimGEOBTR,0.)
#
id5N = ma.abs(latBTR-5).argmin()
id5S = ma.abs(latBTR+5).argmin()
id5Nmoc = ma.abs(lat-5).argmin()
id5Smoc = ma.abs(lat+5).argmin()
#
# AMOC max
# --------
climmean_box = climmean[ (ma.abs(depth+500)).argmin(): (ma.abs(depth+2000)).argmin(),:]
id_amoc_max = ma.argmax(climmean_box , axis=0)
amoc_max    = climmean_box[ id_amoc_max, np.arange(0,3059)]

secdepth = depth[(ma.abs(depth+500)).argmin(): (ma.abs(depth+2000)).argmin()][id_amoc_max]
#
# tabclimBTR_box    = tabclimBTR[    (ma.abs(depth+500)).argmin(): (ma.abs(depth+2000)).argmin(),:]
# tabclimEKM_box    = tabclimEKM[    (ma.abs(depth+500)).argmin(): (ma.abs(depth+2000)).argmin(),:]
# tabclimRES_box    = tabclimRES[    (ma.abs(depth+500)).argmin(): (ma.abs(depth+2000)).argmin(),:]
# tabclimGEO_box    = tabclimGEO[    (ma.abs(depth+500)).argmin(): (ma.abs(depth+2000)).argmin(),:]
# tabclimGEOBTR_box = tabclimGEOBTR[ (ma.abs(depth+500)).argmin(): (ma.abs(depth+2000)).argmin(),:]
# varBTR    = tabclimBTR_box[    id_amoc_max[999:999+1800], np.arange(0,1800)]
# varEKM    = tabclimEKM_box[    id_amoc_max[999:999+1800], np.arange(0,1800)]
# varRES    = tabclimRES_box[    id_amoc_max[999:999+1800], np.arange(0,1800)]
# varGEO    = tabclimGEO_box[    id_amoc_max[999:999+1800], np.arange(0,1800)]
# varGEOBTR = tabclimGEOBTR_box[ id_amoc_max[999:999+1800], np.arange(0,1800)]

#
fslab=10
fstlab = 8
fscbtick = 8
fsti=11
# 
# =============================================================================
#                                  PLOT
# =============================================================================
fig = plt.figure(figsize=(7,10), dpi=1000,facecolor='w')
cmapmean = plt.get_cmap( 'RdBu_r',  21)
cmapstd  = plt.get_cmap( 'ocean_r', 21)
shifted_cmap = pt.shiftedColorMap(cmapmean, midpoint=0.2, name='shifted')
labels = ['25$^\\circ$S','15$^\\circ$S','5$^\\circ$S','EQ','5$^\\circ$N','15$^\\circ$N','25$^\\circ$N','35$^\\circ$N','45$^\\circ$N','55$^\\circ$N','65$^\\circ$N']
#
ax1 = plt.subplot(511)
plt.pcolor(lat,-depth,climstd,cmap=cmapstd,vmin=0,vmax=20)
plt.axvline(x=26,ymin=0,ymax=6000,color='red',linewidth=1.3)
ax1.add_line(Line2D(lat,-secdepth,color='black',lw=1.2))
ti = ax1.set_title('(a) AMOC',fontsize=fsti)
ax1.set_xticks([-25., -15., -5., 0., 5., 15., 25., 35., 45., 55., 65.])
ax1.set_xticklabels(labels,fontsize=fstlab)
plt.setp(ax1.get_yticklabels(), fontsize=fstlab)
ax1.set_xlim([-34., 65.])
ax1.set_ylim([0., 5700.])
ax1.invert_yaxis()
ax1.set_ylabel('depth (m)',fontsize=fslab)
ax1.set_facecolor('lightgray')
#
# axe pour la colorbar 1
divider = make_axes_locatable(ax1)
cax1 = divider.append_axes("right", size="5%", pad=0.3)
cb = plt.colorbar(cax=cax1)
cb.set_label('(Sv)',fontsize=fslab)
cb.ax.tick_params(labelsize=fscbtick)
#
# Subplot: EKM
# ============
ax2 = plt.subplot(512)
plt.pcolor(latBTR,-depth,tabclimEKM,cmap=cmapstd,vmin=0,vmax=+15)
plt.axvline(x=26,ymin=0,ymax=6000,color='red',linewidth=1.3)
ax2.add_line(Line2D(lat,-secdepth,color='black',lw=1.2))
ti = ax2.set_title('(b) EKM',fontsize=fsti)
ax2.set_xticks([-25., -15., -5., 0., 5., 15., 25., 35., 45., 55., 65.])
ax2.set_xticklabels(labels,fontsize=fstlab)
plt.setp(ax2.get_yticklabels(), fontsize=fstlab)
ax2.set_xlim([-34., 65.])
ax2.set_ylim([0., 5700.])
ax2.invert_yaxis()
ax2.set_ylabel('depth (m)',fontsize=fslab)
ax2.set_facecolor('lightgray')
ax2.fill_between(latBTR, 0, 6000, facecolor='lightgray',where=ma.logical_and(latBTR>-5,latBTR<5),edgecolor="b", linewidth=0.0)
#
# axe pour la colorbar 1
divider = make_axes_locatable(ax2)
cax2 = divider.append_axes("right", size="5%", pad=0.3)
cb = plt.colorbar(cax=cax2)
cb.set_label('(Sv)',fontsize=fslab)
cb.ax.tick_params(labelsize=fscbtick)
#
# Subplot: BTR
# ============
ax3 = plt.subplot(513)
plt.pcolor(latBTR,-depth,tabclimBTR,cmap=cmapstd,vmin=0,vmax=+15)
plt.axvline(x=26,ymin=0,ymax=6000,color='red',linewidth=1.3)
ax3.add_line(Line2D(lat,-secdepth,color='black',lw=1.2))
ti = ax3.set_title('(c) BTR',fontsize=fsti)
ax3.set_xticks([-25., -15., -5., 0., 5., 15., 25., 35., 45., 55., 65.])
ax3.set_xticklabels(labels,fontsize=fstlab)
plt.setp(ax3.get_yticklabels(), fontsize=fstlab)
ax3.set_xlim([-34., 65.])
ax3.set_ylim([0., 5700.])
ax3.invert_yaxis()
ax3.set_ylabel('depth (m)',fontsize=fslab)
ax3.set_facecolor('lightgray')
#
# axe pour la colorbar 1
divider = make_axes_locatable(ax3)
cax3 = divider.append_axes("right", size="5%", pad=0.3)
cb = plt.colorbar(cax=cax3)
cb.set_label('(Sv)',fontsize=fslab)
cb.ax.tick_params(labelsize=fscbtick)
#
# Subplot: GEO
# ============
ax4 = plt.subplot(514)
plt.pcolor(latBTR,-depth,tabclimGEO,cmap=cmapstd,vmin=0,vmax=+15)
plt.axvline(x=26,ymin=0,ymax=6000,color='red',linewidth=1.3)
ax4.add_line(Line2D(lat,-secdepth,color='black',lw=1.2))
ti = ax4.set_title('(d) GEOSH',fontsize=fsti)
ax4.set_xticks([-25., -15., -5., 0., 5., 15., 25., 35., 45., 55., 65.])
ax4.set_xticklabels(labels,fontsize=fstlab)
plt.setp(ax4.get_yticklabels(), fontsize=fstlab)
ax4.set_xlim([-34., 65.])
ax4.set_ylim([0., 5700.])
ax4.invert_yaxis()
ax4.set_ylabel('depth (m)',fontsize=fslab)
ax4.set_facecolor('lightgray')
ax4.fill_between(latBTR, 0, 6000, facecolor='lightgray',where=ma.logical_and(latBTR>-5,latBTR<5),edgecolor="b", linewidth=0.0)
#
# axe pour la colorbar 1
divider = make_axes_locatable(ax4)
cax4 = divider.append_axes("right", size="5%", pad=0.3)
cb = plt.colorbar(cax=cax4)
cb.set_label('(Sv)',fontsize=fslab)
cb.ax.tick_params(labelsize=fscbtick)
#
# Subplot : RES
# =============
ax5 = plt.subplot(515)
plt.pcolor(latBTR,-depth,tabclimRES,cmap=cmapstd,vmin=0,vmax=+15)
plt.axvline(x=26,ymin=0,ymax=6000,color='red',linewidth=1.3)
ax5.add_line(Line2D(lat,-secdepth,color='black',lw=1.2))
ti = ax5.set_title('(e) RES',fontsize=fsti)
ax5.set_xticks([-25., -15., -5., 0., 5., 15., 25., 35., 45., 55., 65.])
ax5.set_xticklabels(labels,fontsize=fstlab)
plt.setp(ax5.get_yticklabels(), fontsize=fstlab)
ax5.set_xlim([-34., 65.])
ax5.set_ylim([0., 5700.])
ax5.invert_yaxis()
ax5.set_ylabel('depth (m)',fontsize=fslab)
ax5.set_facecolor('lightgray')
ax5.fill_between(latBTR, 0, 6000, facecolor='lightgray',where=ma.logical_and(latBTR>-5,latBTR<5),edgecolor="b", linewidth=0.0)
#
# axe pour la colorbar 1
divider = make_axes_locatable(ax5)
cax5 = divider.append_axes("right", size="5%", pad=0.3)
cb = plt.colorbar(cax=cax5)
cb.set_label('(Sv)',fontsize=fslab)
cb.ax.tick_params(labelsize=fscbtick)
#


#
fig.tight_layout()
plt.subplots_adjust(hspace=0.3)
plt.savefig('../figures/figure_02.png')

