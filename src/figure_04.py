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
#mpl.rcParams['font.family']= 'sans-serif'
#mpl.rcParams['font.sans-serif'] = 'Helvetica'
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D    
from mpl_toolkits.basemap import Basemap
from mpl_toolkits.axes_grid1 import make_axes_locatable
#
import climtools as ct
import plottools as pt
#===========================================================================
varname = 'sovitmod'
#
ilat='28N'
fileout = '../figures/figure_04.png'
#===========================================================================
fclimmap = '../data/sovitmod_timemean_1960-2012.nc'
#===========================================================================
fclimsec = '../data/vo_timemean_sec%s_1960-2012.nc'%(ilat)
fcompsecBTRPOS = '../data/Composite_vo_%s-BTRPOS.nc'%(ilat)
fcompsecGEOPOS = '../data/Composite_vo_%s-GEOPOS.nc'%(ilat)
#===========================================================================
if not os.path.exists(fclimmap) :
    sys.exit('The fclimmap file does not exit, I quit !')
if not os.path.exists(fclimsec) :
    sys.exit('The fclimsec file does not exit, I quit !')
if not os.path.exists(fcompsecBTRPOS) :
    sys.exit('The fcompsecBTRPOS file does not exit, I quit !')
if not os.path.exists(fcompsecGEOPOS) :
    sys.exit('The fcompsecGEOPOS file does not exit, I quit !')
#
# readfile
# -------
ncid = nc.Dataset(fclimmap)
climmap  = ncid.variables['sovitmod'][:,:]
lons     = ncid.variables["nav_lon"][:,:]
lats     = ncid.variables["nav_lat"][:,:]
ncid.close()
# -------
ncid = nc.Dataset(fclimsec)
climsec = ncid.variables['vo'][:,:]
depth    = ncid.variables["depthv"][:]
lon      = ncid.variables["nav_lon"][:]
ncid.close()
#
ncid = nc.Dataset(fcompsecBTRPOS)
compsecBTRPOS = ncid.variables['vo'][:,:]
ncid.close()
ncid = nc.Dataset(fcompsecGEOPOS)
compsecGEOPOS = ncid.variables['vo'][:,:]
ncid.close()
#
print( climmap.shape )
anosecBTRPOS = ma.subtract(compsecBTRPOS,climsec)
anosecGEOPOS = ma.subtract(compsecGEOPOS,climsec)
#
# Convert data into masked array
# ------------------------------
climmap  = np.nan_to_num(climmap)
# lon       = np.nan_to_num( lon     )
# lat       = np.nan_to_num( lat     )
climmap  = ma.masked_values( climmap, 0.)
# lon       = ma.masked_values( lon,      0.)
# lat       = ma.masked_values( lat,      0.)
#
#
# 
# =============================================================================
#                                  PLOT
# =============================================================================
fslab=10
fstlab=8
fig = plt.figure(figsize=(4 ,6), dpi=1000,facecolor='w')
cmapmean = plt.get_cmap( 'RdBu_r',  21)
cmapstd  = plt.get_cmap( 'ocean_r', 21)
#shifted_cmap = pt.shiftedColorMap(cmapmean, midpoint=0.2, name='shifted')
#labels = ['25$^\\circ$S','15$^\\circ$S','5$^\\circ$S','EQ','5$^\\circ$N','15$^\\circ$N','25$^\\circ$N','35$^\\circ$N','45$^\\circ$N','55$^\\circ$N','65$^\\circ$N']
#
ax1 = plt.subplot(411)
plt.pcolor(lons,lats,climmap,cmap=cmapstd,vmin=0,vmax=1)
ti = ax1.set_title('(a) Surface velocity modulus climatology',fontsize=10)
ax1.set_xticks([-80., -78., -76., -74., -72., -70.])
ax1.tick_params(labelbottom=False)    
ax1.tick_params(labelsize=fslab)
ax1.set_xlim([-82., -70.])
ax1.set_ylim([22,32])
ax1.set_facecolor('lightgray')
ax1.set_ylabel('Latitude',fontsize=fslab)
ax1.axhline(y=26.5, xmin=-100, xmax=10,color='red',linewidth=1.3)
ax1.axhline(y=28,   xmin=-100, xmax=10,color='black',linewidth=1.3)
#
# axe pour la colorbar 1
divider = make_axes_locatable(ax1)
cax1 = divider.append_axes("right", size="5%", pad=0.2)
cb = plt.colorbar(cax=cax1)
cb.set_label('Velocicy (m/s)',fontsize=fslab)
cb.ax.tick_params(labelsize=fslab)
#
#
ax2 = plt.subplot(412)
plt.pcolor(lon,-depth,climsec,cmap=cmapmean,vmin=-0.5,vmax=+0.5)
ti = ax2.set_title('(b) Meridional velocity climatology at 28N',fontsize=10)
ax2.set_xlim([-82., -70.])
ax2.set_xticks([-80., -78., -76., -74., -72., -70.])
ax2.tick_params(labelbottom=False)    
ax2.tick_params(labelsize=fslab)
#ax2.set_xticklabels(labels,fontsize=fstlab)
ax2.set_ylabel('depth (m)',fontsize=fslab)
ax2.set_facecolor('lightgray')
# #
# axe pour la colorbar 1
divider = make_axes_locatable(ax2)
cax2 = divider.append_axes("right", size="5%", pad=0.2)
cb = plt.colorbar(cax=cax2)
cb.set_label('(m/s)',fontsize=fslab)
cb.ax.tick_params(labelsize=fslab)
#
ax3 = plt.subplot(413)
plt.pcolor(lon,-depth,anosecBTRPOS,cmap=cmapmean,vmin=-0.25,vmax=+0.25)
ti = ax3.set_title('(c) Anomalies for high BTR values',fontsize=10)
ax3.set_xlim([-82., -70.])
ax3.set_xticks([-80., -78., -76., -74., -72., -70.])
ax3.tick_params(labelbottom=False)    
ax3.tick_params(labelsize=fslab)
#ax3.set_xticklabels(labels,fontsize=fstlab)
ax3.set_ylabel('depth (m)',fontsize=fslab)
ax3.set_facecolor('lightgray')
# #
# axe pour la colorbar
divider = make_axes_locatable(ax3)
cax3 = divider.append_axes("right", size="5%", pad=0.2)
cb = plt.colorbar(cax=cax3)
cb.set_label('(m/s)',fontsize=fslab)
cb.ax.tick_params(labelsize=fslab)
#
ax4 = plt.subplot(414)
plt.pcolor(lon,-depth,anosecGEOPOS,cmap=cmapmean,vmin=-0.25,vmax=+0.25)
ti = ax4.set_title('(c) Anomalies for high GEOSH values',fontsize=10)
ax4.set_xlim([-82., -70.])
ax4.set_xticks([-80., -78., -76., -74., -72., -70.])
ax4.tick_params(labelsize=fslab)
#ax4.set_xticklabels(labels,fontsize=fstlab)
ax4.set_ylabel('depth (m)',fontsize=fslab)
ax4.set_facecolor('lightgray')
# #
# axe pour la colorbar
divider = make_axes_locatable(ax4)
cax4 = divider.append_axes("right", size="5%", pad=0.2)
cb = plt.colorbar(cax=cax4)
cb.set_label('(m/s)',fontsize=fslab)
cb.ax.tick_params(labelsize=fslab)

#
fig.tight_layout()
plt.subplots_adjust(hspace=0.3)
plt.savefig(fileout)

